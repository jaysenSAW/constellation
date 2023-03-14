import os
import numpy as np
import scipy
import matplotlib.pyplot as plt
import music_tag
import pandas as pd

class MusicLibrary:

    def __init__(self, library_path):
        self.library_path = library_path
        self.library_data = None

    def files_in_folder(self, path):
        """
        list music files present in directory
        Arguments:
        """
        files = []
        extension = ["mp3", "wav", "flac"]
        with os.scandir(path) as entries:
            for entry in entries:
                if not entry.is_file():
                    continue
                if entry.name.split(".")[-1] in extension:
                    files.append(entry.name)
        return files

    def concat_path(self, path, files):
        """
        create list with full path
        """
        list_musics = []
        for file in files:
            list_musics.append(os.path.join(path, file))
        return list_musics

    def dico_albums(self, path, album_dir, dico=None):
        """
        """
        if dico is None:
            dico = {}
        list_musics = self.files_in_folder(path)
        dico[album_dir] = self.concat_path(path, list_musics)
        return dico

    def extract_metadata(self, path, dt=None):
        """
        """
        audio = music_tag.load_file(path)
        if dt is None:
            dt = pd.DataFrame(
                data = (
                    {"Title" : [str(audio['title'])],
                    "Artist" : [str(audio['artist'])],
                    "Album" : [str(audio['album'])],
                    "Album artist" : [str(audio['albumartist'])],
                    "Composer" : [str(audio['composer'])],
                    "Genre" : [str(audio['genre'])],
                    "Path" : [path]}
                )
            )
            return dt
        dt.loc[len(dt.index)] = [
            str(audio['title']),
            str(audio['artist']),
            str(audio['album']),
            str(audio['albumartist']),
            str(audio['composer']),
            str(audio['genre']),
            path
        ]
        return dt

    def list_song(self):
        """
        list all song and store their path into dictionary
        """
        dico = {}
        for entry in os.listdir(self.library_path):
            if not os.path.isdir(os.path.join(self.library_path, entry)):
                continue
            dico = self.dico_albums(os.path.join(self.library_path, entry),
                           entry,
                           dico)
        data = None
        for album in dico.keys():
            for path in dico[album]:
                data = self.extract_metadata(path, data)
        self.library_data = data

    def add_genre_in_dataframe(self):
        """
        extract genre for each music
        """
        genre_in_genre = self.library_data['Genre'].str.split(pat=",")
        list_genre = np.unique(np.char.lower(np.hstack(genre_in_genre.to_numpy())))
        for genre in list_genre:
            self.library_data.insert(loc=self.library_data.shape[1], column=genre, value=np.zeros(self.library_data.shape[0]))
        for i in range(self.library_data.shape[0]):
            for genre in genre_in_genre[i]:
                self.library_data.loc[i, [genre.lower()]] = 1

    def music2pandasDataframe(self):
        self.list_song()
        self.add_genre_in_dataframe()
        return self.library_data


if __name__ == '__main__':
    library_musics = os.path.join(os.environ['HOMEPATH'], 'Music')
    #test = Music2pandas(library_music)
    music_library = MusicLibrary(library_musics)
    dt = music_library.music2pandasDataframe()
    print(dt.head())
