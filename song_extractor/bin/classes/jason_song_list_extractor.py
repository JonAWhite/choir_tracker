from song_info import SongInfo
from song_list import SongList 
from song_list_extractor import SongListExtractor
import re

class JasonSongListExtractor(SongListExtractor):

    def extract_song_list(self):
        song_list = SongList("Jason Baisch")
        song_lines = self.remove_non_song_lines()
        for song_line in song_lines:
            song_info = self.get_info_from_line(song_line)
            song_list.add_song_info(song_info)

        return song_list

    def get_info_from_line(self, song_line):
        word_groups = self.get_word_groups_from_line(song_line)
        title = self.pick_title_from_word_groups(word_groups)

        number_groups = self.get_number_groups_from_line(song_line)
        book, number = self.pick_book_and_number_from_number_groups(number_groups)
        song_info = SongInfo(book, number, title)
        return song_info


