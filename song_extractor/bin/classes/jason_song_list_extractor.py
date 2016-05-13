# -*- coding: utf-8 -*-
from classes.song_info import SongInfo
from classes.song_list import SongList
from classes.song_list_extractor import SongListExtractor


class JasonSongListExtractor(SongListExtractor):

    def extract_song_list(self):
        song_list = SongList("Jason Baisch")
        song_lines = []
        if self.does_html_contain_table() == False:
            song_lines = self.remove_non_song_lines()
        else:
            song_lines = self.convert_tables_to_lines()

        for song_line in song_lines:
            song_info = self.get_info_from_line(song_line)
            if song_info != None:
                song_list.add_song_info(song_info)

        return song_list

    def get_info_from_line(self, song_line):
        original_song_line = song_line
        song_line = self.remove_markdown(song_line)
        song_line = self.remove_parenthesis(song_line)
        word_groups = self.get_word_groups_from_line(song_line)

        # Only do this after you've already parsed the word groups
        song_line = self.remove_spaces_before_numbers(song_line)
        title, word_group_position = self.pick_title_from_word_groups(word_groups)

        number_groups = self.get_number_groups_from_line(song_line)
        book, number, number_group_position = self.pick_book_and_number_from_number_groups(
            number_groups)

        # Check to make sure that the book and number come before the title
        song_info = None
        if number > 0 and number_group_position < word_group_position:
            song_info = SongInfo(book, number, title)
        # else:
            #TODO(jwhite) Log this
            # print "Could not get info from '" + original_song_line + "'"
        return song_info
