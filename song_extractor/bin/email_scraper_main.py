# -*- coding: utf-8 -*-
import io
from classes.email_retriever import EmailRetriever
from classes.jason_song_list_extractor import JasonSongListExtractor
from classes.song_list import SongList
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


CLIENT_SECRET_FILE = '../conf/client_secret.json'
SENDER_CONFIGURATION_FILE = '../conf/sender_configuration.json'

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    email_retriever = EmailRetriever(CLIENT_SECRET_FILE, SENDER_CONFIGURATION_FILE, flags)

    for sender in email_retriever.senders["Sender"]:
        sender_name = sender["Name"]
        search_term = sender["Search"]
        basic_messages = email_retriever.get_basic_messages(sender_name, search_term)

        if len(basic_messages) == 0:
            print('No messages found.')
        else:
            print('Messages:')
            for message in basic_messages:
                subject = message.get_header_value("Subject")
                date = message.get_header_value("Date")
                html = message.get_full_body("text/html")
                text = message.get_full_body("text/plain")
                html_file = io.open('../tmp/saved_songs_2_html.txt', 'a', encoding='utf-8')
                html_file.write(unicode(html))
                html_file.close()
                text_file = io.open('../tmp/saved_songs_2.txt', 'a', encoding='utf-8')
                text_file.write(unicode(text))
                text_file.close()
                songs_extractor = JasonSongListExtractor(text, html)
                song_list = songs_extractor.extract_song_list()
                song_list.set_date(date)
                print(song_list)


if __name__ == '__main__':
    main()
