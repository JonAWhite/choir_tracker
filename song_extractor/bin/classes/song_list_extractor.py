from __future__ import print_function
from song_list import SongList
import re

class SongListExtractor:
    def __init__(self, text):
        self.text = text

    def extract_song_list(self):
        song_list = SongList("")
        return song_list

    def remove_non_song_lines(self):
        lines = self.text.splitlines(True)
        filtered_lines = []
        for line in lines:
            if self.contains_song(line) == True:
                filtered_lines.append(line.rstrip())

        return filtered_lines

    def contains_song(self, line):
        result = self.contains_number(line)
        return result

    def contains_number(self, line):
        result = re.search(r"(\d+)", line)
        return result != None 

    def count_words(self, text):
        count = len(re.findall(r'\w+', text))
        return count

    def get_word_groups_from_line(self, song_line):
        word_groups = []
        for m in re.finditer(r"(?:^|\s)([A-Za-z,! ]+)(?:\s|$)", song_line):
            # print(song_line + " => '" + m.group(0).strip() + "'")
            word_groups.append(m.group(0).strip())

        return word_groups

    def get_number_groups_from_line(self, song_line):
        number_groups = []
        for m in re.finditer(r"(?:^|\s)((?:[CH])?[0-9]+)(?:\s|$)", song_line):
            # print(song_line + " => '" + m.group(0).strip() + "'")
            number_groups.append(m.group(0).strip())

        return number_groups

    def pick_title_from_word_groups(self, word_groups):
        # Set the default
        title = "Default Title"

        # Make a best guess that it is the last word group
        if len(word_groups) > 0:
            title = word_groups[-1]

        # Choose the group with more than one word
        for word_group in word_groups:
            if self.count_words(word_group) > 1:
                title = word_group
                break
            
        return title

    def pick_book_and_number_from_number_groups(self, number_groups):
        # Set the default
        book_and_number_code = "DB0"

        # Make a best guess that it is the last number group
        if len(number_groups) > 0:
            book_and_number_code = number_groups[-1]

        # Choose the group with an H or a C in it
        for number_group in number_groups:
            if re.match(r"[HC]", number_group) != None:
                book_and_number_code = number_group
                break
        return self.get_book_and_number_from_code(book_and_number_code)

    def get_book_and_number_from_code(self, book_and_number_code):
        book = "Default Book"
        number = 0

        match = re.match(r"([HC])?(\d+)", book_and_number_code)
        if match != None:
            book = match.group(1)
            number = match.group(2)

        if book == None:
            book = "CB"

        return book, number