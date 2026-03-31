"use client"

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { 
  Home, 
  Video, 
  TrendingUp, 
  BarChart3, 
  Settings, 
  PlayCircle,
  Lightbulb
} from 'lucide-react'
import { cn } from '@/lib/utils'

const navigation = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Channels', href: '/channels', icon: Video },
  { name: 'All Videos', href: '/videos', icon: PlayCircle },
  { name: 'Generate Video', href: '/generate', icon: PlayCircle },
  { name: 'Video Ideas', href: '/ideas', icon: Lightbulb },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'Trends', href: '/trends', icon: TrendingUp },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export default function Navigation() {
  const pathname = usePathname()

  return (
    <nav className="flex h-full w-64 flex-col bg-gray-900 shadow-xl">
      <div className="flex h-16 shrink-0 items-center px-6">
        <div className="flex items-center">
          <Video className="h-8 w-8 text-red-500 animate-bounce-gentle" />
          <span className="ml-3 text-xl font-semibold text-white">
            YouTube AI
          </span>
        </div>
      </div>
      <div className="flex flex-1 flex-col overflow-y-auto">
        <ul role="list" className="flex flex-1 flex-col gap-y-7">
          <li>
            <ul role="list" className="-mx-2 space-y-1 px-6">
              {navigation.map((item) => {
                const isActive = pathname === item.href
                return (
                  <li key={item.name}>
                    <Link
                      href={item.href}
                      className={cn(
                        'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold transition-all duration-200 transform hover:scale-105',
                        isActive
                          ? 'bg-gray-800 text-white shadow-lg'
                          : 'text-gray-400 hover:text-white hover:bg-gray-800'
                      )}
                    >
                      <item.icon
                        className="h-6 w-6 shrink-0"
                        aria-hidden="true"
                      />
                      {item.name}
                    </Link>
                  </li>
                )
              })}
            </ul>
          </li>
          <li className="mt-auto">
            <div className="px-6 pb-6">
              <div className="rounded-lg bg-gray-800 p-4">
                <div className="flex items-center">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-white">
                      AI Status
                    </p>
                    <p className="text-xs text-gray-400">
                      Groq Connected ✓
                    </p>
                  </div>
                  <div className="ml-3 h-2 w-2 rounded-full bg-green-400"></div>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </nav>
  )
}