from __future__ import print_function
from classes.song_info import SongInfo
from classes.song_list import SongList
from classes.jason_song_list_extractor import JasonSongListExtractor

def main():
    jason_extractor = JasonSongListExtractor()
    song_list = jason_extractor.extract_song_list("Foo")

    print(song_list)

if __name__ == "__main__":
    main()
