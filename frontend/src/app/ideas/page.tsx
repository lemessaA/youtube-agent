"use client"

import { useEffect, useState } from 'react'
import { useSearchParams } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Lightbulb, 
  TrendingUp, 
  Eye, 
  Sparkles, 
  RefreshCw, 
  PlayCircle,
  Clock,
  Target,
  Hash
} from 'lucide-react'
import { api, type Channel, type VideoIdea } from '@/lib/api'
import { getNicheDisplayName, formatNumber } from '@/lib/utils'
import Link from 'next/link'

// Mock video ideas for demonstration
const mockIdeas: VideoIdea[] = [
  {
    id: '1',
    channel_id: 'channel1',
    title: 'ChatGPT vs Claude: Which AI is Better for Coding?',
    description: 'Compare the top AI coding assistants and see which one developers prefer',
    hook: 'I tested both ChatGPT and Claude for coding for 30 days...',
    call_to_action: 'Subscribe for more AI tool comparisons!',
    tags: ['AI', 'coding', 'productivity', 'comparison'],
    estimated_views: 12500,
    confidence_score: 89,
    trend_source: 'Google Trends',
    created_at: '2024-01-15T10:30:00Z'
  },
  {
    id: '2',
    channel_id: 'channel1',
    title: '5 AI Tools That Will Replace Your Job in 2024',
    description: 'The latest AI breakthroughs that are changing entire industries',
    hook: 'These AI tools are so powerful, they might replace entire careers...',
    call_to_action: 'What AI tool should I review next? Comment below!',
    tags: ['AI', 'jobs', 'automation', 'future'],
    estimated_views: 25600,
    confidence_score: 95,
    trend_source: 'YouTube Trending',
    created_at: '2024-01-15T09:15:00Z'
  },
  {
    id: '3',
    channel_id: 'channel1',
    title: 'Free AI Image Generator Better Than DALL-E?',
    description: 'Testing the newest free AI image generator that everyone is talking about',
    hook: 'This free AI tool creates images that look better than DALL-E...',
    call_to_action: 'Try this tool yourself and let me know what you think!',
    tags: ['AI', 'image generation', 'free tools', 'DALL-E'],
    estimated_views: 18900,
    confidence_score: 82,
    trend_source: 'Reddit',
    created_at: '2024-01-15T08:45:00Z'
  }
]

export default function VideoIdeasPage() {
  const searchParams = useSearchParams()
  const channelParam = searchParams.get('channel')
  
  const [channels, setChannels] = useState<Channel[]>([])
  const [selectedChannel, setSelectedChannel] = useState<string>(channelParam || '')
  const [ideas, setIdeas] = useState<VideoIdea[]>(mockIdeas)
  const [loading, setLoading] = useState(false)
  const [generating, setGenerating] = useState(false)

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

  const generateNewIdeas = async () => {
    if (!selectedChannel) return

    setGenerating(true)
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      // Add new mock ideas
      const newIdeas: VideoIdea[] = [
        {
          id: `new-${Date.now()}`,
          channel_id: selectedChannel,
          title: 'AI That Writes Code Better Than Programmers',
          description: 'Testing the latest coding AI that\'s shocking developers worldwide',
          hook: 'This AI just wrote perfect code in 30 seconds...',
          call_to_action: 'Subscribe for more AI coding reviews!',
          tags: ['AI', 'coding', 'programming', 'automation'],
          estimated_views: 22000,
          confidence_score: 91,
          trend_source: 'Twitter/X',
          created_at: new Date().toISOString()
        }
      ]
      
      setIdeas(prev => [...newIdeas, ...prev])
    } catch (error) {
      console.error('Failed to generate ideas:', error)
    } finally {
      setGenerating(false)
    }
  }

  const selectedChannelData = channels.find(c => c.id === selectedChannel)

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Video Ideas</h1>
          <p className="text-gray-600 mt-1">AI-generated trending video concepts for your channel</p>
        </div>
        <Button 
          onClick={generateNewIdeas} 
          disabled={!selectedChannel || generating}
        >
          {generating ? (
            <>
              <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
              Generating...
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4 mr-2" />
              Generate New Ideas
            </>
          )}
        </Button>
      </div>

      {/* Channel Selection */}
      <Card>
        <CardHeader>
          <CardTitle>Select Channel</CardTitle>
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
                </label>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <Lightbulb className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-4 text-lg font-medium text-gray-900">No channels found</h3>
              <p className="mt-2 text-gray-500">Create a channel first to generate video ideas.</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Video Ideas */}
      {selectedChannelData && (
        <div className="space-y-6">
          <div className="text-center">
            <h2 className="text-xl font-semibold">
              Video Ideas for {selectedChannelData.name}
            </h2>
            <p className="text-gray-600 mt-1">
              Trending content ideas optimized for {getNicheDisplayName(selectedChannelData.niche)}
            </p>
          </div>

          <div className="grid gap-6">
            {ideas.map((idea) => (
              <Card key={idea.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-lg leading-tight">
                        {idea.title}
                      </CardTitle>
                      <p className="text-gray-600 mt-2">{idea.description}</p>
                    </div>
                    <div className="ml-4 text-right">
                      <div className="flex items-center gap-1 text-sm">
                        <Eye className="h-4 w-4 text-gray-400" />
                        <span className="font-medium">
                          {formatNumber(idea.estimated_views)}
                        </span>
                        <span className="text-gray-500">views</span>
                      </div>
                      <Badge 
                        variant={idea.confidence_score >= 90 ? "default" : "secondary"}
                        className="mt-1"
                      >
                        {idea.confidence_score}% confidence
                      </Badge>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <h4 className="text-sm font-medium text-gray-900 mb-1">Hook</h4>
                      <p className="text-sm text-gray-600 italic">"{idea.hook}"</p>
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-gray-900 mb-1">Call to Action</h4>
                      <p className="text-sm text-gray-600 italic">"{idea.call_to_action}"</p>
                    </div>
                  </div>

                  <div>
                    <h4 className="text-sm font-medium text-gray-900 mb-2">Tags</h4>
                    <div className="flex flex-wrap gap-2">
                      {idea.tags.map((tag, index) => (
                        <div key={index} className="flex items-center gap-1 px-2 py-1 bg-gray-100 rounded text-xs">
                          <Hash className="h-3 w-3 text-gray-400" />
                          {tag}
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="flex items-center justify-between pt-4 border-t">
                    <div className="flex items-center gap-4 text-sm text-gray-500">
                      <div className="flex items-center gap-1">
                        <TrendingUp className="h-4 w-4" />
                        <span>Source: {idea.trend_source}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <Clock className="h-4 w-4" />
                        <span>{new Date(idea.created_at!).toLocaleDateString()}</span>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <Button variant="outline" size="sm">
                        Edit Idea
                      </Button>
                      <Link href={`/generate?channel=${selectedChannel}&idea=${idea.id}`}>
                        <Button size="sm">
                          <PlayCircle className="w-4 h-4 mr-1" />
                          Generate Video
                        </Button>
                      </Link>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {ideas.length === 0 && (
            <div className="text-center py-16">
              <Lightbulb className="mx-auto h-16 w-16 text-gray-400" />
              <h3 className="mt-6 text-lg font-medium text-gray-900">No ideas generated yet</h3>
              <p className="mt-2 text-gray-500 max-w-md mx-auto">
                Click "Generate New Ideas" to get AI-powered video concepts trending in your niche.
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}