import logging
import time
from typing import Optional, cast

from core.app.app_config.entities import FileExtraConfig
from core.app.apps.base_app_queue_manager import GenerateTaskStoppedException
from core.file.file_obj import FileTransferMethod, FileType, FileVar
from core.workflow.callbacks.base_workflow_callback import BaseWorkflowCallback
from core.workflow.entities.node_entities import NodeRunMetadataKey, NodeRunResult, NodeType
from core.workflow.entities.variable_pool import VariablePool, VariableValue
from core.workflow.entities.workflow_entities import WorkflowNodeAndResult, WorkflowRunState
from core.workflow.errors import WorkflowNodeRunFailedError
from core.workflow.nodes.answer.answer_node import AnswerNode
from core.workflow.nodes.base_node import BaseNode, UserFrom
from core.workflow.nodes.code.code_node import CodeNode
from core.workflow.nodes.end.end_node import EndNode
from core.workflow.nodes.http_request.http_request_node import HttpRequestNode
from core.workflow.nodes.if_else.if_else_node import IfElseNode
from core.workflow.nodes.knowledge_retrieval.knowledge_retrieval_node import KnowledgeRetrievalNode
from core.workflow.nodes.doc_select.doc_select_node import DocSelectNode
from core.workflow.nodes.llm.entities import LLMNodeData
from core.workflow.nodes.llm.llm_node import LLMNode
from core.workflow.nodes.question_classifier.question_classifier_node import QuestionClassifierNode
from core.workflow.nodes.start.start_node import StartNode
from core.workflow.nodes.template_transform.template_transform_node import TemplateTransformNode
from core.workflow.nodes.tool.tool_node import ToolNode
from core.workflow.nodes.variable_assigner.variable_assigner_node import VariableAssignerNode
from extensions.ext_database import db
from models.workflow import (
    Workflow,
    WorkflowNodeExecutionStatus,
)

node_classes = {
    NodeType.START: StartNode,
    NodeType.END: EndNode,
    NodeType.ANSWER: AnswerNode,
    NodeType.LLM: LLMNode,
    NodeType.KNOWLEDGE_RETRIEVAL: KnowledgeRetrievalNode,
    NodeType.DOC_SELECT: DocSelectNode,
    NodeType.IF_ELSE: IfElseNode,
    NodeType.CODE: CodeNode,
    NodeType.TEMPLATE_TRANSFORM: TemplateTransformNode,
    NodeType.QUESTION_CLASSIFIER: QuestionClassifierNode,
    NodeType.HTTP_REQUEST: HttpRequestNode,
    NodeType.TOOL: ToolNode,
    NodeType.VARIABLE_ASSIGNER: VariableAssignerNode,
}

logger = logging.getLogger(__name__)


class WorkflowEngineManager:
    def get_default_configs(self) -> list[dict]:
        """
        Get default block configs
        """
        default_block_configs = []
        for node_type, node_class in node_classes.items():
            default_config = node_class.get_default_config()
            if default_config:
                default_block_configs.append(default_config)

        return default_block_configs

    def get_default_config(self, node_type: NodeType, filters: Optional[dict] = None) -> Optional[dict]:
        """
        Get default config of node.
        :param node_type: node type
        :param filters: filter by node config parameters.
        :return:
        """
        node_class = node_classes.get(node_type)
        if not node_class:
            return None

        default_config = node_class.get_default_config(filters=filters)
        if not default_config:
            return None

        return default_config

    def run_workflow(self, workflow: Workflow,
                     user_id: str,
                     user_from: UserFrom,
                     user_inputs: dict,
                     system_inputs: Optional[dict] = None,
                     callbacks: list[BaseWorkflowCallback] = None) -> None:
        """
        Run workflow
        :param workflow: Workflow instance
        :param user_id: user id
        :param user_from: user from
        :param user_inputs: user variables inputs
        :param system_inputs: system inputs, like: query, files
        :param callbacks: workflow callbacks
        :return:
        """
        # fetch workflow graph
        graph = workflow.graph_dict
        if not graph:
            raise ValueError('workflow graph not found')

        if 'nodes' not in graph or 'edges' not in graph:
            raise ValueError('nodes or edges not found in workflow graph')

        if not isinstance(graph.get('nodes'), list):
            raise ValueError('nodes in workflow graph must be a list')

        if not isinstance(graph.get('edges'), list):
            raise ValueError('edges in workflow graph must be a list')

        # init workflow run
        if callbacks:
            for callback in callbacks:
                callback.on_workflow_run_started()

        # init workflow run state
        workflow_run_state = WorkflowRunState(
            workflow=workflow,
            start_at=time.perf_counter(),
            variable_pool=VariablePool(
                system_variables=system_inputs,
                user_inputs=user_inputs
            ),
            user_id=user_id,
            user_from=user_from
        )

        try:
            predecessor_node = None
            has_entry_node = False
            while True:
                # get next node, multiple target nodes in the future
                next_node = self._get_next_node(
                    workflow_run_state=workflow_run_state,
                    graph=graph,
                    predecessor_node=predecessor_node,
                    callbacks=callbacks
                )

                if not next_node:
                    break

                # check is already ran
                if next_node.node_id in [node_and_result.node.node_id
                                         for node_and_result in workflow_run_state.workflow_nodes_and_results]:
                    predecessor_node = next_node
                    continue

                has_entry_node = True

                # max steps 50 reached
                if len(workflow_run_state.workflow_nodes_and_results) > 50:
                    raise ValueError('Max steps 50 reached.')

                # or max execution time 10min reached
                if self._is_timed_out(start_at=workflow_run_state.start_at, max_execution_time=600):
                    raise ValueError('Max execution time 10min reached.')

                # run workflow, run multiple target nodes in the future
                self._run_workflow_node(
                    workflow_run_state=workflow_run_state,
                    node=next_node,
                    predecessor_node=predecessor_node,
                    callbacks=callbacks
                )

                if next_node.node_type in [NodeType.END]:
                    break

                predecessor_node = next_node

            if not has_entry_node:
                self._workflow_run_failed(
                    error='Start node not found in workflow graph.',
                    callbacks=callbacks
                )
                return
        except GenerateTaskStoppedException as e:
            return
        except Exception as e:
            self._workflow_run_failed(
                error=str(e),
                callbacks=callbacks
            )
            return

        # workflow run success
        self._workflow_run_success(
            callbacks=callbacks
        )

    def single_step_run_workflow_node(self, workflow: Workflow,
                                      node_id: str,
                                      user_id: str,
                                      user_inputs: dict) -> tuple[BaseNode, NodeRunResult]:
        """
        Single step run workflow node
        :param workflow: Workflow instance
        :param node_id: node id
        :param user_id: user id
        :param user_inputs: user inputs
        :return:
        """
        # fetch node info from workflow graph
        graph = workflow.graph_dict
        if not graph:
            raise ValueError('workflow graph not found')

        nodes = graph.get('nodes')
        if not nodes:
            raise ValueError('nodes not found in workflow graph')

        # fetch node config from node id
        node_config = None
        for node in nodes:
            if node.get('id') == node_id:
                node_config = node
                break

        if not node_config:
            raise ValueError('node id not found in workflow graph')

        # Get node class
        node_type = NodeType.value_of(node_config.get('data', {}).get('type'))

        print(node_type)
        node_cls = node_classes.get(node_type)

        # init workflow run state
        node_instance = node_cls(
            tenant_id=workflow.tenant_id,
            app_id=workflow.app_id,
            workflow_id=workflow.id,
            user_id=user_id,
            user_from=UserFrom.ACCOUNT,
            config=node_config
        )

        try:
            # init variable pool
            variable_pool = VariablePool(
                system_variables={},
                user_inputs={}
            )

            # variable selector to variable mapping
            try:
                variable_mapping = node_cls.extract_variable_selector_to_variable_mapping(node_config)
            except NotImplementedError:
                variable_mapping = {}

            for variable_key, variable_selector in variable_mapping.items():
                if variable_key not in user_inputs:
                    raise ValueError(f'Variable key {variable_key} not found in user inputs.')

                # fetch variable node id from variable selector
                variable_node_id = variable_selector[0]
                variable_key_list = variable_selector[1:]

                # get value
                value = user_inputs.get(variable_key)

                # temp fix for image type
                if node_type == NodeType.LLM:
                    new_value = []
                    if isinstance(value, list):
                        node_data = node_instance.node_data
                        node_data = cast(LLMNodeData, node_data)

                        detail = node_data.vision.configs.detail if node_data.vision.configs else None

                        for item in value:
                            if isinstance(item, dict) and 'type' in item and item['type'] == 'image':
                                transfer_method = FileTransferMethod.value_of(item.get('transfer_method'))
                                file = FileVar(
                                    tenant_id=workflow.tenant_id,
                                    type=FileType.IMAGE,
                                    transfer_method=transfer_method,
                                    url=item.get('url') if transfer_method == FileTransferMethod.REMOTE_URL else None,
                                    related_id=item.get(
                                        'upload_file_id') if transfer_method == FileTransferMethod.LOCAL_FILE else None,
                                    extra_config=FileExtraConfig(image_config={'detail': detail} if detail else None),
                                )
                                new_value.append(file)

                    if new_value:
                        value = new_value

                # append variable and value to variable pool
                variable_pool.append_variable(
                    node_id=variable_node_id,
                    variable_key_list=variable_key_list,
                    value=value
                )
            # run node
            node_run_result = node_instance.run(
                variable_pool=variable_pool
            )

            # sign output files
            node_run_result.outputs = self.handle_special_values(node_run_result.outputs)
        except Exception as e:
            raise e
            # raise WorkflowNodeRunFailedError(
            #     node_id=node_instance.node_id,
            #     node_type=node_instance.node_type,
            #     node_title=node_instance.node_data.title,
                # error=str(e)
            # )

        return node_instance, node_run_result

    def _workflow_run_success(self, callbacks: list[BaseWorkflowCallback] = None) -> None:
        """
        Workflow run success
        :param callbacks: workflow callbacks
        :return:
        """

        if callbacks:
            for callback in callbacks:
                callback.on_workflow_run_succeeded()

    def _workflow_run_failed(self, error: str,
                             callbacks: list[BaseWorkflowCallback] = None) -> None:
        """
        Workflow run failed
        :param error: error message
        :param callbacks: workflow callbacks
        :return:
        """
        if callbacks:
            for callback in callbacks:
                callback.on_workflow_run_failed(
                    error=error
                )

    def _get_next_node(self, workflow_run_state: WorkflowRunState,
                       graph: dict,
                       predecessor_node: Optional[BaseNode] = None,
                       callbacks: list[BaseWorkflowCallback] = None) -> Optional[BaseNode]:
        """
        Get next node
        multiple target nodes in the future.
        :param graph: workflow graph
        :param predecessor_node: predecessor node
        :param callbacks: workflow callbacks
        :return:
        """
        nodes = graph.get('nodes')
        if not nodes:
            return None

        if not predecessor_node:
            for node_config in nodes:
                if node_config.get('data', {}).get('type', '') == NodeType.START.value:
                    return StartNode(
                        tenant_id=workflow_run_state.tenant_id,
                        app_id=workflow_run_state.app_id,
                        workflow_id=workflow_run_state.workflow_id,
                        user_id=workflow_run_state.user_id,
                        user_from=workflow_run_state.user_from,
                        config=node_config,
                        callbacks=callbacks
                    )
        else:
            edges = graph.get('edges')
            source_node_id = predecessor_node.node_id

            # fetch all outgoing edges from source node
            outgoing_edges = [edge for edge in edges if edge.get('source') == source_node_id]
            if not outgoing_edges:
                return None

            # fetch target node id from outgoing edges
            outgoing_edge = None
            source_handle = predecessor_node.node_run_result.edge_source_handle \
                if predecessor_node.node_run_result else None
            if source_handle:
                for edge in outgoing_edges:
                    if edge.get('sourceHandle') and edge.get('sourceHandle') == source_handle:
                        outgoing_edge = edge
                        break
            else:
                outgoing_edge = outgoing_edges[0]

            if not outgoing_edge:
                return None

            target_node_id = outgoing_edge.get('target')

            # fetch target node from target node id
            target_node_config = None
            for node in nodes:
                if node.get('id') == target_node_id:
                    target_node_config = node
                    break

            if not target_node_config:
                return None

            # get next node
            target_node = node_classes.get(NodeType.value_of(target_node_config.get('data', {}).get('type')))

            return target_node(
                tenant_id=workflow_run_state.tenant_id,
                app_id=workflow_run_state.app_id,
                workflow_id=workflow_run_state.workflow_id,
                user_id=workflow_run_state.user_id,
                user_from=workflow_run_state.user_from,
                config=target_node_config,
                callbacks=callbacks
            )

    def _is_timed_out(self, start_at: float, max_execution_time: int) -> bool:
        """
        Check timeout
        :param start_at: start time
        :param max_execution_time: max execution time
        :return:
        """
        return time.perf_counter() - start_at > max_execution_time

    def _run_workflow_node(self, workflow_run_state: WorkflowRunState,
                           node: BaseNode,
                           predecessor_node: Optional[BaseNode] = None,
                           callbacks: list[BaseWorkflowCallback] = None) -> None:
        if callbacks:
            for callback in callbacks:
                callback.on_workflow_node_execute_started(
                    node_id=node.node_id,
                    node_type=node.node_type,
                    node_data=node.node_data,
                    node_run_index=len(workflow_run_state.workflow_nodes_and_results) + 1,
                    predecessor_node_id=predecessor_node.node_id if predecessor_node else None
                )

        db.session.close()

        workflow_nodes_and_result = WorkflowNodeAndResult(
            node=node,
            result=None
        )

        # add to workflow_nodes_and_results
        workflow_run_state.workflow_nodes_and_results.append(workflow_nodes_and_result)

        try:
            # run node, result must have inputs, process_data, outputs, execution_metadata
            node_run_result = node.run(
                variable_pool=workflow_run_state.variable_pool
            )
        except GenerateTaskStoppedException as e:
            node_run_result = NodeRunResult(
                status=WorkflowNodeExecutionStatus.FAILED,
                error='Workflow stopped.'
            )
        except Exception as e:
            logger.exception(f"Node {node.node_data.title} run failed: {str(e)}")
            node_run_result = NodeRunResult(
                status=WorkflowNodeExecutionStatus.FAILED,
                error=str(e)
            )

        if node_run_result.status == WorkflowNodeExecutionStatus.FAILED:
            # node run failed
            if callbacks:
                for callback in callbacks:
                    callback.on_workflow_node_execute_failed(
                        node_id=node.node_id,
                        node_type=node.node_type,
                        node_data=node.node_data,
                        error=node_run_result.error,
                        inputs=node_run_result.inputs,
                        outputs=node_run_result.outputs,
                        process_data=node_run_result.process_data,
                    )

            raise ValueError(f"Node {node.node_data.title} run failed: {node_run_result.error}")

        workflow_nodes_and_result.result = node_run_result

        # node run success
        if callbacks:
            for callback in callbacks:
                callback.on_workflow_node_execute_succeeded(
                    node_id=node.node_id,
                    node_type=node.node_type,
                    node_data=node.node_data,
                    inputs=node_run_result.inputs,
                    process_data=node_run_result.process_data,
                    outputs=node_run_result.outputs,
                    execution_metadata=node_run_result.metadata
                )

        if node_run_result.outputs:
            for variable_key, variable_value in node_run_result.outputs.items():
                # append variables to variable pool recursively
                self._append_variables_recursively(
                    variable_pool=workflow_run_state.variable_pool,
                    node_id=node.node_id,
                    variable_key_list=[variable_key],
                    variable_value=variable_value
                )

        if node_run_result.metadata and node_run_result.metadata.get(NodeRunMetadataKey.TOTAL_TOKENS):
            workflow_run_state.total_tokens += int(node_run_result.metadata.get(NodeRunMetadataKey.TOTAL_TOKENS))

        db.session.close()

    def _append_variables_recursively(self, variable_pool: VariablePool,
                                      node_id: str,
                                      variable_key_list: list[str],
                                      variable_value: VariableValue):
        """
        Append variables recursively
        :param variable_pool: variable pool
        :param node_id: node id
        :param variable_key_list: variable key list
        :param variable_value: variable value
        :return:
        """
        variable_pool.append_variable(
            node_id=node_id,
            variable_key_list=variable_key_list,
            value=variable_value
        )

        # if variable_value is a dict, then recursively append variables
        if isinstance(variable_value, dict):
            for key, value in variable_value.items():
                # construct new key list
                new_key_list = variable_key_list + [key]
                self._append_variables_recursively(
                    variable_pool=variable_pool,
                    node_id=node_id,
                    variable_key_list=new_key_list,
                    variable_value=value
                )

    @classmethod
    def handle_special_values(cls, value: Optional[dict]) -> Optional[dict]:
        """
        Handle special values
        :param value: value
        :return:
        """
        if not value:
            return None

        new_value = value.copy()
        if isinstance(new_value, dict):
            for key, val in new_value.items():
                if isinstance(val, FileVar):
                    new_value[key] = val.to_dict()
                elif isinstance(val, list):
                    new_val = []
                    for v in val:
                        if isinstance(v, FileVar):
                            new_val.append(v.to_dict())
                        else:
                            new_val.append(v)

                    new_value[key] = new_val

        return new_value
