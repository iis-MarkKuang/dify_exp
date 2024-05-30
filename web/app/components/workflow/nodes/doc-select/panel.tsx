import type { FC } from 'react'
import React from 'react'
import { useTranslation } from 'react-i18next'
import useConfig from './use-config'
import AddDoc from './components/add-dataset'
import DocumentsV2List from "./components/dataset-list";
import type { DocSelectNodeType } from './types'
import Field from '@/app/components/workflow/nodes/_base/components/field'
import Split from '@/app/components/workflow/nodes/_base/components/split'
import OutputVars, { VarItem } from '@/app/components/workflow/nodes/_base/components/output-vars'
import { InputVarType, type NodePanelProps } from '@/app/components/workflow/types'
import BeforeRunForm from '@/app/components/workflow/nodes/_base/components/before-run-form'
import ResultPanel from '@/app/components/workflow/run/result-panel'

const i18nPrefix = 'workflow.nodes.docSelect'

const Panel: FC<NodePanelProps<DocSelectNodeType>> = ({
  id,
  data,
}) => {
  const { t } = useTranslation()

  const {
    readOnly,
    inputs,
    handleQueryVarChange,
    filterVar,
    handleModelChanged,
    handleCompletionParamsChange,
    handleRetrievalModeChange,
    handleMultipleRetrievalConfigChange,
    selectedDatasets,
    handleOnDatasetsChange,
    isShowSingleRun,
    hideSingleRun,
    runningStatus,
    handleRun,
    handleStop,
    query,
    setQuery,
    runResult,
  } = useConfig(id, data)

  return (
    <div className='mt-2'>
      <div className='px-4 pb-4 space-y-4'>
        {/* {JSON.stringify(inputs, null, 2)} */}

        <Field
          title={t(`${i18nPrefix}.docs`)}
          operations={
            <div className='flex items-center space-x-1'>
              {!readOnly && (<div className='w-px h-3 bg-gray-200'></div>)}
              {!readOnly && (
                <AddDoc
                  selectedIds={inputs.doc_ids}
                  onChange={handleOnDatasetsChange}
                />
              )}
            </div>
          }
        >
          <DocumentsV2List
            list={selectedDatasets}
            onChange={handleOnDatasetsChange}
            readonly={readOnly}
          />
        </Field>
      </div>

      <Split />
      <div className='px-4 pt-4 pb-2'>
        <OutputVars>
          <>
            <VarItem
              name='file_ids'
              type='Array[String]'
              description={t(`${i18nPrefix}.outputVars.file_ids`)}
            />
          </>
        </OutputVars>
        {isShowSingleRun && (
          <BeforeRunForm
            nodeName={inputs.title}
            onHide={hideSingleRun}
            runningStatus={runningStatus}
            onRun={handleRun}
            onStop={handleStop}
            result={<ResultPanel {...runResult} showSteps={false} />}
          />
        )}
      </div>
    </div>
  )
}

export default React.memo(Panel)
