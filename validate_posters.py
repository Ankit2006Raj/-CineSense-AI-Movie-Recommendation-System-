"""
Poster Validation Script - Validate and fix poster URLs
"""

import requests
from app import app
from models import db, Movie
from urllib.parse import urlparse

def is_valid_url(url):
    """Check if URL is properly formatted"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def check_poster_accessible(url, timeout=5):
    """Check if poster URL is accessible"""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return response.status_code == 200
    except:
        return False

def validate_all_posters(check_accessibility=False):
    """Validate all movie posters"""
    
    with app.app_context():
        movies = Movie.query.all()
        
        invalid_movies = []
        valid_count = 0
        
        print(f"\n🔍 Validating {len(movies)} movies...")
        print("=" * 80)
        
        for movie in movies:
            is_valid = True
            reason = ""
            
            # Check if poster URL exists
            if not movie.poster_url or movie.poster_url.strip() == '':
                is_valid = False
                reason = "No poster URL"
            
            # Check if URL is properly formatted
            elif not is_valid_url(movie.poster_url):
                is_valid = False
                reason = "Invalid URL format"
            
            # Check if URL starts with http/https
            elif not movie.poster_url.startswith('http'):
                is_valid = False
                reason = "Not a valid HTTP URL"
            
            # Optionally check if URL is accessible
            elif check_accessibility:
                if not check_poster_accessible(movie.poster_url):
                    is_valid = False
                    reason = "URL not accessible"
            
            if is_valid:
                valid_count += 1
                print(f"✅ {movie.title}")
            else:
                invalid_movies.append((movie, reason))
                print(f"❌ {movie.title} - {reason}")
                print(f"   URL: {movie.poster_url}")
        
        print("=" * 80)
        print(f"\n📊 Validation Results:")
        print(f"   Valid Movies:   {valid_count} ✅")
        print(f"   Invalid Movies: {len(invalid_movies)} ❌")
        print(f"   Coverage:       {(valid_count/len(movies)*100):.1f}%")
        
        return invalid_movies

def remove_invalid_movies(invalid_movies):
    """Remove movies with invalid posters"""
    
    if not invalid_movies:
        print("\n✅ No invalid movies to remove!")
        return 0
    
    print(f"\n⚠️  Found {len(invalid_movies)} movies with invalid posters:")
    print("-" * 80)
    for movie, reason in invalid_movies:
        print(f"  • {movie.title} - {reason}")
    print("-" * 80)
    
    response = input(f"\nDelete these {len(invalid_movies)} movies? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        with app.app_context():
            count = 0
            for movie, reason in invalid_movies:
                db.session.delete(movie)
                count += 1
                print(f"🗑️  Deleted: {movie.title}")
            
            db.session.commit()
            print(f"\n✅ Successfully deleted {count} movies with invalid posters!")
            return count
    else:
        print("\n❌ Deletion cancelled.")
        return 0

def fix_common_poster_issues():
    """Fix common poster URL issues"""
    
    with app.app_context():
        movies = Movie.query.all()
        fixed_count = 0
        
        print("\n🔧 Fixing common poster issues...")
        
        for movie in movies:
            if not movie.poster_url:
                continue
            
            original_url = movie.poster_url
            fixed = False
            
            # Fix: Remove whitespace
            if movie.poster_url != movie.poster_url.strip():
                movie.poster_url = movie.poster_url.strip()
                fixed = True
            
            # Fix: Ensure https (not http)
            if movie.poster_url.startswith('http://'):
                movie.poster_url = movie.poster_url.replace('http://', 'https://')
                fixed = True
            
            if fixed:
                print(f"🔧 Fixed: {movie.title}")
                print(f"   Before: {original_url}")
                print(f"   After:  {movie.poster_url}")
                fixed_count += 1
        
        if fixed_count > 0:
            db.session.commit()
            print(f"\n✅ Fixed {fixed_count} poster URLs!")
        else:
            print("\n✅ No issues to fix!")
        
        return fixed_count

def list_movies_by_poster_domain():
    """List movies grouped by poster URL domain"""
    
    with app.app_context():
        movies = Movie.query.all()
        domains = {}
        
        for movie in movies:
            if movie.poster_url:
                try:
                    domain = urlparse(movie.poster_url).netloc
                    if domain not in domains:
                        domains[domain] = []
                    domains[domain].append(movie.title)
                except:
                    if 'invalid' not in domains:
                        domains['invalid'] = []
                    domains['invalid'].append(movie.title)
        
        print("\n📊 Movies by Poster Domain:")
        print("=" * 80)
        for domain, titles in sorted(domains.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"\n{domain} ({len(titles)} movies):")
            for title in titles[:5]:  # Show first 5
                print(f"  • {title}")
            if len(titles) > 5:
                print(f"  ... and {len(titles) - 5} more")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'validate':
            # Validate poster URLs (format only)
            invalid = validate_all_posters(check_accessibility=False)
            if invalid:
                remove_invalid_movies(invalid)
        
        elif command == 'validate-full':
            # Validate poster URLs (including accessibility check)
            print("⚠️  This will check if each poster URL is accessible (may take time)")
            invalid = validate_all_posters(check_accessibility=True)
            if invalid:
                remove_invalid_movies(invalid)
        
        elif command == 'fix':
            # Fix common issues
            fix_common_poster_issues()
        
        elif command == 'domains':
            # List movies by domain
            list_movies_by_poster_domain()
        
        elif command == 'clean':
            # Full cleanup: fix, validate, and remove
            print("🧹 Running full cleanup...")
            fix_common_poster_issues()
            invalid = validate_all_posters(check_accessibility=False)
            if invalid:
                remove_invalid_movies(invalid)
        
        else:
            print("Unknown command!")
            print("\nUsage:")
            print("  python validate_posters.py validate      - Validate poster URL formats")
            print("  python validate_posters.py validate-full - Validate and check accessibility")
            print("  python validate_posters.py fix           - Fix common poster URL issues")
            print("  python validate_posters.py domains       - List movies by poster domain")
            print("  python validate_posters.py clean         - Full cleanup (fix + validate + remove)")
    else:
        print("Poster Validation Tool")
        print("\nUsage:")
        print("  python validate_posters.py validate      - Validate poster URL formats")
        print("  python validate_posters.py validate-full - Validate and check accessibility")
        print("  python validate_posters.py fix           - Fix common poster URL issues")
        print("  python validate_posters.py domains       - List movies by poster domain")
        print("  python validate_posters.py clean         - Full cleanup (fix + validate + remove)")
        print("\nThis tool ensures all movies have valid, accessible poster URLs.")
