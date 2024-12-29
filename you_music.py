import json
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# Constants
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def authenticate_youtube():
    """
    Authenticate the user with YouTube using OAuth 2.0.
    Returns an authenticated YouTube API client.
    """
    # Load client secrets
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", SCOPES
    )
    credentials = flow.run_console()
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def search_youtube(youtube, query):
    """
    Search for a song on YouTube.
    Args:
        youtube: Authenticated YouTube API client.
        query: Search query string.
    Returns:
        The video ID of the first search result or None.
    """
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=query,
        type="video"
    )
    response = request.execute()
    items = response.get("items", [])
    if items:
        return items[0]["id"]["videoId"]
    return None

def add_to_playlist(youtube, playlist_id, video_id):
    """
    Add a video to a YouTube playlist.
    Args:
        youtube: Authenticated YouTube API client.
        playlist_id: ID of the playlist.
        video_id: ID of the video to add.
    """
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    request.execute()

def main():
    # Authenticate with YouTube
    youtube = authenticate_youtube()

    # Replace with your YouTube playlist ID
    playlist_id = "YOUR_PLAYLIST_ID"

    # Load songs from JSON file
    with open("songs.json", "r", encoding="utf-8") as f:
        songs = json.load(f)

    for song in songs:
        try:
            # Create search query
            query = f"{song['name']} {song['artist']} {song['album']}"
            print(f"Searching for: {query}")

            # Search for the song on YouTube
            video_id = search_youtube(youtube, query)
            if not video_id:
                print(f"Song not found: {query}")
                continue

            # Add the song to the playlist
            add_to_playlist(youtube, playlist_id, video_id)
            print(f"Added to playlist: {song['name']}")
        except Exception as e:
            print(f"Error adding song: {song['name']}. Error: {e}")

if __name__ == "__main__":
    main()
