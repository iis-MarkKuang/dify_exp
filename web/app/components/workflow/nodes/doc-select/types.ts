import type { CommonNodeType, ModelConfig, ValueSelector } from '@/app/components/workflow/types'
import type { RETRIEVE_TYPE } from '@/types/app'

export type DocSelectNodeType = CommonNodeType & {
  query_variable_selector: ValueSelector
  doc_ids: string[]
}
