"use client"

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Settings, 
  Save, 
  Eye, 
  EyeOff,
  Key,
  Database,
  Zap,
  Video,
  Webhook,
  Clock
} from 'lucide-react'

export default function SettingsPage() {
  const [showApiKey, setShowApiKey] = useState(false)
  const [settings, setSettings] = useState({
    // API Configuration
    groq_api_key: 'gsk_...hidden...',
    groq_model: 'llama3-8b-8192',
    groq_temperature: '0.7',
    groq_max_tokens: '1024',

    // Database Configuration
    supabase_url: 'https://example.supabase.co',
    supabase_key: 'sb_...hidden...',

    // YouTube Integration
    youtube_api_key: '',
    youtube_channel_id: '',
    auto_upload: false,

    // Automation Settings
    auto_generation_enabled: true,
    generation_frequency: 'daily',
    generation_time: '09:00',
    max_videos_per_day: '1',

    // Content Preferences
    default_video_length: '60-120',
    default_language: 'en',
    content_rating: 'general',

    // Notifications
    email_notifications: true,
    webhook_url: '',
    notify_on_generation: true,
    notify_on_publish: true,
    notify_on_error: true,
  })

  const handleSettingChange = (key: string, value: string | boolean) => {
    setSettings(prev => ({ ...prev, [key]: value }))
  }

  const handleSaveSettings = async () => {
    try {
      // Here you would save to your API
      console.log('Saving settings:', settings)
      alert('Settings saved successfully!')
    } catch (error) {
      console.error('Failed to save settings:', error)
      alert('Failed to save settings')
    }
  }

  const testConnection = async (type: string) => {
    try {
      // Simulate API test
      await new Promise(resolve => setTimeout(resolve, 1000))
      alert(`${type} connection successful!`)
    } catch (error) {
      alert(`${type} connection failed!`)
    }
  }

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
          <p className="text-gray-600 mt-1">Configure your YouTube automation system</p>
        </div>
        <Button onClick={handleSaveSettings}>
          <Save className="w-4 h-4 mr-2" />
          Save All Settings
        </Button>
      </div>

      {/* API Configuration */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Key className="h-5 w-5" />
            API Configuration
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Groq Settings */}
          <div className="space-y-4">
            <h3 className="text-lg font-medium flex items-center gap-2">
              <Zap className="h-5 w-5 text-blue-500" />
              Groq AI Configuration
              <Badge variant="default">Connected</Badge>
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  API Key
                </label>
                <div className="relative">
                  <input
                    type={showApiKey ? 'text' : 'password'}
                    value={settings.groq_api_key}
                    onChange={(e) => handleSettingChange('groq_api_key', e.target.value)}
                    className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <button
                    type="button"
                    onClick={() => setShowApiKey(!showApiKey)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2"
                  >
                    {showApiKey ? (
                      <EyeOff className="h-4 w-4 text-gray-400" />
                    ) : (
                      <Eye className="h-4 w-4 text-gray-400" />
                    )}
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Model
                </label>
                <select
                  value={settings.groq_model}
                  onChange={(e) => handleSettingChange('groq_model', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="llama3-8b-8192">Llama 3 8B (Fast)</option>
                  <option value="llama3-70b-8192">Llama 3 70B (Powerful)</option>
                  <option value="mixtral-8x7b-32768">Mixtral 8x7B (Balanced)</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Temperature
                </label>
                <input
                  type="number"
                  min="0"
                  max="1"
                  step="0.1"
                  value={settings.groq_temperature}
                  onChange={(e) => handleSettingChange('groq_temperature', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Max Tokens
                </label>
                <input
                  type="number"
                  min="256"
                  max="4096"
                  value={settings.groq_max_tokens}
                  onChange={(e) => handleSettingChange('groq_max_tokens', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            <Button variant="outline" onClick={() => testConnection('Groq')}>
              Test Groq Connection
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Database Configuration */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Database className="h-5 w-5" />
            Database Configuration
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Supabase URL
              </label>
              <input
                type="url"
                value={settings.supabase_url}
                onChange={(e) => handleSettingChange('supabase_url', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Supabase Key
              </label>
              <input
                type="password"
                value={settings.supabase_key}
                onChange={(e) => handleSettingChange('supabase_key', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          <Button variant="outline" onClick={() => testConnection('Database')}>
            Test Database Connection
          </Button>
        </CardContent>
      </Card>

      {/* YouTube Integration */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Video className="h-5 w-5 text-red-500" />
            YouTube Integration
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                YouTube API Key
              </label>
              <input
                type="password"
                value={settings.youtube_api_key}
                onChange={(e) => handleSettingChange('youtube_api_key', e.target.value)}
                placeholder="Enter your YouTube API key"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Default Channel ID
              </label>
              <input
                type="text"
                value={settings.youtube_channel_id}
                onChange={(e) => handleSettingChange('youtube_channel_id', e.target.value)}
                placeholder="Your YouTube channel ID"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              id="auto_upload"
              checked={settings.auto_upload}
              onChange={(e) => handleSettingChange('auto_upload', e.target.checked)}
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <label htmlFor="auto_upload" className="text-sm font-medium text-gray-700">
              Enable automatic video uploads
            </label>
          </div>
        </CardContent>
      </Card>

      {/* Automation Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Clock className="h-5 w-5" />
            Automation Settings
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              id="auto_generation_enabled"
              checked={settings.auto_generation_enabled}
              onChange={(e) => handleSettingChange('auto_generation_enabled', e.target.checked)}
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <label htmlFor="auto_generation_enabled" className="text-sm font-medium text-gray-700">
              Enable automatic video generation
            </label>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Generation Frequency
              </label>
              <select
                value={settings.generation_frequency}
                onChange={(e) => handleSettingChange('generation_frequency', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="daily">Daily</option>
                <option value="every_other_day">Every Other Day</option>
                <option value="weekly">Weekly</option>
                <option value="bi_weekly">Bi-Weekly</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Generation Time
              </label>
              <input
                type="time"
                value={settings.generation_time}
                onChange={(e) => handleSettingChange('generation_time', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Max Videos Per Day
              </label>
              <select
                value={settings.max_videos_per_day}
                onChange={(e) => handleSettingChange('max_videos_per_day', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="1">1 video</option>
                <option value="2">2 videos</option>
                <option value="3">3 videos</option>
                <option value="5">5 videos</option>
              </select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Notifications */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Webhook className="h-5 w-5" />
            Notifications
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-3">
            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                id="email_notifications"
                checked={settings.email_notifications}
                onChange={(e) => handleSettingChange('email_notifications', e.target.checked)}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <label htmlFor="email_notifications" className="text-sm font-medium text-gray-700">
                Enable email notifications
              </label>
            </div>

            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                id="notify_on_generation"
                checked={settings.notify_on_generation}
                onChange={(e) => handleSettingChange('notify_on_generation', e.target.checked)}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <label htmlFor="notify_on_generation" className="text-sm font-medium text-gray-700">
                Notify when video generation completes
              </label>
            </div>

            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                id="notify_on_error"
                checked={settings.notify_on_error}
                onChange={(e) => handleSettingChange('notify_on_error', e.target.checked)}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <label htmlFor="notify_on_error" className="text-sm font-medium text-gray-700">
                Notify on errors
              </label>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Webhook URL (Optional)
            </label>
            <input
              type="url"
              value={settings.webhook_url}
              onChange={(e) => handleSettingChange('webhook_url', e.target.value)}
              placeholder="https://your-webhook-endpoint.com"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p className="text-xs text-gray-500 mt-1">
              Receive real-time notifications via webhook
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Save Button */}
      <div className="text-center">
        <Button size="lg" onClick={handleSaveSettings}>
          <Save className="w-5 h-5 mr-3" />
          Save All Settings
        </Button>
      </div>
    </div>
  )
}