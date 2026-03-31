"use client"

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { ArrowLeft, Video } from 'lucide-react'
import { api, type Channel } from '@/lib/api'
import Link from 'next/link'

const niches = [
  { value: 'ai_tools', label: 'AI Tools', description: 'Latest AI software and applications' },
  { value: 'startup_ideas', label: 'Startup Ideas', description: 'Business opportunities and entrepreneurship' },
  { value: 'tech_explainers', label: 'Tech Explainers', description: 'Technology concepts made simple' },
  { value: 'make_money_online', label: 'Make Money Online', description: 'Online income strategies' },
  { value: 'side_hustles', label: 'Side Hustles', description: 'Part-time income opportunities' },
]

const uploadFrequencies = [
  { value: 'daily', label: 'Daily' },
  { value: 'every_other_day', label: 'Every Other Day' },
  { value: 'weekly', label: 'Weekly' },
  { value: 'bi_weekly', label: 'Bi-Weekly' },
]

const videoLengths = [
  { value: '30-60', label: '30-60 seconds' },
  { value: '60-120', label: '60-120 seconds' },
  { value: '2-5 min', label: '2-5 minutes' },
]

export default function NewChannelPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    niche: '',
    description: '',
    target_audience: '',
    upload_frequency: 'daily',
    video_length_range: '60-120',
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      await api.createChannel(formData as Omit<Channel, 'id' | 'created_at' | 'updated_at'>)
      router.push('/channels')
    } catch (error) {
      console.error('Failed to create channel:', error)
      alert('Failed to create channel. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <div className="flex items-center gap-4 mb-8">
        <Link href="/channels">
          <Button variant="ghost" size="sm">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Channels
          </Button>
        </Link>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center gap-3">
            <Video className="h-6 w-6 text-red-500" />
            <CardTitle>Create New Channel</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Channel Name */}
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                Channel Name *
              </label>
              <input
                type="text"
                id="name"
                name="name"
                required
                value={formData.name}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g., AI Tools Daily"
              />
            </div>

            {/* Niche Selection */}
            <div>
              <label htmlFor="niche" className="block text-sm font-medium text-gray-700 mb-2">
                Niche *
              </label>
              <div className="grid grid-cols-1 gap-3">
                {niches.map((niche) => (
                  <label
                    key={niche.value}
                    className={`flex items-center p-3 border rounded-lg cursor-pointer transition-colors ${
                      formData.niche === niche.value
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-300 hover:border-gray-400'
                    }`}
                  >
                    <input
                      type="radio"
                      name="niche"
                      value={niche.value}
                      checked={formData.niche === niche.value}
                      onChange={handleChange}
                      className="sr-only"
                    />
                    <div className="flex-1">
                      <div className="font-medium text-sm">{niche.label}</div>
                      <div className="text-xs text-gray-500">{niche.description}</div>
                    </div>
                  </label>
                ))}
              </div>
            </div>

            {/* Description */}
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                Channel Description *
              </label>
              <textarea
                id="description"
                name="description"
                required
                value={formData.description}
                onChange={handleChange}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Brief description of your channel's content and purpose..."
              />
            </div>

            {/* Target Audience */}
            <div>
              <label htmlFor="target_audience" className="block text-sm font-medium text-gray-700 mb-2">
                Target Audience *
              </label>
              <input
                type="text"
                id="target_audience"
                name="target_audience"
                required
                value={formData.target_audience}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g., Developers, Entrepreneurs, Tech enthusiasts"
              />
            </div>

            {/* Upload Frequency */}
            <div>
              <label htmlFor="upload_frequency" className="block text-sm font-medium text-gray-700 mb-2">
                Upload Frequency
              </label>
              <select
                id="upload_frequency"
                name="upload_frequency"
                value={formData.upload_frequency}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {uploadFrequencies.map((freq) => (
                  <option key={freq.value} value={freq.value}>
                    {freq.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Video Length */}
            <div>
              <label htmlFor="video_length_range" className="block text-sm font-medium text-gray-700 mb-2">
                Video Length Range
              </label>
              <select
                id="video_length_range"
                name="video_length_range"
                value={formData.video_length_range}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {videoLengths.map((length) => (
                  <option key={length.value} value={length.value}>
                    {length.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex gap-3 pt-4">
              <Link href="/channels" className="flex-1">
                <Button type="button" variant="outline" className="w-full">
                  Cancel
                </Button>
              </Link>
              <Button 
                type="submit" 
                disabled={loading || !formData.name || !formData.niche || !formData.description || !formData.target_audience}
                className="flex-1"
              >
                {loading ? 'Creating...' : 'Create Channel'}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}