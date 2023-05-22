import requests, base64, json
from typing import Any

def makeRequest(method: str, url: str, headers=None, data=None, json=None, params=None) -> dict:
    try:
        response = requests.request(method, url, headers=headers, data=data, json=json, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        raise e
    except requests.exceptions.ConnectionError as e:
        raise e
    except requests.exceptions.Timeout as e:
        raise e
    except requests.exceptions.RequestException as e:
        raise e

def header(t:str) -> str:
    return { 'Authorization' : 'Bearer ' + t}

def encodeStringAsBase64(string: str) -> str:
    return base64.urlsafe_b64encode(string.encode('ascii')).decode('ascii')

def setAccessVars(id: str, secret: str, authCode: str) -> None:
    global token, clientId, clientSecret, code
    clientId, clientSecret, code = id, secret, authCode

    data = {
        'client_id' : clientId,
        'client_secret' : clientSecret,
        'grant_type' : 'client_credentials'
    }
    token = makeRequest('POST', 'https://accounts.spotify.com/api/token', data=data)['access_token']

def setAuthCodeToken() -> None:   
    global userToken
    headers = {
        'Authorization' : 'Basic ' + encodeStringAsBase64(clientId + ':' + clientSecret),
        'Content-Type' : 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type' : 'authorization_code',
        'code' : code,
        'redirect_uri' : 'http://localhost:3000'
    }
    userToken = makeRequest('POST', 'https://accounts.spotify.com/api/token', data=data, headers=headers)['access_token']

def getArtistsTopTracks(artistId: str) -> list[dict[str, Any]]:
    params = {'market' : 'US'}
    return makeRequest('GET', f'https://api.spotify.com/v1/artists/{artistId}/top-tracks', headers=header(token), params=params)['tracks']

def searchForItem(q: str, type: str) -> dict[str, Any]:
    params = {
        'q' : q,
        'type' : type,
        'market' : 'US',
    }
    return makeRequest('GET', 'https://api.spotify.com/v1/search', headers=header(token), params=params)

def getPlaylistById(playlistId: str) -> dict[str, Any]:
    return makeRequest('GET', f'https://api.spotify.com/v1/playlists/{playlistId}', headers=header(token))

def getPlaylistTracks(playlistId: str, offset: int = 0) -> dict[str, Any]:
    return makeRequest('GET', f'https://api.spotify.com/v1/playlists/{playlistId}/tracks?offset={offset}&limit=100', headers=header(token))

def appendTracksToPlaylist(tracks: list[str], playlistId: str) -> dict[str, Any]:
    data = {
        'uris' : tracks
    }
    return makeRequest('POST', f'https://api.spotify.com/v1/playlists/{playlistId}/tracks', headers=header(userToken), data=json.dumps(data))

def removeTracksFromPlaylist(tracks: list[dict], playlistId: str) -> dict[str, Any]:
    data = {
        'tracks' : tracks,
        'snapshot_id' : getPlaylistById(playlistId)['snapshot_id'] 
    }
    return makeRequest('DELETE', f'https://api.spotify.com/v1/playlists/{playlistId}/tracks', headers=header(userToken), data=json.dumps(data))