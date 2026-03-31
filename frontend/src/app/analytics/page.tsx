"use client"

import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Eye, 
  DollarSign, 
  TrendingUp, 
  Clock,
  ThumbsUp,
  MessageSquare,
  BarChart3,
  Calendar
} from 'lucide-react'
import { api, type Analytics, type Channel, type Video } from '@/lib/api'
import { formatNumber, formatCurrency, formatDate } from '@/lib/utils'

// Mock data for demonstration
const mockPerformanceData = [
  { date: '2024-01-01', views: 1200, revenue: 24.50 },
  { date: '2024-01-02', views: 1850, revenue: 37.20 },
  { date: '2024-01-03', views: 2100, revenue: 42.80 },
  { date: '2024-01-04', views: 1650, revenue: 31.90 },
  { date: '2024-01-05', views: 2800, revenue: 58.40 },
  { date: '2024-01-06', views: 3200, revenue: 67.20 },
  { date: '2024-01-07', views: 2950, revenue: 62.30 },
]

export default function AnalyticsPage() {
  const [analytics, setAnalytics] = useState<Analytics | null>(null)
  const [channels, setChannels] = useState<Channel[]>([])
  const [videos, setVideos] = useState<Video[]>([])
  const [selectedChannel, setSelectedChannel] = useState<string>('all')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadAnalytics() {
      try {
        const [analyticsData, channelsData, videosData] = await Promise.all([
          api.getAnalytics().catch(() => ({
            total_videos: 12,
            total_views: 45670,
            total_revenue: 892.45,
            avg_ctr: 3.2,
            avg_retention: 67.8,
            top_performing_video: null,
            recent_performance: mockPerformanceData
          })),
          api.getChannels().catch(() => []),
          api.getVideos().catch(() => [])
        ])

        setAnalytics(analyticsData)
        setChannels(channelsData)
        setVideos(videosData)
      } catch (error) {
        console.error('Failed to load analytics:', error)
      } finally {
        setLoading(false)
      }
    }

    loadAnalytics()
  }, [selectedChannel])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading analytics...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
          <p className="text-gray-600 mt-1">Track your content performance and revenue</p>
        </div>
        <div className="flex items-center gap-3">
          <select 
            value={selectedChannel}
            onChange={(e) => setSelectedChannel(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Channels</option>
            {channels.map((channel) => (
              <option key={channel.id} value={channel.id}>
                {channel.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Views</CardTitle>
            <Eye className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatNumber(analytics?.total_views || 0)}</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-600">+12.5%</span> from last month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatCurrency(analytics?.total_revenue || 0)}</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-600">+23.1%</span> from last month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg. CTR</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analytics?.avg_ctr?.toFixed(1) || '0.0'}%</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-600">+0.8%</span> from last month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg. Retention</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analytics?.avg_retention?.toFixed(1) || '0.0'}%</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-600">+2.3%</span> from last month
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Performance Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Performance Over Time</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {mockPerformanceData.slice(-7).map((data, index) => (
                <div key={data.date} className="flex items-center justify-between">
                  <div className="text-sm text-gray-600">
                    {formatDate(data.date)}
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="text-sm">
                      <span className="text-gray-500">Views:</span> {formatNumber(data.views)}
                    </div>
                    <div className="text-sm font-medium">
                      {formatCurrency(data.revenue)}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Top Performing Videos */}
        <Card>
          <CardHeader>
            <CardTitle>Top Performing Videos</CardTitle>
          </CardHeader>
          <CardContent>
            {videos.length > 0 ? (
              <div className="space-y-4">
                {videos.slice(0, 5).map((video, index) => (
                  <div key={video.id} className="flex items-center gap-4 p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center justify-center w-8 h-8 bg-blue-100 text-blue-600 rounded-full text-sm font-medium">
                      #{index + 1}
                    </div>
                    <div className="flex-1">
                      <h4 className="font-medium text-sm line-clamp-1">{video.title}</h4>
                      <div className="flex items-center gap-4 mt-1 text-xs text-gray-500">
                        <div className="flex items-center gap-1">
                          <Eye className="h-3 w-3" />
                          {formatNumber(video.views || 0)}
                        </div>
                        <div className="flex items-center gap-1">
                          <ThumbsUp className="h-3 w-3" />
                          {formatNumber(video.likes || 0)}
                        </div>
                        <div className="flex items-center gap-1">
                          <MessageSquare className="h-3 w-3" />
                          {formatNumber(video.comments || 0)}
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium">
                        {formatCurrency(video.revenue || 0)}
                      </div>
                      <Badge 
                        variant={video.status === 'published' ? 'default' : 'secondary'}
                        className="text-xs"
                      >
                        {video.status}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <BarChart3 className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-4 text-sm font-medium text-gray-900">No data available</h3>
                <p className="mt-1 text-sm text-gray-500">
                  Generate some videos to see performance analytics.
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Channel Breakdown */}
      {channels.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Channel Performance</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {channels.map((channel) => (
                <div key={channel.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex-1">
                    <h3 className="font-medium">{channel.name}</h3>
                    <p className="text-sm text-gray-500">{channel.description}</p>
                  </div>
                  <div className="grid grid-cols-4 gap-6 text-center">
                    <div>
                      <div className="text-lg font-bold">12</div>
                      <div className="text-xs text-gray-500">Videos</div>
                    </div>
                    <div>
                      <div className="text-lg font-bold">{formatNumber(15420)}</div>
                      <div className="text-xs text-gray-500">Views</div>
                    </div>
                    <div>
                      <div className="text-lg font-bold">{formatCurrency(312.45)}</div>
                      <div className="text-xs text-gray-500">Revenue</div>
                    </div>
                    <div>
                      <div className="text-lg font-bold">3.4%</div>
                      <div className="text-xs text-gray-500">CTR</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Export Options */}
      <Card>
        <CardHeader>
          <CardTitle>Export & Reports</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-3">
            <Button variant="outline">
              <Calendar className="w-4 h-4 mr-2" />
              Download Monthly Report
            </Button>
            <Button variant="outline">
              <BarChart3 className="w-4 h-4 mr-2" />
              Export Analytics Data
            </Button>
            <Button variant="outline">
              <DollarSign className="w-4 h-4 mr-2" />
              Revenue Summary
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}