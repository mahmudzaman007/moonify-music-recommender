
import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

# Load datasets
spotify_df = pd.read_csv('SpotifyFeatures.csv')
album_art_df = pd.read_csv('album_art_urls.csv')

# Merge album art into main dataset
spotify_df = pd.merge(spotify_df, album_art_df, on='track_id', how='left')

# Filter top 5000 popular songs
small_spotify_df = spotify_df.sort_values('popularity', ascending=False).head(5000)

# Select features
features = [
    'acousticness', 'danceability', 'energy', 'instrumentalness',
    'liveness', 'loudness', 'speechiness', 'tempo', 'valence'
]

music_features_small_df = small_spotify_df[['track_name', 'artist_name', 'track_id'] + features + ['album_art_url']]

# Standardize features
scaler = StandardScaler()
scaled_features_small = scaler.fit_transform(music_features_small_df[features])

scaled_features_df = pd.DataFrame(scaled_features_small, columns=features)
scaled_features_df['track_name'] = music_features_small_df['track_name'].values
scaled_features_df['artist_name'] = music_features_small_df['artist_name'].values
scaled_features_df['track_id'] = music_features_small_df['track_id'].values
scaled_features_df['album_art_url'] = music_features_small_df['album_art_url'].values

def recommend_dynamic(track_name, n_recommendations=5):
    if track_name not in scaled_features_df['track_name'].values:
        return pd.DataFrame(columns=['track_name', 'artist_name', 'album_art_url'])

    track_index = scaled_features_df[scaled_features_df['track_name'] == track_name].index[0]
    track_vector = scaled_features_df.loc[track_index, features].values.reshape(1, -1)

    all_vectors = scaled_features_df[features].values
    similarity_scores = cosine_similarity(track_vector, all_vectors).flatten()

    # Get top matches (excluding the same song)
    sorted_indices = similarity_scores.argsort()[::-1]
    sorted_indices = [i for i in sorted_indices if i != track_index]

    top_indices = sorted_indices[:n_recommendations]

    return scaled_features_df.iloc[top_indices][['track_name', 'artist_name', 'album_art_url']].reset_index(drop=True)

# Streamlit UI
st.title("🌙 Moonify - Music Recommender with Album Covers")

partial_name = st.text_input("Enter part of a song name:")

if partial_name:
    matches = scaled_features_df[scaled_features_df['track_name'].str.contains(partial_name, case=False, na=False)]

    if not matches.empty:
        selected_track = st.selectbox("Select a track:", matches['track_name'] + " - " + matches['artist_name'])

        if selected_track:
            selected_track_name = selected_track.split(" - ")[0]
            recommendations = recommend_dynamic(selected_track_name)

            st.subheader(f"Top Recommendations based on '{selected_track_name}':")

            if recommendations.empty:
                st.warning("No similar tracks found.")
            else:
                for _, row in recommendations.iterrows():
                    st.markdown(f"**{row['track_name']} — {row['artist_name']}**")
                    if pd.notna(row['album_art_url']):
                        st.image(row['album_art_url'], width=300)
                    st.markdown("---")
    else:
        st.warning("No matching songs found. Try another keyword.")
