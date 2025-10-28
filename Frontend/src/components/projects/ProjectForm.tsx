'use client'

import React, { useState } from 'react'
import { Button } from '@/components/ui/Button'
import { Modal } from '@/components/ui/Modal'
import { Input } from '@/components/ui/Input'
import { projectsApi } from '@/lib/api'
import { useAppStore } from '@/lib/store'
import { CreateProjectRequest } from '@/types'

interface ProjectFormProps {
  isOpen: boolean
  onClose: () => void
}

export const ProjectForm: React.FC<ProjectFormProps> = ({ isOpen, onClose }) => {
  const { addProject, setCreatingProject, isCreatingProject } = useAppStore()
  const [formData, setFormData] = useState<CreateProjectRequest>({
    name: '',
    description: '',
  })
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!formData.name.trim()) {
      setError('Project name is required')
      return
    }

    setCreatingProject(true)
    setError(null)

    try {
      const result = await projectsApi.create(formData)
      if (result.data) {
        addProject(result.data)
        setFormData({ name: '', description: '' })
        onClose()
      } else if (result.error) {
        setError(result.error)
      }
    } catch (error: any) {
      setError(error.response?.data?.error?.message || 'Failed to create project')
    } finally {
      setCreatingProject(false)
    }
  }

  const handleClose = () => {
    if (!isCreatingProject) {
      setFormData({ name: '', description: '' })
      setError(null)
      onClose()
    }
  }

  return (
    <Modal
      isOpen={isOpen}
      onClose={handleClose}
      title="Create New Project"
    >
      <div>
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="name" className="block text-gray-700 font-medium mb-2">
              Project Name *
            </label>
            <Input
              id="name"
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="Enter project name"
              disabled={isCreatingProject}
              required
            />
          </div>

          <div className="mb-6">
            <label htmlFor="description" className="block text-gray-700 font-medium mb-2">
              Description
            </label>
            <textarea
              id="description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              rows={4}
              placeholder="Enter project description (optional)"
              disabled={isCreatingProject}
            />
          </div>

          <div className="flex space-x-4">
            <Button
              type="submit"
              disabled={isCreatingProject}
              className="flex-1"
            >
              {isCreatingProject ? 'Creating...' : 'Create Project'}
            </Button>
            <Button
              type="button"
              variant="secondary"
              onClick={handleClose}
              disabled={isCreatingProject}
              className="flex-1"
            >
              Cancel
            </Button>
          </div>
        </form>
      </div>
    </Modal>
  )
}