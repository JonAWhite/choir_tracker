import re
from song_list import SongList 

class SongListExtractor:
    def extract_song_list(text):
        song_list = SongList("")
        return song_list

    def remove_non_song_lines(text):
        lines = text.splitlines(True)
        filtered_lines = []
        for line in lines:
            if contains_song(line):
                filtered_lines.append(line)

         return filtered_lines

         # TODO(jwhite) - Implement this function 
         def contains_song(line):
             return True
                

