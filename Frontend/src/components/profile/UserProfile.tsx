'use client'

import React from 'react'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Modal } from '@/components/ui/Modal'
import { useAppStore } from '@/lib/store'
import { User } from '@/types'

interface UserProfileProps {
  isOpen: boolean
  onClose: () => void
}

export const UserProfile: React.FC<UserProfileProps> = ({ isOpen, onClose }) => {
  const { currentUser, setCurrentUser } = useAppStore()
  const [isEditing, setIsEditing] = React.useState(false)
  const [editName, setEditName] = React.useState('')
  const [editEmail, setEditEmail] = React.useState('')

  React.useEffect(() => {
    if (currentUser) {
      setEditName(currentUser.name)
      setEditEmail(currentUser.email)
    }
  }, [currentUser])

  const handleSaveProfile = () => {
    if (!currentUser) return

    const updatedUser: User = {
      ...currentUser,
      name: editName,
      email: editEmail
    }

    setCurrentUser(updatedUser)
    setIsEditing(false)
  }

  const handleCancelEdit = () => {
    if (currentUser) {
      setEditName(currentUser.name)
      setEditEmail(currentUser.email)
    }
    setIsEditing(false)
  }

  if (!currentUser) return null

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="User Profile">
      <div className="space-y-6">
        {/* Avatar and Basic Info */}
        <div className="flex items-center space-x-4">
          <div className="w-16 h-16 bg-accent-blue rounded-full flex items-center justify-center text-white text-xl font-semibold">
            {currentUser.name.charAt(0).toUpperCase()}
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              {currentUser.name}
            </h3>
            <p className="text-sm text-gray-600">
              {currentUser.email}
            </p>
            <p className="text-xs text-gray-500">
              Member since {new Date(currentUser.created_at).toLocaleDateString()}
            </p>
          </div>
        </div>

        {/* Editable Information */}
        {isEditing ? (
          <div className="space-y-4">
            <Input
              label="Name"
              value={editName}
              onChange={(e) => setEditName(e.target.value)}
              placeholder="Enter your name"
            />
            <Input
              label="Email"
              value={editEmail}
              onChange={(e) => setEditEmail(e.target.value)}
              placeholder="Enter your email"
              type="email"
            />
            <div className="flex justify-end space-x-2">
              <Button
                onClick={handleCancelEdit}
                variant="outline"
              >
                Cancel
              </Button>
              <Button
                onClick={handleSaveProfile}
                disabled={!editName.trim() || !editEmail.trim()}
              >
                Save Changes
              </Button>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Name
              </label>
              <p className="text-gray-900">{currentUser.name}</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <p className="text-gray-900">{currentUser.email}</p>
            </div>
            <Button
              onClick={() => setIsEditing(true)}
              variant="outline"
            >
              Edit Profile
            </Button>
          </div>
        )}

        {/* Actions */}
        <div className="border-t pt-4">
          <div className="space-y-2">
            <Button
              variant="outline"
              className="w-full justify-start"
            >
              Account Settings
            </Button>
            <Button
              variant="outline"
              className="w-full justify-start text-red-600 hover:text-red-700 hover:border-red-300"
            >
              Sign Out
            </Button>
          </div>
        </div>
      </div>
    </Modal>
  )
}