import unittest
from classes.jason_song_list_extractor import JasonSongListExtractor
from classes.song_list import SongList
from classes.song_info import SongInfo


class JasonSongListExtractorTestCase(unittest.TestCase):

    def test_songs_with_apostrophes(self):
        text = "COB 92 O come to God's altar v2"
        html = ""
        song_list = JasonSongListExtractor(text, html).extract_song_list()
        self.assertEqual(song_list.song_infos[0].book, "CB")
        self.assertEqual(song_list.song_infos[0].number, "92")
        self.assertEqual(song_list.song_infos[0].title, "O come to God's altar")

    def test_songs_with_markdown(self):
        text = "*OPEN *H56 Praise our God with joyful singing"
        html = ""
        song_list = JasonSongListExtractor(text, html).extract_song_list()
        self.assertEqual(song_list.song_infos[0].book, "H")
        self.assertEqual(song_list.song_infos[0].number, "56")
        self.assertEqual(song_list.song_infos[0].title,
                         "Praise our God with joyful singing")


if __name__ == '__main__':
    unittest.main()
