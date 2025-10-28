'use client'

import React, { useState } from 'react'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { useAppStore } from '@/lib/store'
import { collectionsApi } from '@/lib/api'

export const CreateCollection: React.FC = () => {
  const [showForm, setShowForm] = useState(false)
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const { addCollection, isCreatingCollection, setCreatingCollection } = useAppStore()

  const handleCreateCollection = async () => {
    if (!name.trim()) return

    setCreatingCollection(true)
    try {
      const result = await collectionsApi.create(name.trim(), description.trim())
      if (result.data) {
        addCollection(result.data)
        // Reset form
        setName('')
        setDescription('')
        setShowForm(false)
      } else if (result.error) {
        console.error('Failed to create collection:', result.error)
      }
    } catch (error) {
      console.error('Failed to create collection:', error)
    } finally {
      setCreatingCollection(false)
    }
  }

  return (
    <div className="bg-card-bg rounded-lg p-7.5 mb-7.5 shadow-sm">
      <h2 className="text-lg font-semibold text-gray-800 mb-5">Create a Collection</h2>

      <Button
        onClick={() => setShowForm(!showForm)}
        variant="outline"
        className="w-full mb-4"
      >
        + Create New Collection
      </Button>

      {showForm && (
        <div className="bg-gray-50 rounded-lg p-5 space-y-4">
          <Input
            label="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Collection name"
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Collection description"
              rows={3}
              className="w-full px-3 py-2 border border-input-border rounded-md focus:outline-none focus:ring-2 focus:ring-accent-blue focus:border-transparent resize-vertical"
            />
          </div>

          <div className="flex gap-3">
            <Button
              onClick={handleCreateCollection}
              disabled={!name.trim() || isCreatingCollection}
              className="flex-1"
            >
              {isCreatingCollection ? 'Creating...' : 'Create'}
            </Button>
            <Button
              onClick={() => {
                setShowForm(false)
                setName('')
                setDescription('')
              }}
              variant="outline"
              className="flex-1"
            >
              Cancel
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}