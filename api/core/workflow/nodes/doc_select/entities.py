from typing import Any, Literal, Optional

from pydantic import BaseModel

from core.workflow.entities.base_node_data_entities import BaseNodeData


class RerankingModelConfig(BaseModel):
    """
    Reranking Model Config.
    """
    provider: str
    model: str


class MultipleRetrievalConfig(BaseModel):
    """
    Multiple Retrieval Config.
    """
    top_k: int
    score_threshold: Optional[float]
    reranking_model: RerankingModelConfig


class ModelConfig(BaseModel):
    """
     Model Config.
    """
    provider: str
    name: str
    mode: str
    completion_params: dict[str, Any] = {}


class SingleRetrievalConfig(BaseModel):
    """
    Single Retrieval Config.
    """
    model: ModelConfig


class DocSelectNodeData(BaseNodeData):
    """
    Knowledge retrieval Node Data.
    """
    type: str = 'knowledge-retrieval'
    doc_ids: list[str]
