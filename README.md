# Spotify Playlist Downloader

## Overview

This Python script allows you to download audio tracks from a Spotify playlist by extracting track information via the Spotify API and sourcing the audio from YouTube using `yt-dlp`. The downloaded audio is converted to high-quality MP3 format (320kbps) using FFmpeg.

**Note:** This tool is for personal use only. Ensure you comply with Spotify's and YouTube's terms of service, as well as copyright laws in your region. Downloading copyrighted content without permission may be illegal.

## Features

- Fetches playlist details and track metadata from Spotify.
- Searches for matching tracks on YouTube.
- Downloads audio in MP3 format with metadata.
- Handles pagination for large playlists.
- Provides a progress summary and error handling.

## Requirements

- Python 3.6 or higher.
- FFmpeg (for audio conversion).
- Required Python libraries: `spotipy`, `yt-dlp`, `requests`.

## Installation

Follow these steps to set up the environment and run the script.

### 1. Install Python

If you don't have Python installed:

- Download and install Python from [python.org](https://www.python.org/downloads/).
- Ensure Python is added to your system's PATH during installation.

### 2. Install Required Python Libraries

Open a command prompt and run the following command to install the necessary libraries:

```
pip install spotipy yt-dlp requests
```

This will install:

- `spotipy`: For interacting with the Spotify API.
- `yt-dlp`: For downloading from YouTube (a fork of `youtube-dl` with better performance).
- `requests`: For handling HTTP requests (already included in many Python environments, but installed for safety).

### 3. Install FFmpeg

FFmpeg is required for extracting and converting audio to MP3 format. Installation varies by operating system.

#### Windows

1. Download the latest FFmpeg build from [ffmpeg.org/download.html](https://ffmpeg.org/download.html) (choose a "Windows builds from gyan.dev" or similar trusted source).
2. Extract the ZIP file to a folder, e.g., `C:\ffmpeg`.
3. Add FFmpeg to your system's PATH:
   - Search for "Environment Variables" in the Start menu.
   - Under "System Variables," find "Path" and click "Edit."
   - Add the path to the `bin` folder, e.g., `C:\ffmpeg\bin`.
   - Click OK to save changes.
4. Verify installation: Open a new command prompt and run `ffmpeg -version`. You should see version information.

#### macOS

1. Install Homebrew if not already installed: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`.
2. Run `brew install ffmpeg`.
3. Verify: Run `ffmpeg -version`.

#### Linux (Ubuntu/Debian)

1. Run `sudo apt update && sudo apt install ffmpeg`.
2. Verify: Run `ffmpeg -version`.

**Script Configuration for FFmpeg:** In the script (`playlist.py`), update the `'ffmpeg_location'` in `ydl_opts` to match your FFmpeg installation path if it's not the default. For example:

- Windows: `r"C:\ffmpeg\bin"`
- macOS/Linux: Usually not needed if FFmpeg is in PATH, but you can set it to `/usr/local/bin` or similar if required.

### 4. Set Up Spotify API Credentials

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
2. Log in with your Spotify account (create one if needed).
3. Click "Create an App," provide a name and description, and agree to the terms.
4. Copy your **Client ID** and **Client Secret** from the app's settings.
5. Open `playlist.py` in a text editor and replace the placeholders:

   ```
   SPOTIFY_CLIENT_ID = "your_client_id_here"
   SPOTIFY_CLIENT_SECRET = "your_client_secret_here"
   ```

   with your actual credentials.

**Important:** Never share your Client Secret publicly. If uploading to GitHub, use environment variables or a `.env` file instead (not implemented in this basic script).

## Usage

### Running the Script

1. Save the script as `playlist.py` in a directory of your choice.
2. Open a terminal or command prompt and navigate to the script's directory:

   ```
   cd path/to/your/script/directory
   ```

3. Run the script:

   ```
   python playlist.py
   ```

   - If providing the playlist URL as an argument:

     ```
     python playlist.py https://open.spotify.com/playlist/your_playlist_id
     ```

### Step-by-Step Execution Flow

When you run the script:

1. It will prompt for the Spotify playlist URL (e.g., `https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M` or `spotify:playlist:37i9dQZF1DXcBWIGoYBM5M`). Skip this if provided as a command-line argument.
2. It will prompt for the output directory (press Enter to use the default `downloads` folder).
3. The script connects to the Spotify API using your credentials.
4. It fetches the playlist tracks, displaying the playlist name, owner, and total tracks.
5. For each track:
   - Searches YouTube for the best match.
   - Downloads the audio if found, saving as `Artist - Track Name.mp3` in the output directory.
   - Skips failed downloads and continues.
6. Displays a summary of successful and failed downloads at the end.

**Example Output Directory Structure:**

```
downloads/
├── Track1.mp3 - Artist1
├── Track2.mp3 - Artist2 
└── ...
```

### Tips and Troubleshooting

- **Rate Limits:** Spotify and YouTube have rate limits. For large playlists (>100 tracks), add longer delays in the script (e.g., `time.sleep(5)`).
- **Errors:**
  - "Invalid Client": Check your Spotify credentials.
  - "FFmpeg not found": Ensure FFmpeg is installed and the path is set correctly.
  - "No tracks found": Verify the playlist URL is public and valid.
  - If downloads fail often, check your internet connection or try a VPN.
- **Customization:** You can modify `ydl_opts` in the script for different audio formats or quality.
- **Legal Note:** This tool does not bypass DRM or download directly from Spotify. It uses YouTube as an alternative source, but respect content creators.

## Contributing

Feel free to fork this repository and submit pull requests for improvements, such as adding support for environment variables or better error handling.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details (create one if needed).
