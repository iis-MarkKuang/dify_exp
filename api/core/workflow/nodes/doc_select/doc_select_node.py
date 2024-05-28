from typing import cast

from core.app.entities.app_invoke_entities import ModelConfigWithCredentialsEntity
from core.file.file_obj import FileTransferMethod, FileType, FileVar
from core.entities.model_entities import ModelStatus
from core.errors.error import ModelCurrentlyNotSupportError, ProviderTokenNotInitError, QuotaExceededError
from core.model_manager import ModelInstance, ModelManager
from core.model_runtime.entities.model_entities import ModelFeature, ModelType
from core.model_runtime.model_providers.__base.large_language_model import LargeLanguageModel
from core.workflow.entities.base_node_data_entities import BaseNodeData
from core.workflow.entities.node_entities import NodeRunResult, NodeType
from core.workflow.entities.variable_pool import VariablePool
from core.workflow.nodes.base_node import BaseNode
from core.workflow.nodes.doc_select.entities import DocSelectNodeData
from models.dataset import Dataset, Document, DocumentSegment
from models.model import UploadFile
from models.workflow import WorkflowNodeExecutionStatus

import json

default_retrieval_model = {
    'search_method': 'semantic_search',
    'reranking_enable': False,
    'reranking_model': {
        'reranking_provider_name': '',
        'reranking_model_name': ''
    },
    'top_k': 2,
    'score_threshold_enabled': False
}


class DocSelectNode(BaseNode):
    _node_data_cls = DocSelectNodeData
    node_type = NodeType.DOC_SELECT

    def _run(self, variable_pool: VariablePool) -> NodeRunResult:
        node_data: DocSelectNodeData = cast(self._node_data_cls, self.node_data)
        print(node_data)
        # retrieve knowledge
        try:
            doc_data = []
            for doc_id in node_data.doc_ids:
                doc = Document.query.filter_by(
                    id=doc_id
                ).first()
                if doc:
                    file_info = json.loads(doc.data_source_info)
                    file_id = file_info['upload_file_id']
                    file = UploadFile.query.filter_by(
                        id=file_id
                    ).first()
                    if not file:
                        continue
                    file_id = file.key.split('/')[-1].split('.')[0]
                    ext = file.key.split('/')[-1].split('.')[1]
                    mimetype = 'application/pdf'

                    doc_data.append(FileVar(
                        tenant_id=doc.tenant_id,
                        type=FileType.PDF,
                        transfer_method=FileTransferMethod.LOCAL_FILE,
                        related_id=file_id,
                        filename=doc.name,
                        extension=ext,
                        mime_type=mimetype,
                    ))
            results = doc_data
            print(results)

            outputs = {
                'result': results
            }
            return NodeRunResult(
                status=WorkflowNodeExecutionStatus.SUCCEEDED,
                inputs=node_data,
                process_data=None,
                outputs=outputs
            )

        except Exception as e:

            return NodeRunResult(
                status=WorkflowNodeExecutionStatus.FAILED,
                inputs=node_data,
                error=str(e)
            )


    @classmethod
    def _extract_variable_selector_to_variable_mapping(cls, node_data: BaseNodeData) -> dict[str, list[str]]:
        node_data = node_data
        node_data = cast(cls._node_data_cls, node_data)
        variable_mapping = {}
        return variable_mapping

    def _fetch_model_config(self, node_data: DocSelectNodeData) -> tuple[
        ModelInstance, ModelConfigWithCredentialsEntity]:
        """
        Fetch model config
        :param node_data: node data
        :return:
        """
        model_name = node_data.single_retrieval_config.model.name
        provider_name = node_data.single_retrieval_config.model.provider

        model_manager = ModelManager()
        model_instance = model_manager.get_model_instance(
            tenant_id=self.tenant_id,
            model_type=ModelType.LLM,
            provider=provider_name,
            model=model_name
        )

        provider_model_bundle = model_instance.provider_model_bundle
        model_type_instance = model_instance.model_type_instance
        model_type_instance = cast(LargeLanguageModel, model_type_instance)

        model_credentials = model_instance.credentials

        # check model
        provider_model = provider_model_bundle.configuration.get_provider_model(
            model=model_name,
            model_type=ModelType.LLM
        )

        if provider_model is None:
            raise ValueError(f"Model {model_name} not exist.")

        if provider_model.status == ModelStatus.NO_CONFIGURE:
            raise ProviderTokenNotInitError(f"Model {model_name} credentials is not initialized.")
        elif provider_model.status == ModelStatus.NO_PERMISSION:
            raise ModelCurrentlyNotSupportError(f"Dify Hosted OpenAI {model_name} currently not support.")
        elif provider_model.status == ModelStatus.QUOTA_EXCEEDED:
            raise QuotaExceededError(f"Model provider {provider_name} quota exceeded.")

        # model config
        completion_params = node_data.single_retrieval_config.model.completion_params
        stop = []
        if 'stop' in completion_params:
            stop = completion_params['stop']
            del completion_params['stop']

        # get model mode
        model_mode = node_data.single_retrieval_config.model.mode
        if not model_mode:
            raise ValueError("LLM mode is required.")

        model_schema = model_type_instance.get_model_schema(
            model_name,
            model_credentials
        )

        if not model_schema:
            raise ValueError(f"Model {model_name} not exist.")

        return model_instance, ModelConfigWithCredentialsEntity(
            provider=provider_name,
            model=model_name,
            model_schema=model_schema,
            mode=model_mode,
            provider_model_bundle=provider_model_bundle,
            credentials=model_credentials,
            parameters=completion_params,
            stop=stop,
        )
