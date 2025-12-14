"""
Cleanup Script - Remove movies without valid poster URLs from database
"""

from app import app
from models import db, Movie

def cleanup_movies_without_posters():
    """Remove all movies that don't have valid poster URLs"""
    
    with app.app_context():
        # Find movies without posters
        movies_without_posters = Movie.query.filter(
            (Movie.poster_url.is_(None)) | (Movie.poster_url == '')
        ).all()
        
        if not movies_without_posters:
            print("✅ All movies have valid posters! No cleanup needed.")
            return 0
        
        print(f"🔍 Found {len(movies_without_posters)} movies without posters:")
        print("-" * 60)
        
        for movie in movies_without_posters:
            print(f"  ❌ {movie.title} (ID: {movie.id})")
        
        print("-" * 60)
        
        # Ask for confirmation
        response = input(f"\n⚠️  Delete these {len(movies_without_posters)} movies? (yes/no): ")
        
        if response.lower() in ['yes', 'y']:
            count = 0
            for movie in movies_without_posters:
                db.session.delete(movie)
                count += 1
            
            db.session.commit()
            print(f"\n✅ Successfully deleted {count} movies without posters!")
            return count
        else:
            print("\n❌ Cleanup cancelled.")
            return 0


def list_movies_without_posters():
    """List all movies without valid poster URLs"""
    
    with app.app_context():
        movies_without_posters = Movie.query.filter(
            (Movie.poster_url.is_(None)) | (Movie.poster_url == '')
        ).all()
        
        if not movies_without_posters:
            print("✅ All movies have valid posters!")
            return
        
        print(f"\n📋 Movies without posters ({len(movies_without_posters)}):")
        print("=" * 80)
        
        for i, movie in enumerate(movies_without_posters, 1):
            print(f"{i}. {movie.title}")
            print(f"   ID: {movie.id}")
            print(f"   Release: {movie.release_date}")
            print(f"   Genres: {movie.genres}")
            print(f"   Poster URL: {movie.poster_url or 'None'}")
            print("-" * 80)


def count_movies_stats():
    """Show statistics about movies in database"""
    
    with app.app_context():
        total_movies = Movie.query.count()
        movies_with_posters = Movie.query.filter(
            Movie.poster_url.isnot(None),
            Movie.poster_url != ''
        ).count()
        movies_without_posters = total_movies - movies_with_posters
        
        print("\n📊 Movie Database Statistics:")
        print("=" * 60)
        print(f"Total Movies:              {total_movies}")
        print(f"Movies with Posters:       {movies_with_posters} ✅")
        print(f"Movies without Posters:    {movies_without_posters} ❌")
        print(f"Poster Coverage:           {(movies_with_posters/total_movies*100):.1f}%")
        print("=" * 60)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'cleanup':
            cleanup_movies_without_posters()
        elif command == 'list':
            list_movies_without_posters()
        elif command == 'stats':
            count_movies_stats()
        else:
            print("Unknown command!")
            print("\nUsage:")
            print("  python cleanup_movies.py stats    - Show database statistics")
            print("  python cleanup_movies.py list     - List movies without posters")
            print("  python cleanup_movies.py cleanup  - Remove movies without posters")
    else:
        print("Movie Database Cleanup Tool")
        print("\nUsage:")
        print("  python cleanup_movies.py stats    - Show database statistics")
        print("  python cleanup_movies.py list     - List movies without posters")
        print("  python cleanup_movies.py cleanup  - Remove movies without posters")
        print("\nThis tool helps maintain a clean database with only movies that have valid posters.")
