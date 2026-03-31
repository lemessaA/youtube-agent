"use client"

import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  TrendingUp, 
  RefreshCw, 
  Search, 
  Calendar,
  Hash,
  Eye,
  Clock,
  Globe,
  Lightbulb
} from 'lucide-react'
import { formatNumber } from '@/lib/utils'

interface TrendingTopic {
  id: string
  title: string
  description: string
  category: string
  search_volume: number
  growth_rate: number
  platform: string
  relevance_score: number
  keywords: string[]
  content_ideas: string[]
  created_at: string
}

// Mock trending topics data
const mockTrends: TrendingTopic[] = [
  {
    id: '1',
    title: 'AI Agents Revolution 2024',
    description: 'Autonomous AI agents are transforming business processes and personal productivity',
    category: 'AI Tools',
    search_volume: 150000,
    growth_rate: 340,
    platform: 'Google Trends',
    relevance_score: 95,
    keywords: ['AI agents', 'automation', 'productivity', 'business'],
    content_ideas: [
      'Building your first AI agent in 10 minutes',
      'AI agents vs human workers: The comparison',
      'Top 5 AI agent platforms for beginners'
    ],
    created_at: '2024-01-15T10:00:00Z'
  },
  {
    id: '2',
    title: 'No-Code App Development Surge',
    description: 'Visual programming platforms enabling anyone to create applications without coding',
    category: 'Tech Explainers',
    search_volume: 89000,
    growth_rate: 180,
    platform: 'YouTube Trending',
    relevance_score: 88,
    keywords: ['no-code', 'app development', 'visual programming', 'startup'],
    content_ideas: [
      'I built a $10K/month app without coding',
      'No-code vs traditional programming',
      'Best no-code platforms in 2024'
    ],
    created_at: '2024-01-15T09:30:00Z'
  },
  {
    id: '3',
    title: 'AI-Powered Side Hustles',
    description: 'New income opportunities emerging from AI tools and automation',
    category: 'Side Hustles',
    search_volume: 120000,
    growth_rate: 245,
    platform: 'Social Media',
    relevance_score: 92,
    keywords: ['side hustle', 'AI income', 'automation', 'passive income'],
    content_ideas: [
      '$5K/month with AI writing services',
      'AI side hustles anyone can start today',
      'From zero to $1K with AI tools'
    ],
    created_at: '2024-01-15T08:45:00Z'
  },
  {
    id: '4',
    title: 'Micro-SaaS Boom',
    description: 'Small, focused software solutions solving specific problems for niche markets',
    category: 'Startup Ideas',
    search_volume: 67000,
    growth_rate: 190,
    platform: 'Reddit',
    relevance_score: 85,
    keywords: ['micro saas', 'startup', 'niche market', 'software'],
    content_ideas: [
      'How I built a $2K MRR micro-SaaS',
      'Micro-SaaS ideas with low competition',
      'From idea to first customer in 30 days'
    ],
    created_at: '2024-01-15T08:15:00Z'
  }
]

const categories = [
  'All Categories',
  'AI Tools',
  'Startup Ideas',
  'Tech Explainers',
  'Make Money Online',
  'Side Hustles'
]

const platforms = [
  'All Platforms',
  'Google Trends',
  'YouTube Trending',
  'Social Media',
  'Reddit',
  'Twitter/X'
]

export default function TrendsPage() {
  const [trends, setTrends] = useState<TrendingTopic[]>(mockTrends)
  const [loading, setLoading] = useState(false)
  const [selectedCategory, setSelectedCategory] = useState('All Categories')
  const [selectedPlatform, setSelectedPlatform] = useState('All Platforms')
  const [searchQuery, setSearchQuery] = useState('')

  const refreshTrends = async () => {
    setLoading(true)
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // Add a new trending topic
      const newTrend: TrendingTopic = {
        id: `new-${Date.now()}`,
        title: 'Voice AI Cloning Technology',
        description: 'Advanced voice synthesis creating realistic human speech from text',
        category: 'AI Tools',
        search_volume: 95000,
        growth_rate: 280,
        platform: 'Google Trends',
        relevance_score: 90,
        keywords: ['voice AI', 'text to speech', 'voice cloning', 'synthetic media'],
        content_ideas: [
          'I cloned my voice with AI in 5 minutes',
          'Voice AI: The future of content creation',
          'Ethical concerns with voice cloning technology'
        ],
        created_at: new Date().toISOString()
      }
      
      setTrends(prev => [newTrend, ...prev])
    } catch (error) {
      console.error('Failed to refresh trends:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredTrends = trends.filter(trend => {
    const matchesCategory = selectedCategory === 'All Categories' || trend.category === selectedCategory
    const matchesPlatform = selectedPlatform === 'All Platforms' || trend.platform === selectedPlatform
    const matchesSearch = searchQuery === '' || 
      trend.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      trend.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      trend.keywords.some(keyword => keyword.toLowerCase().includes(searchQuery.toLowerCase()))
    
    return matchesCategory && matchesPlatform && matchesSearch
  })

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Trending Topics</h1>
          <p className="text-gray-600 mt-1">Discover viral content opportunities across platforms</p>
        </div>
        <Button onClick={refreshTrends} disabled={loading}>
          {loading ? (
            <>
              <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
              Refreshing...
            </>
          ) : (
            <>
              <RefreshCw className="w-4 h-4 mr-2" />
              Refresh Trends
            </>
          )}
        </Button>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Search */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search trends..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Category Filter */}
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {categories.map((category) => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </select>

            {/* Platform Filter */}
            <select
              value={selectedPlatform}
              onChange={(e) => setSelectedPlatform(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {platforms.map((platform) => (
                <option key={platform} value={platform}>
                  {platform}
                </option>
              ))}
            </select>
          </div>
        </CardContent>
      </Card>

      {/* Trending Topics */}
      <div className="space-y-6">
        {filteredTrends.length > 0 ? (
          filteredTrends.map((trend, index) => (
            <Card key={trend.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-3">
                    <div className="flex items-center justify-center w-8 h-8 bg-orange-100 text-orange-600 rounded-full text-sm font-bold">
                      #{index + 1}
                    </div>
                    <div className="flex-1">
                      <CardTitle className="text-xl">{trend.title}</CardTitle>
                      <p className="text-gray-600 mt-1">{trend.description}</p>
                    </div>
                  </div>
                  <Badge 
                    variant={trend.relevance_score >= 90 ? "default" : "secondary"}
                    className="ml-4"
                  >
                    {trend.relevance_score}% relevant
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Metrics */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center p-3 bg-blue-50 rounded-lg">
                    <Eye className="h-5 w-5 mx-auto text-blue-500 mb-1" />
                    <div className="text-lg font-bold text-blue-600">
                      {formatNumber(trend.search_volume)}
                    </div>
                    <div className="text-xs text-gray-600">Search Volume</div>
                  </div>
                  <div className="text-center p-3 bg-green-50 rounded-lg">
                    <TrendingUp className="h-5 w-5 mx-auto text-green-500 mb-1" />
                    <div className="text-lg font-bold text-green-600">
                      +{trend.growth_rate}%
                    </div>
                    <div className="text-xs text-gray-600">Growth Rate</div>
                  </div>
                  <div className="text-center p-3 bg-purple-50 rounded-lg">
                    <Globe className="h-5 w-5 mx-auto text-purple-500 mb-1" />
                    <div className="text-sm font-medium text-purple-600">
                      {trend.platform}
                    </div>
                    <div className="text-xs text-gray-600">Platform</div>
                  </div>
                  <div className="text-center p-3 bg-orange-50 rounded-lg">
                    <Hash className="h-5 w-5 mx-auto text-orange-500 mb-1" />
                    <div className="text-sm font-medium text-orange-600">
                      {trend.category}
                    </div>
                    <div className="text-xs text-gray-600">Category</div>
                  </div>
                </div>

                {/* Keywords */}
                <div>
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Related Keywords</h4>
                  <div className="flex flex-wrap gap-2">
                    {trend.keywords.map((keyword, index) => (
                      <Badge key={index} variant="outline">
                        {keyword}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Content Ideas */}
                <div>
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Content Ideas</h4>
                  <div className="space-y-2">
                    {trend.content_ideas.map((idea, index) => (
                      <div key={index} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                        <Lightbulb className="h-4 w-4 text-yellow-500 mt-0.5 flex-shrink-0" />
                        <span className="text-sm text-gray-700">{idea}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="flex items-center justify-between pt-4 border-t">
                  <div className="flex items-center gap-1 text-sm text-gray-500">
                    <Clock className="h-4 w-4" />
                    <span>Updated {new Date(trend.created_at).toLocaleDateString()}</span>
                  </div>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm">
                      Save Topic
                    </Button>
                    <Button size="sm">
                      <Lightbulb className="w-4 h-4 mr-1" />
                      Create Video Idea
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))
        ) : (
          <div className="text-center py-16">
            <Search className="mx-auto h-16 w-16 text-gray-400" />
            <h3 className="mt-6 text-lg font-medium text-gray-900">No trends found</h3>
            <p className="mt-2 text-gray-500">
              Try adjusting your filters or search query to find relevant trends.
            </p>
          </div>
        )}
      </div>

      {/* Insights */}
      <Card>
        <CardHeader>
          <CardTitle>Trend Insights</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">AI Tools</div>
              <div className="text-sm text-gray-600">Fastest growing category</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">+215%</div>
              <div className="text-sm text-gray-600">Average growth rate</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">12 hrs</div>
              <div className="text-sm text-gray-600">Average trend lifespan</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}