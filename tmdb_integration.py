"""
TMDB (The Movie Database) Integration
Fetches real movie posters and data
"""

import requests
import os
from datetime import datetime

# TMDB API Configuration
TMDB_API_KEY = os.environ.get('TMDB_API_KEY', 'YOUR_API_KEY_HERE')  # Get free key from themoviedb.org
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p'

# Image sizes
POSTER_SIZES = {
    'small': 'w185',
    'medium': 'w342',
    'large': 'w500',
    'original': 'original'
}

BACKDROP_SIZES = {
    'small': 'w300',
    'medium': 'w780',
    'large': 'w1280',
    'original': 'original'
}

class TMDBClient:
    """Client for TMDB API"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or TMDB_API_KEY
        self.session = requests.Session()
        self.session.params = {'api_key': self.api_key}
    
    def search_movie(self, title, year=None):
        """Search for a movie by title"""
        try:
            params = {'query': title}
            if year:
                params['year'] = year
            
            response = self.session.get(
                f'{TMDB_BASE_URL}/search/movie',
                params=params
            )
            response.raise_for_status()
            
            results = response.json().get('results', [])
            return results[0] if results else None
        except Exception as e:
            print(f"Error searching movie '{title}': {e}")
            return None
    
    def get_movie_details(self, tmdb_id):
        """Get detailed movie information"""
        try:
            response = self.session.get(
                f'{TMDB_BASE_URL}/movie/{tmdb_id}',
                params={'append_to_response': 'credits,videos'}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting movie details for ID {tmdb_id}: {e}")
            return None
    
    def get_poster_url(self, poster_path, size='large'):
        """Get full poster URL"""
        if not poster_path:
            return None
        
        size_code = POSTER_SIZES.get(size, 'w500')
        return f'{TMDB_IMAGE_BASE_URL}/{size_code}{poster_path}'
    
    def get_backdrop_url(self, backdrop_path, size='large'):
        """Get full backdrop URL"""
        if not backdrop_path:
            return None
        
        size_code = BACKDROP_SIZES.get(size, 'w1280')
        return f'{TMDB_IMAGE_BASE_URL}/{size_code}{backdrop_path}'
    
    def get_popular_movies(self, page=1):
        """Get popular movies"""
        try:
            response = self.session.get(
                f'{TMDB_BASE_URL}/movie/popular',
                params={'page': page}
            )
            response.raise_for_status()
            return response.json().get('results', [])
        except Exception as e:
            print(f"Error getting popular movies: {e}")
            return []
    
    def get_trending_movies(self, time_window='week'):
        """Get trending movies (day or week)"""
        try:
            response = self.session.get(
                f'{TMDB_BASE_URL}/trending/movie/{time_window}'
            )
            response.raise_for_status()
            return response.json().get('results', [])
        except Exception as e:
            print(f"Error getting trending movies: {e}")
            return []


def update_movie_posters_from_tmdb():
    """Update all movies in database with TMDB posters"""
    from app import app
    from models import db, Movie
    
    client = TMDBClient()
    
    with app.app_context():
        movies = Movie.query.all()
        updated_count = 0
        
        print(f"🎬 Updating posters for {len(movies)} movies...")
        
        for movie in movies:
            try:
                # Extract year from release_date
                year = movie.release_date.year if movie.release_date else None
                
                # Search TMDB
                tmdb_movie = client.search_movie(movie.title, year)
                
                if tmdb_movie:
                    # Update poster and backdrop URLs
                    if tmdb_movie.get('poster_path'):
                        movie.poster_url = client.get_poster_url(
                            tmdb_movie['poster_path'],
                            size='large'
                        )
                    
                    if tmdb_movie.get('backdrop_path'):
                        movie.backdrop_url = client.get_backdrop_url(
                            tmdb_movie['backdrop_path'],
                            size='large'
                        )
                    
                    updated_count += 1
                    print(f"✅ Updated: {movie.title}")
                else:
                    print(f"⚠️  Not found: {movie.title}")
                
            except Exception as e:
                print(f"❌ Error updating {movie.title}: {e}")
        
        # Commit all changes
        db.session.commit()
        
        print(f"\n🎉 Updated {updated_count}/{len(movies)} movies with TMDB posters!")
        return updated_count


def fetch_and_add_popular_movies(count=100):
    """Fetch popular movies from TMDB and add to database"""
    from app import app
    from models import db, Movie
    
    client = TMDBClient()
    
    with app.app_context():
        added_count = 0
        pages = (count // 20) + 1  # TMDB returns 20 per page
        
        print(f"🎬 Fetching {count} popular movies from TMDB...")
        
        for page in range(1, pages + 1):
            movies = client.get_popular_movies(page)
            
            for tmdb_movie in movies:
                if added_count >= count:
                    break
                
                try:
                    # Check if movie already exists
                    existing = Movie.query.filter_by(
                        title=tmdb_movie['title']
                    ).first()
                    
                    if existing:
                        continue
                    
                    # Create new movie
                    movie = Movie(
                        title=tmdb_movie['title'],
                        overview=tmdb_movie.get('overview', ''),
                        genres=','.join([str(g) for g in tmdb_movie.get('genre_ids', [])]),
                        release_date=datetime.strptime(
                            tmdb_movie['release_date'], '%Y-%m-%d'
                        ).date() if tmdb_movie.get('release_date') else None,
                        runtime=120,  # Default, would need separate API call
                        language=tmdb_movie.get('original_language', 'en'),
                        poster_url=client.get_poster_url(
                            tmdb_movie.get('poster_path'),
                            size='large'
                        ),
                        backdrop_url=client.get_backdrop_url(
                            tmdb_movie.get('backdrop_path'),
                            size='large'
                        ),
                        avg_rating=tmdb_movie.get('vote_average', 0),
                        vote_count=tmdb_movie.get('vote_count', 0),
                        popularity=tmdb_movie.get('popularity', 0),
                        cast='',
                        director=''
                    )
                    
                    db.session.add(movie)
                    added_count += 1
                    print(f"✅ Added: {movie.title}")
                    
                except Exception as e:
                    print(f"❌ Error adding movie: {e}")
            
            if added_count >= count:
                break
        
        db.session.commit()
        print(f"\n🎉 Added {added_count} movies from TMDB!")
        return added_count


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'update':
            # Update existing movies with TMDB posters
            update_movie_posters_from_tmdb()
        
        elif command == 'fetch':
            # Fetch and add popular movies
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 100
            fetch_and_add_popular_movies(count)
        
        else:
            print("Usage:")
            print("  python tmdb_integration.py update       - Update existing movies")
            print("  python tmdb_integration.py fetch [N]    - Fetch N popular movies")
    else:
        print("TMDB Integration Module")
        print("\nUsage:")
        print("  python tmdb_integration.py update       - Update existing movies with TMDB posters")
        print("  python tmdb_integration.py fetch [N]    - Fetch N popular movies from TMDB")
        print("\nNote: Set TMDB_API_KEY environment variable or edit the file")
        print("Get free API key from: https://www.themoviedb.org/settings/api")
