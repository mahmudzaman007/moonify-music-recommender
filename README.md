
# 🌙 Moonify — Smart Music Recommendation App

Moonify is a smart, Spotify-powered music recommendation app built with Streamlit.  
It helps users discover songs similar to their favorites using real audio features like energy, mood, and danceability — with beautiful album art included.

---

## 🎧 Features

- 🔍 Search for any song by name (partial matches supported)
- 🎵 Recommend 5 similar songs using audio-based similarity
- 🖼️ Show real-time album art from Spotify
- ⚡ Fast, clean Streamlit web interface
- 🎛️ Uses acoustic features like danceability, energy, valence, and tempo

---

## 🚀 How to Run

1. **Clone this repo** and navigate to the folder:

```bash
git clone https://github.com/yourusername/moonify.git
cd moonify
```

2. **Install dependencies**:

```bash
pip install streamlit pandas scikit-learn spotipy
```

3. **Make sure these files are present**:
- `moonify_app.py` — the main app
- `SpotifyFeatures.csv` — the dataset
- `album_art_urls.csv` — generated album art links using Spotify API

4. **Run the app**:

```bash
streamlit run moonify_app.py
```

5. **Go to**: [http://localhost:8501](http://localhost:8501)  
Use the app to explore and discover music!

---

## 🔑 Spotify API Usage

To fetch album covers:
- Create a Spotify Developer App
- Get your **Client ID** and **Client Secret**
- Run `fetch_album_art.py` to generate `album_art_urls.csv`

---

## 🧠 How It Works

Moonify compares tracks using Spotify's acoustic features like:

- `danceability`
- `energy`
- `acousticness`
- `valence`
- `tempo`
- `loudness`

Then recommends the most sonically similar tracks based on **cosine similarity** between features.

---

## 📸 Screenshot

![App Screenshot](assets/moonify-preview.png)

---

## 🛠 Built With

- Python
- Streamlit
- Pandas
- Scikit-learn
- Spotipy (Spotify API)

---

## 📄 License

MIT License © 2025 [moon]

# moonify-music-recommender
