from song import Song
from typing import List
from songIterator import SongIterator
class SongPlaylist:
    def __init__(self):
        self.songList:List[Song] = []
    def addSong(self,songName,singerName):
        self.songList.append(Song(song_name=songName,song_singer=singerName))
    def createIterator(self):
        return SongIterator(self.songList)

