# -*- coding: utf-8 -*-
from __future__ import print_function
from classes.song_list import SongList
from bs4 import BeautifulSoup
import regex as re


class HTMLSongListExtractor:

    def __init__(self, text):
        self.text = text

    def extract_song_list(self):
        song_list = SongList("")
        return song_list

    def convert_table_to_lines(self):
        filtered_lines = []
        ugly_soup = BeautifulSoup(self.text, "html5lib")
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
                line += cell_text + "|"
        return line.strip()
