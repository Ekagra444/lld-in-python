from iteratorInterface import InteratorInterface
from typing import List
from song import Song
class SongIterator(InteratorInterface):
    def __init__(self, songList:List[Song]):
        self.__songList = songList
        self.__position =0  
    def has_next(self):
        if self.__position< len(self.__songList):
            return True
        return False
    def next(self):
        if self.has_next()==True:
            song = self.__songList[self.__position]
            self.__position+=1
            return song
        else:
            return None
