class Movie:
    """
    Creates a Movie object from the movie title, story line,
    poster image and a link to youtube trailer.
    """
    def __init__(self, title, story_line, poster_img, yt_trailer):
        self.title = title
        self.story_line = story_line
        self.poster_img = poster_img
        self.yt_trailer = yt_trailer
