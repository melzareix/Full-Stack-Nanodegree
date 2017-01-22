import tmdbv4, fresh_tomatoes

# Replace API Key with yours.
r = tmdbv4.Tmdbv4('7a92830968431fb779419ce910d711a3')

# Generate the website from the movies list.
fresh_tomatoes.open_movies_page(r.get_popular_movies())
