import sqlite3
import pandas as pd


class SongInfo:
    """
    Scraped song data structure.
    """

    def __init__(self, artist: str, song: str):
        self.artist = artist
        self.song = song

    
    def csv(self) -> str:
        return f"{self.song},{self.artist}"

    
    def __eq__(self, other) -> bool:
        if isinstance(other, SongInfo):
            return all([self.artist == other.artist, self.song == other.song])
        return False



class IDSongInfo:
    """
    Main song data structure for the database.
    """

    def __init__(self, song_id: str, album_id: str, artist_id: str, title: str,
                 release_date: str, featured: int, popularity: int):
        if not all([isinstance(song_id, str), isinstance(album_id, str), isinstance(artist_id, str)]):
            raise ValueError("song_id, album_id and artist_id must be strings.")
        self.song_id = song_id
        self.album_id = album_id
        self.artist_id = artist_id
        self.title = title
        self.release_date = release_date
        self.featured = featured
        self.popularity = popularity


    def csv(self) -> str:
        return f"{self.song_id},{self.album_id},{self.artist_id},{self.title},{self.release_date},{self.featured},{self.popularity}"

    
    def __eq__(self, other) -> bool:
        if isinstance(other, IDSongInfo):
            return self.song_id == other.song_id
        return False


    def __str__(self) -> str:
        return f"{self.album_id}: '{self.song_id}' by {self.artist_id} - {self.title}"



class SongsContainer:
    """
    Container for the scraped songs.
    """

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
    


class SongFeatures:
    """
    Song Features data structure for the database.
    """


    def __init__(self, song_id: str, acousticness: float, danceability: float, energy: float,
                 instrumentalness: float, liveness: float, loudness: float, speechiness: float,
                 tempo: float, valence: float, mode: int, key: int, duration_ms: int):
        if not isinstance(song_id, str):
            raise ValueError("song_id must be a string.")
        self.song_id = song_id
        self.acousticness = acousticness
        self.danceability = danceability
        self.energy = energy
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.loudness = loudness
        self.speechiness = speechiness
        self.tempo = tempo
        self.valence = valence
        self.mode = mode
        self.key = key
        self.duration_ms = duration_ms


    def csv(self) -> str:
        return ",".join([str(attr) for attr in [self.song_id, self.acousticness, self.danceability, self.energy, self.instrumentalness,
                                               self.liveness, self.loudness, self.speechiness, self.tempo, self.valence, self.mode, self.key, self.duration_ms]])


    def __eq__(self, other) -> bool:
        if isinstance(other, SongFeatures):
            return self.song_id == other.song_id
        return False
    


class ArtistInfo:
    """
    Artist data structure for the database.
    """


    def __init__(self, artist_id: str, name: str, genres: str):
        if not isinstance(artist_id, str):
            raise ValueError("artist_id must be a string.")
        self.artist_id = artist_id
        self.name = name
        self.genres = genres

    
    def csv(self) -> str:
        return f"{self.artist_id},{self.name},{self.genres}"
    

    def __eq__(self, other) -> bool:
        if isinstance(other, ArtistInfo):
            return self.artist_id == other.artist_id
        return False
    


class AlbumInfo:
    """
    Album data structure for the database.
    """


    def __init__(self, album_id: str, name: str, release_date: str, total_tracks: int, genres: str, popularity: int):
        if not isinstance(album_id, str):
            raise ValueError("album_id must be a string.")
        self.album_id = album_id
        self.name = name
        self.release_date = release_date
        self.total_tracks = total_tracks
        self.genres = genres
        self.popularity = popularity


    def csv(self) -> str:
        return f"{self.album_id},{self.name},{self.release_date},{self.total_tracks},{self.genres},{self.popularity}"
    

    def __eq__(self, other) -> bool:
        if isinstance(other, AlbumInfo):
            return self.album_id == other.album_id
        return False
    


class LyricsInfo:
    """
    Lyrics data structure for the database.
    """


    def __init__(self, song_id: str, lyrics: str):
        if not all([isinstance(song_id, str), isinstance(lyrics, str)]):
            raise ValueError("song_id and lyrics must be strings.")
        self.song_id = song_id
        self.lyrics = lyrics
            

    
    def csv(self) -> str:
        return f"{self.song_id},{self.lyrics}"
    

    def __eq__(self, other) -> bool:
        if isinstance(other, LyricsInfo):
            return self.song_id == other.song_id
        return False




class SongsDB:


    def __init__(self):
        self.conn = sqlite3.connect("db_management/data/songs.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS scraped_songs (
                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                             title TEXT,
                             artist TEXT,
                             UNIQUE(title, artist));
                            """)
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS songs (
                             song_spotify_id TEXT PRIMARY KEY,
                             album_spotify_id TEXT NOT NULL,
                             artist_spotify_id TEXT NOT NULL,
                             title TEXT,
                             release_date TEXT,
                             featured INTEGER,
                             popularity INTEGER,
                             FOREIGN KEY(song_spotify_id) REFERENCES songs_features(song_spotify_id),
                             FOREIGN KEY(album_spotify_id) REFERENCES albums(album_spotify_id),
                             FOREIGN KEY(artist_spotify_id) REFERENCES artists(artist_spotify_id));
                            """)
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS songs_features (
                             song_spotify_id TEXT PRIMARY KEY,
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
                             duration_ms INTEGER);
                            """)
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS artists (
                             artist_spotify_id TEXT PRIMARY KEY,
                             name TEXT,
                             genres TEXT);
                            """)
        

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS albums (
                             album_spotify_id TEXT PRIMARY KEY,
                             name TEXT,
                             release_date TEXT,
                             total_tracks INTEGER,
                             genres TEXT,
                             popularity INTEGER);
                            """)
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS lyrics (
                             song_spotify_id TEXT PRIMARY KEY,
                             lyrics TEXT,
                             FOREIGN KEY(song_spotify_id) REFERENCES songs_features(song_spotify_id));
                            """)
        
        self.conn.commit()
        

    # ================== INSERT METHODS ==================

    def scraped_songs_insert(self, song: SongInfo) -> None:
        try:
            self.cursor.execute("""INSERT INTO scraped_songs 
                                (title, artist) VALUES (?, ?)""", (song.song, song.artist))
            self.conn.commit()
        except Exception as exception:
            raise DBException(song.song, song.artist, *exception.args)
        

    def songs_insert(self, song: IDSongInfo) -> None:
        try:
            self.cursor.execute("""INSERT INTO songs
                                 (song_spotify_id, album_spotify_id, artist_spotify_id, title, release_date, featured, popularity)
                                 VALUES (?, ?, ?, ?, ?, ?, ?)""", (song.song_id, song.album_id, song.artist_id,
                                                                 song.title, song.release_date, song.featured, song.popularity))
            self.conn.commit()
        except Exception as exception:
            raise DBException(song.song_id, song.title, *exception.args)
        

    def songs_features_insert(self, songf: SongFeatures) -> None:
        try:
            self.cursor.execute("""INSERT INTO songs_features
                                 (song_spotify_id, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, valence, mode, key, duration_ms)
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (songf.song_id, songf.acousticness, songf.danceability, songf.energy,
                                                                                songf.instrumentalness, songf.liveness, songf.loudness, songf.speechiness,
                                                                                songf.tempo, songf.valence, songf.mode, songf.key, songf.duration_ms))
            self.conn.commit()
        except Exception as exception:
            raise DBException(songf.song_id, *exception.args)
        

    def artists_insert(self, artist: ArtistInfo) -> None:
        try:
            self.cursor.execute("""INSERT INTO artists
                                 (artist_spotify_id, name, genres)
                                 VALUES (?, ?, ?)""", (artist.artist_id, artist.name, artist.genres))
            self.conn.commit()
        except Exception as exception:
            raise DBException(artist.artist_id, artist.name, *exception.args)
        

    def albums_insert(self, album: AlbumInfo) -> None:
        try:
            self.cursor.execute("""INSERT INTO albums
                                 (album_spotify_id, name, release_date, total_tracks, genres, popularity)
                                 VALUES (?, ?, ?, ?, ?, ?)""", (album.album_id, album.name, album.release_date, album.total_tracks, album.genres, album.popularity))
            self.conn.commit()
        except Exception as exception:
            raise DBException(album.album_id, album.name, *exception.args)
        

    def lyrics_insert(self, lyrics: LyricsInfo) -> None:
        try:
            self.cursor.execute("""INSERT INTO lyrics
                                 (song_spotify_id, lyrics)
                                 VALUES (?, ?)""", (lyrics.song_id, lyrics.lyrics))
            self.conn.commit()
        except Exception as exception:
            raise DBException(lyrics.song_id, *exception.args)
        

    
    # ================== GET METHODS ==================

    def get_scraped_songs(self) -> list:
        self.cursor.execute("SELECT * FROM scraped_songs")
        return self.cursor.fetchall()
    


    def get_artists(self) -> list:
        self.cursor.execute("SELECT * FROM artists")
        return self.cursor.fetchall()
    

    def get_albums(self) -> list:
        self.cursor.execute("SELECT * FROM albums")
        return self.cursor.fetchall()
    





    # ================== POPULATE METHODS ==================

    def songs_populate_csv(self, csv_path: str) -> None:
        songs = SongsContainer()
        songs.from_csv(csv_path)
        for song in songs.songs:
            try:
                self.songs_insert(song)
            except:
                continue
        

    def close_connection(self) -> None:
        self.conn.close()







# TODO:

# - implement getting the playlists from Spotify API and populating the database with the songs along with ids and other stuff
# - implement a method to get the features of the songs from the Spotify API and populate the database with the features




class DBException(Exception):

    def __init__(self, *args):
        pass



if __name__ == "__main__":
    db = SongsDB()
    #db.songs_populate_csv("songs2.csv")
    db.close_connection()