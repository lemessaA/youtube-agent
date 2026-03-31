"use client"

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { 
  Play, 
  Download, 
  Eye, 
  ThumbsUp, 
  MessageSquare,
  Clock,
  DollarSign,
  ExternalLink
} from 'lucide-react'
import { formatNumber, formatCurrency, getStatusColor } from '@/lib/utils'
import type { Video } from '@/lib/api'

interface VideoCardProps {
  video: Video
  compact?: boolean
}

export function VideoCard({ video, compact = false }: VideoCardProps) {
  const handleDownload = () => {
    if (video.video_url) {
      const downloadUrl = `http://localhost:8000${video.video_url}`
      window.open(downloadUrl, '_blank')
    }
  }

  const handlePreview = () => {
    if (video.video_url) {
      const videoUrl = `http://localhost:8000${video.video_url}`
      window.open(videoUrl, '_blank')
    }
  }

  if (compact) {
    return (
      <Card className="hover:shadow-md transition-shadow">
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <div className="flex-1 pr-4">
              <h4 className="font-medium text-sm line-clamp-2 mb-2">{video.title}</h4>
              <div className="flex items-center gap-3 text-xs text-gray-500">
                <div className="flex items-center gap-1">
                  <Eye className="h-3 w-3" />
                  {formatNumber(video.views || 0)}
                </div>
                <div className="flex items-center gap-1">
                  <DollarSign className="h-3 w-3" />
                  {formatCurrency(video.revenue || 0)}
                </div>
                <Badge variant={video.status === 'ready' ? 'default' : 'secondary'} className="text-xs">
                  {video.status}
                </Badge>
              </div>
            </div>
            <div className="flex gap-1">
              {video.video_url && (
                <>
                  <Button variant="ghost" size="sm" onClick={handlePreview}>
                    <Play className="h-3 w-3" />
                  </Button>
                  <Button variant="ghost" size="sm" onClick={handleDownload}>
                    <Download className="h-3 w-3" />
                  </Button>
                </>
              )}
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardContent className="p-6">
        <div className="space-y-4">
          {/* Header */}
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h3 className="text-lg font-semibold line-clamp-2 mb-2">{video.title}</h3>
              <p className="text-sm text-gray-600 line-clamp-2">{video.description}</p>
            </div>
            <Badge 
              variant={video.status === 'ready' ? 'default' : 'secondary'}
              className="ml-4"
            >
              {video.status}
            </Badge>
          </div>

          {/* Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-3 bg-blue-50 rounded-lg">
              <Eye className="h-4 w-4 mx-auto text-blue-600 mb-1" />
              <div className="text-sm font-bold text-blue-600">
                {formatNumber(video.views || 0)}
              </div>
              <div className="text-xs text-gray-600">Views</div>
            </div>
            
            <div className="text-center p-3 bg-green-50 rounded-lg">
              <ThumbsUp className="h-4 w-4 mx-auto text-green-600 mb-1" />
              <div className="text-sm font-bold text-green-600">
                {formatNumber(video.likes || 0)}
              </div>
              <div className="text-xs text-gray-600">Likes</div>
            </div>
            
            <div className="text-center p-3 bg-purple-50 rounded-lg">
              <MessageSquare className="h-4 w-4 mx-auto text-purple-600 mb-1" />
              <div className="text-sm font-bold text-purple-600">
                {formatNumber(video.comments || 0)}
              </div>
              <div className="text-xs text-gray-600">Comments</div>
            </div>
            
            <div className="text-center p-3 bg-orange-50 rounded-lg">
              <DollarSign className="h-4 w-4 mx-auto text-orange-600 mb-1" />
              <div className="text-sm font-bold text-orange-600">
                {formatCurrency(video.revenue || 0)}
              </div>
              <div className="text-xs text-gray-600">Revenue</div>
            </div>
          </div>

          {/* Duration and Tags */}
          {(video.duration || video.tags?.length) && (
            <div className="flex items-center justify-between">
              {video.duration && (
                <div className="flex items-center gap-1 text-sm text-gray-600">
                  <Clock className="h-4 w-4" />
                  <span>{Math.floor(video.duration / 60)}:{(video.duration % 60).toString().padStart(2, '0')}</span>
                </div>
              )}
              {video.tags && video.tags.length > 0 && (
                <div className="flex flex-wrap gap-1">
                  {video.tags.slice(0, 3).map((tag, index) => (
                    <span key={index} className="px-2 py-1 bg-gray-100 rounded text-xs">
                      #{tag}
                    </span>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Actions */}
          <div className="flex gap-3 pt-4 border-t">
            {video.video_url ? (
              <>
                <Button onClick={handlePreview} className="flex-1">
                  <Play className="h-4 w-4 mr-2" />
                  Watch Video
                </Button>
                <Button onClick={handleDownload} variant="outline">
                  <Download className="h-4 w-4 mr-2" />
                  Download
                </Button>
              </>
            ) : (
              <div className="flex-1 text-center py-2">
                <span className="text-sm text-gray-500">Video file not available</span>
              </div>
            )}
            <Button variant="ghost" size="sm">
              <ExternalLink className="h-4 w-4 mr-2" />
              Edit
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}