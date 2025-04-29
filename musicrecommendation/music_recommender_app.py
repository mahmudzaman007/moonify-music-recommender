
# music_recommender_app.py

import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
spotify_df = pd.read_csv('SpotifyFeatures.csv')

# Preprocessing
small_spotify_df = spotify_df.sort_values('popularity', ascending=False).head(5000)

features = [
    'acousticness', 'danceability', 'energy', 'instrumentalness',
    'liveness', 'loudness', 'speechiness', 'tempo', 'valence'
]

music_features_small_df = small_spotify_df[['track_name', 'artist_name'] + features]

scaler = StandardScaler()
scaled_features_small = scaler.fit_transform(music_features_small_df[features])

scaled_features_df = pd.DataFrame(scaled_features_small, columns=features)
scaled_features_df['track_name'] = music_features_small_df['track_name'].values
scaled_features_df['artist_name'] = music_features_small_df['artist_name'].values

def recommend_dynamic(track_name, n_recommendations=5):
    if track_name not in scaled_features_df['track_name'].values:
        return f"Track '{track_name}' not found."
    
    track_vector = scaled_features_df[scaled_features_df['track_name'] == track_name][features].values
    all_vectors = scaled_features_df[features].values
    similarity_scores = cosine_similarity(track_vector, all_vectors).flatten()
    top_indices = similarity_scores.argsort()[-n_recommendations-1:-1][::-1]
    recommended_tracks = scaled_features_df.iloc[top_indices][['track_name', 'artist_name']]
    
    return recommended_tracks.reset_index(drop=True)

# Streamlit UI
st.title("🎵 Spotify Music Recommendation System")

partial_name = st.text_input("Enter part of a song name:")

if partial_name:
    matches = scaled_features_df[scaled_features_df['track_name'].str.contains(partial_name, case=False, na=False)]
    
    if not matches.empty:
        selected_track = st.selectbox("Select a track:", matches['track_name'] + " - " + matches['artist_name'])
        
        if selected_track:
            selected_track_name = selected_track.split(" - ")[0]
            recommendations = recommend_dynamic(selected_track_name)
            
            st.subheader(f"Top Recommendations based on '{selected_track_name}':")
            st.dataframe(recommendations)
    else:
        st.warning("No matching songs found. Try another keyword.")
