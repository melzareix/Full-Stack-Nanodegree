import requests, grequests, media

class Tmdbv4:
    """ An API Wrapper for tmdb Discover route."""
    BASE_API = 'https://api.themoviedb.org/3'

    def __init__(self, api_key):
        self.api_key = '?api_key=' + str(api_key)

    def get_popular_movies(self):
        """
        Get a list of the top movies on tmdb.
        :return: List of Media.Movie Objects with the corresponding information.
        """

        url = Tmdbv4.BASE_API + '/discover/movie' + self.api_key
        r = requests.get(url).json()
        movies_ids = [x['id'] for x in r['results']]
        titles = [x['original_title'] for x in r['results']]
        storylines = [x['overview'] for x in r['results']]
        trailers = self.get_popular_movies_youtube_trailers(movies_ids)
        posters = [self.get_movie_poster_url(x['poster_path']) for x in r['results']]

        movies = []
        for x in range(len(r['results'])):
            movies.append(media.Movie(titles[x], storylines[x], posters[x], trailers[x]))
        return movies

    def get_popular_movies_youtube_trailers(self, movies_ids):
        """
        Get a list of one trailer for each movie.
        :param movies_ids: The ids of the movies.
        :return: List of youtube trailer links
        """
        movies_trailers = []
        reqs = []
        for mid in movies_ids:
            url = Tmdbv4.BASE_API + '/movie/' + str(mid) \
                  + '/videos' + self.api_key
            reqs.append(url)
        reqs = grequests.map([grequests.get(u) for u in reqs])
        for x in reqs:
            trailer_exists = False
            for y in x.json()['results']:
                if y['site'] == 'YouTube' and y['type'] == 'Trailer':
                    movies_trailers.append(self.get_movie_trailer_url(y['key']))
                    trailer_exists = True
                    break

            if not trailer_exists:
                movies_trailers.append('')

        return movies_trailers

    def get_movie_poster_url(self, poster_id):
        return 'https://image.tmdb.org/t/p/w300' + str(poster_id)

    def get_movie_trailer_url(self, yt_id):
        return 'https://www.youtube.com/watch?v=' + yt_id
