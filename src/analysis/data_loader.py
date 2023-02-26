import os
import numpy as np
import scipy
import matplotlib.pyplot as plt
#import eyed3
import music_tag
import pandas as pd

# Load data

def files_in_folder(path: str) -> list:
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

def concat_path(path: str, files: list) -> list:
    """
    create list with full path
    """
    list_musics = []
    for file in files:
        list_musics.append(os.path.join(path, file))
    return list_musics


def dico_albums(path: str, album_dir: str, dico: dict = None) -> dict:
    """
    """
    if dico is None:
        dico = {}
    list_musics = files_in_folder(path)
    dico[album_dir] = concat_path(path, list_musics)
    return dico

def extract_metadata(path: str, dt: pd.DataFrame = None):
    """
    """
    # if path.split(".")[-1] != "mp3":
    #     print("cannot read metada from other file as mp3")
    #     return dt
    # audio=eyed3.load(path)
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
                "Year" : [str(audio['year'])],
                "Path" : [path]}
            )
        )
        return dt
    # add new row
    dt.loc[len(dt.index)] = [
        str(audio['title']),
        str(audio['artist']),
        str(audio['album']),
        str(audio['albumartist']),
        str(audio['composer']),
        str(audio['genre']),
        str(audio['year']),
        path
    ]
    return dt

if __name__ == __main__:

    #list all song and store their path into dictionary
    library_music = os.path.join(os.environ['HOMEPATH'], 'Music')
    dico = {} #album's folder name is the key
    for entry in os.listdir(library_music):
        if not os.path.isdir(os.path.join(library_music, entry)):
            continue
        dico = dico_albums(os.path.join(library_music, entry),
                           entry,
                           dico)

    data = None
    for album in dico.keys():
        for path in dico[album]:
            data = extract_metadata(path, data)
