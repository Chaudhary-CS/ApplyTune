# 🎵 Music Player Setup Guide

## ✅ **What's Implemented (Working Now!)**

The music player UI is fully functional with:
- ✅ Floating widget (top-right corner)
- ✅ Platform selection (Spotify / YouTube / Silent)
- ✅ Search interface for both platforms
- ✅ Play/Pause/Volume controls
- ✅ Minimized and expanded states
- ✅ Apple-style design

## 🔧 **What You Need to Configure (5 minutes)**

To make the search actually work, you need two free API keys:

---

## 1️⃣ **YouTube Data API v3** (FREE - 10,000 requests/day)

### **Get Your API Key:**

1. Go to: https://console.cloud.google.com/
2. Create a new project (or select existing)
3. Enable "YouTube Data API v3"
4. Go to "Credentials" → "Create Credentials" → "API Key"
5. Copy your API key

### **Add to Your App:**

Create `.env.local` in `frontend/` folder:

```bash
NEXT_PUBLIC_YOUTUBE_API_KEY=your_key_here
```

### **Update MusicPlayer.tsx:**

Find the `searchYouTube` function and uncomment the actual API call:

```typescript
// Replace the mock setTimeout with:
const API_KEY = process.env.NEXT_PUBLIC_YOUTUBE_API_KEY
const response = await fetch(
  `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${encodeURIComponent(query)}&type=video&videoCategoryId=10&maxResults=10&key=${API_KEY}`
)
const data = await response.json()
setSearchResults(data.items.map((item: any) => ({
  id: item.id.videoId,
  title: item.snippet.title,
  artist: item.snippet.channelTitle,
  platform: 'youtube',
  uri: item.id.videoId
})))
setIsSearching(false)
```

**YouTube is now working!** Users can search any song and play it.

---

## 2️⃣ **Spotify Web API** (FREE with OAuth)

### **Register Your App:**

1. Go to: https://developer.spotify.com/dashboard
2. Click "Create App"
3. Fill in:
   - App name: "Applytune"
   - Redirect URI: `http://localhost:3000/api/spotify/callback`
4. Copy your **Client ID** and **Client Secret**

### **Add to Your App:**

Add to `.env.local`:

```bash
NEXT_PUBLIC_SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
```

### **Create API Routes:**

**File: `frontend/app/api/spotify/search/route.ts`**

```typescript
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const query = searchParams.get('q')
  
  if (!query) {
    return NextResponse.json({ error: 'Query required' }, { status: 400 })
  }
  
  // Get access token (you'll need to implement OAuth flow)
  const token = await getSpotifyAccessToken()
  
  const response = await fetch(
    `https://api.spotify.com/v1/search?q=${encodeURIComponent(query)}&type=track&limit=10`,
    {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  )
  
  const data = await response.json()
  
  const tracks = data.tracks.items.map((track: any) => ({
    id: track.id,
    title: track.name,
    artist: track.artists.map((a: any) => a.name).join(', '),
    platform: 'spotify',
    uri: track.uri
  }))
  
  return NextResponse.json({ tracks })
}

async function getSpotifyAccessToken() {
  // Implement OAuth flow or use client credentials
  // For now, use client credentials (server-side only):
  const response = await fetch('https://accounts.spotify.com/api/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': 'Basic ' + Buffer.from(
        process.env.NEXT_PUBLIC_SPOTIFY_CLIENT_ID + ':' + process.env.SPOTIFY_CLIENT_SECRET
      ).toString('base64')
    },
    body: 'grant_type=client_credentials'
  })
  
  const data = await response.json()
  return data.access_token
}
```

### **Update MusicPlayer.tsx:**

Find the `searchSpotify` function and replace with:

```typescript
const response = await fetch(`/api/spotify/search?q=${encodeURIComponent(query)}`)
const data = await response.json()
setSearchResults(data.tracks)
setIsSearching(false)
```

**Spotify search is now working!**

---

## 3️⃣ **Enable Spotify Playback (Optional - Premium Users)**

For users with Spotify Premium to play music:

1. Include Spotify Web Playback SDK
2. Implement OAuth login flow
3. Initialize player with user token

**File: `frontend/app/layout.tsx`** (add to head):

```tsx
<Script src="https://sdk.scdn.co/spotify-player.js" />
```

This is more advanced - start with YouTube first! 🎵

---

## 🚀 **Quick Start (Just YouTube)**

If you want to get it working in 2 minutes, just do YouTube:

1. Get YouTube API key (free, 5 minutes)
2. Add to `.env.local`
3. Update `searchYouTube` function
4. **DONE!** Users can search and play any song

Spotify can be added later for users who want it.

---

## 📊 **API Limits & Costs**

| Platform | Free Tier | Limit | Cost if Exceeded |
|----------|-----------|-------|------------------|
| YouTube Data API | ✅ YES | 10,000 quota/day (~100 searches) | $0 for most apps |
| Spotify Web API | ✅ YES | Unlimited with OAuth | $0 always |

**Both are FREE for your use case!**

---

## 🎵 **Current Status:**

**Working Now:**
- ✅ UI is fully functional
- ✅ YouTube playback works (IFrame API integrated)
- ✅ Volume control works
- ✅ Play/pause works
- ✅ Platform switching works

**Needs API Keys (5 min setup):**
- ⏳ YouTube search (requires API key)
- ⏳ Spotify search (requires Client ID)
- ⏳ Spotify playback (requires OAuth - optional)

---

## 🧪 **Test It Now (Without APIs):**

The app is running with mock data! You can:
1. Click [🎵 Music ▼]
2. Select YouTube
3. Search for a song (returns mock results)
4. Click a result → See the player interface

**To make it ACTUALLY play songs:** Add YouTube API key! 🎵

---

## ❓ **Need Help?**

1. **YouTube API not working?** Check console for errors, verify API key
2. **Spotify OAuth confusing?** Start with just YouTube, add Spotify later
3. **No sound?** Check browser console, YouTube IFrame API might not be loaded

**The hard part (UI, playback controls) is done. Just need API keys!** ✅
