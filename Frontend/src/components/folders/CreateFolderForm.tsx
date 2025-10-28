'use client'

import React, { useState } from 'react'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Project, CreateFolderRequest } from '@/types'

interface CreateFolderFormProps {
  isOpen: boolean
  onClose: () => void
  onSubmit: (folderData: CreateFolderRequest) => void
  projects: Project[]
}

export const CreateFolderForm: React.FC<CreateFolderFormProps> = ({
  isOpen,
  onClose,
  onSubmit,
  projects
}) => {
  const [formData, setFormData] = useState<CreateFolderRequest>({
    name: '',
    description: '',
    parentFolderId: 'root',
    projectIds: []
  })

  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      parentFolderId: 'root',
      projectIds: []
    })
  }

  const handleSubmit = () => {
    if (!formData.name.trim()) return

    onSubmit(formData)
    resetForm()
  }

  const handleClose = () => {
    resetForm()
    onClose()
  }

  const handleProjectToggle = (projectId: number) => {
    setFormData(prev => ({
      ...prev,
      projectIds: prev.projectIds.includes(projectId)
        ? prev.projectIds.filter(id => id !== projectId)
        : [...prev.projectIds, projectId]
    }))
  }

  return (
    <div className="space-y-4">
      <Input
        label="Folder Name"
        value={formData.name}
        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
        placeholder="Enter folder name"
        required
      />

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <textarea
          value={formData.description || ''}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          placeholder="Enter folder description (optional)"
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent-blue focus:border-transparent resize-vertical"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Project Access
        </label>
        <div className="space-y-2 max-h-48 overflow-y-auto">
          {projects.length === 0 ? (
            <p className="text-sm text-gray-500 italic">
              No projects available. Create projects first to assign folder access.
            </p>
          ) : (
            projects.map((project) => (
              <label
                key={project.id}
                className="flex items-center space-x-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer"
              >
                <input
                  type="checkbox"
                  checked={formData.projectIds.includes(project.id)}
                  onChange={() => handleProjectToggle(project.id)}
                  className="w-4 h-4 text-accent-blue border-gray-300 rounded focus:ring-accent-blue"
                />
                <div className="flex-1">
                  <div className="font-medium text-gray-900">{project.name}</div>
                  {project.description && (
                    <div className="text-sm text-gray-500">{project.description}</div>
                  )}
                </div>
              </label>
            ))
          )}
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Select which projects should have access to this folder. Subfolders will inherit these permissions.
        </p>
      </div>

      <div className="flex justify-end space-x-2 pt-4 border-t">
        <Button
          onClick={handleClose}
          variant="outline"
        >
          Cancel
        </Button>
        <Button
          onClick={handleSubmit}
          disabled={!formData.name.trim()}
        >
          Create Folder
        </Button>
      </div>
    </div>
  )
}