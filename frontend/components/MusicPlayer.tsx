'use client'

import { useState, useEffect, useRef } from 'react'

// Types
type Platform = 'none' | 'spotify' | 'youtube'
type PlayerState = 'idle' | 'playing' | 'paused'

interface Track {
  id: string
  title: string
  artist: string
  platform: Platform
  uri?: string // Spotify URI or YouTube video ID
}

export default function MusicPlayer() {
  const [isOpen, setIsOpen] = useState(false)
  const [platform, setPlatform] = useState<Platform>('none')
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<Track[]>([])
  const [currentTrack, setCurrentTrack] = useState<Track | null>(null)
  const [playerState, setPlayerState] = useState<PlayerState>('idle')
  const [volume, setVolume] = useState(30)
  const [isSearching, setIsSearching] = useState(false)
  
  const youtubePlayerRef = useRef<any>(null)

  // Initialize YouTube IFrame API
  useEffect(() => {
    if (typeof window !== 'undefined' && !window.YT) {
      const tag = document.createElement('script')
      tag.src = 'https://www.youtube.com/iframe_api'
      const firstScriptTag = document.getElementsByTagName('script')[0]
      firstScriptTag.parentNode?.insertBefore(tag, firstScriptTag)
    }
  }, [])

  // Search Spotify
  const searchSpotify = async (query: string) => {
    if (!query.trim()) return
    
    setIsSearching(true)
    try {
      // Note: For production, you'd use Spotify Web API
      // This is a simplified example - you'll need to implement proper OAuth
      
      // Mock results for demo (replace with actual API call)
      setTimeout(() => {
        setSearchResults([
          {
            id: '1',
            title: query,
            artist: 'Search Spotify...',
            platform: 'spotify',
            uri: 'spotify:track:mock'
          }
        ])
        setIsSearching(false)
      }, 500)
      
      // Actual implementation would be:
      // const response = await fetch(`/api/spotify/search?q=${query}`)
      // const data = await response.json()
      // setSearchResults(data.tracks)
      
    } catch (error) {
      console.error('Spotify search error:', error)
      setIsSearching(false)
    }
  }

  // Search YouTube
  const searchYouTube = async (query: string) => {
    if (!query.trim()) return
    
    setIsSearching(true)
    try {
      // Note: For production, you'd use YouTube Data API v3
      // You'll need an API key (free tier: 10,000 quota/day)
      
      // Mock results for demo (replace with actual API call)
      setTimeout(() => {
        setSearchResults([
          {
            id: '1',
            title: query,
            artist: 'Search YouTube...',
            platform: 'youtube',
            uri: 'jfKfPfyJRdk' // Example video ID
          }
        ])
        setIsSearching(false)
      }, 500)
      
      // Actual implementation would be:
      // const API_KEY = process.env.NEXT_PUBLIC_YOUTUBE_API_KEY
      // const response = await fetch(
      //   `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${query}&type=video&videoCategoryId=10&key=${API_KEY}`
      // )
      // const data = await response.json()
      // setSearchResults(data.items.map(item => ({
      //   id: item.id.videoId,
      //   title: item.snippet.title,
      //   artist: item.snippet.channelTitle,
      //   platform: 'youtube',
      //   uri: item.id.videoId
      // })))
      
    } catch (error) {
      console.error('YouTube search error:', error)
      setIsSearching(false)
    }
  }

  // Handle search
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (platform === 'spotify') {
      searchSpotify(searchQuery)
    } else if (platform === 'youtube') {
      searchYouTube(searchQuery)
    }
  }

  // Play track
  const playTrack = (track: Track) => {
    setCurrentTrack(track)
    
    if (track.platform === 'youtube') {
      // Initialize YouTube player if not exists
      if (!youtubePlayerRef.current && window.YT) {
        youtubePlayerRef.current = new window.YT.Player('youtube-player', {
          height: '0',
          width: '0',
          videoId: track.uri,
          playerVars: {
            autoplay: 1,
            controls: 0,
          },
          events: {
            onReady: (event: any) => {
              event.target.setVolume(volume)
              event.target.playVideo()
              setPlayerState('playing')
            },
            onStateChange: (event: any) => {
              if (event.data === window.YT.PlayerState.PLAYING) {
                setPlayerState('playing')
              } else if (event.data === window.YT.PlayerState.PAUSED) {
                setPlayerState('paused')
              }
            }
          }
        })
      } else if (youtubePlayerRef.current) {
        youtubePlayerRef.current.loadVideoById(track.uri)
        youtubePlayerRef.current.setVolume(volume)
        setPlayerState('playing')
      }
    } else if (track.platform === 'spotify') {
      // For Spotify, you'd use Spotify Web Playback SDK
      // This requires user authentication (OAuth)
      alert('Spotify playback requires connecting your Spotify account. Feature coming soon!')
    }
  }

  // Toggle play/pause
  const togglePlayPause = () => {
    if (!currentTrack) return
    
    if (currentTrack.platform === 'youtube' && youtubePlayerRef.current) {
      if (playerState === 'playing') {
        youtubePlayerRef.current.pauseVideo()
        setPlayerState('paused')
      } else {
        youtubePlayerRef.current.playVideo()
        setPlayerState('playing')
      }
    }
  }

  // Change volume
  const handleVolumeChange = (newVolume: number) => {
    setVolume(newVolume)
    if (currentTrack?.platform === 'youtube' && youtubePlayerRef.current) {
      youtubePlayerRef.current.setVolume(newVolume)
    }
  }

  // Stop music
  const stopMusic = () => {
    if (youtubePlayerRef.current) {
      youtubePlayerRef.current.stopVideo()
    }
    setCurrentTrack(null)
    setPlayerState('idle')
    setPlatform('none')
    setSearchResults([])
    setSearchQuery('')
    setIsOpen(false)
  }

  return (
    <>
      {/* Hidden YouTube player */}
      <div id="youtube-player" style={{ display: 'none' }}></div>

      {/* Main Widget */}
      <div className="fixed top-20 right-4 z-[100]">
        {!isOpen && !currentTrack && (
          // Minimized - Initial state
          <button
            onClick={() => setIsOpen(true)}
            className="bg-white shadow-apple rounded-full px-6 py-3 border border-gray-100 hover:shadow-lg transition-all flex items-center space-x-2"
          >
            <span className="text-xl">🎵</span>
            <span className="text-sm font-medium text-gray-700">Music</span>
            <span className="text-gray-400">▼</span>
          </button>
        )}

        {!isOpen && currentTrack && (
          // Minimized - Playing
          <div className="bg-white shadow-apple rounded-full px-6 py-3 border border-gray-100 flex items-center space-x-3">
            <span className="text-xl">🎵</span>
            <span className="text-sm font-medium text-gray-700 max-w-32 truncate">
              {currentTrack.title}
            </span>
            <button
              onClick={togglePlayPause}
              className="text-lg hover:scale-110 transition-transform"
            >
              {playerState === 'playing' ? '⏸️' : '▶️'}
            </button>
            <button
              onClick={() => setIsOpen(true)}
              className="text-gray-400 hover:text-gray-600 text-sm"
            >
              ▲
            </button>
            <button
              onClick={stopMusic}
              className="text-gray-400 hover:text-red-500 text-sm"
            >
              ✕
            </button>
          </div>
        )}

        {isOpen && (
          // Expanded Widget
          <div className="bg-white shadow-apple rounded-3xl p-6 border border-gray-100 w-96 max-h-[600px] overflow-y-auto animate-slide-up">
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-gray-900">🎵 Music Player</h3>
              <button
                onClick={() => setIsOpen(false)}
                className="text-gray-400 hover:text-gray-600 text-xl"
              >
                {currentTrack ? '▼' : '✕'}
              </button>
            </div>

            {platform === 'none' && (
              // Platform Selection
              <div className="space-y-3">
                <p className="text-sm text-gray-500 mb-4">Choose your music source:</p>
                
                <button
                  onClick={() => setPlatform('spotify')}
                  className="w-full p-4 rounded-xl border-2 border-gray-200 hover:border-green-500 hover:bg-green-50 transition-all text-left group"
                >
                  <div className="flex items-center space-x-3">
                    <span className="text-2xl">🎧</span>
                    <div>
                      <p className="font-semibold text-gray-900 group-hover:text-green-600">Spotify</p>
                      <p className="text-xs text-gray-500">Search Spotify's library</p>
                      <p className="text-xs text-gray-400 mt-1">ℹ️ Ads depend on your Spotify plan</p>
                    </div>
                  </div>
                </button>

                <button
                  onClick={() => setPlatform('youtube')}
                  className="w-full p-4 rounded-xl border-2 border-gray-200 hover:border-red-500 hover:bg-red-50 transition-all text-left group"
                >
                  <div className="flex items-center space-x-3">
                    <span className="text-2xl">📺</span>
                    <div>
                      <p className="font-semibold text-gray-900 group-hover:text-red-600">YouTube</p>
                      <p className="text-xs text-gray-500">Search YouTube's library</p>
                      <p className="text-xs text-gray-400 mt-1">ℹ️ Ads depend on your YouTube plan</p>
                    </div>
                  </div>
                </button>

                <button
                  onClick={() => setIsOpen(false)}
                  className="w-full p-4 rounded-xl border-2 border-gray-200 hover:border-gray-400 transition-all text-left"
                >
                  <div className="flex items-center space-x-3">
                    <span className="text-2xl">🔇</span>
                    <div>
                      <p className="font-semibold text-gray-900">Silent Mode</p>
                      <p className="text-xs text-gray-500">Focus without music</p>
                    </div>
                  </div>
                </button>
              </div>
            )}

            {platform !== 'none' && (
              <>
                {/* Search Box */}
                <form onSubmit={handleSearch} className="mb-4">
                  <div className="relative">
                    <input
                      type="text"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      placeholder={`Search ${platform === 'spotify' ? 'Spotify' : 'YouTube'}...`}
                      className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-primary-900 focus:border-transparent text-sm"
                    />
                    <button
                      type="submit"
                      disabled={isSearching}
                      className="absolute right-2 top-1/2 -translate-y-1/2 px-4 py-2 bg-primary-900 text-white rounded-lg text-xs font-medium hover:bg-primary-800 disabled:opacity-50"
                    >
                      {isSearching ? '...' : '🔍'}
                    </button>
                  </div>
                </form>

                {/* Search Results */}
                {searchResults.length > 0 && (
                  <div className="mb-4 space-y-2 max-h-64 overflow-y-auto">
                    <p className="text-xs text-gray-500 mb-2">Search results:</p>
                    {searchResults.map((track) => (
                      <button
                        key={track.id}
                        onClick={() => playTrack(track)}
                        className="w-full p-3 rounded-lg border border-gray-200 hover:border-primary-900 hover:bg-primary-50 transition-all text-left"
                      >
                        <p className="font-medium text-sm text-gray-900 truncate">{track.title}</p>
                        <p className="text-xs text-gray-500 truncate">{track.artist}</p>
                      </button>
                    ))}
                  </div>
                )}

                {/* Now Playing */}
                {currentTrack && (
                  <div className="bg-gradient-to-r from-primary-900 to-primary-700 rounded-xl p-4 text-white mb-4">
                    <p className="text-xs opacity-80 mb-1">Now Playing:</p>
                    <p className="font-semibold truncate">{currentTrack.title}</p>
                    <p className="text-sm opacity-90 truncate">{currentTrack.artist}</p>
                    
                    {/* Playback Controls */}
                    <div className="flex items-center justify-between mt-4">
                      <button
                        onClick={togglePlayPause}
                        className="bg-white/20 hover:bg-white/30 rounded-full p-3 transition-all"
                      >
                        <span className="text-2xl">{playerState === 'playing' ? '⏸️' : '▶️'}</span>
                      </button>

                      {/* Volume Control */}
                      <div className="flex items-center space-x-2 flex-1 mx-4">
                        <span className="text-sm">🔊</span>
                        <input
                          type="range"
                          min="0"
                          max="100"
                          value={volume}
                          onChange={(e) => handleVolumeChange(parseInt(e.target.value))}
                          className="flex-1 h-2 bg-white/20 rounded-lg appearance-none cursor-pointer"
                        />
                        <span className="text-xs w-8">{volume}%</span>
                      </div>
                    </div>
                  </div>
                )}

                {/* Actions */}
                <div className="flex space-x-2">
                  <button
                    onClick={() => {
                      setPlatform('none')
                      setSearchResults([])
                      setSearchQuery('')
                    }}
                    className="flex-1 px-4 py-2 rounded-lg border border-gray-200 text-sm font-medium text-gray-700 hover:bg-gray-50"
                  >
                    ← Change Source
                  </button>
                  
                  {currentTrack && (
                    <button
                      onClick={stopMusic}
                      className="px-4 py-2 rounded-lg bg-red-50 text-red-600 text-sm font-medium hover:bg-red-100"
                    >
                      Stop Music
                    </button>
                  )}
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </>
  )
}
