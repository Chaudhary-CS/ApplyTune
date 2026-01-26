// YouTube IFrame Player API Type Definitions
declare global {
  interface Window {
    YT: typeof YT
    onYouTubeIframeAPIReady: () => void
  }
}

declare namespace YT {
  enum PlayerState {
    UNSTARTED = -1,
    ENDED = 0,
    PLAYING = 1,
    PAUSED = 2,
    BUFFERING = 3,
    CUED = 5
  }

  interface PlayerOptions {
    height?: string | number
    width?: string | number
    videoId?: string
    playerVars?: PlayerVars
    events?: Events
  }

  interface PlayerVars {
    autoplay?: 0 | 1
    controls?: 0 | 1
    disablekb?: 0 | 1
    enablejsapi?: 0 | 1
    fs?: 0 | 1
    iv_load_policy?: 1 | 3
    loop?: 0 | 1
    modestbranding?: 0 | 1
    origin?: string
    playlist?: string
    playsinline?: 0 | 1
    rel?: 0 | 1
    showinfo?: 0 | 1
    start?: number
    end?: number
  }

  interface Events {
    onReady?: (event: PlayerEvent) => void
    onStateChange?: (event: OnStateChangeEvent) => void
    onPlaybackQualityChange?: (event: OnPlaybackQualityChangeEvent) => void
    onPlaybackRateChange?: (event: OnPlaybackRateChangeEvent) => void
    onError?: (event: OnErrorEvent) => void
    onApiChange?: (event: PlayerEvent) => void
  }

  interface PlayerEvent {
    target: Player
  }

  interface OnStateChangeEvent extends PlayerEvent {
    data: PlayerState
  }

  interface OnPlaybackQualityChangeEvent extends PlayerEvent {
    data: string
  }

  interface OnPlaybackRateChangeEvent extends PlayerEvent {
    data: number
  }

  interface OnErrorEvent extends PlayerEvent {
    data: number
  }

  class Player {
    constructor(elementId: string, options: PlayerOptions)
    
    // Queueing functions
    loadVideoById(videoId: string, startSeconds?: number): void
    cueVideoById(videoId: string, startSeconds?: number): void
    loadVideoByUrl(mediaContentUrl: string, startSeconds?: number): void
    cueVideoByUrl(mediaContentUrl: string, startSeconds?: number): void
    
    // Playback controls
    playVideo(): void
    pauseVideo(): void
    stopVideo(): void
    seekTo(seconds: number, allowSeekAhead: boolean): void
    
    // Volume controls
    setVolume(volume: number): void
    getVolume(): number
    mute(): void
    unMute(): void
    isMuted(): boolean
    
    // Playback status
    getPlayerState(): PlayerState
    getCurrentTime(): number
    getDuration(): number
    getVideoLoadedFraction(): number
    
    // Playback rate
    setPlaybackRate(suggestedRate: number): void
    getPlaybackRate(): number
    getAvailablePlaybackRates(): number[]
    
    // Setting event listeners
    addEventListener(event: string, listener: string): void
    removeEventListener(event: string, listener: string): void
    
    // Accessing and modifying DOM nodes
    getIframe(): HTMLIFrameElement
    destroy(): void
  }
}

export {}
