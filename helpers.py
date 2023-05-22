from dbHelpers import *
from datetime import datetime, timedelta
from fuzzywuzzy import fuzz
import re

def parseArtistName(artistName: str) -> str:
    splitStrings = ['-', '–', ':', '+', '(', 'featuring']
    for splitString in splitStrings:
        artistName = artistName.split(splitString)[0].strip()
    return artistName

def artistNameIsMatch(s1: str, s2: str, minConfidence: int) -> bool:
    s1 = re.sub('\bthe\b', '', s1)
    s2 = re.sub('\bthe\b', '', s2)
    return fuzz.ratio(s1.lower(), s2.lower()) > minConfidence

def parseTracks(tracks: list[str]) -> list[str]:
    return ['spotify:track:' + track for track in tracks]

def getCurrentDateString() -> str:
    return datetime.today().strftime('%Y-%m-%d')

def addDaysToDateString(dateString: str, daysToAdd: int) -> str:
    date = datetime.strptime(dateString, '%Y-%m-%d')
    return (date + timedelta(days=daysToAdd)).strftime('%Y-%m-%d')

def dateInRange(checkDate: str, minDate: str, maxDate: str) -> bool:
    cd = datetime.strptime(checkDate, '%Y-%m-%d')
    min = datetime.strptime(minDate, '%Y-%m-%d')
    max = datetime.strptime(maxDate, '%Y-%m-%d')
    return cd >= min and cd <= max

def anySubstringInListOfStrings(subStrings: list[str], strings: list[str]) -> bool:
    for string in strings:
        for subString in subStrings:
            if subString in string:
                return True
    return False

def getArtistDataByArtistName(artistName: str) -> dict:
    artistObject = searchForItem(artistName, 'artist')
    artistId = '-1'
    genres = []

    for artist in artistObject['artists']['items']:
        if artistNameIsMatch(artist['name'], artistName, 98):
            artistId = artist['id']
            genres = artist['genres']
            break

    if artistId == '-1' and '&' in artistName:
        tempArtistData = getArtistDataByArtistName(artistName.split('&')[0].strip())
        artistName = tempArtistData['artistName']
        artistId = tempArtistData['artistId']
        genres = tempArtistData['genres']

    return {
        'artistName': artistName,
        'artistId': artistId,
        'genres': genres,
    }

def insertNewArtistIfValid(conn: sqlite3.Connection, artistName: str, excludedGenres: list[str], excludedKeywords: list[str]) -> str:
    if any(keyword.lower() in artistName.lower() for keyword in excludedKeywords):
        return '-1'
    artistData = getArtistDataByArtistName(parseArtistName(artistName))
    if artistData['artistId'] != '-1' and not anySubstringInListOfStrings(excludedGenres, artistData['genres']):
        if not getArtistById(conn, artistData['artistId']):
            insertArtist(conn, artistData['artistId'], artistData['artistName'])
        spotifyArtistID = artistData['artistId']
    else:
        spotifyArtistID = '-1'
    return spotifyArtistID

def insertNewShowIfValid(conn: sqlite3.Connection, venueId: int, artistId: str, date: str) -> str:
    today = getCurrentDateString()
    dateLimit = addDaysToDateString(today, 60)
    shows = getShowsByShowData(conn, venueId, artistId)
    if shows or not dateInRange(date, today, dateLimit):
        showId = '-1'
    else:
        showId = insertShow(conn, venueId, artistId, date)
    return showId

def insertSongIfNew(conn: sqlite3.Connection, songId: str, title: str) -> str: 
    if not getSongById(conn, songId):
        insertSong(conn, songId, title)
        
def insertShowSongs(conn: sqlite3.Connection, showId: int, tracks: list[dict]) -> list[str]:
    songIds = []
    for i in range(min(3, len(tracks))): 
        songId = tracks[i]['id']
        songIds.append(songId)
        insertSongIfNew(conn, songId, tracks[i]['name'])
        insertShowSong(conn, showId, songId)

    return songIds

def clearOldSongsFromPlaylist(conn: sqlite3.Connection, playlistId: str) -> None:
    date = getCurrentDateString()
    showData = getVenueShowsBeforeDate(conn, playlistId, date)
    for show in showData:
        showId = show['ShowID']
        songData = getSongsByShowId(conn, showId)
        for song in songData:
            showSongId = song['ShowSongID']
            tracks = parseTracks([song['SongID']])
            removeTracksFromPlaylist(tracks, playlistId)
            deleteShowSong(conn, showSongId)
        deleteShow(conn, showId)
