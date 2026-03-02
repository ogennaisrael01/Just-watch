# just-watch Project — Detailed Summary

## Overview

**just-watch** is a FastAPI-based backend application for a movie platform. It allows users to search movies, maintain watchlists, rate content, and receive personalized recommendations. The system manages user authentication, messaging between users and AI, and integrates caching and rate limiting for performance and API protection.

---

## What It Does

1. **User Management** — Registration, authentication (JWT via SimpleJWT), profile management.
2. **Movie Operations** — Browse, search, and filter movies by title.
3. **Watchlist Management** — Users can add/remove movies to personal watch-lists, track viewing progress.
4. **Ratings & Reviews** — Users rate movies on a scale; ratings are stored and can influence recommendations.
5. **Messaging** — Direct messaging between user and AI
6. **Activity Based Recommendations** — Personalized movie recommendations based on user in app activity.
7. **Performance Optimization** — In-memory caching by default; rate limiting to prevent abuse.

---

## Core Features

### Authentication & User Roles
- Custom User model
- JWT token-based auth (JWT) 


### Movie Management
- **MovieSearch** — Search/filter movies by title, 
- **WatchList** — Track movies a user is watching or plans to watch
- **Rate** — User ratings for movies (1–10 scale or similar)


### Caching & Performance
- **FastAPICache** with InMemoryBackend (initialized in app lifespan)
- Decorators to cache endpoint responses (e.g., movie lists, recommendations)
- Configurable TTL per endpoint

### Rate Limiting
- **slowapi** Limiter integrated as middleware
- Default: 10 requests/minute (configurable per route)
- Tracks requests by remote IP address

### CORS & Security
- CORS middleware allows cross-origin requests (all origins in dev; restrict in production)
- SlowAPI middleware for rate limiting enforcement

---

## Project Structure

```
src/
├── manage.py                          # FastAPI app definition (main entry point)
├── config/
│   └── database/
│       └── base.py                    # SQLAlchemy DeclarativeBase & engine config
├── apps/
│   ├── users/
│   │   ├── models/
│   │   │   ├── auth_models.py         # User model (imported in manage.py)
│   │   │   └── message_model.py       # Message model (imported in manage.py)
│   │   ├── routes/                    # User endpoints (auth, profile, messaging)
│   │   └── services/                  # Business logic, JWT helpers
│   └── movies/
│       ├── models/
│       │   └── movie_model.py         # MovieSearch, WatchList, Rate models
│       ├── routes/                    # Movie endpoints (search, watchlist, ratings)
│       └── services/                  # Recommendation logic, filtering
└── pyproject.toml                   # Python dependencies
```

---

## External Libraries & Dependencies

### Core Web Framework
| Package | Purpose |
|---------|---------|
| **FastAPI** | Modern async web framework; auto-generates OpenAPI docs |
| **Uvicorn** | ASGI server to run FastAPI app |

### Database & ORM
| Package | Purpose |
|---------|---------|
| **SQLAlchemy** | ORM for database operations |
| **psycopg2-binary** | PostgreSQL adapter |
| **alembic** | Database migrations  |

### Authentication & Security
| Package | Purpose |
|---------|---------|
| **python-jose** | JWT token generation/validation |
| **passlib** | Password hashing (bcrypt backend ) |
| **python-multipart** | Form data parsing |

### Caching
| Package | Purpose |
|---------|---------|
| **fastapi-cache2** | Caching layer with multiple backends (in-memory.) |

### Rate Limiting
| Package | Purpose |
|---------|---------|
| **slowapi** | Rate limiting middleware |

### Middleware & CORS
| Package | Purpose |
|---------|---------|
| **fastapi.middleware.cors** | Built into FastAPI for cross-origin support |

### AI
| Package | Purpose                                |
|---------|----------------------------------------|
| **google-genai** | Google Gemini API for AI-powered chats |


## Key Workflows

### 1. User Registration & Login
```
User Registration Flow:
  ├─ User sends email, password → POST /auth/register
  ├─ User logs in → POST /auth/login
  └─ JWT tokens issued (access + refresh)

Subsequent Requests:
  └─ Bearer token included in Authorization header
```

### 2. Movie Search & Watchlist
```
Movie Discovery Flow:
  ├─ User searches movies → GET /movies/search?q=spider-man
  ├─ Results filtered 
  ├─ Response cached for performance
  ├─ User adds movie to watchlist → POST /watch-list/
  ├─ Watchlist persists in database
  └─ User fetches watchlist → GET /watch-list
```

### 3. Ratings & Recommendations
```
Recommendation Flow:
  ├─ User rates a movie → POST /movies/{movie_id}/rate {score: 4}
  ├─ Rating stored in database
  ├─ AI engine analyzes user interests + ratings
  ├─ Personalized recommendations generated
  └─ Recommendations returned → GET /recommendations-for_user
```

## Performance & Scalability

### Caching Strategy
- **In-Memory** (default) — Fast for single-instance deployments

### Database Optimization
- UUID primary keys for scalability
- Indexed columns for common queries
- Connection pooling via SQLAlchemy

### Rate Limiting
- Per-IP tracking (default 10 requests/minute)
- Customizable per route
- Can extend to per-user limits if needed

### Async Design
- All I/O operations are non-blocking
- FastAPI handles concurrent requests efficiently

---

## Quick Start (Windows)

### Prerequisites
- Python 3.10 or higher
- Git
- PostgreSQL (or use SQLite for development)
- (Optional) Docker for Redis/PostgreSQL

### Setup Steps

1. **Clone the repository**
   ```powershell
   git clone <repo-url> just-watch
   cd just-watch
   ```

2. **Create and activate virtual environment**
   ```powershell
   uv venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   uv sync
   ```

4. **Create `.env` file** in project root
    `
     check .env.example
5. `

5. **Initialize database** (if using migrations)
   ```powershell
   alembic upgrade head
   ```

7. **Run development server**
   ```powershell
   python -m uvicorn src.manage:app --reload --host 0.0.0.0 --port 8000
   ```

8. **Access the application**
   - API Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - API Root: http://localhost:8000
   - Live_url: https://just-watch-nu.vercel.app/docs/

---

## Testing

### Run Tests
```powershell
cd src
pytest -v
```

## License

This project is licensed under the MIT License. See `LICENSE` file for details.

---

## Support & Contact

For questions, issues, or contributions, reach out to:

📧 **Email:** ogennaisrael@gmail.com  
📱 **GitHub:** [Check GitHub Profile]

---
