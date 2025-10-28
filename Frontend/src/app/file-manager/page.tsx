'use client'

import React, { useEffect, useState } from 'react'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Modal } from '@/components/ui/Modal'
import { FolderTree } from '@/components/folders/FolderTree'
import { CreateFolderForm } from '@/components/folders/CreateFolderForm'
import { useAppStore } from '@/lib/store'
import { Folder, CreateFolderRequest } from '@/types'

export default function FileManagerPage() {
  const {
    folders,
    projects,
    currentUser,
    addFolder,
    updateFolder,
    removeFolder,
    setFolders,
    isLoadingFolders,
    setLoadingFolders
  } = useAppStore()

  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [editingFolder, setEditingFolder] = useState<Folder | null>(null)
  const [isEditModalOpen, setIsEditModalOpen] = useState(false)

  useEffect(() => {
    loadFolders()
  }, [])

  const loadFolders = async () => {
    setLoadingFolders(true)
    try {
      // For now, use mock data - replace with actual API call
      const mockFolders: Folder[] = [
        {
          id: 'root',
          name: 'Root',
          description: 'Main folder',
          projectIds: [],
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          createdBy: 1,
          path: '/',
          isExpanded: true
        }
      ]
      setFolders(mockFolders)
    } catch (error) {
      console.error('Failed to load folders:', error)
    } finally {
      setLoadingFolders(false)
    }
  }

  const handleCreateFolder = (folderData: CreateFolderRequest) => {
    if (!currentUser) return

    const newFolder: Folder = {
      id: `folder_${Date.now()}`,
      name: folderData.name,
      description: folderData.description,
      parentFolderId: folderData.parentFolderId || 'root',
      projectIds: folderData.projectIds,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      createdBy: currentUser.id,
      path: folderData.parentFolderId ? `/parent/${folderData.name}` : `/${folderData.name}`,
      isExpanded: false
    }

    addFolder(newFolder)
    setIsCreateModalOpen(false)
  }

  const handleEditFolder = (folderId: string) => {
    const folder = folders.find(f => f.id === folderId)
    if (folder) {
      setEditingFolder(folder)
      setIsEditModalOpen(true)
    }
  }

  const handleUpdateFolder = (updates: Partial<Folder>) => {
    if (editingFolder) {
      updateFolder(editingFolder.id, {
        ...updates,
        updated_at: new Date().toISOString()
      })
      setIsEditModalOpen(false)
      setEditingFolder(null)
    }
  }

  const handleDeleteFolder = (folderId: string) => {
    if (window.confirm('Are you sure you want to delete this folder?')) {
      removeFolder(folderId)
    }
  }

  const handleToggleExpansion = (folderId: string) => {
    updateFolder(folderId, { isExpanded: !folders.find(f => f.id === folderId)?.isExpanded })
  }

  return (
    <div className="p-6 bg-gray-50 h-full">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">File Manager</h1>
              <p className="text-gray-600 mt-1">
                Organize your files and folders, and manage project access permissions.
              </p>
            </div>
            <Button
              onClick={() => setIsCreateModalOpen(true)}
              className="bg-accent-blue hover:bg-accent-blue-hover"
            >
              Create Folder
            </Button>
          </div>
        </div>

        {/* Main Content */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          {isLoadingFolders ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-accent-blue mr-3"></div>
              <span className="text-gray-600">Loading folders...</span>
            </div>
          ) : (
            <FolderTree
              folders={folders}
              projects={projects}
              onEdit={handleEditFolder}
              onDelete={handleDeleteFolder}
              onToggleExpansion={handleToggleExpansion}
            />
          )}
        </div>
      </div>

      {/* Create Folder Modal */}
      <CreateFolderForm
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onSubmit={handleCreateFolder}
        projects={projects}
      />

      {/* Edit Folder Modal */}
      <Modal
        isOpen={isEditModalOpen}
        onClose={() => {
          setIsEditModalOpen(false)
          setEditingFolder(null)
        }}
        title="Edit Folder"
      >
        {editingFolder && (
          <div className="space-y-4">
            <Input
              label="Folder Name"
              value={editingFolder.name}
              onChange={(e) => setEditingFolder({ ...editingFolder, name: e.target.value })}
              placeholder="Enter folder name"
            />
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <textarea
                value={editingFolder.description || ''}
                onChange={(e) => setEditingFolder({ ...editingFolder, description: e.target.value })}
                placeholder="Enter folder description"
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent-blue focus:border-transparent resize-vertical"
              />
            </div>
            <div className="flex justify-end space-x-2">
              <Button
                onClick={() => {
                  setIsEditModalOpen(false)
                  setEditingFolder(null)
                }}
                variant="outline"
              >
                Cancel
              </Button>
              <Button
                onClick={() => handleUpdateFolder(editingFolder)}
                disabled={!editingFolder.name.trim()}
              >
                Save Changes
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  )
}