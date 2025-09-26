import os
import re
import sys
import json
import time
from typing import List, Dict, Optional
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
import requests

# Spotify API credentials (SET HERE)
SPOTIFY_CLIENT_ID = "SPOTIFY_CLIENT_ID" #Replace with your client id
SPOTIFY_CLIENT_SECRET = "SPOTIFY_CLIENT_ID" #Replace with your client secret

class SpotifyPlaylistDownloader:
    def __init__(self, client_id: str, client_secret: str):
        """Initialize the downloader with Spotify credentials."""
        if client_id == "your_client_id_here" or client_secret == "your_client_secret_here": # Dont chnage this line
            print("❌ Please set your Spotify API credentials in the script!")
            print("Visit: https://developer.spotify.com/dashboard/")
            sys.exit(1)
        
        # Initialize Spotify client
        try:
            self.spotify = spotipy.Spotify(
                client_credentials_manager=SpotifyClientCredentials(
                    client_id=client_id,
                    client_secret=client_secret
                )
            )
            print("✅ Spotify API connected successfully!")
        except Exception as e:
            print(f"❌ Failed to connect to Spotify API: {e}")
            sys.exit(1)
        
        # Configure yt-dlp for high quality audio
        self.ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'extractaudio': True,
            'audioformat': 'mp3',
            'audioquality': '320k',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'ignoreerrors': True,
            'no_warnings': False,
            'ffmpeg_location': r"C:\ffmpeg\bin",  # ffmpeg location (chnage if defferent)
        }
    
    def extract_playlist_id(self, url: str) -> Optional[str]:
        """Extract playlist ID from Spotify URL."""
        patterns = [
            r'playlist/([a-zA-Z0-9]+)',
            r'playlist:([a-zA-Z0-9]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_playlist_tracks(self, playlist_url: str) -> List[Dict]:
        """Get all tracks from a Spotify playlist."""
        playlist_id = self.extract_playlist_id(playlist_url)
        if not playlist_id:
            raise ValueError("Invalid Spotify playlist URL")
        
        try:
            # Get playlist info
            playlist = self.spotify.playlist(playlist_id)
            print(f"📋 Playlist: {playlist['name']}")
            print(f"👤 Owner: {playlist['owner']['display_name']}")
            print(f"🎵 Total tracks: {playlist['tracks']['total']}")
            
            tracks = []
            results = self.spotify.playlist_tracks(playlist_id)
            
            while results:
                for item in results['items']:
                    if item['track'] and item['track']['type'] == 'track':
                        track = item['track']
                        track_info = {
                            'name': track['name'],
                            'artists': [artist['name'] for artist in track['artists']],
                            'album': track['album']['name'],
                            'duration_ms': track['duration_ms'],
                            'popularity': track['popularity'],
                            'preview_url': track['preview_url']
                        }
                        tracks.append(track_info)
                
                # Get next batch of tracks
                results = self.spotify.next(results) if results['next'] else None
            
            print(f"✅ Found {len(tracks)} valid tracks")
            return tracks
            
        except Exception as e:
            print(f"❌ Error getting playlist tracks: {e}")
            return []
    
    def search_youtube(self, track: Dict) -> Optional[str]:
        """Search for track on YouTube and return the best match URL."""
        # Create search query
        artists = " ".join(track['artists'])
        query = f"{artists} - {track['name']}"
        
        # Clean query for better search results
        query = re.sub(r'[^\w\s-]', '', query)
        
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                search_results = ydl.extract_info(
                    f"ytsearch5:{query}",
                    download=False
                )
                
                if 'entries' in search_results and search_results['entries']:
                    # Return the first result URL
                    return search_results['entries'][0]['webpage_url']
        except Exception as e:
            print(f"⚠️  Search failed for {query}: {e}")
        
        return None
    
    def download_track(self, youtube_url: str, track_info: Dict, output_dir: str) -> bool:
        """Download a single track from YouTube."""
        try:
            # Create custom output template
            artists = " & ".join(track_info['artists'])
            safe_filename = re.sub(r'[^\w\s-]', '', f"{artists} - {track_info['name']}")
            
            custom_opts = self.ydl_opts.copy()
            custom_opts['outtmpl'] = os.path.join(output_dir, f"{safe_filename}.%(ext)s")
            
            with yt_dlp.YoutubeDL(custom_opts) as ydl:
                ydl.download([youtube_url])
            
            return True
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False
    
    def download_playlist(self, playlist_url: str, output_dir: str = "downloads"):
        """Download entire playlist."""
        print("🚀 Starting playlist download...")
        print("=" * 60)
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Get playlist tracks
        tracks = self.get_playlist_tracks(playlist_url)
        if not tracks:
            print("❌ No tracks found!")
            return
        
        print("\n🔍 Starting downloads...")
        print("=" * 60)
        
        successful_downloads = 0
        failed_downloads = 0
        
        for i, track in enumerate(tracks, 1):
            artists_str = " & ".join(track['artists'])
            print(f"\n[{i}/{len(tracks)}] {artists_str} - {track['name']}")
            
            # Search for track on YouTube
            youtube_url = self.search_youtube(track)
            if not youtube_url:
                print("❌ Not found on YouTube")
                failed_downloads += 1
                continue
            
            print(f"🎯 Found: {youtube_url}")
            
            # Download track
            if self.download_track(youtube_url, track, output_dir):
                print("✅ Downloaded successfully!")
                successful_downloads += 1
            else:
                print("❌ Download failed!")
                failed_downloads += 1
            
            # Small delay to be respectful to services
            time.sleep(1)
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 DOWNLOAD SUMMARY")
        print("=" * 60)
        print(f"✅ Successful: {successful_downloads}")
        print(f"❌ Failed: {failed_downloads}")
        print(f"📁 Files saved to: {os.path.abspath(output_dir)}")


def main():
    """Main function to run the downloader."""
    print("🎵 Spotify Playlist Downloader")
    print("=" * 60)
    
    # Get playlist URL from user
    if len(sys.argv) > 1:
        playlist_url = sys.argv[1]
    else:
        playlist_url = input("Enter Spotify playlist URL: ").strip()
    
    if not playlist_url:
        print("❌ No playlist URL provided!")
        return
    
    # Get output directory
    output_dir = input("Enter output directory (press Enter for 'downloads'): ").strip()
    if not output_dir:
        output_dir = "downloads"
    
    # Initialize downloader
    downloader = SpotifyPlaylistDownloader(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )
    
    # Start download
    try:
        downloader.download_playlist(playlist_url, output_dir)
    except KeyboardInterrupt:
        print("\n⏹️  Download interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
