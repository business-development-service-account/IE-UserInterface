'use client'

import React from 'react'

export const ChatInterface: React.FC = () => {
  return (
    <div className="flex-1 flex items-center justify-center bg-gray-50">
      <div className="text-center max-w-md">
        <div className="bg-white rounded-lg shadow-md p-8">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Chat Interface
          </h3>
          <p className="text-gray-600 mb-4">
            Chat functionality will be available in future updates. This will allow you to interact with your LangGraph agents and workflows.
          </p>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="font-medium text-blue-900 mb-2">Coming Soon</h4>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• Real-time chat with LangGraph agents</li>
              <li>• Message history and persistence</li>
              <li>• File and document sharing in chat</li>
              <li>• Agent response streaming</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}