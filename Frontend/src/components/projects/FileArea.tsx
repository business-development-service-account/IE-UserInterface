'use client'

import React from 'react'

export const FileArea: React.FC = () => {
  return (
    <div className="w-1/2 p-4 bg-white">
      <h3 className="font-medium text-gray-800 mb-4">File Management</h3>
      <div className="text-center text-gray-500">
        <p className="text-sm mb-4">File management coming soon</p>
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <h4 className="font-medium text-gray-700 mb-2">Future Features</h4>
          <ul className="text-xs text-gray-600 space-y-1">
            <li>• Upload and manage project files</li>
            <li>• Support for multiple file formats</li>
            <li>• File preview and editing</li>
            <li>• Cloud storage integration</li>
          </ul>
        </div>
      </div>
    </div>
  )
}