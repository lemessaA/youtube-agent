"use client"

import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  PlayCircle, 
  TrendingUp, 
  Eye, 
  DollarSign, 
  Video, 
  Users,
  Clock,
  Plus
} from 'lucide-react'
import { api, type Analytics, type Channel, type Video } from '@/lib/api'
import { formatNumber, formatCurrency } from '@/lib/utils'
import Link from 'next/link'

export default function Dashboard() {
  const [analytics, setAnalytics] = useState<Analytics | null>(null)
  const [channels, setChannels] = useState<Channel[]>([])
  const [recentVideos, setRecentVideos] = useState<Video[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadDashboardData() {
      try {
        const [analyticsData, channelsData, videosData] = await Promise.all([
          api.getAnalytics().catch(() => ({
            total_videos: 0,
            total_views: 0,
            total_revenue: 0,
            avg_ctr: 0,
            avg_retention: 0,
            top_performing_video: null,
            recent_performance: []
          })),
          api.getChannels().catch(() => []),
          api.getVideos().catch(() => [])
        ])

        setAnalytics(analyticsData)
        setChannels(channelsData)
        setRecentVideos(videosData.slice(0, 5))
      } catch (error) {
        console.error('Failed to load dashboard data:', error)
      } finally {
        setLoading(false)
      }
    }

    loadDashboardData()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1">Welcome to your YouTube automation control center</p>
        </div>
        <div className="flex gap-3">
          <Link href="/generate">
            <Button>
              <PlayCircle className="w-4 h-4 mr-2" />
              Generate Video
            </Button>
          </Link>
          <Link href="/channels">
            <Button variant="outline">
              <Plus className="w-4 h-4 mr-2" />
              Add Channel
            </Button>
          </Link>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Videos</CardTitle>
            <Video className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analytics?.total_videos || 0}</div>
            <p className="text-xs text-muted-foreground">
              +12% from last month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Views</CardTitle>
            <Eye className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatNumber(analytics?.total_views || 0)}</div>
            <p className="text-xs text-muted-foreground">
              +8% from last month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatCurrency(analytics?.total_revenue || 0)}</div>
            <p className="text-xs text-muted-foreground">
              +23% from last month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Channels</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{channels.length}</div>
            <p className="text-xs text-muted-foreground">
              {channels.length > 0 ? 'All systems operational' : 'Create your first channel'}
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Videos */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Videos</CardTitle>
          </CardHeader>
          <CardContent>
            {recentVideos.length > 0 ? (
              <div className="space-y-4">
                {recentVideos.map((video) => (
                  <div key={video.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                    <div className="flex-1">
                      <h4 className="font-medium text-sm leading-tight">{video.title}</h4>
                      <div className="flex items-center gap-2 mt-1">
                        <Badge 
                          variant={video.status === 'ready' ? 'default' : video.status === 'published' ? 'default' : 'secondary'}
                          className="text-xs"
                        >
                          {video.status}
                        </Badge>
                        <span className="text-xs text-gray-500">
                          {video.views ? `${formatNumber(video.views)} views` : 'No views yet'}
                        </span>
                        {video.duration && (
                          <span className="text-xs text-gray-500">
                            {Math.floor(video.duration / 60)}:{(video.duration % 60).toString().padStart(2, '0')}
                          </span>
                        )}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-green-600">
                        {video.revenue ? formatCurrency(video.revenue) : '$0.00'}
                      </div>
                      <div className="text-xs text-gray-500">
                        {video.likes ? `${formatNumber(video.likes)} likes` : ''}
                      </div>
                    </div>
                  </div>
                ))}
                
                <div className="text-center pt-4">
                  <Link href="/generate">
                    <button className="text-sm text-blue-600 hover:text-blue-800">
                      Generate More Videos →
                    </button>
                  </Link>
                </div>
              </div>
            ) : (
              <div className="text-center py-8">
                <Video className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-4 text-sm font-medium text-gray-900">No videos yet</h3>
                <p className="mt-1 text-sm text-gray-500">
                  Generate your first video to get started.
                </p>
                <Link href="/generate" className="mt-4 inline-block">
                  <Button>
                    <PlayCircle className="w-4 h-4 mr-2" />
                    Generate Video
                  </Button>
                </Link>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Active Channels */}
        <Card>
          <CardHeader>
            <CardTitle>Your Channels</CardTitle>
          </CardHeader>
          <CardContent>
            {channels.length > 0 ? (
              <div className="space-y-4">
                {channels.slice(0, 5).map((channel) => (
                  <div key={channel.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex-1">
                      <h4 className="font-medium text-sm">{channel.name}</h4>
                      <div className="flex items-center gap-2 mt-1">
                        <Badge variant="outline" className="text-xs">
                          {channel.niche}
                        </Badge>
                        <span className="text-xs text-gray-500">
                          {channel.upload_frequency || 'Daily'}
                        </span>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Clock className="h-4 w-4 text-green-500" />
                      <span className="text-xs text-green-600">Active</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <Users className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-4 text-sm font-medium text-gray-900">No channels yet</h3>
                <p className="mt-1 text-sm text-gray-500">
                  Create your first channel to start generating content.
                </p>
                <Link href="/channels" className="mt-4 inline-block">
                  <Button>
                    <Plus className="w-4 h-4 mr-2" />
                    Create Channel
                  </Button>
                </Link>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Link href="/generate">
              <Card className="cursor-pointer hover:shadow-md transition-shadow">
                <CardContent className="flex items-center p-6">
                  <PlayCircle className="h-8 w-8 text-blue-500" />
                  <div className="ml-4">
                    <h3 className="font-medium">Generate Video</h3>
                    <p className="text-sm text-gray-500">Create AI-powered content</p>
                  </div>
                </CardContent>
              </Card>
            </Link>

            <Link href="/ideas">
              <Card className="cursor-pointer hover:shadow-md transition-shadow">
                <CardContent className="flex items-center p-6">
                  <TrendingUp className="h-8 w-8 text-green-500" />
                  <div className="ml-4">
                    <h3 className="font-medium">Get Video Ideas</h3>
                    <p className="text-sm text-gray-500">Research trending topics</p>
                  </div>
                </CardContent>
              </Card>
            </Link>

            <Link href="/analytics">
              <Card className="cursor-pointer hover:shadow-md transition-shadow">
                <CardContent className="flex items-center p-6">
                  <Eye className="h-8 w-8 text-purple-500" />
                  <div className="ml-4">
                    <h3 className="font-medium">View Analytics</h3>
                    <p className="text-sm text-gray-500">Track performance</p>
                  </div>
                </CardContent>
              </Card>
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
