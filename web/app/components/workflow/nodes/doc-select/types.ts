import type { CommonNodeType, ModelConfig, ValueSelector } from '@/app/components/workflow/types'
import type { RETRIEVE_TYPE } from '@/types/app'

export type MultipleRetrievalConfig = {
  top_k: number
  score_threshold: number | null | undefined
  reranking_model?: {
    provider: string
    model: string
  }
}

export type SingleRetrievalConfig = {
  model: ModelConfig
}

export type DocSelectNodeType = CommonNodeType & {
  dataset_ids: string[]
}
