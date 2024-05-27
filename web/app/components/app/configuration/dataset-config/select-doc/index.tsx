'use client'
import type { FC } from 'react'
import React, { useRef, useState } from 'react'
import { useGetState, useInfiniteScroll } from 'ahooks'
import cn from 'classnames'
import { useTranslation } from 'react-i18next'
import Link from 'next/link'
import produce from 'immer'
import TypeIcon from '../type-icon'
import s from './style.module.css'
import Modal from '@/app/components/base/modal'
import type {DataSet, Document} from '@/models/datasets'
import Button from '@/app/components/base/button'
import { fetchDatasets } from '@/service/datasets'
import Loading from '@/app/components/base/loading'
import { formatNumber } from '@/utils/format'

export type ISelectDocProps = {
  isShow: boolean
  onClose: () => void
  selectedIds: string[]
  onSelect: (dataSet: DataSet[]) => void
}

const SelectDoc: FC<ISelectDocProps> = ({
  isShow,
  onClose,
  selectedIds,
  onSelect,
}) => {
  const { t } = useTranslation()
  const [selected, setSelected] = React.useState<Document[]>(selectedIds.map(id => ({ id }) as any))
  const [loaded, setLoaded] = React.useState(false)
  const [documents, setDocuments] = React.useState<Document[] | null>(null)
  const hasNoData = !documents || documents?.length === 0
  const canSelectMulti = true

  const listRef = useRef<HTMLDivElement>(null)
  const [page, setPage, getPage] = useGetState(1)
  const [isNoMore, setIsNoMore] = useState(false)

  useInfiniteScroll(
    async () => {
      if (!isNoMore) {
        const { data, has_more } = await fetchDatasets({ url: '/datasets/documents', params: { page } })
        setPage(getPage() + 1)
        setIsNoMore(!has_more)
        const newList = [...(documents || []), ...data]
        setDocuments(newList)
        setLoaded(true)
        if (!selected.find(item => !item.name))
          return { list: [] }

        const newSelected = produce(selected, (draft) => {
          selected.forEach((item, index) => {
            if (!item.name) { // not fetched database
              const newItem = newList.find(i => i.id === item.id)
              if (newItem)
                draft[index] = newItem
            }
          })
        })
        setSelected(newSelected)
      }
      return { list: [] }
    },
    {
      target: listRef,
      isNoMore: () => {
        return isNoMore
      },
      reloadDeps: [isNoMore],
    },
  )

  const toggleSelect = (document: DataSet) => {
    const isSelected = selected.some(item => item.id === document.id)
    if (isSelected) {
      setSelected(selected.filter(item => item.id !== document.id))
    }
    else {
      if (canSelectMulti)
        setSelected([...selected, document])
      else
        setSelected([document])
    }
  }

  const handleSelect = () => {
    onSelect(selected)
  }
  return (
    <Modal
      isShow={isShow}
      onClose={onClose}
      className='w-[400px]'
      wrapperClassName='!z-[101]'
      title={t('appDebug.feature.doc.selectTitle')}
    >
      {!loaded && (
        <div className='flex h-[200px]'>
          <Loading type='area' />
        </div>
      )}

      {/*TODO Change to doc create*/}
      {(loaded && hasNoData) && (
        <div className='flex items-center justify-center mt-6 rounded-lg space-x-1  h-[128px] text-[13px] border'
          style={{
            background: 'rgba(0, 0, 0, 0.02)',
            borderColor: 'rgba(0, 0, 0, 0.02',
          }}
        >
          <span className='text-gray-500'>{t('appDebug.feature.dataSet.noDataSet')}</span>
          <Link href="/datasets/create" className='font-normal text-[#155EEF]'>{t('appDebug.feature.dataSet.toCreate')}</Link>
        </div>
      )}

      {documents && documents?.length > 0 && (
        <>
          <div ref={listRef} className='mt-7 space-y-1 max-h-[286px] overflow-y-auto'>
            {documents.map(item => (
              <div
                key={item.id}
                className={cn(s.item, selected.some(i => i.id === item.id) && s.selected, 'flex justify-between items-center h-10 px-2 rounded-lg bg-white border border-gray-200  cursor-pointer', !item.embedding_available && s.disabled)}
                onClick={() => {
                  toggleSelect(item)
                }}
              >
                <div className='mr-1 flex items-center'>
                  <div className={cn('mr-2', 'opacity-50')}>
                    <TypeIcon type="upload_file" size='md'/>
                  </div>
                  <div
                    className={cn('max-w-[200px] text-[13px] font-medium text-gray-800 overflow-hidden text-ellipsis whitespace-nowrap', 'opacity-50 !max-w-[120px]')}>{item.name}</div>
                </div>
                <div
                  className={cn('shrink-0 flex text-xs text-gray-500 overflow-hidden whitespace-nowrap', 'opacity-50')}>
                  {/*<span className='max-w-[100px] overflow-hidden text-ellipsis whitespace-nowrap'>{formatNumber(item.word_count)}</span>*/}
                  {/*{t('appDebug.feature.dataSet.words')}*/}
                  <span className='px-0.5'>·</span>
                  <span
                    className='max-w-[100px] min-w-[8px] overflow-hidden text-ellipsis whitespace-nowrap'>{formatNumber(item.document_count)} </span>
                  {t('appDebug.feature.dataSet.textBlocks')}
                </div>
              </div>
            ))}
          </div>
        </>
      )}
      {loaded && (
        <div className='flex justify-between items-center mt-8'>
          <div className='text-sm  font-medium text-gray-700'>
            {selected.length > 0 && `${selected.length} ${t('appDebug.feature.dataSet.selected')}`}
          </div>
          <div className='flex space-x-2'>
            <Button className='!w-24 !h-9' onClick={onClose}>{t('common.operation.cancel')}</Button>
            <Button className='!w-24 !h-9' type='primary' onClick={handleSelect}
                    disabled={hasNoData}>{t('common.operation.add')}</Button>
          </div>
        </div>
      )}
    </Modal>
  )
}
export default React.memo(SelectDoc)
