# -*- coding: utf-8 -*-
from __future__ import print_function
from bs4 import BeautifulSoup
from markdown import markdown
import unidecode
from classes.song_list import SongList
from classes.group import Group
import regex as re

class SongListExtractor:

    def __init__(self, text, html):
        self.text = text
        self.html = html

    def extract_song_list(self):
        song_list = SongList("")
        return song_list

    def remove_non_song_lines(self):
        lines = self.text.splitlines(True)
        filtered_lines = []
        for line in lines:
            if self.contains_song(line) == True and self.is_original_in_reply(line) == False:
                filtered_lines.append(line.rstrip())

        return filtered_lines

    def is_original_in_reply(self, line):
        return re.match(r'^>', line) != None

    def contains_song(self, line):
        result = self.contains_number(line)
        return result

    def contains_number(self, line):
        result = re.search(r"(\d+)", line)
        return result != None

    def count_words(self, text):
        count = len(re.findall(r'\w+', text))
        return count

    def remove_markdown(self, line):
        html = markdown(line)
        text = ''.join(BeautifulSoup(html, "html5lib").findAll(text=True))
        return text

    def remove_spaces_before_numbers(self, line):
        modified_line = re.sub(r'([A-Za-z])\s+([0-9])', r'\1\2', line)
        # if modified_line != line:
            # print("'" + line + "' => '" + line1 + "'")
        return modified_line 

    def remove_parenthesis(self, line):
        modified_line = re.sub(r'\(.*\)', '', line)
        return modified_line

    def get_word_groups_from_line(self, song_line):
        word_groups = []
        # for match in re.finditer(r"(?:^|\s)([A-Za-z,'! &?.]+)(?:\s|$)", song_line):
        for match in re.finditer(r"(?:^|\s)([^-0-9;]+)(?:\s|$)", song_line):
            # print(song_line + " => '" + m.group(0).strip() + "'")
            word_group = Group(match.start(), match.group(0).strip())
            word_groups.append(word_group)

        return word_groups

    def get_number_groups_from_line(self, song_line):
        number_groups = []

        # First do a strict match looking for <BOOK>?<NUMBER>
        # If not, just take number
        strict_matches = re.finditer(r"(?:^|\s)((?:[CH])?[0-9]+)(?:\s|$)", song_line)

        number_of_matches = sum(1 for _ in strict_matches)  # list-comprehension
        if number_of_matches > 0:
            # print("There are " + str(number_of_matches) + " of strict matches")
            matches = re.finditer(r"(?:^|\s)((?:[CH])?[0-9]+)(?:\s|$)", song_line)
        else:
            loose_matches = re.finditer(r"([0-9]+)(?:\s|$)", song_line)
            number_of_matches = sum(1 for _ in loose_matches)
            # print("There are " + str(number_of_matches) + " of loose matches")
            matches = re.finditer(r"([0-9]+)(?:\s|$)", song_line)

        for match in matches:
            # print(song_line + " => '" + match.group(0).strip() + "'")
            number_group = Group(match.start(), match.group(0).strip())
            number_groups.append(number_group)

        return number_groups

    def pick_title_from_word_groups(self, word_groups):
        # Set the default
        title = "Default Title"
        position = -1

        # Make a best guess that it is the last word group
        if len(word_groups) > 0:
            title = word_groups[-1].value
            position = word_groups[-1].position

        # Choose the group with more than one word
        for word_group in word_groups:
            if self.count_words(word_group.value) > 1:
                title = word_group.value
                position = word_group.position
                break

        return title, position

    def pick_book_and_number_from_number_groups(self, number_groups):
        # Set the default
        book_and_number_code = "DB0"
        position = -1

        # Make a best guess that it is the last number group
        if len(number_groups) > 0:
            book_and_number_code = number_groups[0].value
            position = number_groups[0].position

        # Choose the group with an H or a C in it
        for number_group in number_groups:
            if re.match(r"[HC]", number_group.value) != None:
                book_and_number_code = number_group.value
                position = number_group.position
                break


        book, number = self.get_book_and_number_from_code(book_and_number_code)
        return book, number, position

    def get_book_and_number_from_code(self, book_and_number_code):
        book = "DB"
        number = 0

        match = re.match(r'([HC])?(\d+)', book_and_number_code)
        if match != None:
            book = match.group(1)
            number = match.group(2)
            # print("Group1: " + match.group(1) + "; Group2 " + match.group(2))
        # else:
            # TODO(jwhite) log this
            # print(book_and_number_code + " don't match anything")

        if book == None:
            book = "CB"

        return book, number

    def does_html_contain_table(self):
        soup = BeautifulSoup(self.html, "html5lib")
        return len(soup.findAll("table")) > 0

    def convert_tables_to_lines(self):
        filtered_lines = []
        ugly_soup = BeautifulSoup(self.html, "html5lib")
        soup = BeautifulSoup(
            ugly_soup.prettify(formatter=lambda s: s.replace(u'\xa0', ' ')),
            "html5lib")
        tables = soup.findAll("table")
        for table in tables:
            rows = table.findAll('tr')
            for row in rows:
                line = self.convert_row_to_line(row)
                filtered_lines.append(line)
        return filtered_lines

    def convert_row_to_line(self, row):
        line = ""
        cells = row.findAll("td")
        for cell in cells:
            cell_text = cell.get_text()
            if cell_text != None:
                cell_text = re.sub(r"\s*\n\s*", ' ', cell_text.strip())
                if self.contains_number(cell_text) == True:
                    cell_text = re.sub(r"[ ]*", '', cell_text)
                line += cell_text + " "
        return line.strip()
