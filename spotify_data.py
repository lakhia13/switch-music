import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

# Spotify API credentials (replace with your credentials)
CLIENT_ID = 'foo'
CLIENT_SECRET = 'bar'

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_playlist_tracks(playlist_url):
    """
    Fetch all tracks from a Spotify playlist.

    Args:
        playlist_url (str): The URL of the Spotify playlist.

    Returns:
        list: A list of dictionaries containing track data.
    """
    playlist_id = playlist_url.split("/")[-1].split("?")[0]  # Extract playlist ID
    results = sp.playlist_items(playlist_id)
    tracks = []

    while results:
        for item in results['items']:
            track = item['track']
            if track:  # Ensure the track data exists
                track_data = {
                    "name": track['name'],
                    "artist": ", ".join([artist['name'] for artist in track['artists']]),
                    "album": track['album']['name'],
                    "release_date": track['album']['release_date'],
                    "duration_ms": track['duration_ms'],
                    "spotify_url": track['external_urls']['spotify']
                }
                tracks.append(track_data)
        # Check for next batch of tracks
        results = sp.next(results) if results['next'] else None

    return tracks

def save_tracks_to_json(tracks, filename="playlist_tracks.json"):
    """
    Save track data to a JSON file.

    Args:
        tracks (list): List of track dictionaries.
        filename (str): Name of the JSON file to save.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tracks, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    # Replace with your Spotify playlist URL
    playlist_url = input("Enter the Spotify playlist URL: ").strip()

    try:
        tracks = get_playlist_tracks(playlist_url)
        print(f"Retrieved {len(tracks)} tracks from the playlist.")
        save_tracks_to_json(tracks)
    except Exception as e:
        print(f"Error: {e}")
