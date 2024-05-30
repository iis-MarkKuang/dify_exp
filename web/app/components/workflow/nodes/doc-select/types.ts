import type { CommonNodeType } from '@/app/components/workflow/types'

export type DocSelectNodeType = CommonNodeType & {
  doc_ids: string[]
}
