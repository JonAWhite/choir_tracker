# -*- coding: utf-8 -*-
class SongInfo:

    def __init__(self, book, number, title):
        self.book = book
        self.number = number
        self.title = title

    def __str__(self):
         return unicode(self).encode('utf-8')

    def __unicode__(self):
        string = self.book + unicode(self.number).encode('utf-8') + u": " + self.title
        return string
