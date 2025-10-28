'use client'

import React from 'react'
import { ProjectList } from './ProjectList'
import { ChatInterface } from './ChatInterface'
import { SkillsEditor } from './SkillsEditor'
import { FileArea } from './FileArea'
import { useAppStore } from '@/lib/store'

const ContentSelector: React.FC = () => {
  const { selectedContentArea, setSelectedContentArea } = useAppStore()

  // Add Collections option
  const contentOptions = [
    { id: 'collections', label: 'Collections', status: 'Active' },
    { id: 'files', label: 'File Management', status: 'Active' },
    { id: 'tools', label: 'Tools', status: 'Coming Soon' },
    { id: 'skills', label: 'Skills Editor', status: 'Active' }
  ]

  return (
    <div className="grid grid-cols-2 gap-2">
      {/* Left Column: Collections and File Management */}
      <button
        onClick={() => setSelectedContentArea('collections')}
        className={`
          px-3 py-2 rounded-md text-sm font-medium transition-all text-left
          ${selectedContentArea === 'collections'
            ? 'bg-accent-blue text-white'
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }
        `}
      >
        Collections
      </button>

      <button
        onClick={() => setSelectedContentArea('tools')}
        className={`
          px-3 py-2 rounded-md text-sm font-medium transition-all text-left
          ${selectedContentArea === 'tools'
            ? 'bg-accent-blue text-white'
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }
          opacity-60 cursor-not-allowed
        `}
        disabled
      >
        Tools
        <span className="ml-2 text-xs opacity-75">(Coming Soon)</span>
      </button>

      {/* Right Column: Tools and Skills */}
      <button
        onClick={() => setSelectedContentArea('files')}
        className={`
          px-3 py-2 rounded-md text-sm font-medium transition-all text-left
          ${selectedContentArea === 'files'
            ? 'bg-accent-blue text-white'
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }
        `}
      >
        File Management
      </button>

      <button
        onClick={() => setSelectedContentArea('skills')}
        className={`
          px-3 py-2 rounded-md text-sm font-medium transition-all text-left
          ${selectedContentArea === 'skills'
            ? 'bg-accent-blue text-white'
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }
        `}
      >
        Skills Editor
      </button>
    </div>
  )
}

const CollectionsContent: React.FC = () => {
  return (
    <div className="flex-1 flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <div className="bg-white rounded-lg shadow-sm p-8 max-w-md">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Collections</h3>
          <p className="text-gray-600 mb-4">
            Connect to existing collections or create new ones for data management.
          </p>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-blue-800">
              Navigate to the Collections section from the main navigation to manage your data collections.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

const ToolsContent: React.FC = () => {
  return (
    <div className="flex-1 flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <div className="bg-white rounded-lg shadow-sm p-8 max-w-md">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Tools</h3>
          <p className="text-gray-600 mb-4">
            Configure and manage available AI tools and functionalities for your projects.
          </p>
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p className="text-sm text-yellow-800">
              Tools configuration is coming soon. This area will allow you to enable/disable specific AI capabilities.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export const ProjectsLayout: React.FC = () => {
  const { currentProject, selectedContentArea } = useAppStore()

  const renderContentArea = () => {
    switch (selectedContentArea) {
      case 'collections':
        return <CollectionsContent />
      case 'tools':
        return <ToolsContent />
      case 'skills':
        return <SkillsEditor />
      case 'files':
        return <FileArea />
      default:
        return <ToolsContent />
    }
  }

  return (
    <>
      {/* Project Workspace */}
      {currentProject && (
        <div className="flex-1 flex flex-col">
          {/* Project Header */}
          <div className="bg-white border-b border-gray-200 px-6 py-4">
            <div className="flex justify-between items-start">
              {/* Left: Project Information */}
              <div>
                <h1 className="text-xl font-semibold text-gray-800">
                  {currentProject.name}
                </h1>
                {currentProject.description && (
                  <p className="text-gray-600 mt-1">
                    {currentProject.description}
                  </p>
                )}
                <p className="text-sm text-gray-500 mt-2">
                  Created: {new Date(currentProject.created_at).toLocaleDateString()} •
                  Updated: {new Date(currentProject.updated_at).toLocaleDateString()}
                </p>
              </div>

              {/* Right: Vertical Content Selectables */}
              <div className="ml-8">
                <ContentSelector />
              </div>
            </div>
          </div>

          {/* Main Content Area - Two Vertical Sections */}
          <div className="flex-1 flex overflow-hidden">
            {/* Left: Chat Interface */}
            <div className="w-1/2 border-r border-gray-200 flex flex-col">
              <ChatInterface />
            </div>

            {/* Right: Selected Content Area */}
            <div className="w-1/2 flex flex-col">
              {renderContentArea()}
            </div>
          </div>
        </div>
      )}

      {/* Empty State when no project selected */}
      {!currentProject && (
        <div className="flex-1 flex items-center justify-center bg-gray-50">
          <div className="text-center max-w-md">
            <div className="bg-white rounded-lg shadow-md p-8">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">
                Welcome to Project Manager
              </h2>
              <p className="text-gray-600 mb-6">
                Select an existing project from the sidebar or create a new one to get started.
              </p>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h3 className="font-medium text-blue-900 mb-2">Getting Started</h3>
                <ul className="text-sm text-blue-800 space-y-1">
                  <li>• Click "Create New Project" to get started</li>
                  <li>• Select a project from the sidebar to view details</li>
                  <li>• Use the chat interface to interact with your agents</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  )
}