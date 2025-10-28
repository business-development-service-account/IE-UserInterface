'use client'

import React from 'react'

export const SkillsEditor: React.FC = () => {
  return (
    <div className="w-1/2 border-r border-gray-200 p-4 bg-white">
      <h3 className="font-medium text-gray-800 mb-4">Skills Editor</h3>
      <div className="text-center text-gray-500">
        <p className="text-sm mb-4">Skills management coming soon</p>
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <h4 className="font-medium text-gray-700 mb-2">Future Features</h4>
          <ul className="text-xs text-gray-600 space-y-1">
            <li>• Create and edit skill templates</li>
            <li>• Import skills from templates</li>
            <li>• Test skills before deployment</li>
            <li>• Version control for skills</li>
          </ul>
        </div>
      </div>
    </div>
  )
}