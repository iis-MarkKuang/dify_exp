import datetime
import logging
import time

import click
from celery import shared_task
from flask import current_app

from core.indexing_runner import DocumentIsPausedException, IndexingRunner
from core.rag.index_processor.index_processor_factory import IndexProcessorFactory
from extensions.ext_database import db
from models.dataset import Dataset, Document, DocumentSegment
from services.feature_service import FeatureService


@shared_task(queue="dataset")
def duplicate_document_indexing_task(dataset_id: str, document_ids: list):
    """
    Async process document
    :param dataset_id:
    :param document_ids:

    Usage: duplicate_document_indexing_task.delay(dataset_id, document_id)
    """
    documents = []
    start_at = time.perf_counter()

    dataset = db.session.query(Dataset).filter(Dataset.id == dataset_id).first()

    # check document limit
    features = FeatureService.get_features(dataset.tenant_id)
    try:
        if features.billing.enabled:
            vector_space = features.vector_space
            count = len(document_ids)
            batch_upload_limit = int(current_app.config["BATCH_UPLOAD_LIMIT"])
            if count > batch_upload_limit:
                raise ValueError(f"You have reached the batch upload limit of {batch_upload_limit}.")
            if 0 < vector_space.limit <= vector_space.size:
                raise ValueError(
                    "Your total number of documents plus the number of uploads have over the limit of "
                    "your subscription."
                )
    except Exception as e:
        for document_id in document_ids:
            document = (
                db.session.query(Document).filter(Document.id == document_id, Document.dataset_id == dataset_id).first()
            )
            if document:
                document.indexing_status = "error"
                document.error = str(e)
                document.stopped_at = datetime.datetime.utcnow()
                db.session.add(document)
        db.session.commit()
        return

    for document_id in document_ids:
        logging.info(click.style("Start process document: {}".format(document_id), fg="green"))

        document = (
            db.session.query(Document).filter(Document.id == document_id, Document.dataset_id == dataset_id).first()
        )

        if document:
            # clean old data
            index_type = document.doc_form
            index_processor = IndexProcessorFactory(index_type).init_index_processor()

            segments = db.session.query(DocumentSegment).filter(DocumentSegment.document_id == document_id).all()
            if segments:
                index_node_ids = [segment.index_node_id for segment in segments]

                # delete from vector index
                index_processor.clean(dataset, index_node_ids)

                for segment in segments:
                    db.session.delete(segment)
                db.session.commit()

            document.indexing_status = "parsing"
            document.processing_started_at = datetime.datetime.utcnow()
            documents.append(document)
            db.session.add(document)
    db.session.commit()

    try:
        indexing_runner = IndexingRunner()
        indexing_runner.run(documents)
        end_at = time.perf_counter()
        logging.info(click.style("Processed dataset: {} latency: {}".format(dataset_id, end_at - start_at), fg="green"))
    except DocumentIsPausedException as ex:
        logging.info(click.style(str(ex), fg="yellow"))
    except Exception:
        pass
