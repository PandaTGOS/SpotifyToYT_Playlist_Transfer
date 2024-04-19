from ytmusicapi import YTMusic
from dotenv import load_dotenv
from requests import post, get
import json
import os
import base64

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv ("CLIENT_SECRET")


def get_token (): 
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf8")
    auth_base64 = str (base64. b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    
    if "access_token" in json_result: 
        token = json_result["access_token"]
        return token
    else:
        print(json_result)
        return None


def get_auth_header():
    return {"Authorization": "Bearer " + token}


def search_playlist(link): 
    playlist_id = link.split("/")[4].split("?")[0] 
                             
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_auth_header()

    result = get(url, headers = headers)
    json_result = json.loads(result.content)

    name = json_result["name"]
    tracks = json_result.get("tracks", {}).get("items", [])
    
    while json_result.get("tracks", {}).get("next"):
        next_url = json_result["tracks"]["next"]
        result = get(next_url, headers=headers)
        json_result = json.loads(result.content)
        tracks.extend(json_result.get("items", []))

    return name, tracks



def add_to_yt(song):
    query = song + " official audio" 
    search_results = yt.search(query, filter="songs", limit=1)
    if search_results:
        top_result = search_results[0]
        yt.add_playlist_items(playlistId, [top_result['videoId']])
        print("Added: ",song)
    else:
        print("NOT FOUND: ",song)



if __name__ == "__main__":
    token = get_token()
    link = input("Paste spotify link here: ")
    name, playlist = search_playlist(link)
    
    songs_list = [ str(song["track"]["name"] +" by "+ song["track"]["artists"][0]["name"]) for song in playlist]
    print(len(songs_list),"Songs to be transferred")
    
    #yt
    yt = YTMusic('oauth.json')
    playlistId = yt.create_playlist(name, 'playlist '+name+' transferred from Spotify')

    print("PLAYLIST: ",name,"\n")

    i=1
    for song in songs_list:
        try:
            print(i,end='_')
            add_to_yt(song)
            i+=1
        except:
            print("NOT FOUND: ",song)
            i+=1
            continue
    
    print("\nSuccessfully transferred "+name+" !")


#test_link
#https://open.spotify.com/playlist/5H1RoueEQHIrxaTaRJvmSc?si=3kvZFt9vQGWd7vr_NDNoXQ&pi=a-mYEsMLz2Qtme