# -*- coding: utf-8 -*-
from classes.email_scraper import EmailScraper
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

CLIENT_SECRET_FILE = '../conf/client_secret.json'

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    search_results = service.users().messages().list(
        userId='me',
        labelIds=None,
        q='"Songs for Sunday" from: Jason Baisch',
        maxResults=20).execute()
    messages = search_results.get('messages', [])

    if not messages:
        print('No messages found.')
    else:
        print('Messages:')
        for message in messages:
            email_results = service.users().messages().get(
                userId='me', id=message['id'],
                format='full').execute()
            subject = get_header_value(email_results, "Subject")
            date = get_header_value(email_results, "Date")
            html = get_full_body(email_results, "text/html")
            text = get_full_body(email_results, "text/plain")
            html_file = open('saved_songs_html.txt', 'a', encoding='utf-8')
            html_file.write(html)
            html_file.close()
            text_file = open('saved_songs.txt', 'a', encoding='utf-8')
            text_file.write(text)
            text_file.close()
            songs_extractor = JasonSongListExtractor(text, html)
            song_list = songs_extractor.extract_song_list()
            song_list.set_date(date)
            print(song_list)


if __name__ == '__main__':
    main()
