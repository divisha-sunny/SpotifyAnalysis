import os
from dotenv import load_dotenv
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time
import main
import re

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_genres(access_token, limit=50, offset=0):
    genres_url = 'https://api.spotify.com/v1/browse/categories'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'limit': limit,
        'offset': offset
    }
    response = requests.get(genres_url, headers=headers, params=params)
    genres_data = response.json()
    genres = [(category['id'], category['name']) for category in genres_data['categories']['items']]
    return genres


client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_artist_genre(artist_id):
    artist = sp.artist(artist_id)
    return artist['genres']

def create_dataframe(query_list, limit=50):
    data = {
        'Track_ID': [],
        'Track_name': [],
        'Artist_name': [],
        'Popularity_score': [],
        'Release_year': [],
        'Genre': []
    }

    for query in query_list:
        search_results = sp.search(query, limit=limit, type='track')
        tracks = search_results['tracks']['items']

        for track in tracks:
            data['Track_ID'].append(track['id'])
            data['Track_name'].append(track['name'])
            data['Artist_name'].append(track['artists'][0]['name'])
            data['Popularity_score'].append(track['popularity'])
            data['Release_year'].append(track['album']['release_date'][:4])
            data['Genre'].append(query)

        time.sleep(2)

    df = pd.DataFrame(data)
    return df

token = main.get_access_token(client_id, client_secret)
genres = get_genres(token)

def get_genres_list(token):
    genres = get_genres(token)  # Retrieve genres using the token

    # Format genres with quotes and "genre:" prefix:
    genres_with_quote = ['"genre:{}"'.format(genre) for genre in genres]
    return genres_with_quote

genres_list = get_genres_list(token)

df = create_dataframe(genres_list, limit=50)

#Function to retrive each tracks audio features

def get_audio_features(track_ids):
    features_list = []

    for i in range(0, len(track_ids), 50):
        batch = track_ids[i:i + 50]
        feature_results = sp.audio_features(batch)
        features_list += feature_results
    
    return features_list

track_ids = df['Track_ID'].tolist()
audio_features = get_audio_features(track_ids)

# Assuming audio_features is a list containing dictionaries as elements
filtered_audio_features = [feature for feature in audio_features if feature is not None]

# Create DataFrame
audio_features_df = pd.DataFrame(filtered_audio_features)

merged_df = df.merge(audio_features_df, left_on='Track_ID', right_on='id', how='inner')

merged_df['Genre'] = merged_df['Genre'].apply(lambda x: x[::-1])
merged_df['Genre'] = merged_df['Genre'].apply(lambda x: re.search(r"'([^']+)'", x).group(1) if re.search(r"'([^']+)'", x) else None)
merged_df['Genre'] = merged_df['Genre'].apply(lambda x: x[::-1])

unique_df = merged_df.drop_duplicates(subset='Track_ID', keep='first')
