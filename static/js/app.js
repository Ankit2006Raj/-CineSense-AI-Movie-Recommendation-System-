// Global state
let currentUser = null;
let authModal = null;
let movieModal = null;
let preferencesModal = null;
let currentAuthMode = 'login';

// Initialize on page load
document.addEventListener('DOMContentLoaded', function () {
    // Initialize AOS animations
    AOS.init({
        duration: 800,
        easing: 'ease-out-cubic',
        once: true,
        offset: 100
    });

    // Initialize modals
    authModal = new bootstrap.Modal(document.getElementById('authModal'));
    movieModal = new bootstrap.Modal(document.getElementById('movieModal'));
    preferencesModal = new bootstrap.Modal(document.getElementById('preferencesModal'));

    // Check if user is logged in
    checkAuthStatus();

    // Load initial data
    loadMoodOptions();
    loadTrending(7);

    // Setup auth form
    setupAuthForm();

    // Setup search
    document.getElementById('searchInput').addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            searchMovies();
        }
    });

    // Navbar scroll effect
    window.addEventListener('scroll', handleNavbarScroll);

    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
});

// Navbar scroll effect
function handleNavbarScroll() {
    const navbar = document.getElementById('mainNav');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
}

// Authentication Functions
function setupAuthForm() {
    const form = document.getElementById('authForm');
    const toggle = document.getElementById('authToggle');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        if (currentAuthMode === 'signup') {
            const username = document.getElementById('username').value;
            await signup(username, email, password);
        } else {
            await login(email, password);
        }
    });

    toggle.addEventListener('click', function (e) {
        e.preventDefault();
        toggleAuthMode();
    });
}

function showAuthModal(mode) {
    currentAuthMode = mode;
    updateAuthModal();
    authModal.show();
}

function toggleAuthMode() {
    currentAuthMode = currentAuthMode === 'login' ? 'signup' : 'login';
    updateAuthModal();
}

function updateAuthModal() {
    const title = document.getElementById('authModalTitle');
    const signupFields = document.getElementById('signupFields');
    const buttonText = document.getElementById('authButtonText');
    const toggle = document.getElementById('authToggle');

    if (currentAuthMode === 'signup') {
        title.textContent = 'Sign Up';
        signupFields.classList.remove('d-none');
        buttonText.textContent = 'Sign Up';
        toggle.textContent = 'Already have an account? Login';
    } else {
        title.textContent = 'Login';
        signupFields.classList.add('d-none');
        buttonText.textContent = 'Login';
        toggle.textContent = "Don't have an account? Sign up";
    }
}

async function signup(username, email, password) {
    try {
        const response = await fetch('/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            showNotification('Account created successfully! Please login.', 'success');
            currentAuthMode = 'login';
            updateAuthModal();
        } else {
            showNotification(data.error || 'Signup failed', 'error');
        }
    } catch (error) {
        showNotification('Network error. Please try again.', 'error');
    }
}

async function login(email, password) {
    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            currentUser = data.user;
            updateUIForLoggedInUser();
            authModal.hide();
            showNotification('Welcome back, ' + data.user.username + '!', 'success');
            loadPersonalizedRecommendations();
        } else {
            showNotification(data.error || 'Login failed', 'error');
        }
    } catch (error) {
        showNotification('Network error. Please try again.', 'error');
    }
}

async function logout() {
    try {
        await fetch('/logout', { method: 'POST' });
        currentUser = null;
        updateUIForLoggedOutUser();
        showNotification('Logged out successfully', 'success');
    } catch (error) {
        showNotification('Logout failed', 'error');
    }
}

function checkAuthStatus() {
    // In a real app, check session/token
    // For now, we'll rely on server-side session
}

function updateUIForLoggedInUser() {
    document.getElementById('authSection').classList.add('d-none');
    document.getElementById('userSection').classList.remove('d-none');
    document.getElementById('usernameDisplay').textContent = currentUser.username;
}

function updateUIForLoggedOutUser() {
    document.getElementById('authSection').classList.remove('d-none');
    document.getElementById('userSection').classList.add('d-none');

    // Clear recommendations
    document.getElementById('recommendationsContainer').innerHTML = `
        <div class="text-center py-5">
            <i class="fas fa-user-lock fa-3x text-gray-600 mb-3"></i>
            <p class="text-gray-400">Please login to see personalized recommendations</p>
            <button class="btn btn-purple mt-3" onclick="showAuthModal('login')">Login Now</button>
        </div>
    `;
}

// Mood Functions
const moods = [
    { name: 'happy', icon: '😊', color: '#fbbf24', label: 'Happy' },
    { name: 'sad', icon: '😢', color: '#60a5fa', label: 'Sad' },
    { name: 'romantic', icon: '💕', color: '#f472b6', label: 'Romantic' },
    { name: 'motivated', icon: '💪', color: '#34d399', label: 'Motivated' },
    { name: 'thriller', icon: '😱', color: '#ef4444', label: 'Thriller' },
    { name: 'scared', icon: '👻', color: '#8b5cf6', label: 'Scared' },
    { name: 'adventurous', icon: '🗺️', color: '#f59e0b', label: 'Adventurous' },
    { name: 'relaxed', icon: '😌', color: '#10b981', label: 'Relaxed' },
    { name: 'nostalgic', icon: '🎞️', color: '#a78bfa', label: 'Nostalgic' },
    { name: 'curious', icon: '🤔', color: '#06b6d4', label: 'Curious' },
    { name: 'energetic', icon: '⚡', color: '#fbbf24', label: 'Energetic' },
    { name: 'thoughtful', icon: '🧠', color: '#8b5cf6', label: 'Thoughtful' }
];

function loadMoodOptions() {
    const grid = document.getElementById('moodGrid');

    grid.innerHTML = moods.map((mood, index) => `
        <div class="col-lg-3 col-md-4 col-sm-6" data-aos="fade-up" data-aos-delay="${index * 50}">
            <div class="mood-card" onclick="selectMood('${mood.name}')">
                <span class="mood-icon" style="filter: drop-shadow(0 0 10px ${mood.color});">
                    ${mood.icon}
                </span>
                <h5 class="fw-bold mb-0">${mood.label}</h5>
            </div>
        </div>
    `).join('');
}

async function selectMood(mood) {
    if (!currentUser) {
        showNotification('Please login to get mood-based recommendations', 'warning');
        showAuthModal('login');
        return;
    }

    const container = document.getElementById('moodRecommendations');
    container.innerHTML = '<div class="spinner"></div>';

    try {
        const response = await fetch('/api/recommendations/mood', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mood })
        });

        const data = await response.json();

        if (response.ok) {
            displayMovies(data.recommendations, container, `Movies for ${mood} mood`);
            scrollToElement(container);
        } else {
            container.innerHTML = '<p class="text-center text-danger">Failed to load recommendations</p>';
        }
    } catch (error) {
        container.innerHTML = '<p class="text-center text-danger">Network error</p>';
    }
}

// Movie Display Functions
function displayMovies(movies, container, title = '') {
    if (!movies || movies.length === 0) {
        container.innerHTML = '<p class="text-center text-gray-400">No movies found</p>';
        return;
    }

    // Filter out movies without valid poster URLs
    const validMovies = movies.filter(movie =>
        movie.poster_url &&
        movie.poster_url.trim() !== '' &&
        movie.poster_url.startsWith('http')
    );

    if (validMovies.length === 0) {
        container.innerHTML = '<p class="text-center text-gray-400">No movies with posters found</p>';
        return;
    }

    let html = '';

    if (title) {
        html += `<h3 class="mb-4 fw-bold">${title}</h3>`;
    }

    html += '<div class="movie-grid">';

    validMovies.forEach(movie => {
        html += createMovieCard(movie);
    });

    html += '</div>';

    container.innerHTML = html;
}

function createMovieCard(movie) {
    // Only use valid HTTP poster URLs - NO PLACEHOLDERS
    const posterUrl = movie.poster_url && movie.poster_url.startsWith('http') ? movie.poster_url : '';

    // Skip movies without valid posters
    if (!posterUrl) {
        return '';
    }

    const rating = movie.avg_rating ? movie.avg_rating.toFixed(1) : 'N/A';
    const genres = Array.isArray(movie.genres) ? movie.genres.slice(0, 2).join(', ') : movie.genres;

    return `
        <div class="movie-card" onclick="showMovieDetails(${movie.id})">
            <div class="movie-poster-container">
                <img src="${posterUrl}" alt="${movie.title}" class="movie-poster" 
                     onerror="this.parentElement.parentElement.style.display='none';"
                     loading="lazy">
                <div class="movie-overlay">
                    <i class="fas fa-play-circle"></i>
                </div>
            </div>
            <div class="movie-info">
                <div class="movie-title">${movie.title}</div>
                <div class="movie-meta">
                    <span class="rating">
                        <i class="fas fa-star"></i>
                        ${rating}
                    </span>
                    <span>${movie.release_date ? new Date(movie.release_date).getFullYear() : 'N/A'}</span>
                </div>
                ${movie.reason ? `<div class="movie-reason"><i class="fas fa-lightbulb me-1"></i>${movie.reason}</div>` : ''}
            </div>
        </div>
    `;
}

// Generate beautiful gradient placeholder for movies
function generatePosterPlaceholder(title) {
    const gradients = [
        'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
        'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
        'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
        'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
        'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
        'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)',
        'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
        'linear-gradient(135deg, #ff6e7f 0%, #bfe9ff 100%)'
    ];

    // Use title to consistently select a gradient
    const index = Math.abs(title.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)) % gradients.length;
    const gradient = gradients[index];

    // Create SVG placeholder with gradient and movie title
    const svg = `
        <svg width="300" height="450" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="grad${index}" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:${gradient.match(/#[0-9a-f]{6}/gi)[0]};stop-opacity:1" />
                    <stop offset="100%" style="stop-color:${gradient.match(/#[0-9a-f]{6}/gi)[1]};stop-opacity:1" />
                </linearGradient>
            </defs>
            <rect width="300" height="450" fill="url(#grad${index})"/>
            <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="24" font-weight="bold" 
                  fill="white" text-anchor="middle" dominant-baseline="middle" opacity="0.9">
                <tspan x="50%" dy="0">${title.substring(0, 20)}</tspan>
                ${title.length > 20 ? `<tspan x="50%" dy="30">${title.substring(20, 40)}</tspan>` : ''}
            </text>
            <circle cx="150" cy="350" r="40" fill="rgba(255,255,255,0.2)"/>
            <path d="M 135 335 L 135 365 L 160 350 Z" fill="white" opacity="0.8"/>
        </svg>
    `;

    return 'data:image/svg+xml;base64,' + btoa(svg);
}

// Movie Details
async function showMovieDetails(movieId) {
    const modalBody = document.getElementById('movieModalBody');
    modalBody.innerHTML = '<div class="spinner"></div>';
    movieModal.show();

    try {
        const response = await fetch(`/api/movies/${movieId}`);
        const data = await response.json();

        if (response.ok) {
            renderMovieDetails(data);
        } else {
            modalBody.innerHTML = '<p class="text-center text-danger">Failed to load movie details</p>';
        }
    } catch (error) {
        modalBody.innerHTML = '<p class="text-center text-danger">Network error</p>';
    }
}

function renderMovieDetails(data) {
    const movie = data.movie;
    const sentiment = data.sentiment;
    const similar = data.similar_movies;

    // Use actual URLs only - no placeholders
    const backdropUrl = (movie.backdrop_url && movie.backdrop_url.startsWith('http')) ? movie.backdrop_url :
        (movie.poster_url && movie.poster_url.startsWith('http')) ? movie.poster_url : '';
    const posterUrl = (movie.poster_url && movie.poster_url.startsWith('http')) ? movie.poster_url : '';

    let html = `
        <div class="position-relative" style="margin: -1px -1px 0 -1px;">
            ${backdropUrl ? `<img src="${backdropUrl}" class="w-100" style="max-height: 400px; object-fit: cover; border-radius: 16px 16px 0 0;" 
                 onerror="this.style.display='none';"
                 loading="lazy">` : ''}
            <div style="position: absolute; bottom: 0; left: 0; right: 0; height: 150px; background: linear-gradient(to top, var(--dark-elevated), transparent);"></div>
        </div>
        <div class="p-4">
            <div class="row">
                ${posterUrl ? `<div class="col-md-4 mb-4 mb-md-0">
                    <img src="${posterUrl}" class="w-100 rounded shadow-lg" style="border: 3px solid var(--border-color);"
                         onerror="this.parentElement.style.display='none';"
                         loading="lazy">
                </div>` : ''}
                <div class="${posterUrl ? 'col-md-8' : 'col-12'}">
                    <h2 class="fw-bold mb-3" style="font-size: 2rem;">${movie.title}</h2>
                    <div class="d-flex gap-2 mb-3 flex-wrap">
                        <span style="background: linear-gradient(135deg, #fbbf24, #f59e0b); padding: 0.5rem 1rem; border-radius: 8px; font-weight: 600; display: inline-flex; align-items: center; gap: 0.5rem;">
                            <i class="fas fa-star"></i>${movie.avg_rating ? movie.avg_rating.toFixed(1) : 'N/A'}
                        </span>
                        <span style="background: rgba(255,255,255,0.05); padding: 0.5rem 1rem; border-radius: 8px; font-weight: 500;">
                            <i class="fas fa-clock me-1"></i>${movie.runtime} min
                        </span>
                        <span style="background: rgba(255,255,255,0.05); padding: 0.5rem 1rem; border-radius: 8px; font-weight: 500;">
                            <i class="fas fa-language me-1"></i>${movie.language}
                        </span>
                        <span style="background: rgba(255,255,255,0.05); padding: 0.5rem 1rem; border-radius: 8px; font-weight: 500;">
                            <i class="fas fa-calendar me-1"></i>${movie.release_date ? new Date(movie.release_date).getFullYear() : 'N/A'}
                        </span>
                    </div>
                    <div class="mb-3">
                        ${Array.isArray(movie.genres) ? movie.genres.map(g => `<span style="background: var(--primary-gradient); padding: 0.4rem 0.9rem; border-radius: 20px; font-size: 0.85rem; font-weight: 500; display: inline-block; margin-right: 0.5rem; margin-bottom: 0.5rem;">${g}</span>`).join('') : ''}
                    </div>
                    <p style="color: var(--text-secondary); line-height: 1.7; margin-bottom: 1.5rem;">${movie.overview || 'No overview available'}</p>
                    <div class="mb-3">
                        <strong><i class="fas fa-video me-2"></i>Director:</strong> <span style="color: var(--text-secondary);">${movie.director || 'N/A'}</span>
                    </div>
                    <div class="mb-4">
                        <strong><i class="fas fa-users me-2"></i>Cast:</strong> <span style="color: var(--text-secondary);">${Array.isArray(movie.cast) ? movie.cast.slice(0, 5).join(', ') : movie.cast || 'N/A'}</span>
                    </div>
                    
                    ${currentUser ? `
                    <div class="mb-4">
                        <label class="form-label fw-bold"><i class="fas fa-star me-2"></i>Rate this movie:</label>
                        <div class="d-flex gap-2 flex-wrap">
                            ${[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(i => `
                                <button class="btn btn-outline-white" style="min-width: 45px;" onclick="rateMovie(${movie.id}, ${i})">
                                    ${i}
                                </button>
                            `).join('')}
                        </div>
                    </div>
                    <button class="btn btn-primary-gradient btn-lg" onclick="addToWatchHistory(${movie.id})">
                        <i class="fas fa-check me-2"></i>Mark as Watched
                    </button>
                    ` : ''}
                    
                    ${sentiment && sentiment.total_reviews > 0 ? `
                    <div class="mt-4 p-3 rounded" style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-color);">
                        <h5 class="fw-bold mb-3"><i class="fas fa-chart-pie me-2"></i>Audience Sentiment</h5>
                        <div class="d-flex gap-2 flex-wrap mb-3">
                            <span style="background: rgba(16, 185, 129, 0.2); color: #10b981; padding: 0.5rem 1rem; border-radius: 8px; font-weight: 600;">
                                ${sentiment.positive_count} Positive
                            </span>
                            <span style="background: rgba(156, 163, 175, 0.2); color: #9ca3af; padding: 0.5rem 1rem; border-radius: 8px; font-weight: 600;">
                                ${sentiment.neutral_count} Neutral
                            </span>
                            <span style="background: rgba(239, 68, 68, 0.2); color: #ef4444; padding: 0.5rem 1rem; border-radius: 8px; font-weight: 600;">
                                ${sentiment.negative_count} Negative
                            </span>
                        </div>
                        <div>
                            <strong>Overall:</strong> 
                            <span style="color: ${sentiment.overall_sentiment === 'positive' ? '#10b981' : sentiment.overall_sentiment === 'negative' ? '#ef4444' : '#9ca3af'}; font-weight: 600;">
                                ${sentiment.overall_sentiment.toUpperCase()}
                            </span>
                        </div>
                    </div>
                    ` : ''}
                </div>
            </div>
        </div>
    `;

    if (similar && similar.length > 0) {
        html += `
            <div class="p-4 pt-0">
                <h4 class="fw-bold mb-4"><i class="fas fa-film me-2"></i>Similar Movies</h4>
                <div class="movie-grid">
                    ${similar.map(m => createMovieCard(m)).join('')}
                </div>
            </div>
        `;
    }

    document.getElementById('movieModalBody').innerHTML = html;
}

// Rating and Watch History
async function rateMovie(movieId, rating) {
    try {
        const response = await fetch('/api/rate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ movie_id: movieId, rating })
        });

        if (response.ok) {
            showNotification(`Rated ${rating}/10!`, 'success');
            // Reload recommendations
            loadPersonalizedRecommendations();
        } else {
            showNotification('Failed to save rating', 'error');
        }
    } catch (error) {
        showNotification('Network error', 'error');
    }
}

async function addToWatchHistory(movieId) {
    try {
        const response = await fetch('/api/watch-history', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ movie_id: movieId })
        });

        if (response.ok) {
            showNotification('Added to watch history!', 'success');
        } else {
            showNotification('Failed to add to history', 'error');
        }
    } catch (error) {
        showNotification('Network error', 'error');
    }
}

// Recommendations
async function loadPersonalizedRecommendations() {
    const container = document.getElementById('recommendationsContainer');
    container.innerHTML = '<div class="spinner"></div>';

    try {
        const response = await fetch('/api/recommendations');
        const data = await response.json();

        if (response.ok) {
            displayMovies(data.recommendations, container);
        } else {
            container.innerHTML = '<p class="text-center text-danger">Failed to load recommendations</p>';
        }
    } catch (error) {
        container.innerHTML = '<p class="text-center text-danger">Network error</p>';
    }
}

// Trending
async function loadTrending(days) {
    const container = document.getElementById('trendingMovies');
    container.innerHTML = '<div class="spinner"></div>';

    // Update active filter button
    document.querySelectorAll('.trending-filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.closest('.trending-filter-btn').classList.add('active');

    try {
        const response = await fetch(`/api/recommendations/trending?days=${days}`);
        const data = await response.json();

        if (response.ok) {
            displayTrendingMovies(data.trending, container);
        } else {
            container.innerHTML = '<p class="text-center text-danger">Failed to load trending movies</p>';
        }
    } catch (error) {
        container.innerHTML = '<p class="text-center text-danger">Network error</p>';
    }
}

function displayTrendingMovies(movies, container) {
    if (!movies || movies.length === 0) {
        container.innerHTML = '<p class="text-center text-gray-400">No trending movies found</p>';
        return;
    }

    // Filter out movies without valid poster URLs
    const validMovies = movies.filter(movie =>
        movie.poster_url &&
        movie.poster_url.trim() !== '' &&
        movie.poster_url.startsWith('http')
    );

    if (validMovies.length === 0) {
        container.innerHTML = '<p class="text-center text-gray-400">No trending movies with posters found</p>';
        return;
    }

    let html = '';

    validMovies.forEach((movie, index) => {
        html += createTrendingMovieCard(movie, index + 1);
    });

    container.innerHTML = html;
}

function createTrendingMovieCard(movie, rank) {
    // Only use valid HTTP poster URLs - NO PLACEHOLDERS
    const posterUrl = movie.poster_url && movie.poster_url.startsWith('http') ? movie.poster_url : '';

    // Skip movies without valid posters
    if (!posterUrl) {
        return '';
    }

    const rating = movie.avg_rating ? movie.avg_rating.toFixed(1) : 'N/A';

    return `
        <div class="movie-card" onclick="showMovieDetails(${movie.id})" data-aos="fade-up" data-aos-delay="${Math.min(rank * 50, 500)}">
            <div class="trending-rank">#${rank}</div>
            <div class="movie-poster-container">
                <img src="${posterUrl}" alt="${movie.title}" class="movie-poster" 
                     onerror="this.parentElement.parentElement.style.display='none';"
                     loading="lazy">
                <div class="movie-overlay">
                    <i class="fas fa-play-circle"></i>
                </div>
            </div>
            <div class="movie-info">
                <div class="movie-title">${movie.title}</div>
                <div class="movie-meta">
                    <span class="rating">
                        <i class="fas fa-star"></i>
                        ${rating}
                    </span>
                    <span>${movie.release_date ? new Date(movie.release_date).getFullYear() : 'N/A'}</span>
                </div>
            </div>
        </div>
    `;
}

// Search
async function searchMovies() {
    const query = document.getElementById('searchInput').value.trim();

    if (!query) {
        showNotification('Please enter a search term', 'warning');
        return;
    }

    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();

        if (response.ok) {
            const container = document.getElementById('recommendationsContainer');
            displayMovies(data.results, container, `Search results for "${query}"`);
            scrollToSection('recommendations');
        } else {
            showNotification('Search failed', 'error');
        }
    } catch (error) {
        showNotification('Network error', 'error');
    }
}

// Preferences
function showPreferences() {
    loadPreferencesForm();
    preferencesModal.show();
}

function loadPreferencesForm() {
    const genres = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary',
        'Drama', 'Family', 'Fantasy', 'Horror', 'Mystery', 'Romance',
        'Sci-Fi', 'Thriller', 'War', 'Western'];

    const languages = ['English', 'Spanish', 'French', 'German', 'Italian', 'Japanese',
        'Korean', 'Chinese', 'Hindi', 'Arabic'];

    const genreContainer = document.getElementById('genreCheckboxes');
    const languageContainer = document.getElementById('languageCheckboxes');

    genreContainer.innerHTML = genres.map(genre => `
        <div>
            <input type="checkbox" class="tag-checkbox" id="genre-${genre}" value="${genre}">
            <label class="tag-label" for="genre-${genre}">${genre}</label>
        </div>
    `).join('');

    languageContainer.innerHTML = languages.map(lang => `
        <div>
            <input type="checkbox" class="tag-checkbox" id="lang-${lang}" value="${lang}">
            <label class="tag-label" for="lang-${lang}">${lang}</label>
        </div>
    `).join('');

    // Load existing preferences
    loadExistingPreferences();

    // Setup form submission
    document.getElementById('preferencesForm').onsubmit = savePreferences;
}

async function loadExistingPreferences() {
    try {
        const response = await fetch('/api/preferences');
        if (response.ok) {
            const prefs = await response.json();

            if (prefs.favorite_genres) {
                prefs.favorite_genres.forEach(genre => {
                    const checkbox = document.getElementById(`genre-${genre}`);
                    if (checkbox) checkbox.checked = true;
                });
            }

            if (prefs.preferred_languages) {
                prefs.preferred_languages.forEach(lang => {
                    const checkbox = document.getElementById(`lang-${lang}`);
                    if (checkbox) checkbox.checked = true;
                });
            }
        }
    } catch (error) {
        console.error('Failed to load preferences');
    }
}

async function savePreferences(e) {
    e.preventDefault();

    const selectedGenres = Array.from(document.querySelectorAll('#genreCheckboxes input:checked'))
        .map(cb => cb.value);

    const selectedLanguages = Array.from(document.querySelectorAll('#languageCheckboxes input:checked'))
        .map(cb => cb.value);

    try {
        const response = await fetch('/api/preferences', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                genres: selectedGenres,
                languages: selectedLanguages
            })
        });

        if (response.ok) {
            showNotification('Preferences saved!', 'success');
            preferencesModal.hide();
            loadPersonalizedRecommendations();
        } else {
            showNotification('Failed to save preferences', 'error');
        }
    } catch (error) {
        showNotification('Network error', 'error');
    }
}

// Utility Functions
function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function scrollToElement(element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function showNotification(message, type = 'info') {
    // Create modern toast notification
    const toast = document.createElement('div');
    const colors = {
        success: { bg: 'rgba(16, 185, 129, 0.15)', border: '#10b981', icon: 'check-circle' },
        error: { bg: 'rgba(239, 68, 68, 0.15)', border: '#ef4444', icon: 'exclamation-circle' },
        warning: { bg: 'rgba(251, 191, 36, 0.15)', border: '#fbbf24', icon: 'exclamation-triangle' },
        info: { bg: 'rgba(102, 126, 234, 0.15)', border: '#667eea', icon: 'info-circle' }
    };

    const color = colors[type] || colors.info;

    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        background: ${color.bg};
        backdrop-filter: blur(10px);
        border: 1px solid ${color.border};
        border-left: 4px solid ${color.border};
        border-radius: 12px;
        padding: 1rem 1.5rem;
        min-width: 300px;
        max-width: 400px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        animation: slideIn 0.3s ease-out;
    `;

    toast.innerHTML = `
        <div style="display: flex; align-items: center; gap: 12px;">
            <i class="fas fa-${color.icon}" style="color: ${color.border}; font-size: 1.25rem;"></i>
            <span style="color: var(--text-primary); font-weight: 500; flex: 1;">${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" style="background: none; border: none; color: var(--text-secondary); cursor: pointer; font-size: 1.25rem; padding: 0; line-height: 1;">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;

    // Add animation keyframes if not already added
    if (!document.getElementById('toast-animations')) {
        const style = document.createElement('style');
        style.id = 'toast-animations';
        style.textContent = `
            @keyframes slideIn {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(400px);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function showWatchHistory() {
    showNotification('Watch history feature coming soon!', 'info');
}


// Generate backdrop placeholder
function generateBackdropPlaceholder(title) {
    const gradients = [
        'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
        'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
        'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
        'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
        'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
        'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)',
        'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
        'linear-gradient(135deg, #ff6e7f 0%, #bfe9ff 100%)'
    ];

    const index = Math.abs(title.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)) % gradients.length;
    const gradient = gradients[index];

    const svg = `
        <svg width="1200" height="400" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="backdropGrad${index}" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:${gradient.match(/#[0-9a-f]{6}/gi)[0]};stop-opacity:1" />
                    <stop offset="100%" style="stop-color:${gradient.match(/#[0-9a-f]{6}/gi)[1]};stop-opacity:1" />
                </linearGradient>
            </defs>
            <rect width="1200" height="400" fill="url(#backdropGrad${index})"/>
            <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="48" font-weight="bold" 
                  fill="white" text-anchor="middle" dominant-baseline="middle" opacity="0.7">
                ${title}
            </text>
        </svg>
    `;

    return 'data:image/svg+xml;base64,' + btoa(svg);
}
