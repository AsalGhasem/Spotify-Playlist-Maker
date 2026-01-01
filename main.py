import requests
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tkinter import messagebox, Tk, Button, Entry
import pygame

# 1. create an app in spotify using this : https://developer.spotify.com/dashboard/
# 2. tick all those boxes (web api etc(just in case..))
# 3. as the redirect url, use: https://example.com
# 4. enter your client id, client secret in the json file + enter your spotify's account name in line 89 (sry i was too goshad to create another box for that:()
# 5. after running the program, a page will open askin permission from u, after agreein to that,
# copy the url in the example domain site & paste it in the terminal
# 6. a token.txt file must be created afterwards & bammm the playlist will be made :D

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

RED = "#ce1247"
GREEN = "#6bed71"
YELLOW = "#f7f5dd"

def play_audio_click():
    pygame.mixer.music.load("mixkit-gear-fast-lock-tap-2857.wav")  
    pygame.mixer.music.play()

date = None
to_continue = False
def ok_clicked():
    global date
    global to_continue
    to_continue = True
    date = entry.get()
    root.destroy()

def cancel_clicked():
    root.destroy()

root = Tk()
root.title("Spotify Playlist Creator")
entry = Entry(width= 75, bg= YELLOW)
entry.insert(string="Enter the time you would like to travel to in YYYY-MM-DD format.", index= 0)
entry.focus()
entry.grid(column=0, row=0, columnspan=2)

button1 = Button(text="Ok", command= lambda : {ok_clicked(), play_audio_click()}, width=31, fg= "black", bg= GREEN)
button1.grid(column=0, row=1, columnspan=1)
button2 = Button(text="Ok", command= lambda : {cancel_clicked(), play_audio_click()}, width=31, fg= "black", bg= RED)
button2.grid(column=1, row=1)

root.bind('<Return>', lambda event=None: button1.invoke())
root.mainloop()

while to_continue == True:
        URL = f"https://www.billboard.com/charts/hot-100/{date}"
        response = requests.get(url= URL)
        website = response.text

        soup = BeautifulSoup(website, "html.parser")
        all_music = soup.select(selector= "li ul li h3")
        all_artists = soup.select(selector= "div ul li ul li span")
        all_titles = [music.getText().strip() for music in all_music]
        all_artist_names = [artist.getText().strip() for artist in all_artists]

        def is_number(s):
            try:
                int(s)
                return False
            except ValueError:
                return True

        new_artist_names = []
        for name in all_artist_names:
            if is_number(s=name):
                new_artist_names.append(name)

        filtered_names = [s for s in new_artist_names if s!="-"]

        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope="playlist-modify-private",
                redirect_uri="https://example.com",
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                show_dialog=True,
                cache_path="token.txt",
                username="YOUR SPOTIFY ACCOUNT NAME", 
            ),
            requests_timeout= 15
        )

        user_id = sp.current_user()["id"]
        song_uris = []
        for title in all_titles:
            current_index = all_titles.index(title)
            song = sp.search(q= f"track : {title} year: {date.split("-")[0]} artist: {filtered_names[current_index]}", type= "track")
            try:
                song_uri = song["tracks"]["items"][0]["uri"]
                song_uris.append(song_uri)
            except IndexError:
                print(f"{title} does not exist in spotify!")

        playlist = sp.user_playlist_create(name= f"*{date} Billboard top 100*", user= user_id, public= False)
        sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

        messagebox.showinfo("Spotify Playlist Creator",f"I think your playlist named: *{date} Billboard top 100* is ready! Check it out :D")
        to_continue = False