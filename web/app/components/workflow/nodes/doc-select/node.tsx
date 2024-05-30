import { type FC, useEffect, useRef, useState } from 'react'
import React from 'react'
import type { DocSelectNodeType } from './types'
import { Folder } from '@/app/components/base/icons/src/vender/solid/files'
import type { NodeProps } from '@/app/components/workflow/types'
import {fetchDocs} from '@/service/datasets'
import type {Document} from '@/models/datasets'

const Node: FC<NodeProps<DocSelectNodeType>> = ({
  data,
}) => {
  const [selectedDocuments, setselectedDocuments] = useState<Document[]>([])
  const updateTime = useRef(0)
  useEffect(() => {
    (async () => {
      updateTime.current = updateTime.current + 1
      const currUpdateTime = updateTime.current

      if (data.doc_ids?.length > 0) {
        // TODO remove
        console.log(data.doc_ids);
        const { data: documentsWithDetail } = await fetchDocs({ url: '/datasets/documents', params: { page: 1, ids: data.doc_ids } })
        //  avoid old data overwrite new data
        if (currUpdateTime < updateTime.current)
          return
        setselectedDocuments(documentsWithDetail)
      }
      else {
        setselectedDocuments([])
      }
    })()
  }, [data.doc_ids])

  if (!selectedDocuments.length)
    return null

  return (
    <div className='mb-1 px-3 py-1'>
      <div className='space-y-0.5'>
        {selectedDocuments.map(({ id, name, key }) => (
          <div key={id}
               className='flex items-center h-[26px] bg-gray-100 rounded-md  px-1 text-xs font-normal text-gray-700'>
            <div className='mr-1 shrink-0 p-1 bg-[#F5F8FF] rounded-md border-[0.5px] border-[#E0EAFF]'>
              <Folder className='w-3 h-3 text-[#444CE7]'/>
            </div>
            <div className='grow w-0 text-xs font-normal text-gray-700 truncate'>
              {name}
            </div>
            <div className='grow w-0 text-xs font-normal text-gray-700 truncate'>
              {key}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default React.memo(Node)
