import re
from song_list import SongList 
from song_info import SongInfo

class JasonSongListExtractor(SongListExtractor):
    def extract_song_list(self, text):
        song_list = SongList("Jason Baisch")
        song_info1 = SongInfo("C", 21, "God Loves Us All")
        song_info2 = SongInfo("H", 121, "Nearer My God to Thee")
        song_list.set_date("20160508")
        song_list.add_song_info(song_info1)
        song_list.add_song_info(song_info2)
        return song_list
    

