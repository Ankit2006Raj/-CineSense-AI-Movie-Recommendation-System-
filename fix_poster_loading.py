"""
Fix Poster Loading Issues
Ensures all TMDB poster URLs are properly formatted and accessible
"""

from app import app
from models import db, Movie

def fix_tmdb_poster_urls():
    """Ensure all TMDB poster URLs use HTTPS and proper size"""
    
    with app.app_context():
        movies = Movie.query.all()
        fixed_count = 0
        
        print(f"\n🔧 Fixing TMDB poster URLs for {len(movies)} movies...")
        print("=" * 80)
        
        for movie in movies:
            if not movie.poster_url:
                continue
            
            original_url = movie.poster_url
            modified = False
            
            # Ensure HTTPS
            if movie.poster_url.startswith('http://'):
                movie.poster_url = movie.poster_url.replace('http://', 'https://')
                modified = True
            
            # Ensure proper TMDB image size (w500 is good balance)
            if 'image.tmdb.org' in movie.poster_url:
                # Replace any size with w500 for consistency
                sizes = ['w92', 'w154', 'w185', 'w342', 'w780', 'original']
                for size in sizes:
                    if f'/{size}/' in movie.poster_url and size != 'w500':
                        movie.poster_url = movie.poster_url.replace(f'/{size}/', '/w500/')
                        modified = True
                        break
            
            if modified:
                print(f"✅ Fixed: {movie.title}")
                if original_url != movie.poster_url:
                    print(f"   Before: {original_url}")
                    print(f"   After:  {movie.poster_url}")
                fixed_count += 1
        
        if fixed_count > 0:
            db.session.commit()
            print("=" * 80)
            print(f"\n✅ Fixed {fixed_count} poster URLs!")
        else:
            print("=" * 80)
            print("\n✅ All poster URLs are already properly formatted!")
        
        return fixed_count

def add_cache_buster():
    """Add cache-busting parameter to force image reload"""
    
    with app.app_context():
        movies = Movie.query.all()
        updated_count = 0
        
        print(f"\n🔄 Adding cache-buster to {len(movies)} poster URLs...")
        
        for movie in movies:
            if movie.poster_url and '?' not in movie.poster_url:
                movie.poster_url = f"{movie.poster_url}?v=2"
                updated_count += 1
        
        if updated_count > 0:
            db.session.commit()
            print(f"✅ Added cache-buster to {updated_count} URLs!")
        else:
            print("✅ Cache-busters already present!")
        
        return updated_count

def verify_poster_format():
    """Verify all posters are properly formatted"""
    
    with app.app_context():
        movies = Movie.query.all()
        
        print(f"\n📊 Poster URL Analysis:")
        print("=" * 80)
        
        https_count = 0
        http_count = 0
        tmdb_count = 0
        w500_count = 0
        
        for movie in movies:
            if movie.poster_url:
                if movie.poster_url.startswith('https://'):
                    https_count += 1
                elif movie.poster_url.startswith('http://'):
                    http_count += 1
                
                if 'image.tmdb.org' in movie.poster_url:
                    tmdb_count += 1
                    if '/w500/' in movie.poster_url:
                        w500_count += 1
        
        print(f"Total Movies:           {len(movies)}")
        print(f"HTTPS URLs:             {https_count} ✅")
        print(f"HTTP URLs:              {http_count} {'⚠️' if http_count > 0 else '✅'}")
        print(f"TMDB Images:            {tmdb_count}")
        print(f"Optimal Size (w500):    {w500_count}")
        print("=" * 80)
        
        if http_count > 0:
            print("\n⚠️  Some URLs use HTTP instead of HTTPS. Run 'fix' command to update.")
        else:
            print("\n✅ All poster URLs are properly formatted!")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'fix':
            fix_tmdb_poster_urls()
            verify_poster_format()
        
        elif command == 'verify':
            verify_poster_format()
        
        elif command == 'cache-bust':
            add_cache_buster()
        
        elif command == 'all':
            print("🚀 Running complete poster fix...")
            fix_tmdb_poster_urls()
            verify_poster_format()
        
        else:
            print("Unknown command!")
            print("\nUsage:")
            print("  python fix_poster_loading.py fix        - Fix TMDB poster URLs")
            print("  python fix_poster_loading.py verify     - Verify poster URL formats")
            print("  python fix_poster_loading.py cache-bust - Add cache-busting parameters")
            print("  python fix_poster_loading.py all        - Run all fixes")
    else:
        print("Poster Loading Fix Tool")
        print("\nUsage:")
        print("  python fix_poster_loading.py fix        - Fix TMDB poster URLs (HTTPS, size)")
        print("  python fix_poster_loading.py verify     - Verify poster URL formats")
        print("  python fix_poster_loading.py cache-bust - Add cache-busting parameters")
        print("  python fix_poster_loading.py all        - Run all fixes")
        print("\nThis ensures all TMDB posters load properly with HTTPS and optimal size.")
