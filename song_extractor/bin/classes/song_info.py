
class SongInfo:

    def __init__(self, book, number, title):
        self.book = book
        self.number = number
        self.title = title

    def __str__(self):
        string = self.book + str(self.number) + ": " + self.title
        return string
