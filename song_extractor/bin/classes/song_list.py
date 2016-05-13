# -*- coding: utf-8 -*-
class SongList:

    def __init__(self, director):
        self.director = director
        self.song_infos = []
        self.date = ""

    def add_song_info(self, song_info):
        self.song_infos.append(song_info)

    def set_date(self, date):
        self.date = date

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        string = u''
        if len(self.song_infos) > 0:
            string = self.director + " [" + self.date + "]: "
            for song_info in self.song_infos:
                string += u"\n\t" + song_info.__unicode__()
        return string
