'use client'

import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { useAppStore } from '@/lib/store'
import { collectionsApi } from '@/lib/api'

export const CollectionConnector: React.FC = () => {
  const { collections, setCollections, addCollection } = useAppStore()
  const [selectedCollection, setSelectedCollection] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    loadCollections()
  }, [])

  const loadCollections = async () => {
    setIsLoading(true)
    try {
      const result = await collectionsApi.list()
      if (result.data) {
        setCollections(result.data)
      }
    } catch (error) {
      console.error('Failed to load collections:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleConnectCollection = async () => {
    if (!selectedCollection) return

    try {
      const result = await collectionsApi.connect(selectedCollection)
      if (result.error) {
        console.error('Failed to connect:', result.error)
      } else {
        console.log('Connected to collection successfully')
      }
    } catch (error) {
      console.error('Failed to connect to collection:', error)
    }
  }

  return (
    <div className="bg-card-bg rounded-lg p-7.5 mb-7.5 shadow-sm">
      <h2 className="text-lg font-semibold text-gray-800 mb-5">Connect a Collection</h2>

      {isLoading ? (
        <div className="text-center py-4 text-text-muted">
          <p className="text-sm">Loading collections...</p>
        </div>
      ) : (
        <div className="space-y-4">
          <select
            value={selectedCollection}
            onChange={(e) => setSelectedCollection(e.target.value)}
            className="w-full px-3 py-2 border border-input-border rounded-md focus:outline-none focus:ring-2 focus:ring-accent-blue focus:border-transparent"
          >
            <option value="">Select a collection</option>
            {collections.map((collection) => (
              <option key={collection.id} value={collection.id}>
                {collection.name}
              </option>
            ))}
          </select>

          {collections.length === 0 && (
            <p className="text-sm text-text-muted text-center py-2">
              No collections available. Create one first.
            </p>
          )}

          <Button
            onClick={handleConnectCollection}
            disabled={!selectedCollection}
            className="w-full"
          >
            Connect to Collection
          </Button>
        </div>
      )}
    </div>
  )
}