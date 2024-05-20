from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
#imports


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
#client id and client secret initialised from .env file



def get_token():
# this function returns an access token

    authenticator  = client_id + ":" + client_secret
    authenticator_byt = authenticator.encode("utf_8")

    authenticator_b64 = str(base64.b64encode(authenticator_byt), "utf-8")
     

    url = "https://accounts.spotify.com/api/token"
    #url request is sent to

    headers = {
        "Authorization": "Basic " + authenticator_b64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    #header created

    
    data = {"grant_type": "client_credentials"}
    #in data grant type is set to client credentails

    final = post(url, headers=headers, data=data)
    #final is set to the result of a post request with url, headers and data passed in 

    json_result = json.loads(final.content)
    token = json_result["access_token"]
    return token
    #access token is returned 

def get_auth_header(token):
    #returns authentication header

    return{"Authorization": "Bearer " + token}



def search_for_artist(token, artist_name):
    #token and the artists name is passed into the search for artist function


    url = "https://api.spotify.com/v1/search"
    
    headers = get_auth_header(token)
    #headers = get auth header with token passed in

    query = f"?q={artist_name}&type=artist&limit=1"
    #query that looks for the top 1 artist that comes up when artist_name is looked up


    query_url = url + query
    final = get(query_url, headers = headers)
    json_result = json.loads(final.content)["artists"]["items"]
    #filter json so that only artists and items are stored in json_result

    if len (json_result) == 0:
        return None
        #if there where no search results for the artists name return nothing
    

    return json_result[0]
    #if there are results for the artists name return the first element of json result




def get_songs_by_artist_location(token, artist_id, location):
#token, artist_id and location are passed into get songs_by_artist_location

    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country={location}"
    #url is set to url with artists name and location concatonated in

    headers = get_auth_header(token)
    final = get(url, headers=headers)
    json_result = json.loads(final.content)["tracks"]
    #everything but the songs is filtered out

    return json_result
    #list of top 10 song results are output



token = get_token()
#get_token is called and output is set to token variable



def song_list(location, name):
    # song list takes in location and name
    final = search_for_artist(token, name)
    artist_id = final["id"]
    
    songs = get_songs_by_artist_location(token, artist_id, location)
    #songs is set equal to the output of get songs by artist location with token artist_id and location passed in

    
    song_list = []
    # Initialize an empty list to store the song information

    
    for song in songs:
        #Extract the song name and ID from each song information in songs
        song_name = song['name']
        song_id = song['id']

        
        song_link = f"https://open.spotify.com/track/{song_id}"
        # song link is set equal to link to song

        
        artist_name = final["name"]
        # artist_name is set equal to the artists name from search results

    
        country_code = location.upper()
        #country_code is set to an upper case version of location

        
        song_list.append({"name": song_name, "link": song_link, "artist_name": artist_name, "country_code": country_code})
        # all of the song information is stored to song list 

    
    return song_list
    # song list is returned

def printertron(input):
    print(input)