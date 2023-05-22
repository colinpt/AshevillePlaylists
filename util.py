from spotify import *
from dbHelpers import *
from helpers import *
import sqlite3
import os

def resetDB() -> None:
    os.remove('AshevilleMusic')
    conn = sqlite3.connect('AshevilleMusic')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    with open('.\\db.sql', 'r') as f:
        sql = f.read()
    
    c.executescript(sql)
    conn.commit()
    insertVenue(conn, '68QdMSGY0wuHpp22BF1Xwy', 'The Orange Peel')
    insertVenue(conn, '28murVhE6udBN9fxyZw9NE', 'The Grey Eagle')
    insertVenue(conn, '7xXn5Po4zceOqNHGshXHEM', 'Salvage Station')

def resetPlaylists(playlistIds: list[str]) -> None:
    for playlistId in playlistIds:
        offset = 0
        playlist = getPlaylistTracks(playlistId, offset=offset)
        totalTracks = playlist['total']
        tracks = []
        while totalTracks - offset > 100:
            for item in playlist['items']:
                tracks.append(item['track']['id'])
                if len(tracks) == 100: #Spotify can only remove 100 tracks at a time
                    offset += 100
                    playlist = getPlaylistTracks(playlistId, offset=offset)
                    parsedTracks = parseTracks(tracks)
                    removeTracksFromPlaylist([{'uri' : parsedTrack} for parsedTrack in parsedTracks], playlistId)
                    tracks = []

        parsedTracks = parseTracks(tracks)
        removeTracksFromPlaylist([{'uri' : parsedTrack} for parsedTrack in parsedTracks], playlistId)
    return

