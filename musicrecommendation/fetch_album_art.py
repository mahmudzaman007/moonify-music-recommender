
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Step 1: Spotify API credentials
client_id = "e704999fc26c467d8b3e3c1a2c57f1d2"
client_secret = "7fc170b6074c4590bb10a247e8d1109d"

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Step 2: Load your dataset
df = pd.read_csv("SpotifyFeatures.csv")  # Make sure it's in the same folder

# Step 3: Fetch album art for each unique track_id (limit for testing)
track_ids = df['track_id'].dropna().unique()
album_data = []

print("Fetching album art URLs from Spotify...")
for tid in track_ids[:2000]:  # you can increase limit gradually
    try:
        track_info = sp.track(tid)
        album_img = track_info['album']['images'][0]['url']
        album_data.append((tid, album_img))
    except Exception as e:
        album_data.append((tid, None))

# Step 4: Save to CSV
album_df = pd.DataFrame(album_data, columns=['track_id', 'album_art_url'])
album_df.to_csv("album_art_urls.csv", index=False)

print("✅ Done! Saved album_art_urls.csv.")
