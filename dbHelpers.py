import sqlite3
from spotify import *

def insertVenue(conn: sqlite3.Connection, playlistId: str, name: str) -> None:
    query = 'insert into Venues (PlaylistID, Name) values (?,?)'
    args = [playlistId, name]
    c = conn.cursor()
    c.execute(query, args)
    conn.commit()

def insertArtist(conn: sqlite3.Connection, artistId: str, Name: str) -> None:
    query = 'insert into Artists (ArtistId, Name) values (?,?)'
    args = [artistId, Name]
    c = conn.cursor()
    c.execute(query, args)
    conn.commit()

def insertShow(conn: sqlite3.Connection, venueId: str, artistId: str, date: str) -> int:
    query = 'insert into Shows (VenueID, ArtistID, Date) values (?,?,?)'
    args = [venueId, artistId, date]
    c = conn.cursor()
    c.execute(query, args)
    conn.commit()
    return c.lastrowid

def insertSong(conn: sqlite3.Connection, songId: str, title: str) -> None:
    query = 'insert into Songs (SongID, Title) values (?,?)'
    args = [songId, title]
    c = conn.cursor()
    c.execute(query, args)
    conn.commit()

def insertShowSong(conn: sqlite3.Connection, showId: int, songId: str):
    query = 'insert into ShowSongs (ShowID, SongID) values (?,?)'
    args = [showId, songId]
    c = conn.cursor()
    c.execute(query, args)
    conn.commit()

def getArtistById(conn: sqlite3.Connection, artistId: str) -> dict:
    query = 'select ArtistID from Artists where ArtistID = ?'
    args = [artistId]
    c = conn.cursor()
    c.execute(query, args)
    return fetchOne(c)

def getSongById(conn: sqlite3.Connection, songId: str) -> dict:
    query = 'select * from Songs where SongID = ?'
    args = [songId]
    c = conn.cursor()
    c.execute(query, args)
    return fetchOne(c)

def getShowsByShowData(conn: sqlite3.Connection, venueId: int, artistId: str):
    query = 'select ShowID from shows where VenueID = ? and ArtistID = ? and DeletedOn is null'
    args = [venueId, artistId]
    c = conn.cursor()
    c.execute(query, args)
    return fetchAll(c)

def getVenueShowsBeforeDate(conn: sqlite3.Connection, playlistId: str, date: str) -> list:
    query = '''
        select ShowID from Shows s
        join Venues v on v.VenueID = s.VenueID
        where v.PlaylistID = ? 
        and s.Date < ?
    '''
    args = [playlistId, date]
    c = conn.cursor()
    c.execute(query, args)
    return fetchAll(c)

def getSongsByShowId(conn: sqlite3.Connection, showId: int) -> list:
    query = 'select id as ShowSongID, SongID from ShowSongs where ShowID = ?'
    args = [showId]
    c = conn.cursor()
    c.execute(query, args)
    return fetchAll(c)

def deleteShow(conn: sqlite3.Connection, showId: int) -> None:
    query = 'update Shows set DeletedOn = current_timestamp where ShowID = ?'
    args = [showId]
    c = conn.cursor()
    c.execute(query, args)
    conn.commit()

def deleteShowSongs(conn: sqlite3.Connection, showId: int) -> None:
    query = 'update ShowSongs set DeletedOn = current_timestamp where ShowID = ?'
    args = [showId]
    c = conn.cursor()
    c.execute(query, args)
    conn.commit()

def fetchAll(c: sqlite3.Cursor) -> list:
    rows = c.fetchall()
    return [dict(row) for row in rows] if rows else []

def fetchOne(c: sqlite3.Cursor) -> dict:
    row = c.fetchone()
    return dict(row) if row else {}
