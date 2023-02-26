import os
import numpy as np
import scipy
import matplotlib.pyplot as plt

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

def dico_albums(path: str, album: str, dico: None) -> dict:
    """
    """
    if dico is None:
        dico = {}
    list_musics = files_in_folder(os.path.join(library_music, entry))
    dico[album] = concat_path(os.path.join(library_music, entry), list_musics)
    return dico

if __name__ == __main__:

    library_music = os.path.join(os.environ['HOMEPATH'], 'Music')
    dico = {}
    for entry in os.listdir(library_music):
        # list_musics = files_in_folder(os.path.join(library_music, entry))
        # tmp = concat_path(os.path.join(library_music, entry), list_musics)
        if not os.path.isdir(os.path.join(library_music, entry)):
            continue
        dico = dico_albums(os.path.join(library_music, entry),
                           entry,
                           dico)
