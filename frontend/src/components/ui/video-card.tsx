"use client"

import { useState } from 'react'
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
  ExternalLink,
  Maximize,
  Minimize
} from 'lucide-react'
import { formatNumber, formatCurrency, getStatusColor } from '@/lib/utils'
import type { Video } from '@/lib/api'

interface VideoCardProps {
  video: Video
  compact?: boolean
  showEmbeddedPlayer?: boolean
}

export function VideoCard({ video, compact = false, showEmbeddedPlayer = false }: VideoCardProps) {
  const [isPlaying, setIsPlaying] = useState(false)
  const [showFullPlayer, setShowFullPlayer] = useState(false)

  const handleDownload = () => {
    if (video.video_url) {
      const downloadUrl = `http://localhost:8000${video.video_url}`
      window.open(downloadUrl, '_blank')
    }
  }

  const handlePreview = () => {
    if (showEmbeddedPlayer && video.video_url) {
      setShowFullPlayer(!showFullPlayer)
    } else if (video.video_url) {
      const videoUrl = `http://localhost:8000${video.video_url}`
      window.open(videoUrl, '_blank')
    }
  }

  const togglePlay = () => {
    setIsPlaying(!isPlaying)
  }

  if (compact) {
    return (
      <Card className="hover:shadow-md transition-shadow">
        <CardContent className="p-4">
          <div className="space-y-3">
            {/* Video Header */}
            <div className="flex items-start justify-between">
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
                  {video.video_url && (
                    <Badge variant="default" className="text-xs bg-green-600">
                      Real MP4 ✓
                    </Badge>
                  )}
                </div>
              </div>
              <div className="flex gap-1">
                {video.video_url && (
                  <>
                    <Button variant="ghost" size="sm" onClick={togglePlay}>
                      <Play className="h-3 w-3" />
                    </Button>
                    <Button variant="ghost" size="sm" onClick={handleDownload}>
                      <Download className="h-3 w-3" />
                    </Button>
                    <Button variant="ghost" size="sm" onClick={handlePreview}>
                      <Maximize className="h-3 w-3" />
                    </Button>
                  </>
                )}
              </div>
            </div>

            {/* Embedded Video Player */}
            {video.video_url && (isPlaying || showEmbeddedPlayer) && (
              <div className="relative">
                <video 
                  className="w-full h-48 bg-black rounded-lg"
                  controls
                  preload="metadata"
                  poster={video.thumbnail_url ? `http://localhost:8000${video.thumbnail_url}` : undefined}
                >
                  <source src={`http://localhost:8000${video.video_url}`} type="video/mp4" />
                  <p className="text-center text-gray-500 p-4">
                    Your browser doesn't support video playback.
                    <a href={`http://localhost:8000${video.video_url}`} className="text-blue-600 hover:underline ml-1">
                      Download the video instead.
                    </a>
                  </p>
                </video>
                
                {/* Video overlay info */}
                <div className="absolute top-2 left-2 bg-black bg-opacity-75 text-white text-xs px-2 py-1 rounded">
                  {video.duration && `${Math.floor(video.duration / 60)}:${(video.duration % 60).toString().padStart(2, '0')}`}
                </div>
                
                <Button 
                  variant="ghost" 
                  size="sm" 
                  className="absolute top-2 right-2 bg-black bg-opacity-75 text-white hover:bg-opacity-90"
                  onClick={() => setIsPlaying(false)}
                >
                  <Minimize className="h-3 w-3" />
                </Button>
              </div>
            )}
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
            <div className="flex items-center gap-2 ml-4">
              <Badge 
                variant={video.status === 'ready' ? 'default' : 'secondary'}
              >
                {video.status}
              </Badge>
              {video.video_url && (
                <Badge variant="default" className="bg-green-600">
                  Real MP4 ✓
                </Badge>
              )}
            </div>
          </div>

          {/* Embedded Video Player for Full Cards */}
          {video.video_url && showEmbeddedPlayer && (
            <div className="relative bg-black rounded-lg overflow-hidden">
              <video 
                className="w-full h-64 object-contain"
                controls
                preload="metadata"
                poster={video.thumbnail_url ? `http://localhost:8000${video.thumbnail_url}` : undefined}
                onPlay={() => setIsPlaying(true)}
                onPause={() => setIsPlaying(false)}
              >
                <source src={`http://localhost:8000${video.video_url}`} type="video/mp4" />
                <p className="text-center text-gray-300 p-8">
                  Your browser doesn't support video playback.
                  <a href={`http://localhost:8000${video.video_url}`} className="text-blue-400 hover:underline ml-1">
                    Download the video instead.
                  </a>
                </p>
              </video>
              
              {/* Video overlay with metadata */}
              <div className="absolute top-3 left-3 flex gap-2">
                {video.duration && (
                  <div className="bg-black bg-opacity-75 text-white text-xs px-2 py-1 rounded">
                    {Math.floor(video.duration / 60)}:{(video.duration % 60).toString().padStart(2, '0')}
                  </div>
                )}
                <div className="bg-green-600 bg-opacity-90 text-white text-xs px-2 py-1 rounded">
                  AI Generated
                </div>
              </div>
            </div>
          )}

          {/* Video Thumbnail/Preview (when not playing) */}
          {video.video_url && !showEmbeddedPlayer && (
            <div 
              className="relative bg-gray-900 rounded-lg overflow-hidden cursor-pointer group h-64 flex items-center justify-center"
              onClick={() => setShowFullPlayer(true)}
            >
              <div className="absolute inset-0 bg-gradient-to-br from-blue-600 to-purple-700 opacity-90"></div>
              
              {/* Play button overlay */}
              <div className="relative z-10 flex flex-col items-center text-white">
                <div className="w-16 h-16 bg-white bg-opacity-20 rounded-full flex items-center justify-center mb-3 group-hover:bg-opacity-30 transition-all">
                  <Play className="w-8 h-8 text-white ml-1" fill="white" />
                </div>
                <p className="text-sm font-medium">Click to play video</p>
                <p className="text-xs opacity-75">AI-generated content ready to watch</p>
              </div>
              
              {/* Video metadata overlay */}
              <div className="absolute bottom-3 left-3 right-3 flex justify-between items-end">
                <div className="text-white text-xs">
                  {video.duration && (
                    <span className="bg-black bg-opacity-50 px-2 py-1 rounded">
                      {Math.floor(video.duration / 60)}:{(video.duration % 60).toString().padStart(2, '0')}
                    </span>
                  )}
                </div>
                <div className="text-white text-xs bg-green-600 bg-opacity-90 px-2 py-1 rounded">
                  MP4 Ready
                </div>
              </div>
            </div>
          )}

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

          {/* Embedded Player Modal */}
          {showFullPlayer && video.video_url && (
            <div className="fixed inset-0 bg-black bg-opacity-90 z-50 flex items-center justify-center p-4">
              <div className="bg-white rounded-lg p-6 max-w-4xl w-full max-h-[90vh] overflow-auto">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold">{video.title}</h3>
                  <Button variant="ghost" onClick={() => setShowFullPlayer(false)}>
                    <ExternalLink className="h-4 w-4" />
                  </Button>
                </div>
                
                <video 
                  className="w-full h-auto bg-black rounded-lg"
                  controls
                  autoPlay
                  preload="metadata"
                >
                  <source src={`http://localhost:8000${video.video_url}`} type="video/mp4" />
                </video>
                
                <div className="mt-4 text-sm text-gray-600">
                  <p>{video.description}</p>
                </div>
              </div>
            </div>
          )}

          {/* Actions */}
          <div className="flex gap-3 pt-4 border-t">
            {video.video_url ? (
              <>
                <Button onClick={handlePreview} className="flex-1">
                  {showEmbeddedPlayer ? <Maximize className="h-4 w-4 mr-2" /> : <Play className="h-4 w-4 mr-2" />}
                  {showEmbeddedPlayer ? 'Full Screen' : 'Play Video'}
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