"use client"

import { useState, useRef } from 'react'
import { Button } from '@/components/ui/button'
import { 
  Play, 
  Pause, 
  Volume2, 
  VolumeX, 
  Maximize, 
  Minimize,
  Download,
  RotateCcw
} from 'lucide-react'

interface VideoPlayerProps {
  videoUrl: string
  title: string
  thumbnail?: string
  className?: string
  autoPlay?: boolean
}

export function VideoPlayer({ 
  videoUrl, 
  title, 
  thumbnail, 
  className = "",
  autoPlay = false 
}: VideoPlayerProps) {
  const [isPlaying, setIsPlaying] = useState(autoPlay)
  const [isMuted, setIsMuted] = useState(false)
  const [isFullscreen, setIsFullscreen] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const videoRef = useRef<HTMLVideoElement>(null)

  const togglePlay = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause()
      } else {
        videoRef.current.play()
      }
      setIsPlaying(!isPlaying)
    }
  }

  const toggleMute = () => {
    if (videoRef.current) {
      videoRef.current.muted = !isMuted
      setIsMuted(!isMuted)
    }
  }

  const toggleFullscreen = () => {
    if (videoRef.current) {
      if (!isFullscreen) {
        videoRef.current.requestFullscreen()
        setIsFullscreen(true)
      } else {
        document.exitFullscreen()
        setIsFullscreen(false)
      }
    }
  }

  const restart = () => {
    if (videoRef.current) {
      videoRef.current.currentTime = 0
      videoRef.current.play()
      setIsPlaying(true)
    }
  }

  const handleDownload = () => {
    const link = document.createElement('a')
    link.href = videoUrl
    link.download = `${title}.mp4`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  const handleTimeUpdate = () => {
    if (videoRef.current) {
      setCurrentTime(videoRef.current.currentTime)
    }
  }

  const handleLoadedMetadata = () => {
    if (videoRef.current) {
      setDuration(videoRef.current.duration)
    }
  }

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const time = Number(e.target.value)
    if (videoRef.current) {
      videoRef.current.currentTime = time
      setCurrentTime(time)
    }
  }

  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60)
    const seconds = Math.floor(time % 60)
    return `${minutes}:${seconds.toString().padStart(2, '0')}`
  }

  return (
    <div className={`relative bg-black rounded-lg overflow-hidden group ${className}`}>
      {/* Video Element */}
      <video 
        ref={videoRef}
        className="w-full h-full object-contain"
        poster={thumbnail}
        onPlay={() => setIsPlaying(true)}
        onPause={() => setIsPlaying(false)}
        onTimeUpdate={handleTimeUpdate}
        onLoadedMetadata={handleLoadedMetadata}
        onEnded={() => setIsPlaying(false)}
        muted={isMuted}
      >
        <source src={videoUrl} type="video/mp4" />
        <p className="text-center text-gray-300 p-8">
          Your browser doesn't support video playback.
          <a href={videoUrl} className="text-blue-400 hover:underline ml-1">
            Download the video instead.
          </a>
        </p>
      </video>

      {/* Controls Overlay */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-black/30 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
        {/* Top Controls */}
        <div className="absolute top-4 left-4 right-4 flex justify-between items-start">
          <div className="bg-black/50 text-white text-sm px-3 py-1 rounded backdrop-blur-sm">
            {title}
          </div>
          <div className="flex gap-2">
            <Button 
              variant="ghost" 
              size="sm" 
              className="bg-black/50 text-white hover:bg-black/70 backdrop-blur-sm"
              onClick={handleDownload}
            >
              <Download className="h-4 w-4" />
            </Button>
            <Button 
              variant="ghost" 
              size="sm" 
              className="bg-black/50 text-white hover:bg-black/70 backdrop-blur-sm"
              onClick={toggleFullscreen}
            >
              <Maximize className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* Center Play Button */}
        {!isPlaying && (
          <div className="absolute inset-0 flex items-center justify-center">
            <Button 
              variant="ghost" 
              size="lg"
              className="bg-white/20 hover:bg-white/30 text-white rounded-full w-20 h-20 backdrop-blur-sm"
              onClick={togglePlay}
            >
              <Play className="h-8 w-8 ml-1" fill="white" />
            </Button>
          </div>
        )}

        {/* Bottom Controls */}
        <div className="absolute bottom-4 left-4 right-4 space-y-2">
          {/* Progress Bar */}
          {duration > 0 && (
            <div className="flex items-center gap-3">
              <span className="text-white text-xs font-mono">
                {formatTime(currentTime)}
              </span>
              <input
                type="range"
                min={0}
                max={duration}
                value={currentTime}
                onChange={handleSeek}
                className="flex-1 h-2 bg-gray-600 rounded-lg appearance-none cursor-pointer"
                style={{
                  background: `linear-gradient(to right, #3b82f6 0%, #3b82f6 ${(currentTime / duration) * 100}%, #6b7280 ${(currentTime / duration) * 100}%, #6b7280 100%)`
                }}
              />
              <span className="text-white text-xs font-mono">
                {formatTime(duration)}
              </span>
            </div>
          )}

          {/* Action Controls */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Button 
                variant="ghost" 
                size="sm"
                className="bg-black/50 text-white hover:bg-black/70 backdrop-blur-sm"
                onClick={togglePlay}
              >
                {isPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
              </Button>
              
              <Button 
                variant="ghost" 
                size="sm"
                className="bg-black/50 text-white hover:bg-black/70 backdrop-blur-sm"
                onClick={restart}
              >
                <RotateCcw className="h-4 w-4" />
              </Button>
              
              <Button 
                variant="ghost" 
                size="sm"
                className="bg-black/50 text-white hover:bg-black/70 backdrop-blur-sm"
                onClick={toggleMute}
              >
                {isMuted ? <VolumeX className="h-4 w-4" /> : <Volume2 className="h-4 w-4" />}
              </Button>
            </div>
            
            <div className="bg-green-600/80 text-white text-xs px-2 py-1 rounded backdrop-blur-sm">
              AI Generated
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}