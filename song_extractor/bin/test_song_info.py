
from __future__ import print_function
from classes.song_info import SongInfo
from classes.song_list import SongList
from classes.jason_song_list_extractor import JasonSongListExtractor
# from classes.html_song_list_extractor import HTMLSongListExtractor


def main():
    html_song_file = open('saved_songs_html.txt', 'r')
    text_song_file = open('saved_songs.txt', 'r')
    jason_extractor = JasonSongListExtractor(text_song_file.read(), html_song_file.read())
    song_list = jason_extractor.extract_song_list()
    # html_extractor = HTMLSongListExtractor(song_file.read())
    # html_extractor.convert_table_to_lines()
    # song_list = html_extractor.extract_song_list()
    song_list.set_date("20160508")

    print(song_list)


if __name__ == "__main__":
    main()
