CREATE TABLE Artists ( 
	ArtistID             TEXT NOT NULL  PRIMARY KEY,
	Name                 VARCHAR(100),
	AddedOn              DATETIME  DEFAULT CURRENT_TIMESTAMP
 );

CREATE TABLE Songs ( 
	SongID               TEXT NOT NULL  PRIMARY KEY,
	Title                VARCHAR(64),
	AddedOn              DATETIME  DEFAULT CURRENT_TIMESTAMP   
 );

CREATE TABLE Venues ( 
	VenueID              INTEGER NOT NULL  PRIMARY KEY,
    PlaylistID           VARCHAR(32),
	Name                 VARCHAR(100)     
 );

CREATE TABLE Shows ( 
	ShowID               INTEGER NOT NULL  PRIMARY KEY,
	VenueID              TEXT NOT NULL,
    ArtistID             TEXT NOT NULL,
	Date                 DATE NOT NULL,
	AddedOn              DATETIME  DEFAULT CURRENT_TIMESTAMP,
	DeletedOn            DATETIME,
	FOREIGN KEY ( VenueID ) REFERENCES Venue( VenueID ),
	FOREIGN KEY ( ArtistID ) REFERENCES Artists( ArtistID )  
 );

CREATE TABLE ShowSongs ( 
	id                   INTEGER NOT NULL  PRIMARY KEY,
	ShowID               INTEGER NOT NULL,
	SongID               TEXT NOT NULL,
	AddedOn              DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	DeletedOn            DATETIME,
	FOREIGN KEY ( ShowID ) REFERENCES Shows( ShowID ),
	FOREIGN KEY ( SongID ) REFERENCES Songs( SongID )  
 );
