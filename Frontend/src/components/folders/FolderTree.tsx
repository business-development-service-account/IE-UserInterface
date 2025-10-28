'use client'

import React from 'react'
import { Folder, Project } from '@/types'

interface FolderTreeProps {
  folders: Folder[]
  projects: Project[]
  onEdit: (folderId: string) => void
  onDelete: (folderId: string) => void
  onToggleExpansion: (folderId: string) => void
}

interface FolderItemProps {
  folder: Folder
  projects: Project[]
  level: number
  onEdit: (folderId: string) => void
  onDelete: (folderId: string) => void
  onToggleExpansion: (folderId: string) => void
}

const FolderItem: React.FC<FolderItemProps> = ({
  folder,
  projects,
  level,
  onEdit,
  onDelete,
  onToggleExpansion
}) => {
  const hasChildren = false // For now, we'll implement this logic when we have nested folders
  const paddingLeft = `${level * 24}px`

  const getProjectNames = (projectIds: number[]) => {
    return projects
      .filter(p => projectIds.includes(p.id))
      .map(p => p.name)
      .join(', ') || 'No projects'
  }

  return (
    <div className="select-none">
      <div
        className={`
          flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer
          border ${level === 0 ? 'border-gray-200' : 'border-l-2 border-l-gray-300 border-t-0 border-r-0 border-b-0 ml-2'}
        `}
        style={{ paddingLeft: `${level * 20 + 12}px` }}
        onClick={() => onToggleExpansion(folder.id)}
      >
        <div className="flex items-center flex-1">
          {/* Expand/Collapse Icon */}
          {hasChildren && (
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              className={`mr-2 transition-transform ${folder.isExpanded ? 'rotate-90' : ''}`}
            >
              <path d="M9 18l6-6-6-6"/>
            </svg>
          )}

          {/* Folder Icon */}
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            className="mr-3 text-yellow-600"
          >
            <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
          </svg>

          {/* Folder Info */}
          <div className="flex-1">
            <div className="flex items-center">
              <span className="font-medium text-gray-900">{folder.name}</span>
              {folder.isExpanded && (
                <span className="ml-3 text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                  {folder.path}
                </span>
              )}
            </div>
            {folder.description && (
              <p className="text-sm text-gray-600 mt-1">{folder.description}</p>
            )}
            <div className="flex items-center mt-2 text-xs text-gray-500">
              <span className="mr-4">
                Projects: <span className="font-medium">{getProjectNames(folder.projectIds)}</span>
              </span>
              <span>
                Created: {new Date(folder.created_at).toLocaleDateString()}
              </span>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center space-x-2 opacity-0 hover:opacity-100 transition-opacity">
          <button
            onClick={(e) => {
              e.stopPropagation()
              onEdit(folder.id)
            }}
            className="p-1 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded"
            title="Edit folder"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
          </button>
          {folder.id !== 'root' && (
            <button
              onClick={(e) => {
                e.stopPropagation()
                onDelete(folder.id)
              }}
              className="p-1 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded"
              title="Delete folder"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="3,6 5,6 21,6"/>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
              </svg>
            </button>
          )}
        </div>
      </div>

      {/* Children would go here when we implement nested folders */}
    </div>
  )
}

export const FolderTree: React.FC<FolderTreeProps> = ({
  folders,
  projects,
  onEdit,
  onDelete,
  onToggleExpansion
}) => {
  // Filter to show only root folders for now (no nesting implemented yet)
  const rootFolders = folders.filter(f => f.parentFolderId === undefined || f.parentFolderId === 'root')

  if (folders.length === 0) {
    return (
      <div className="text-center py-12">
        <svg
          width="48"
          height="48"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          className="mx-auto text-gray-400 mb-4"
        >
          <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
        </svg>
        <h3 className="text-lg font-medium text-gray-900 mb-2">No folders yet</h3>
        <p className="text-gray-600 mb-6">
          Create your first folder to start organizing your files and managing project access.
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-2">
      <div className="mb-4 pb-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">Folder Structure</h2>
        <p className="text-sm text-gray-600 mt-1">
          Click on folders to expand/collapse, or use the action buttons to edit or delete.
        </p>
      </div>

      {rootFolders.map((folder) => (
        <FolderItem
          key={folder.id}
          folder={folder}
          projects={projects}
          level={0}
          onEdit={onEdit}
          onDelete={onDelete}
          onToggleExpansion={onToggleExpansion}
        />
      ))}
    </div>
  )
}