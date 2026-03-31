"use client"

import { useEffect, useState } from 'react'
import { useSearchParams } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  PlayCircle, 
  Loader2, 
  CheckCircle, 
  AlertCircle, 
  Video,
  Sparkles,
  Clock,
  Target
} from 'lucide-react'
import { api, type Channel, type Video } from '@/lib/api'
import { getNicheDisplayName } from '@/lib/utils'

interface GenerationStep {
  id: string
  title: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  description: string
}

const generationSteps: GenerationStep[] = [
  {
    id: 'research',
    title: 'Research Trending Topics',
    description: 'Finding viral content ideas in your niche',
    status: 'pending'
  },
  {
    id: 'script',
    title: 'Write Engaging Script',
    description: 'Creating a compelling 60-120 second script',
    status: 'pending'
  },
  {
    id: 'title',
    title: 'Optimize Title & Description',
    description: 'Generating SEO-optimized metadata',
    status: 'pending'
  },
  {
    id: 'thumbnail',
    title: 'Design Thumbnail',
    description: 'Creating click-worthy thumbnail design',
    status: 'pending'
  },
  {
    id: 'video',
    title: 'Generate Video',
    description: 'Assembling final video with voiceover',
    status: 'pending'
  }
]

export default function GenerateVideoPage() {
  const searchParams = useSearchParams()
  const channelId = searchParams.get('channel')
  
  const [channels, setChannels] = useState<Channel[]>([])
  const [selectedChannel, setSelectedChannel] = useState<string>(channelId || '')
  const [isGenerating, setIsGenerating] = useState(false)
  const [steps, setSteps] = useState<GenerationStep[]>(generationSteps)
  const [currentStep, setCurrentStep] = useState<string | null>(null)
  const [generatedVideo, setGeneratedVideo] = useState<Video | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadChannels() {
      try {
        const channelsData = await api.getChannels()
        setChannels(channelsData)
        
        if (!selectedChannel && channelsData.length > 0) {
          setSelectedChannel(channelsData[0].id!)
        }
      } catch (error) {
        console.error('Failed to load channels:', error)
      }
    }

    loadChannels()
  }, [selectedChannel])

  const simulateGeneration = async () => {
    setIsGenerating(true)
    setError(null)
    setSteps(generationSteps.map(step => ({ ...step, status: 'pending' })))

    try {
      for (let i = 0; i < steps.length; i++) {
        const step = steps[i]
        setCurrentStep(step.id)
        
        // Update current step to running
        setSteps(prev => prev.map(s => 
          s.id === step.id 
            ? { ...s, status: 'running' }
            : s
        ))

        // Simulate processing time
        await new Promise(resolve => setTimeout(resolve, 2000))

        // Mark as completed
        setSteps(prev => prev.map(s => 
          s.id === step.id 
            ? { ...s, status: 'completed' }
            : s
        ))
      }

      // Simulate successful video generation
      setGeneratedVideo({
        id: 'generated-' + Date.now(),
        channel_id: selectedChannel,
        title: 'How AI Will Change Everything in 2024',
        description: 'Discover the revolutionary AI tools that are transforming industries and how you can leverage them for success.',
        script: 'AI is revolutionizing the way we work...',
        status: 'ready',
        views: 0,
        created_at: new Date().toISOString()
      })

      setCurrentStep(null)
    } catch (error) {
      setError('Failed to generate video. Please try again.')
      setCurrentStep(null)
    } finally {
      setIsGenerating(false)
    }
  }

  const handleGenerate = async () => {
    if (!selectedChannel) return

    try {
      await simulateGeneration()
    } catch (error) {
      console.error('Generation failed:', error)
      setError('Failed to generate video. Please try again.')
    }
  }

  const selectedChannelData = channels.find(c => c.id === selectedChannel)

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900">Generate Video</h1>
        <p className="text-gray-600 mt-2">Create AI-powered content in minutes</p>
      </div>

      {/* Channel Selection */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Video className="h-5 w-5 text-red-500" />
            Select Channel
          </CardTitle>
        </CardHeader>
        <CardContent>
          {channels.length > 0 ? (
            <div className="space-y-3">
              {channels.map((channel) => (
                <label
                  key={channel.id}
                  className={`flex items-center p-4 border rounded-lg cursor-pointer transition-colors ${
                    selectedChannel === channel.id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  <input
                    type="radio"
                    name="channel"
                    value={channel.id}
                    checked={selectedChannel === channel.id}
                    onChange={(e) => setSelectedChannel(e.target.value)}
                    className="sr-only"
                  />
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <div>
                        <h3 className="font-medium">{channel.name}</h3>
                        <div className="flex items-center gap-2 mt-1">
                          <Badge variant="outline">
                            {getNicheDisplayName(channel.niche)}
                          </Badge>
                          <span className="text-sm text-gray-500">
                            {channel.target_audience}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="ml-4">
                    {selectedChannel === channel.id && (
                      <CheckCircle className="h-5 w-5 text-blue-500" />
                    )}
                  </div>
                </label>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <Video className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-4 text-lg font-medium text-gray-900">No channels found</h3>
              <p className="mt-2 text-gray-500">Create a channel first to generate videos.</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Channel Preview */}
      {selectedChannelData && (
        <Card>
          <CardHeader>
            <CardTitle>Generation Settings</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="flex items-center gap-3">
                <Target className="h-5 w-5 text-gray-400" />
                <div>
                  <div className="font-medium text-sm">Niche</div>
                  <div className="text-sm text-gray-600">
                    {getNicheDisplayName(selectedChannelData.niche)}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <Clock className="h-5 w-5 text-gray-400" />
                <div>
                  <div className="font-medium text-sm">Video Length</div>
                  <div className="text-sm text-gray-600">
                    {selectedChannelData.video_length_range || '60-120 seconds'}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <Sparkles className="h-5 w-5 text-gray-400" />
                <div>
                  <div className="font-medium text-sm">Style</div>
                  <div className="text-sm text-gray-600">Faceless automation</div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Generate Button */}
      {selectedChannelData && !isGenerating && !generatedVideo && (
        <div className="text-center">
          <Button 
            size="lg" 
            onClick={handleGenerate}
            className="px-8 py-6 text-lg"
          >
            <PlayCircle className="w-6 h-6 mr-3" />
            Generate AI Video
          </Button>
          <p className="text-sm text-gray-500 mt-3">
            This process typically takes 2-5 minutes
          </p>
        </div>
      )}

      {/* Generation Progress */}
      {isGenerating && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Loader2 className="h-5 w-5 animate-spin" />
              Generating Your Video
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {steps.map((step) => (
                <div key={step.id} className="flex items-center gap-4">
                  <div className="flex items-center justify-center w-8 h-8 rounded-full border-2">
                    {step.status === 'completed' && (
                      <CheckCircle className="w-5 h-5 text-green-500" />
                    )}
                    {step.status === 'running' && (
                      <Loader2 className="w-4 h-4 animate-spin text-blue-500" />
                    )}
                    {step.status === 'pending' && (
                      <div className="w-3 h-3 rounded-full bg-gray-300"></div>
                    )}
                    {step.status === 'failed' && (
                      <AlertCircle className="w-5 h-5 text-red-500" />
                    )}
                  </div>
                  <div className="flex-1">
                    <div className="font-medium text-sm">{step.title}</div>
                    <div className="text-xs text-gray-500">{step.description}</div>
                  </div>
                  <div className="text-xs">
                    {step.status === 'running' && (
                      <Badge>In Progress</Badge>
                    )}
                    {step.status === 'completed' && (
                      <Badge variant="secondary">Complete</Badge>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Error Display */}
      {error && (
        <Card className="border-red-200 bg-red-50">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <AlertCircle className="h-5 w-5 text-red-500" />
              <div>
                <h3 className="font-medium text-red-800">Generation Failed</h3>
                <p className="text-sm text-red-600 mt-1">{error}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Success - Generated Video */}
      {generatedVideo && (
        <Card className="border-green-200 bg-green-50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-green-800">
              <CheckCircle className="h-5 w-5" />
              Video Generated Successfully!
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h3 className="font-medium text-lg">{generatedVideo.title}</h3>
                <p className="text-sm text-gray-600 mt-1">{generatedVideo.description}</p>
              </div>
              
              <div className="flex gap-3">
                <Button>
                  Download Video
                </Button>
                <Button variant="outline">
                  Preview Script
                </Button>
                <Button variant="outline">
                  Edit Details
                </Button>
              </div>

              <div className="text-sm text-gray-500">
                Video is ready for review and publishing. You can make edits or publish directly to your channel.
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {generatedVideo && (
        <div className="text-center">
          <Button 
            size="lg" 
            onClick={() => {
              setGeneratedVideo(null)
              setSteps(generationSteps.map(step => ({ ...step, status: 'pending' })))
            }}
            variant="outline"
          >
            Generate Another Video
          </Button>
        </div>
      )}
    </div>
  )
}