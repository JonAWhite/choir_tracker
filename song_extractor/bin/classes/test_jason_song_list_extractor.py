# -*- coding: utf-8 -*-
import unittest
from classes.jason_song_list_extractor import JasonSongListExtractor
from classes.song_list import SongList
from classes.song_info import SongInfo


class JasonSongListExtractorTestCase(unittest.TestCase):

    def test_songs_with_amperstands(self):
        text = u"Pre3 231 Blest & Holy"
        html = ""
        song_list = JasonSongListExtractor(text, html).extract_song_list()
        self.assertEqual(song_list.song_infos[0].book, "CB")
        self.assertEqual(song_list.song_infos[0].number, "231")
        self.assertEqual(song_list.song_infos[0].title, "Blest & Holy")

    def test_songs_with_apostrophes(self):
        text = u"COB 92 O come to God's altar v2"
        html = ""
        song_list = JasonSongListExtractor(text, html).extract_song_list()
        self.assertEqual(song_list.song_infos[0].book, "CB")
        self.assertEqual(song_list.song_infos[0].number, "92")
        self.assertEqual(song_list.song_infos[0].title, "O come to God's altar")

    def test_songs_with_markdown(self):
        text = u"*OPEN *H56 Praise our God with joyful singing"
        html = ""
        song_list = JasonSongListExtractor(text, html).extract_song_list()
        self.assertEqual(song_list.song_infos[0].book, "H")
        self.assertEqual(song_list.song_infos[0].number, "56")
        self.assertEqual(song_list.song_infos[0].title,
                         "Praise our God with joyful singing")

    def test_songs_with_spaces_between_the_book_and_number(self):
        text = u"C 86 - Jesus name above all names (new - this is a lead in to #87 Fairest Lord Jesus)"
        html = ""
        song_list = JasonSongListExtractor(text, html).extract_song_list()
        self.assertEqual(song_list.song_infos[0].book, "C")
        self.assertEqual(song_list.song_infos[0].number, "86")
        self.assertEqual(song_list.song_infos[0].title,
                         "Jesus name above all names")

    def test_songs_with_book_and_number_after_the_title(self):
        text = u"Yes, die hard singers, you can still start sininging at 10:15 tomorrow"
        html = ""
        song_list = JasonSongListExtractor(text, html).extract_song_list()
        self.assertEqual(len(song_list.song_infos), 0)


    def test_songs_with_verses_after_the_title(self):
        text = u"H29 Worthy of worship 1+3"
        html = ""
        song_list = JasonSongListExtractor(text, html).extract_song_list()
        self.assertEqual(song_list.song_infos[0].book, "H")
        self.assertEqual(song_list.song_infos[0].number, "29")
        self.assertEqual(song_list.song_infos[0].title, "Worthy of worship")

    def test_songs_in_original_in_reply(self):
        text = u">  ~ Jeremiah 29:11-13  New Living Translaion"
        html = ""
        song_list = JasonSongListExtractor(text, html).extract_song_list()
        self.assertEqual(len(song_list.song_infos), 0)

    def test_songs_with_parenthesis(self):
        text = u"C734 Be strong in the Lord (We may know this one?)"
        html = ""
        song_list = JasonSongListExtractor(text, html).extract_song_list()
        self.assertEqual(song_list.song_infos[0].book, "C")
        self.assertEqual(song_list.song_infos[0].number, "734")
        self.assertEqual(song_list.song_infos[0].title, u"Be strong in the Lord")

    def test_songs_with_unicode(self):
        text = u"C631 The Lord’s Prayer (May be a stretch)"
        html = ""
        song_list = JasonSongListExtractor(text, html).extract_song_list()
        self.assertEqual(song_list.song_infos[0].book, "C")
        self.assertEqual(song_list.song_infos[0].number, "631")
        self.assertEqual(song_list.song_infos[0].title, u"The Lord’s Prayer")

if __name__ == '__main__':
    unittest.main()
