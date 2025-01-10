import omdb

def fetch_movie_details(title, year=None):
    """
    Fetch movie details from OMDb API using the title and optional year.
    """
    try:
        response = omdb.title(title, year=year)
        if response:
            return {
                'name': response.get('title'),
                'director': response.get('director'),
                'year': response.get('year'),
                'rating': response.get('imdb_rating')
            }
        else:
            return {'error': 'Movie not found'}
    except Exception as e:
        return {'error': f'Error fetching data from OMDb: {str(e)}'}
