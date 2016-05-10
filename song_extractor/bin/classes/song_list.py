class SongList:
    def __init__(self, director):
        self.director = director
        self.song_infos = []

    def add_song_info(self, song_info):
        self.song_infos.append(song_info)

    def set_date(self, date):
        self.date = date

    def __str__(self):
        string = self.director + " [" + self.date + "]: "
        for song_info in self.song_infos:
            string += "\n\t" + song_info.__str__()
        return string
