'use client'

import React, { useEffect, useState } from 'react'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Modal } from '@/components/ui/Modal'
import { useAppStore } from '@/lib/store'
import { projectsApi } from '@/lib/api'
import { Project, ProjectGroup } from '@/types'

interface ProjectItemProps {
  project: Project
  isDraggedOver: boolean
  onDragStart: (project: Project) => void
  onDragEnd: () => void
  onDragOver: (e: React.DragEvent) => void
  onDragLeave: () => void
  onDrop: (e: React.DragEvent, targetProject: Project) => void
  onClick: (project: Project) => void
  isActive: boolean
}

const ProjectItem: React.FC<ProjectItemProps> = ({
  project,
  isDraggedOver,
  onDragStart,
  onDragEnd,
  onDragOver,
  onDragLeave,
  onDrop,
  onClick,
  isActive
}) => {
  return (
    <div
      draggable
      onDragStart={() => onDragStart(project)}
      onDragEnd={onDragEnd}
      onDragOver={onDragOver}
      onDragLeave={onDragLeave}
      onDrop={(e) => onDrop(e, project)}
      onClick={() => onClick(project)}
      className={`
        p-3 mb-1 rounded cursor-pointer transition-all duration-300 select-none
        ${isActive
          ? 'bg-accent-blue text-white'
          : 'bg-gray-50 hover:bg-gray-100 text-gray-700'
        }
        ${isDraggedOver
          ? 'ring-2 ring-accent-blue ring-opacity-50 bg-blue-50'
          : ''
        }
        hover:shadow-sm
      `}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className="cursor-grab active:cursor-grabbing">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="9" cy="5" r="1"/>
              <circle cx="15" cy="5" r="1"/>
              <circle cx="9" cy="12" r="1"/>
              <circle cx="15" cy="12" r="1"/>
              <circle cx="9" cy="19" r="1"/>
              <circle cx="15" cy="19" r="1"/>
            </svg>
          </div>
          <div>
            <div className="font-medium text-sm">{project.name}</div>
            <div className="text-xs opacity-75">
              {project.description || 'No description'}
            </div>
            <div className="text-xs opacity-50">
              Created: {new Date(project.created_at).toLocaleDateString()}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

interface ProjectGroupItemProps {
  group: ProjectGroup
  onUpdateGroup: (groupId: string, updates: Partial<ProjectGroup>) => void
  onDeleteGroup: (groupId: string) => void
  onToggleCollapse: (groupId: string) => void
  onRemoveProjectFromGroup: (groupId: string, projectId: number) => void
  onProjectClick: (project: Project) => void
  currentProject: Project | null
}

const ProjectGroupItem: React.FC<ProjectGroupItemProps> = ({
  group,
  onUpdateGroup,
  onDeleteGroup,
  onToggleCollapse,
  onRemoveProjectFromGroup,
  onProjectClick,
  currentProject
}) => {
  const [isEditing, setIsEditing] = useState(false)
  const [editName, setEditName] = useState(group.name)

  const handleSaveName = () => {
    onUpdateGroup(group.id, { name: editName })
    setIsEditing(false)
  }

  const handleCancelEdit = () => {
    setEditName(group.name)
    setIsEditing(false)
  }

  return (
    <div className="mb-3 border border-gray-200 rounded-lg bg-white">
      {/* Group Header */}
      <div className="p-3 bg-gray-50 border-b border-gray-200 rounded-t-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <button
              onClick={() => onToggleCollapse(group.id)}
              className="p-1 hover:bg-gray-200 rounded transition-colors"
            >
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                className={`transition-transform ${group.isCollapsed ? '' : 'rotate-90'}`}
              >
                <path d="M9 18l6-6-6-6"/>
              </svg>
            </button>

            {isEditing ? (
              <div className="flex items-center space-x-2">
                <Input
                  value={editName}
                  onChange={(e) => setEditName(e.target.value)}
                  className="text-sm h-6 px-2"
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') handleSaveName()
                    if (e.key === 'Escape') handleCancelEdit()
                  }}
                />
                <button
                  onClick={handleSaveName}
                  className="text-green-600 hover:text-green-700"
                >
                  ✓
                </button>
                <button
                  onClick={handleCancelEdit}
                  className="text-red-600 hover:text-red-700"
                >
                  ✕
                </button>
              </div>
            ) : (
              <div
                className="flex items-center space-x-2"
                onDoubleClick={() => setIsEditing(true)}
              >
                <span className="font-medium text-sm text-gray-700">
                  {group.name}
                </span>
                <span className="text-xs text-gray-500">
                  ({group.projects.length} projects)
                </span>
              </div>
            )}
          </div>

          <div className="flex items-center space-x-1">
            {!isEditing && (
              <button
                onClick={() => setIsEditing(true)}
                className="p-1 text-gray-500 hover:text-gray-700"
                title="Rename group"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                </svg>
              </button>
            )}
            <button
              onClick={() => onDeleteGroup(group.id)}
              className="p-1 text-red-500 hover:text-red-700"
              title="Delete group"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="3,6 5,6 21,6"/>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Group Content */}
      {!group.isCollapsed && (
        <div className="p-2">
          {group.projects.map((project) => (
            <div
              key={project.id}
              onClick={() => onProjectClick(project)}
              className={`
                p-2 mb-1 rounded cursor-pointer transition-all duration-300 text-sm
                ${currentProject?.id === project.id
                  ? 'bg-accent-blue text-white'
                  : 'bg-gray-50 hover:bg-gray-100 text-gray-700'
                }
              `}
            >
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-medium">{project.name}</div>
                  <div className="text-xs opacity-75">
                    {project.description || 'No description'}
                  </div>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    onRemoveProjectFromGroup(group.id, project.id)
                  }}
                  className="p-1 text-red-500 hover:text-red-700 opacity-0 hover:opacity-100 transition-opacity"
                  title="Remove from group"
                >
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export const ProjectList: React.FC = () => {
  const {
    projects,
    projectGroups,
    currentProject,
    addProject,
    setCurrentProject,
    setCreatingProject,
    isCreatingProject,
    setProjects,
    isLoadingProjects,
    setLoadingProjects,
    draggedProject,
    setDraggedProject,
    createProjectGroup,
    addProjectToGroup,
    updateProjectGroup,
    deleteProjectGroup,
    toggleProjectGroupCollapse,
    removeProjectFromGroup
  } = useAppStore()

  const [draggedOverProject, setDraggedOverProject] = useState<Project | null>(null)
  const [showGroupModal, setShowGroupModal] = useState(false)
  const [newGroupName, setNewGroupName] = useState('')

  // Load projects on component mount
  useEffect(() => {
    loadProjects()
  }, [])

  const loadProjects = async () => {
    setLoadingProjects(true)
    try {
      const result = await projectsApi.list()
      if (result.data) {
        setProjects(result.data.projects)
      }
    } catch (error) {
      console.error('Failed to load projects:', error)
    } finally {
      setLoadingProjects(false)
    }
  }

  const handleCreateProject = async () => {
    setCreatingProject(true)
    try {
      const result = await projectsApi.create({
        name: 'New Project',
        description: 'Created from frontend'
      })
      if (result.data) {
        addProject(result.data)
      }
    } catch (error) {
      console.error('Failed to create project:', error)
    } finally {
      setCreatingProject(false)
    }
  }

  const handleDragStart = (project: Project) => {
    setDraggedProject(project)
  }

  const handleDragEnd = () => {
    setDraggedProject(null)
    setDraggedOverProject(null)
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    e.dataTransfer.dropEffect = 'move'
  }

  const handleDragOverProject = (e: React.DragEvent, project: Project) => {
    e.preventDefault()
    if (draggedProject && draggedProject.id !== project.id) {
      setDraggedOverProject(project)
    }
  }

  const handleDragLeave = () => {
    setDraggedOverProject(null)
  }

  const handleDropOnProject = (e: React.DragEvent, targetProject: Project) => {
    e.preventDefault()
    setDraggedOverProject(null)

    if (!draggedProject || draggedProject.id === targetProject.id) return

    // Create a group with the two projects
    createProjectGroup([draggedProject, targetProject], 'New Group')
    setDraggedProject(null)
  }

  const handleCreateGroupModal = () => {
    if (!draggedProject) return
    setShowGroupModal(true)
    setNewGroupName(`Group ${projectGroups.length + 1}`)
  }

  const handleCreateGroup = () => {
    if (!draggedProject) return
    createProjectGroup([draggedProject], newGroupName)
    setShowGroupModal(false)
    setNewGroupName('')
    setDraggedProject(null)
  }

  return (
    <div className="w-[280px] bg-white border-r border-gray-200 flex flex-col">
      <div className="p-5">
        <h2 className="text-lg font-semibold text-gray-800">
          Projects
        </h2>
      </div>

      <div className="flex-1 overflow-y-auto p-2.5 custom-scrollbar">
        {/* Create Project Button at Top */}
        <div className="mb-3">
          <Button
            onClick={handleCreateProject}
            disabled={isCreatingProject}
            className="w-full"
          >
            {isCreatingProject ? 'Creating...' : 'Create New Project'}
          </Button>
        </div>

        {/* Create Group from Dragged Project */}
        {draggedProject && (
          <div className="mb-3 p-3 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-sm text-blue-800 mb-2">
              Drag "{draggedProject.name}" onto another project to group them
            </p>
            <Button
              onClick={handleCreateGroupModal}
              size="sm"
              className="w-full"
            >
              Create New Group
            </Button>
          </div>
        )}

        {isLoadingProjects ? (
          <div className="text-center text-text-muted py-8">
            <p className="text-sm">Loading projects...</p>
          </div>
        ) : (
          <>
            {/* Project Groups */}
            {projectGroups.map((group) => (
              <ProjectGroupItem
                key={group.id}
                group={group}
                onUpdateGroup={updateProjectGroup}
                onDeleteGroup={deleteProjectGroup}
                onToggleCollapse={toggleProjectGroupCollapse}
                onRemoveProjectFromGroup={removeProjectFromGroup}
                onProjectClick={setCurrentProject}
                currentProject={currentProject}
              />
            ))}

            {/* Individual Projects */}
            {projects.length === 0 && projectGroups.length === 0 ? (
              <div className="text-center text-text-muted py-8">
                <p className="text-sm">No projects yet</p>
                <p className="text-xs mt-2">Create your first project to get started</p>
              </div>
            ) : projects.length > 0 && (
              <>
                {projectGroups.length > 0 && (
                  <div className="mb-2 text-xs font-medium text-gray-500 uppercase">
                    Ungrouped Projects
                  </div>
                )}
                {projects.map((project) => (
                  <ProjectItem
                    key={project.id}
                    project={project}
                    isDraggedOver={draggedOverProject?.id === project.id}
                    onDragStart={handleDragStart}
                    onDragEnd={handleDragEnd}
                    onDragOver={handleDragOverProject}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDropOnProject}
                    onClick={setCurrentProject}
                    isActive={currentProject?.id === project.id}
                  />
                ))}
              </>
            )}
          </>
        )}
      </div>

      {/* Create Group Modal */}
      <Modal
        isOpen={showGroupModal}
        onClose={() => {
          setShowGroupModal(false)
          setNewGroupName('')
        }}
        title="Create Project Group"
      >
        <div className="space-y-4">
          <Input
            label="Group Name"
            value={newGroupName}
            onChange={(e) => setNewGroupName(e.target.value)}
            placeholder="Enter group name"
          />
          <div className="flex justify-end space-x-2">
            <Button
              onClick={() => {
                setShowGroupModal(false)
                setNewGroupName('')
              }}
              variant="outline"
            >
              Cancel
            </Button>
            <Button
              onClick={handleCreateGroup}
              disabled={!newGroupName.trim()}
            >
              Create Group
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}