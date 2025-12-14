"""
Data Loader - Loads sample movie data into the database
"""

from datetime import datetime, date
from models import db, Movie

def load_sample_data():
    """Load sample movie data into the database"""
    
    sample_movies = [
        {
            'title': 'The Shawshank Redemption',
            'overview': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
            'genres': 'Drama,Crime',
            'release_date': date(1994, 9, 23),
            'runtime': 142,
            'language': 'en',
            'poster_url': 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
            'backdrop_url': 'https://image.tmdb.org/t/p/w1280/kXfqcdQKsToO0OUXHcrrNCHDBzO.jpg',
            'cast': 'Tim Robbins,Morgan Freeman,Bob Gunton',
            'director': 'Frank Darabont',
            'avg_rating': 8.7,
            'vote_count': 23000,
            'popularity': 95.5
        },
        {
            'title': 'The Godfather',
            'overview': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
            'genres': 'Drama,Crime',
            'release_date': date(1972, 3, 24),
            'runtime': 175,
            'language': 'en',
            'poster_url': 'https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg',
            'backdrop_url': 'https://image.tmdb.org/t/p/w1280/tmU7GeKVybMWFButWEGl2M4GeiP.jpg',
            'cast': 'Marlon Brando,Al Pacino,James Caan',
            'director': 'Francis Ford Coppola',
            'avg_rating': 8.7,
            'vote_count': 17000,
            'popularity': 92.3
        },
        {
            'title': 'The Dark Knight',
            'overview': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests.',
            'genres': 'Action,Crime,Drama',
            'release_date': date(2008, 7, 18),
            'runtime': 152,
            'language': 'en',
            'poster_url': 'https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg',
            'backdrop_url': 'https://image.tmdb.org/t/p/w1280/hkBaDkMWbLaf8B1lsWsKX7Ew3Xq.jpg',
            'cast': 'Christian Bale,Heath Ledger,Aaron Eckhart',
            'director': 'Christopher Nolan',
            'avg_rating': 8.5,
            'vote_count': 28000,
            'popularity': 98.7
        },
        {
            'title': 'Pulp Fiction',
            'overview': 'The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.',
            'genres': 'Crime,Drama',
            'release_date': date(1994, 10, 14),
            'runtime': 154,
            'language': 'en',
            'poster_url': 'https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg',
            'backdrop_url': 'https://image.tmdb.org/t/p/w1280/suaEOtk1N1sgg2MTM7oZd2cfVp3.jpg',
            'cast': 'John Travolta,Uma Thurman,Samuel L. Jackson',
            'director': 'Quentin Tarantino',
            'avg_rating': 8.5,
            'vote_count': 25000,
            'popularity': 89.4
        },
        {
            'title': 'Forrest Gump',
            'overview': 'The presidencies of Kennedy and Johnson, the Vietnam War, and other historical events unfold from the perspective of an Alabama man.',
            'genres': 'Drama,Romance',
            'release_date': date(1994, 7, 6),
            'runtime': 142,
            'language': 'en',
            'poster_url': 'https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg',
            'backdrop_url': 'https://image.tmdb.org/t/p/w1280/7c9UVPPiTPltouxRVY6N9uFiJ3p.jpg',
            'cast': 'Tom Hanks,Robin Wright,Gary Sinise',
            'director': 'Robert Zemeckis',
            'avg_rating': 8.4,
            'vote_count': 24000,
            'popularity': 87.2
        },
        {
            'title': 'Inception',
            'overview': 'A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea.',
            'genres': 'Action,Science Fiction,Adventure',
            'release_date': date(2010, 7, 16),
            'runtime': 148,
            'language': 'en',
            'poster_url': 'https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg',
            'backdrop_url': 'https://image.tmdb.org/t/p/w1280/s3TBrRGB1iav7gFOCNx3H31MoES.jpg',
            'cast': 'Leonardo DiCaprio,Joseph Gordon-Levitt,Ellen Page',
            'director': 'Christopher Nolan',
            'avg_rating': 8.4,
            'vote_count': 31000,
            'popularity': 96.8
        },
        {
            'title': 'The Matrix',
            'overview': 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
            'genres': 'Action,Science Fiction',
            'release_date': date(1999, 3, 31),
            'runtime': 136,
            'language': 'en',
            'poster_url': 'https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg',
            'backdrop_url': 'https://image.tmdb.org/t/p/w1280/icmmSD4vTTDKOq2vvdulafOGw93.jpg',
            'cast': 'Keanu Reeves,Laurence Fishburne,Carrie-Anne Moss',
            'director': 'Lana Wachowski',
            'avg_rating': 8.2,
            'vote_count': 22000,
            'popularity': 91.5
        },
        {
            'title': 'Interstellar',
            'overview': "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
            'genres': 'Adventure,Drama,Science Fiction',
            'release_date': date(2014, 11, 7),
            'runtime': 169,
            'language': 'en',
            'poster_url': 'https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg',
            'backdrop_url': 'https://image.tmdb.org/t/p/w1280/xu9zaAevzQ5nnrsXN6JcahLnG4i.jpg',
            'cast': 'Matthew McConaughey,Anne Hathaway,Jessica Chastain',
            'director': 'Christopher Nolan',
            'avg_rating': 8.3,
            'vote_count': 29000,
            'popularity': 94.1
        },
        {
            'title': 'The Silence of the Lambs',
            'overview': 'A young FBI cadet must receive the help of an incarcerated cannibal killer to catch another serial killer.',
            'genres': 'Crime,Drama,Thriller',
            'release_date': date(1991, 2, 14),
            'runtime': 118,
            'language': 'en',
            'poster_url': 'https://image.tmdb.org/t/p/w500/uS9m8OBk1A8eM9I042bx8XXpqAq.jpg',
            'backdrop_url': 'https://image.tmdb.org/t/p/w1280/mfwq2nMBzArzQ7Y9RKE8SKeeTkg.jpg',
            'cast': 'Jodie Foster,Anthony Hopkins,Scott Glenn',
            'director': 'Jonathan Demme',
            'avg_rating': 8.3,
            'vote_count': 13000,
            'popularity': 85.7
        },
        {
            'title': 'Parasite',
            'overview': 'All unemployed, the Kim family takes peculiar interest in the wealthy Park family.',
            'genres': 'Comedy,Thriller,Drama',
            'release_date': date(2019, 5, 30),
            'runtime': 132,
            'language': 'ko',
            'poster_url': 'https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg',
            'backdrop_url': 'https://image.tmdb.org/t/p/w1280/TU9NIjwzjoKPwQHoHshkFcQUCG.jpg',
            'cast': 'Song Kang-ho,Lee Sun-kyun,Cho Yeo-jeong',
            'director': 'Bong Joon-ho',
            'avg_rating': 8.5,
            'vote_count': 15000,
            'popularity': 88.9
        }
    ]
    
    print("📊 Loading sample movie data...")
    
    for movie_data in sample_movies:
        # Check if movie already exists
        existing = Movie.query.filter_by(title=movie_data['title']).first()
        if not existing:
            movie = Movie(**movie_data)
            db.session.add(movie)
            print(f"✅ Added: {movie_data['title']}")
        else:
            print(f"⏭️  Skipped (exists): {movie_data['title']}")
    
    db.session.commit()
    print(f"\n🎉 Sample data loaded successfully!")
    
    return len(sample_movies)


if __name__ == '__main__':
    from app import app
    
    with app.app_context():
        load_sample_data()
