import unittest
from classes.jason_song_list_extractor import JasonSongListExtractor
from classes.song_list import SongList


class JasonSongListExtractorTestCase(unittest.TestCase):
    def test_songs_with_apostrophes(self):
        text = "COB 92 O come to God's altar v2 "
        html = ""
        song_list = JasonSongListExtractor(text, html).extract_song_list()
        print song_list


if __name__ == '__main__':
    unittest.main()
