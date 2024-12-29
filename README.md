# What is this?
This is a script to migrate from spotify to youtube music. 

## Requirements
`pip install spotipy
pip install pip install google-api-python-client
pip install google_auth_oauthlib
`
## Spotify API
Follow the link to generate Spotify API credentials. These credentials need to be put in keys.py
[Spotify_API](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)

## Youtube API
Follow the link to generate Youtube API credentials. From there download the client_secrets.json file and replace the same file.
[Youtube_API](https://developers.google.com/youtube/v3/getting-started)

## Usage
Use the spotify_data.py script to generate the playlist_tracks.json file. This file will be used to add the songs to the playlist using the you_music.py script.
