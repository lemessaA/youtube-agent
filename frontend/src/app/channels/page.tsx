"use client"

import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Plus, Edit, Trash2, Video, Calendar, Target } from 'lucide-react'
import { api, type Channel } from '@/lib/api'
import { getNicheDisplayName, formatDate } from '@/lib/utils'
import Link from 'next/link'

export default function ChannelsPage() {
  const [channels, setChannels] = useState<Channel[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadChannels() {
      try {
        const channelsData = await api.getChannels()
        setChannels(channelsData)
      } catch (error) {
        console.error('Failed to load channels:', error)
      } finally {
        setLoading(false)
      }
    }

    loadChannels()
  }, [])

  const handleDeleteChannel = async (channelId: string) => {
    if (!confirm('Are you sure you want to delete this channel?')) return

    try {
      await api.deleteChannel(channelId)
      setChannels(channels.filter(c => c.id !== channelId))
    } catch (error) {
      console.error('Failed to delete channel:', error)
      alert('Failed to delete channel')
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading channels...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Channels</h1>
          <p className="text-gray-600 mt-1">Manage your YouTube channels and content strategy</p>
        </div>
        <Link href="/channels/new">
          <Button>
            <Plus className="w-4 h-4 mr-2" />
            Create Channel
          </Button>
        </Link>
      </div>

      {channels.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {channels.map((channel) => (
            <Card key={channel.id} className="hover:shadow-lg transition-shadow">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <Video className="h-6 w-6 text-red-500" />
                  <div className="flex gap-2">
                    <Button variant="ghost" size="sm">
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button 
                      variant="ghost" 
                      size="sm"
                      onClick={() => channel.id && handleDeleteChannel(channel.id)}
                    >
                      <Trash2 className="h-4 w-4 text-red-500" />
                    </Button>
                  </div>
                </div>
                <CardTitle className="text-xl">{channel.name}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <p className="text-sm text-gray-600 line-clamp-2">
                  {channel.description}
                </p>
                
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-500">Niche</span>
                    <Badge variant="outline">
                      {getNicheDisplayName(channel.niche)}
                    </Badge>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-500">Upload Frequency</span>
                    <div className="flex items-center gap-1">
                      <Calendar className="h-3 w-3 text-gray-400" />
                      <span className="text-xs">{channel.upload_frequency || 'Daily'}</span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-500">Video Length</span>
                    <span className="text-xs">{channel.video_length_range || '60-120s'}</span>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-500">Target Audience</span>
                    <div className="flex items-center gap-1">
                      <Target className="h-3 w-3 text-gray-400" />
                      <span className="text-xs">{channel.target_audience}</span>
                    </div>
                  </div>
                </div>

                <div className="pt-3 border-t">
                  <div className="flex gap-2">
                    <Link href={`/generate?channel=${channel.id}`} className="flex-1">
                      <Button variant="default" size="sm" className="w-full">
                        Generate Video
                      </Button>
                    </Link>
                    <Link href={`/ideas?channel=${channel.id}`} className="flex-1">
                      <Button variant="outline" size="sm" className="w-full">
                        Get Ideas
                      </Button>
                    </Link>
                  </div>
                </div>

                {channel.created_at && (
                  <div className="text-xs text-gray-400">
                    Created {formatDate(channel.created_at)}
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <div className="text-center py-16">
          <Video className="mx-auto h-16 w-16 text-gray-400" />
          <h3 className="mt-6 text-lg font-medium text-gray-900">No channels yet</h3>
          <p className="mt-2 text-gray-500 max-w-md mx-auto">
            Create your first YouTube channel to start generating AI-powered content. 
            Each channel can focus on a specific niche for better targeting.
          </p>
          <div className="mt-6">
            <Link href="/channels/new">
              <Button>
                <Plus className="w-4 h-4 mr-2" />
                Create Your First Channel
              </Button>
            </Link>
          </div>
        </div>
      )}
    </div>
  )
}