from spotify import *
from dbHelpers import *
from helpers import *
from util import *
from webDriver import getSpotifyAuthCode
import venues.OrangePeel as OrangePeel
import venues.GreyEagle as GreyEagle
import venues.SalvageStation as SalvageStation
import sqlite3, json

if __name__ == '__main__':
  
    with open('./creds.json', 'r') as f:
        creds = json.load(f)

    keywordExclusions = ['tribute', 'comedy', 'festival', 'burlesque']
    genreExclusions = ['comedy']

    venueData = [
        {
        'data' : OrangePeel.getShowData(),
        'venueId' : '1',
        'playlistId' : '68QdMSGY0wuHpp22BF1Xwy'
        },
        {
        'data' : GreyEagle.getShowData(),
        'venueId' : '2',
        'playlistId' : '28murVhE6udBN9fxyZw9NE'
        }
        ,{
        'data' : SalvageStation.getShowData(),
        'venueId' : '3',
        'playlistId' : '7xXn5Po4zceOqNHGshXHEM'
        }
    ]

    spotifyAuthCode = getSpotifyAuthCode(creds)
    setAccessVars(creds['clientId'], creds['clientSecret'], spotifyAuthCode)
    setAuthCodeToken()

    #For testing. Clears out existing data
    # resetDB()
    # resetPlaylists([venue['playlistId'] for venue in venueData])

    conn = sqlite3.connect('AshevilleMusic')
    conn.row_factory = sqlite3.Row

    for venue in venueData:
        clearOldSongsFromPlaylist(conn, venue['playlistId'])
        for show in venue['data']:
            artistName = show['artist']
            artistId = insertNewArtistIfValid(conn, artistName, genreExclusions, keywordExclusions)
            if artistId == '-1':
                continue
            date = show['date']
            showId = insertNewShowIfValid(conn, venue['venueId'], artistId, date)
            if showId == '-1':
                continue
            topTracks = getArtistsTopTracks(artistId)
            songIds = insertShowSongs(conn, showId, topTracks)
            appendTracksToPlaylist(parseTracks(songIds), venue['playlistId'])