from songPlaylist import SongPlaylist
songs = SongPlaylist()
songs.addSong("illahi","arijitiSingh")
songs.addSong("tu har lambha", "arijit singh")
iterator = songs.createIterator()

while iterator.has_next():
    song = iterator.next()
    print(f'Song name: {song.getSongName()} is sung by: {song.getSingerName()}')
   

