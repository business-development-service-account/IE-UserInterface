'use client'

import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { useAppStore } from '@/lib/store'
import { settingsApi } from '@/lib/api'

export const SettingsPanel: React.FC = () => {
  const { settings, setSettings, isLoadingSettings, setLoadingSettings } = useAppStore()
  const [availableTools, setAvailableTools] = useState<string[]>([])
  const [isSaving, setIsSaving] = useState(false)

  useEffect(() => {
    loadSettings()
    loadAvailableTools()
  }, [])

  const loadSettings = async () => {
    setLoadingSettings(true)
    try {
      const result = await settingsApi.get()
      if (result.data) {
        setSettings(result.data)
      }
    } catch (error) {
      console.error('Failed to load settings:', error)
    } finally {
      setLoadingSettings(false)
    }
  }

  const loadAvailableTools = async () => {
    try {
      const result = await settingsApi.getAvailableTools()
      if (result.data) {
        setAvailableTools(result.data)
      }
    } catch (error) {
      console.error('Failed to load available tools:', error)
    }
  }

  const handleSaveSettings = async () => {
    if (!settings) return

    setIsSaving(true)
    try {
      const result = await settingsApi.update(settings)
      if (result.error) {
        console.error('Failed to save settings:', result.error)
      } else {
        console.log('Settings saved successfully')
      }
    } catch (error) {
      console.error('Failed to save settings:', error)
    } finally {
      setIsSaving(false)
    }
  }

  const handleBasicValueChange = (key: string, value: any) => {
    if (!settings) return

    setSettings({
      ...settings,
      basicValues: {
        ...settings.basicValues,
        [key]: value
      }
    })
  }

  const handleToolToggle = (toolName: string) => {
    if (!settings) return

    const currentTools = settings.availableTools || []
    const updatedTools = currentTools.includes(toolName)
      ? currentTools.filter(tool => tool !== toolName)
      : [...currentTools, toolName]

    setSettings({
      ...settings,
      availableTools: updatedTools
    })
  }

  if (isLoadingSettings) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-accent-blue mx-auto mb-4"></div>
          <p className="text-text-muted">Loading settings...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-10 overflow-y-auto h-full custom-scrollbar">
      <div className="max-w-4xl mx-auto">
        <div className="bg-card-bg rounded-lg p-7.5 mb-7.5 shadow-sm">
          <h2 className="text-lg font-semibold text-gray-800 mb-5">Settings</h2>

          {/* Basic Values Section */}
          <div className="space-y-4">
            <h3 className="text-md font-medium text-gray-700 mb-3">Basic Values</h3>

            {settings?.basicValues && Object.entries(settings.basicValues).map(([key, value]) => (
              <div key={key} className="py-4 border-b border-gray-100 last:border-b-0">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {key.charAt(0).toUpperCase() + key.slice(1).replace(/([A-Z])/g, ' $1')}
                </label>
                <Input
                  value={typeof value === 'string' ? value : ''}
                  onChange={(e) => handleBasicValueChange(key, e.target.value)}
                  placeholder={`Enter ${key}`}
                />
              </div>
            ))}

            {(!settings?.basicValues || Object.keys(settings.basicValues).length === 0) && (
              <p className="text-text-muted text-center py-8">
                No basic values configured yet
              </p>
            )}
          </div>

          {/* Available Tools Section */}
          <div className="mt-8">
            <h3 className="text-md font-medium text-gray-700 mb-3">Available Functionalities</h3>

            <div className="space-y-2">
              {availableTools.map((tool) => (
                <label key={tool} className="flex items-center justify-between py-3 px-4 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100">
                  <span className="text-sm font-medium text-gray-700">{tool}</span>
                  <input
                    type="checkbox"
                    checked={settings?.availableTools?.includes(tool) || false}
                    onChange={() => handleToolToggle(tool)}
                    className="w-4 h-4 text-accent-blue border-gray-300 rounded focus:ring-accent-blue"
                  />
                </label>
              ))}
            </div>

            {availableTools.length === 0 && (
              <p className="text-text-muted text-center py-8">
                No tools available. Configure tools in your backend.
              </p>
            )}
          </div>

          {/* Save Button */}
          <div className="mt-8">
            <Button
              onClick={handleSaveSettings}
              disabled={isSaving}
              className="w-full"
            >
              {isSaving ? 'Saving...' : 'Save Settings'}
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}