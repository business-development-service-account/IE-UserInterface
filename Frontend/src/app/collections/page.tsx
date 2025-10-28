'use client'

import React from 'react'
import { CollectionConnector } from '@/components/collections/CollectionConnector'
import { CreateCollection } from '@/components/collections/CreateCollection'

export default function CollectionsPage() {
  return (
    <div className="p-10 overflow-y-auto h-full custom-scrollbar">
      <div className="max-w-4xl mx-auto">
        <CollectionConnector />
        <CreateCollection />
      </div>
    </div>
  )
}