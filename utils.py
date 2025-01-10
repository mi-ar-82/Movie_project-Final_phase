import omdb


def fetch_movie_details(title, year = None):
    """Fetch movie details from OMDb API."""
    try:
        # Simulate fetching movie details from OMDb
        response = omdb.title(title, year = year)
        if not response:
            return {'error': 'Movie not found.'}
        
        return {
            'name': response['title'],
            'director': response.get('director'),
            'year': response.get('year'),
            'rating': response.get('imdb_rating'),
        }
    except Exception as e:
        # Return a consistent error message for API errors
        return {'error': 'Failed to fetch movie details.'}

