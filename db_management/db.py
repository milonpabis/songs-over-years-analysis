import sqlite3
import pandas as pd


class SongInfo:

    def __init__(self, artist: str, song: str):
        self.artist = artist
        self.song = song

    
    def csv(self) -> str:
        return f"{self.song},{self.artist}"

    
    def __eq__(self, other) -> bool:
        if isinstance(other, SongInfo):
            return all([self.artist == other.artist, self.song == other.song])
        return False



class IDSongInfo(SongInfo):

    def __init__(self, artist: str, song:str, release_date: str, id: str, featured: bool, popularity: int):
        super().__init__(artist, song)
        self.release_date = release_date
        self.id = id
        self.featured = featured
        self.popularity = popularity


    def csv(self) -> str:
        return f"{self.song},{self.artist},{self.id},{self.release_date},{self.featured},{self.popularity}"

    
    def __eq__(self, other) -> bool:
        if isinstance(other, IDSongInfo):
            return self.id == other.id
        return False


    def __str__(self) -> str:
        return f"{self.artist}: '{self.song}' | {self.id}"



class SongsContainer:

    def __init__(self):
        self.songs = []


    def add_song(self, song: SongInfo) -> None:
        if song not in self.songs and isinstance(song, SongInfo):
            self.songs.append(song)


    def save_to_csv(self, name: str, mode: str = "a") -> None:
        with open(name, mode, encoding="utf-8") as file:
            file.write(self.get_csv())

    
    def get_csv(self) -> str:
        return "\n".join([song.csv() for song in self.songs])

    
    def from_csv(self, csv_path: str) -> None:
        data = pd.read_csv(csv_path, on_bad_lines='skip', header=None, names=["Song", "Artist"])
        for idx, song in data.iterrows():
            try:
                self.songs.append(SongInfo(song["Artist"], song["Song"]))
            except Exception as exception:
                print(idx)
                raise exception from None
        

    def __len__(self) -> int:
        return len(self.songs)



class SongsDB:


    def __init__(self):
        self.conn = sqlite3.connect("db_management/data/songs.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS songs 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             title TEXT,
                             artist TEXT,
                             UNIQUE(title, artist)""")
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS songs_ids
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             song_spotify_id UNIQUE INTEGER NOT NULL,
                             title TEXT,
                             artist TEXT,
                             release_date TEXT,
                             featured INTEGER,
                             popularity INTEGER)""")
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS songs_features
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             song_spotify_id TEXT,
                             acousticness REAL,
                             danceability REAL,
                             energy REAL,
                             instrumentalness REAL,
                             liveness REAL,
                             loudness REAL,
                             speechiness REAL,
                             tempo REAL,
                             valence REAL,
                             mode INTEGER,
                             key INTEGER,
                             duration_ms INTEGER)""")
        


    def songs_insert(self, song: SongInfo) -> None:
        try:
            self.cursor.execute("""INSERT INTO songs 
                                (title, artist) VALUES (?, ?)""", (song.song, song.artist))
            self.conn.commit()
        except Exception as exception:
            raise DBException(song.song, song.artist, *exception.args)
        

    def songs_ids_insert(self, song: IDSongInfo) -> None:
        try:
            self.cursor.execute("""INSERT INTO songs_ids
                                 (song_spotify_id, title, artist, release_date, featured, popularity)
                                 VALUES (?, ?, ?, ?, ?, ?)""", (song.id, song.song, song.artist, song.release_date, song.featured, song.popularity))
            self.conn.commit()
        except Exception as exception:
            raise DBException(song.id, song.song, song.artist, *exception.args)
        

    def songs_features_insert(self, song_spotify_id: int, acousticness: float,
                               danceability: float, energy: float, instrumentalness: float,
                                 liveness: float, loudness: float, speechiness: float,
                                   tempo: float, valence: float, mode: int, key: int, duration_ms: int) -> None:
        pass







# TODO:
# - create a method to insert scraped songs from csv to the database
# - implement getting the playlists from Spotify API and populating the database with the songs along with ids and other stuff
# - implement a method to get the features of the songs from the Spotify API and populate the database with the features
# ...



class DBException(Exception):

    def __init__(self, *args):
        pass