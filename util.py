from spotify import *
from dbHelpers import *
from helpers import *
from logger import log
import sqlite3
import os

def resetDB() -> None:
    os.remove('AshevilleMusic')
    log.info('DATABASE DELETED')
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
        log.info(f'Playlist "{playlistId}" has {totalTracks} tracks')
        while totalTracks > 0:
            tracks = [item['track']['id'] for item in playlist['items']]
            parseTracksAndRemove(tracks, playlistId)
            totalTracks -= len(tracks)
            if totalTracks > 0:
                offset += 100
                playlist = getPlaylistTracks(playlistId, offset=offset)

def parseTracksAndRemove(tracks: list[str], playlistId: str) -> None:
    parsedTracks = parseTracks(tracks)
    log.info(f'removing {len(tracks)} tracks from playlist "{playlistId}"')
    removeTracksFromPlaylist([{'uri' : parsedTrack} for parsedTrack in parsedTracks], playlistId)