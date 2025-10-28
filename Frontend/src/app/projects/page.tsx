'use client'

import React, { useState } from 'react'
import { ProjectsLayout } from '@/components/projects/ProjectsLayout'
import { ProjectList } from '@/components/projects/ProjectList'
import { ProjectForm } from '@/components/projects/ProjectForm'
import { UserProfile } from '@/components/profile/UserProfile'
import { Button } from '@/components/ui/Button'
import { useAppStore } from '@/lib/store'

export default function ProjectsPage() {
  const [isFormOpen, setIsFormOpen] = useState(false)
  const [isProfileOpen, setIsProfileOpen] = useState(false)
  const { currentUser } = useAppStore()

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Top Header Section - Full Width */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              Project Manager
            </h1>
          </div>
          <Button
            onClick={() => setIsProfileOpen(true)}
            className="bg-gray-600 hover:bg-gray-700 flex items-center space-x-2"
          >
            <div className="w-6 h-6 bg-white rounded-full flex items-center justify-center text-xs font-semibold text-gray-600">
              {currentUser?.name.charAt(0).toUpperCase()}
            </div>
            <span>{currentUser?.name}</span>
          </Button>
        </div>
      </div>

      {/* Main Content Area - Below Header */}
      <div className="flex flex-1 overflow-hidden">
        {/* Projects List - Left Side */}
        <ProjectList />

        {/* Main Working Area - Right Side */}
        <div className="flex-1 flex flex-col">
          <ProjectsLayout />
        </div>
      </div>

      {/* Project Form Modal */}
      <ProjectForm
        isOpen={isFormOpen}
        onClose={() => setIsFormOpen(false)}
      />

      {/* User Profile Modal */}
      <UserProfile
        isOpen={isProfileOpen}
        onClose={() => setIsProfileOpen(false)}
      />
    </div>
  )
}