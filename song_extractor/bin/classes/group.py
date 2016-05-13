# -*- coding: utf-8 -*-
class Group:

    def __init__(self, position, value):
        self.position = position
        self.value = value

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        string = "[ " + self.position + " ]: " + self.value
        return string
