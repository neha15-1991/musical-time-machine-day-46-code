from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
spotify_client_id="64426bef27df4fdc88b23c4e7d102cf8"
spotify_client_secret="35ab712c36fa41119caecf99e4bb6886"
date=input("which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
year=date.split("-")[0]
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"
}

response=requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}/", headers=header)
music_data=response.text
soup=BeautifulSoup(music_data, "html.parser")
songs_in_span=soup.select("li ul li h3")
print(songs_in_span)
songs_list=[song.get_text().strip() for song in songs_in_span]
print(songs_list)




spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com",
        client_id=spotify_client_id,
        client_secret=spotify_client_secret,
        show_dialog=True,
        cache_path="token.txt",
        username="nsinghal1000"
))
results = spotify.current_user()
print(results)
print(results["id"])
#uris = [spotify.search(song, type="track")['tracks']['items'][0]['uri'] for song in songs_list]
#or we can use for loop with try except block
song_uris=[]
for song in songs_list:
    result = spotify.search(q=f"track:{song} year:{year}", type="track")

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
playlist=spotify.user_playlist_create(user=f"{results["id"]}", name=f"{date} Billboard 100", public=False)
print(playlist["id"])
spotify.playlist_add_items(playlist_id=playlist["id"], items=song_uris)