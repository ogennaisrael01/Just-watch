# Just-Watch: Complete Project Documentation

## Project Name

**Just-Watch** — A movie discovery and recommendation platform where users can search for movies, build personal watchlists, rate content, and receive AI-powered personalized recommendations.

---

## Overview

Just-Watch is a backend API service built with FastAPI that powers a modern movie discovery platform. It's designed to solve the problem of movie decision fatigue — helping users discover, organize, and find movies they'll actually want to watch.

The platform allows registered users to search through millions of movies using the TMDB (The Movie Database) API, save movies to personal watchlists, rate movies they've seen, and get intelligent recommendations based on their viewing history and preferences. The system includes an AI chat assistant powered by Google Gemini that can answer questions about movies and help users find what to watch next.

Think of it as having a personal movie librarian with AI intelligence built in. Non-technical users can simply register, search for movies, add them to their watchlist, rate what they watch, and get smart recommendations — all without worrying about the technical details behind the scenes.

---

## Tech Stack

### Core Framework & Server
| Technology | Purpose |
|------------|---------|
| **FastAPI** | Modern, fast async Python web framework that auto-generates interactive API documentation. Chosen for its async support, type validation, and developer experience. |
| **Uvicorn** | ASGI server that runs the FastAPI application. Provides high-performance async request handling. |
| **Python 3.13+** | Programming language foundation for the entire project. |

### Database & ORM
| Technology | Purpose |
|------------|---------|
| **SQLAlchemy 2.0+** | Powerful ORM (Object-Relational Mapper) for database operations. Provides type safety, query building, and relationship management. |
| **PostgreSQL** | Primary production database. Chosen for reliability, performance, and JSONB support. Uses the `psycopg2-binary` and `asyncpg` drivers for async operations. |
| **SQLite** | Lightweight alternative for development/testing using `aiosqlite`. |
| **Alembic** | Database migration tool. Allows version control of database schema changes. Essential for team development and production deployments. |

### Authentication & Security
| Technology | Purpose |
|------------|---------|
| **PyJWT** (python-jose) | Creates and validates JWT (JSON Web Tokens) for stateless authentication. Tokens carry user identity without storing sessions on the server. |
| **Passlib + Bcrypt** | Password hashing library. Bcrypt is a cryptographically strong algorithm that makes password cracking exponentially harder. Passwords are never stored in plaintext. |
| **OAuth2 with Bearer Tokens** | FastAPI's built-in OAuth2 implementation. Users send JWT in the Authorization header with each request. |

### Performance & Caching
| Technology | Purpose |
|------------|---------|
| **FastAPI-Cache2** | In-memory caching layer with InMemoryBackend. Caches expensive API calls (TMDB requests, recommendations) to reduce response time and external API hits. |
| **Redis** | (Optional) Can be configured for distributed caching in multi-instance deployments. Currently uses in-memory backend for single-instance deployment. |

### Rate Limiting
| Technology | Purpose |
|------------|---------|
| **SlowAPI** | Rate limiting middleware based on IP address. Prevents API abuse by limiting requests (default: 10/minute per endpoint). Protects TMDB API quota and server resources. |

### External APIs
| Technology | Purpose |
|------------|---------|
| **TMDB API** (The Movie Database) | Source of all movie data: titles, descriptions, ratings, genres, posters, release dates. Provides comprehensive movie metadata and search functionality. |
| **Google Gemini API** | Powers the AI chat assistant. Enables conversational AI responses about movies and personalized recommendations. |

### Middleware & CORS
| Technology | Purpose |
|------------|---------|
| **CORS Middleware** | Cross-Origin Resource Sharing. Allows the API to be called from web/mobile frontends on different domains. |
| **FastAPI Built-in Middleware** | Request/response logging, exception handling, and standard HTTP middleware. |

### Development & Testing
| Technology | Purpose |
|------------|---------|
| **Pytest** | Testing framework for writing unit and integration tests. Configured with fixtures for database setup and test isolation. |
| **python-multipart** | Parses form data in HTTP requests (used for file uploads if needed). |
| **Requests** | HTTP client library for making calls to external APIs (TMDB, Gemini). |

### Data Validation
| Technology | Purpose |
|------------|---------|
| **Pydantic** | Data validation and serialization. Ensures all request/response data matches expected schemas, with automatic error messages. |
| **Pydantic Settings** | Configuration management. Reads environment variables into typed Python objects. |

---

## System Architecture

### High-Level Architecture Flow

```
Client (Web/Mobile) 
    ↓
FastAPI Application (manage.py)
    ↓
┌─────────────────────────────────────┐
│  Middleware Layer                   │
│  - CORS                             │
│  - Rate Limiting (SlowAPI)          │
│  - Exception Handlers               │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Router Layer (Endpoints)           │
│  - /v1/auth/* (Authentication)      │
│  - /v1/p3/* (Movies)                │
│  - /v1/ai/* (Chat/AI)               │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Service Layer (Business Logic)     │
│  - UserService                      │
│  - MovieService                     │
│  - WatchListService                 │
│  - RatingService                    │
│  - RecommendationService            │
│  - ChatBoxService                   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Data Layer                         │
│  - CRUD Operations                  │
│  - SQLAlchemy ORM                   │
│  - Database Models                  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  External Services                  │
│  - PostgreSQL Database              │
│  - TMDB API                         │
│  - Google Gemini API                │
│  - FastAPI Cache (In-Memory)        │
└─────────────────────────────────────┘
```

### Folder Structure & Responsibilities

```
src/
├── manage.py                    # FastAPI app initialization & configuration
├── main.py                      # Router registration & entry point setup
├── exception_handler.py         # Global exception handling (rate limits, etc)
│
├── config/
│   ├── settings/
│   │   ├── base.py             # Base configuration (SECRET_KEY, DEBUG, API_KEYS)
│   │   ├── dev.py              # Development settings (local DB URL)
│   │   └── prod.py             # Production settings (production DB URL)
│   └── database/
│       ├── base.py             # SQLAlchemy DeclarativeBase (shared ORM base class)
│       └── setup.py            # Database engine & session creation
│
└── apps/
    ├── users/                   # User management module
    │   ├── models/
    │   │   ├── auth_models.py   # User model with relationships
    │   │   └── message_model.py # Message/Chat model (User ↔ AI)
    │   ├── schemas/
    │   │   ├── auth_schemas.py  # Request/response validation (Register, Login, Profile)
    │   │   ├── auth_validator.py # Email & password validation logic
    │   │   └── message_schemas.py # Message validation
    │   ├── services/
    │   │   ├── user_services.py  # Core user operations (create, authenticate, profile)
    │   │   ├── jwt_services.py   # JWT token creation & validation
    │   │   ├── chat_box_services.py # AI chat logic & message persistence
    │   │   ├── security.py       # Token verification & retry decorators
    │   │   ├── helpers.py        # Password hashing, utility functions
    │   │   ├── crud.py           # Database CRUD operations (create/read/update)
    │   │   └── security.py       # Security helpers & retries
    │   ├── exceptions/
    │   │   ├── exceptions.py     # Custom exception classes (UserNotFound, etc)
    │   │   └── exception_handler.py # Exception response formatting
    │   ├── api/
    │   │   └── router/
    │   │       ├── route_v1.py   # Auth routes (register, login, profile)
    │   │       └── chat_box.py   # Chat routes (send msg, list, delete)
    │   └── tests/
    │       └── test_users.py     # User authentication tests
    │
    └── movies/                   # Movie management module
        ├── models/
        │   └── movie_model.py    # MovieSearch, WatchList, Rate models
        ├── schemas/
        │   └── movie_schema.py   # Request/response validation for movies
        ├── services/
        │   ├── movies.py         # Movie search & history operations
        │   ├── watchlist.py      # Watchlist management
        │   ├── ratings.py        # Rating operations
        │   ├── recommedation_service.py # AI recommendation engine
        │   ├── tmdb.py           # TMDB API integration
        │   ├── utils.py          # Utility functions (checks, validators)
        │   └── crud.py           # Database CRUD operations
        ├── exceptions/
        │   └── exceptions.py     # Movie-specific exceptions
        └── api/
            └── routers/
                ├── v1.py         # Movie search & details
                ├── watchlist_v1.py # Watchlist endpoints
                ├── rating_v1.py  # Rating endpoints
                └── recommend_v1.py # Recommendation endpoints
```

### Key Design Patterns

**1. Service Layer Pattern**
- Services encapsulate business logic separate from routes
- Makes logic reusable and testable
- Example: `UserService.authenticate_user()` is called by the login route

**2. CRUD Separation**
- Dedicated `crud.py` files handle all database operations
- Services call CRUD functions, keeping business logic separate
- Makes database queries centralized and easy to modify

**3. Schema Validation (Pydantic)**
- All inputs validated against Pydantic schemas before processing
- Invalid requests rejected with clear error messages
- Type safety throughout the application

**4. Dependency Injection (FastAPI Depends)**
- Current user, database session injected into routes via `Depends()`
- Makes testing easier and reduces boilerplate
- Promotes loose coupling between components

**5. Async/Await Throughout**
- All I/O operations (database, APIs) are async
- Allows the single-threaded event loop to handle many concurrent requests
- Better resource utilization and responsiveness

---

## Core Features

### 1. User Authentication & Registration

**What it does:** Users create accounts with email, password, username, and optional name fields. Users log in with email and password to receive JWT tokens for subsequent requests.

**How it works:**
1. User submits registration with email, username, password, confirm_password
2. Email format & password strength validated (via Pydantic)
3. Password hashed with bcrypt (one-way encryption, cannot be reversed)
4. User record created in database with hashed password
5. User automatically logged in, receiving access and refresh JWT tokens
6. Tokens include user ID and email, signed with SECRET_KEY
7. Tokens sent back to client and stored locally

**Who uses it:** All users must authenticate before accessing protected endpoints (watchlist, ratings, recommendations, chat).

**Rate limiting:** 5 requests/minute on register/login to prevent brute force attacks

---

### 2. Movie Search & Browse

**What it does:** Users search for movies by title, browse popular movies, and view movie details (description, ratings, genres, poster, reviews).

**How it works:**
1. User sends search query (e.g., "spider-man") to `/v1/p3/search/movie?query=spider-man`
2. Request forwarded to TMDB API with user's query
3. TMDB returns paginated list of matching movies
4. Response cached for 6 hours to avoid repeated TMDB calls
5. When user views movie details, movie is auto-saved to their search history
6. Users can clear their search history

**Who uses it:** Authenticated users only. Movie search integrates with watchlist (add movie to watch) and ratings (rate what you watched).

**Features:**
- Pagination support (adjust page number)
- Flexible append parameters (get credits, recommendations, similar movies in one call)
- Caching reduces load on TMDB (rate limit: 10 requests/minute)
- Search history tracking (what user searched previously)

---

### 3. Watchlist Management

**What it does:** Users maintain a personal list of movies they want to watch or are currently watching.

**How it works:**
1. User clicks "Add to Watchlist" on any movie
2. System checks if movie already in watchlist (prevent duplicates)
3. Movie added to `watchlist` table with timestamp
4. If not already viewed, movie added to search history
5. User can view all watchlisted movies (GET `/v1/p3/watch-list/`)
6. User can remove individual movies or bulk delete watchlist

**Who uses it:** Authenticated users. Each user has separate watchlist stored in database.

**Relationships:**
- Watchlist ← User (foreign key relationship)
- Watchlist ← Movie (by movie_id from TMDB)
- Cascading delete: If user deleted, watchlist deleted automatically

---

### 4. Movie Ratings & Reviews

**What it does:** Users rate movies on a 1-10 scale. Ratings are stored and used to power personalized recommendations.

**How it works:**
1. User submits rating (1-10 score) for a movie via POST `/v1/p3/movie/{movie_id}/rate`
2. System validates score is between 1-10 (via Pydantic validator)
3. Prevents duplicate ratings (can't rate same movie twice)
4. Rating stored in database linked to user and movie
5. User can update rating later (PATCH) with new score
6. User can view all their ratings
7. Users can delete specific ratings

**Who uses it:** Authenticated users. Ratings are personalized per user.

**Usage in recommendations:** Recommendation engine analyzes user's rated movies to find genres they prefer, then recommends similar movies.

---

### 5. Personalized Recommendations

**What it does:** AI-powered recommendation engine suggests movies based on user's rating history and browsing behavior.

**How it works:**
1. System analyzes user's last 20 movies in search history
2. Extracts all genres from those movies
3. Weights genres by frequency (movies with same genre seen multiple times = stronger preference)
4. Filters genres with strength ≥ 10 (minimum threshold to qualify)
5. Queries TMDB's discover API for movies in those genres, sorted by popularity
6. Results cached for 1 hour
7. Recommendations include movies user likely hasn't rated yet

**Who uses it:** Authenticated users only. Recommendations are personalized per user.

**Example:** If user watched 3 sci-fi, 2 action, 5 thriller movies, system recommends more thrillers (weight=5) and sci-fi (weight=3).

**Second feature:** Similar movies - Given a specific movie ID, returns visually/narratively similar movies via TMDB.

---

### 6. AI Chat Assistant

**What it does:** Users can chat with an AI assistant powered by Google Gemini about movies, get recommendations, ask questions, and maintain conversation history.

**How it works:**
1. User sends message via POST `/v1/ai/chat-box/`
2. System retrieves user's previous chat history from database
3. Chat history formatted and sent to Google Gemini API with new message
4. Gemini responds with conversational answer about movies/recommendations
5. User message saved to database with role="USER"
6. AI response saved to database with role="AI"
7. User can view full chat history (GET `/v1/ai/chat-box/chats/`)
8. User can delete individual messages or entire chat history

**Who uses it:** Authenticated users only. Each user has isolated chat history.

**Features:**
- Conversational context (AI remembers previous messages in same conversation)
- Rate limiting: 5 messages/hour (prevents API quota abuse)
- Retry mechanism: Auto-retries failed API calls up to 5 times
- Message persistence: All messages stored in database for audit trail

---

### 7. Search History Tracking

**What it does:** System automatically tracks all movies users view (search for, add to watchlist, rate, get details).

**How it works:**
1. Every time user views movie details, system auto-saves to search history
2. System prevents duplicate histories (same user + movie = one record)
3. User can view their search history (GET `/v1/p3/history/`)
4. User can delete individual search history entries
5. Search history used to power recommendations

**Who uses it:** Tracked automatically for authenticated users.

**Why it matters:** Provides insights into user behavior and powers the AI recommendation engine.

---

## API Overview

### Authentication Endpoints

**POST** `/v1/auth/register/`
- **Purpose:** Register new user account
- **Input:** email, username, password, confirm_password, first_name, last_name
- **Output:** Registration success message + JWT tokens
- **Rate limit:** 5/minute
- **Auth required:** No

**POST** `/v1/auth/login/`
- **Purpose:** Authenticate user and get JWT tokens
- **Input:** email, password
- **Output:** JWT access token, refresh token, token type
- **Rate limit:** 5/minute
- **Auth required:** No

**GET** `/v1/auth/user-me/`
- **Purpose:** Fetch current authenticated user's profile
- **Output:** user_id, email, username, first/last name, created_at, updated_at
- **Cache:** 10 minutes
- **Rate limit:** 10/minute
- **Auth required:** Yes (JWT token)

**PATCH** `/v1/auth/user-me/`
- **Purpose:** Update user profile (username, name)
- **Input:** username (optional), first_name, last_name
- **Output:** Updated profile
- **Rate limit:** 10/minute
- **Auth required:** Yes
- **Restrictions:** Email cannot be updated

---

### Movie Endpoints

**GET** `/v1/p3/movie`
- **Purpose:** List popular movies from TMDB
- **Query params:** page (integer)
- **Output:** Paginated list of movies with title, rating, release date, poster
- **Cache:** 3 hours
- **Rate limit:** 10/minute
- **Auth required:** No (public)

**GET** `/v1/p3/search/movie`
- **Purpose:** Search movies by title
- **Query params:** query (search string), page (integer)
- **Output:** Paginated search results
- **Cache:** 6 hours
- **Rate limit:** 10/minute
- **Auth required:** No (public)

**GET** `/v1/p3/movie/{movie_id}`
- **Purpose:** Get detailed information for specific movie
- **Path params:** movie_id (integer)
- **Query params:** append (optional list of additional data: videos, credits, recommendations, similar)
- **Output:** Full movie details (description, runtime, budget, revenue, reviews, etc.)
- **Side effect:** Auto-saves movie to user's search history
- **Cache:** 6 hours
- **Rate limit:** 10/minute
- **Auth required:** Yes

**DELETE** `/v1/p3/movie/{movie_id}`
- **Purpose:** Delete movie from search history
- **Path params:** movie_id
- **Output:** Number of deleted rows
- **Rate limit:** 10/minute
- **Auth required:** Yes

**GET** `/v1/p3/history/`
- **Purpose:** Fetch user's search history
- **Output:** List of movies user has viewed with timestamps
- **Cache:** 5 minutes
- **Rate limit:** 10/minute
- **Auth required:** Yes

---

### Watchlist Endpoints

**POST** `/v1/p3/watch-list/`
- **Purpose:** Add movie to watchlist
- **Query params:** movie_id (integer)
- **Output:** Movie details
- **Side effect:** Prevents duplicates, auto-saves to search history if not already there
- **Rate limit:** 10/minute
- **Auth required:** Yes

**GET** `/v1/p3/watch-list/`
- **Purpose:** Retrieve all movies in user's watchlist
- **Output:** Array of watchlist items with movie details, added_at timestamp
- **Cache:** 20 minutes
- **Rate limit:** 10/minute
- **Auth required:** Yes

**GET** `/v1/p3/watch-list/{movie_id}`
- **Purpose:** Get specific watchlist item
- **Path params:** movie_id
- **Output:** Single watchlist item details
- **Cache:** 3 hours
- **Rate limit:** 10/minute
- **Auth required:** Yes

**DELETE** `/v1/p3/watch-list/` or **DELETE** `/v1/p3/watch-list/{movie_id}`
- **Purpose:** Delete from watchlist
- **Query params (for bulk delete):** email (required to confirm identity)
- **Path params (for single delete):** movie_id (optional)
- **Output:** Number of deleted rows
- **Rate limit:** 10/minute
- **Auth required:** Yes
- **Restrictions:** Can only delete own watchlist (email verification)

---

### Rating Endpoints

**POST** `/v1/p3/movie/{movie_id}/rate`
- **Purpose:** Rate a movie
- **Path params:** movie_id
- **Input:** score (1-10 integer, required)
- **Output:** Movie details (confirmation)
- **Validations:** Score must be 1-10, prevents duplicate ratings
- **Rate limit:** 10/minute
- **Auth required:** Yes

**GET** `/v1/p3/movie-ratings/`
- **Purpose:** Retrieve all user's ratings
- **Output:** Array of ratings with score and movie_id
- **Cache:** 1 hour
- **Rate limit:** 10/minute
- **Auth required:** Yes

**PATCH** `/v1/p3/movie/{movie_id}/rate`
- **Purpose:** Update rating for a movie
- **Path params:** movie_id
- **Input:** score (1-10)
- **Output:** Updated rating
- **Rate limit:** 10/minute
- **Auth required:** Yes
- **Restrictions:** Can only update existing ratings

---

### Recommendation Endpoints

**GET** `/v1/p3/recommendations-for_you/`
- **Purpose:** Get personalized recommendations for authenticated user
- **Query params:** page (integer for pagination)
- **Output:** Paginated list of recommended movies
- **Algorithm:** Based on user's rating history and browse behavior
- **Cache:** 1 hour
- **Rate limit:** 10/minute
- **Auth required:** Yes

**GET** `/v1/p3/movie/{movie_id}/recommendations`
- **Purpose:** Get movies similar to specified movie
- **Path params:** movie_id
- **Query params:** page (optional)
- **Output:** Similar movies from TMDB
- **Cache:** 1 hour
- **Rate limit:** 10/minute
- **Auth required:** No (public)

---

### Chat/AI Endpoints

**POST** `/v1/ai/chat-box/`
- **Purpose:** Send message to AI assistant
- **Input:** message (string)
- **Output:** AI response with generated recommendation or answer
- **Features:** Maintains conversation context using chat history
- **Rate limit:** 5/hour (strict limit due to API costs)
- **Auth required:** Yes
- **Retry logic:** Auto-retries on API failure up to 5 times

**GET** `/v1/ai/chat-box/chats/`
- **Purpose:** Retrieve user's chat history
- **Output:** Array of messages with user_role (USER or AI) and timestamp
- **Cache:** 5 minutes
- **Rate limit:** 10/minute
- **Auth required:** Yes

**DELETE** `/v1/ai/chat-box/chats/`
- **Purpose:** Delete chat message(s)
- **Query params:** message_id (optional - if not provided, clears entire history)
- **Output:** Number of deleted rows
- **Rate limit:** 10/minute
- **Auth required:** Yes

---

### Health Check

**GET** `/health`
- **Purpose:** Check if API is running
- **Output:** "OK" response
- **Rate limit:** 2/minute
- **Auth required:** No
- **Use case:** Load balancers, monitoring services use this to verify uptime

---

## Authentication & Security

### How Authentication Works

Just-Watch uses **JWT (JSON Web Token)** based authentication:

1. **Token Creation (on login):**
   - User provides email and password
   - System finds user by email, verifies password against stored hash using bcrypt
   - If valid, creates JWT containing: `{sub: user_id, email: user_email}`
   - JWT is signed with SECRET_KEY using HS256 algorithm
   - Two tokens returned: access_token (short-lived, 15 min), refresh_token (long-lived)
   - Tokens sent to client as JSON

2. **Token Storage (client-side):**
   - Frontend stores access_token in memory or secure storage
   - Refresh_token stored in httpOnly cookie (if using web frontend)

3. **Token Usage (on every request):**
   - Client includes token in Authorization header: `Authorization: Bearer {access_token}`
   - FastAPI's OAuth2PasswordBearer automatically extracts token from header

4. **Token Validation (on protected endpoints):**
   - Uvicorn receives request with Bearer token
   - `JWTService.decode_jwt_token()` called to verify:
     - Token signature is valid (signed with SECRET_KEY)
     - Token hasn't expired (expires in 15 minutes by default)
     - Token contains required sub (user_id) and email claims
   - If valid, user_id extracted and user fetched from database
   - If invalid/expired, 401 Unauthorized response returned
   - User object passed to route handler via dependency injection

5. **Token Refresh:**
   - When access_token expires, client uses refresh_token to get new access_token
   - Prevents user being logged out during long sessions

### Route Protection

Routes are protected using FastAPI's dependency injection pattern:

```python
@router.get("/protected-endpoint/")
async def protected(current_user: User = Depends(UserService.get_current_user)):
    # current_user automatically injected only if token valid
    # If token missing/invalid, request never reaches this function
    return {"user": current_user.username}
```

**Protected endpoints** require valid JWT in Authorization header. **Public endpoints** don't use the `get_current_user` dependency.

### Password Security

**Passwords are hashed with bcrypt:**
- One-way hash: Original password cannot be recovered from hash
- Salted: Each hash unique even if passwords are identical
- Slow: Takes ~0.1 seconds to hash/verify (prevents rapid brute-force)
- Validated on registration: Must be 3-50 characters with complexity requirements

**In database:** Only hash stored, never plaintext password

### Rate Limiting

Implemented via SlowAPI middleware:

```
IP Address → Tracked by address → 10 requests/minute (global default)
```

**Per-endpoint configuration:**
- Register/Login: 5/minute (prevent brute force)
- Chat: 5/hour (prevent expensive API calls)
- General endpoints: 10/minute

**How it works:**
1. SlowAPI tracks requests by IP address
2. Increments counter when request received
3. If counter exceeds limit, returns 429 Too Many Requests
4. Counter resets after time window expires

### CORS (Cross-Origin Resource Sharing)

Configured to allow requests from any origin (development mode). In production, should restrict to specific frontend domains:

```
Current: allow_origins=["*"]  # Allow all origins
Recommended production: allow_origins=["https://just-watch.com"]
```

### Other Security Measures

**SQL Injection Prevention:** SQLAlchemy ORM uses parameterized queries automatically (not vulnerable to SQL injection)

**Request Validation:** Pydantic validates all inputs:
- Email format checked (must be valid email)
- Password strength enforced
- Type validation (integers must be integers, not strings)
- Extra fields rejected

**Exception Handling:** Errors don't expose internal details:
- Generic 400/404/500 messages to clients
- Detailed error logs on server side only

---

## Database Design

### Data Models & Relationships

**User Model**
```python
user_id (UUID)          [Primary Key] - Unique identifier
email (String)          [Unique] - Required, indexed for quick lookup
username (String)       [Unique] - Required, indexed
first_name (String)     - Optional
last_name (String)      - Optional
password (Bytes)        - Bcrypt hash, binary stored
created_at (DateTime)   - Auto-set to current time
updated_at (DateTime)   - Auto-updated on changes

Relationships:
  ↓ movies_search (1-to-many) → MovieSearch.owner_id
  ↓ watchlist (1-to-many)     → WatchList.owner_id
  ↓ ratings (1-to-many)       → Rate.owner_id
  ↓ messages (1-to-many)      → Message.user_id
```

**MovieSearch Model (Search History)**
```python
movie_id (Integer)      [Primary Key] - TMDB movie ID
movie_title (String)    - Title of movie, indexed
owner_id (UUID)         [Foreign Key] → User.user_id, indexed
release_date (String)   - Release date, indexed
genre_ids (Array(Int))  - List of genre IDs, indexed
poster_path (String)    - URL to movie poster image
saved_at (DateTime)     - When user viewed this movie

Constraints:
  - Unique: movie_id
  - Foreign key: owner_id references User
  - Cascading delete: When user deleted, all their search history deleted
```

**WatchList Model**
```python
watchlist_id (UUID)     [Primary Key] - Unique watchlist entry ID
movie_id (Integer)      - TMDB movie ID, unique per user
owner_id (UUID)         [Foreign Key] → User.user_id, indexed
added_at (DateTime)     - When added to watchlist

Constraints:
  - movie_id must be unique (user can't watchlist same movie twice)
  - Foreign key: owner_id references User
  - Cascading delete: When user deleted, watchlist deleted
```

**Rate Model (Movie Ratings)**
```python
rating_id (UUID)        [Primary Key] - Unique rating ID
movie_id (Integer)      - TMDB movie ID, unique per user
owner_id (UUID)         [Foreign Key] → User.user_id, indexed
score (Integer)         - Rating 1-10, validated in code
created_at (DateTime)   - When rated

Constraints:
  - movie_id must be unique (user can't rate same movie twice)
  - score must be 1-10 (enforced by SQLAlchemy validator)
  - Foreign key: owner_id references User
  - Cascading delete: When user deleted, ratings deleted
```

**Message Model (Chat History)**
```python
message_id (UUID)       [Primary Key] - Unique message ID
user_id (UUID)          [Foreign Key] → User.user_id
user_role (String)      - Either "USER" or "AI", indexed
message (String)        - The message content
created_at (DateTime)   - When message was sent
updated_at (DateTime)   - When message was last updated

Constraints:
  - Foreign key: user_id references User
  - user_role can only be "USER" or "AI"
  - Cascading delete: When user deleted, all messages deleted
```

### Database Schema Decisions

**Why UUIDs for User IDs?**
- Scalability: Can generate IDs without central authority (unlike auto-increment)
- Privacy: Don't leak user count via sequential IDs
- Distribution: Works well in microservices and sharded databases

**Why Movie ID from TMDB, not UUID?**
- TMDB is source of truth for movies
- Easier to reference external data
- Reduces storage (integer smaller than UUID)

**Why Cascading Delete?**
- When user deleted, automatically clean up their data
- Prevents orphaned records (watchlist items with no user)
- Maintains referential integrity

**Why Indexed Fields?**
- email, username: Frequently searched for (login, registration)
- owner_id: Frequent filtering (user's watchlist, user's ratings)
- movie_id: Checking if movie already exists in user's data
- release_date, genre_ids: Used in search/filter queries
- user_role: Used in chat history filtering

### Relationships Diagram

```
┌─────────────────────┐
│       User          │
├─────────────────────┤
│ user_id (PK, UUID)  │
│ email (unique)      │
│ username (unique)   │
│ password (hash)     │
└──────────┬──────────┘
           │
           │ (1-to-many)
           ├──────────────────────┐
           │                      │
        owns              owns    owns      owns
           │                      │         │      │
    ┌──────▼────────┐    ┌──────▼────┐ ┌──▼──┐ ┌▼────────┐
    │ MovieSearch   │    │ WatchList  │ │Rate │ │ Message │
    ├───────────────┤    ├────────────┤ ├─────┤ ├─────────┤
    │ movie_id(PK)  │    │watchlist_id│ │id   │ │ msg_id  │
    │ owner_id(FK)  │    │ owner_id   │ │owner│ │ user_id │
    └───────────────┘    └────────────┘ └─────┘ └─────────┘
     (search history)     (watchlist)    (rating) (chat)
```

---

## Getting Started

### Prerequisites

Before you can run Just-Watch locally, ensure you have:

1. **Python 3.13 or higher**
   - Download from https://www.python.org/downloads/
   - Verify: `python --version`

2. **Git**
   - Download from https://git-scm.com/
   - Verify: `git --version`

3. **PostgreSQL 12+** (for production) or **SQLite** (for development)
   - PostgreSQL: https://www.postgresql.org/download/
   - SQLite comes built into Python

4. **API Keys:**
   - **TMDB API Key:** Register free at https://www.themoviedb.org/settings/api
   - **Google Gemini API Key:** Get from https://aistudio.google.com/app/apikey
   - **JWT Secret Key:** Any random string (generate: `python -c "import secrets; print(secrets.token_hex(32))"`)

5. **UV Package Manager** (recommended but optional)
   - Download from https://github.com/astral-sh/uv
   - Or use `pip` if you prefer

### Installation Steps

#### Step 1: Clone the Repository

```powershell
# Navigate to where you want the project
cd C:\Users\YourName\Projects

# Clone the repository
git clone <repository-url>
cd just-watch
```

#### Step 2: Create Virtual Environment

**Option A: Using UV (Recommended)**
```powershell
uv venv
.\.venv\Scripts\Activate.ps1
```

**Option B: Using Python's venv**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

After activation, your prompt should show `(.venv)` prefix.

#### Step 3: Install Dependencies

```powershell
# If using UV:
uv sync

# If using pip:
pip install -r requirements.txt
# or for pyproject.toml projects:
pip install -e .
```

This installs all required packages:
- fastapi, uvicorn (web framework)
- sqlalchemy, asyncpg (database)
- pydantic (validation)
- python-jose, passlib (authentication)
- google-genai (AI)
- slowapi (rate limiting)
- pytest (testing)
- And all dependencies...

#### Step 4: Create Environment Variables File

Create a `.env` file in the project root with:

```env
# Application Settings
DEBUG=true
SECRET_KEY=your-random-secret-key-here-at-least-32-characters
ALGORITHM=HS256
EXPIRES_IN=15
REFRESH_LIFESPAN=1

# Database Configuration (Choose one)
# For PostgreSQL (production):
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/justwatch

# OR for SQLite (development):
DATABASE_URL=sqlite+aiosqlite:///./database.db

# TMDB API Configuration
TMDB_API_KEY=your-tmdb-api-key-here
BASE_URL=https://api.themoviedb.org/3/

# Google Gemini AI Configuration
GEMINI_MODEL=gemini-2.0-flash
GEMINI_API_KEY=your-google-gemini-api-key-here

# Alembic Migration URL (same as DATABASE_URL but for migrations)
ALEMBIC_URL=postgresql://username:password@localhost:5432/justwatch
```

**Getting the API Keys:**

1. **TMDB API Key:**
   - Go to https://www.themoviedb.org/settings/api
   - Create account (free)
   - Request API access
   - Copy your API key

2. **Gemini API Key:**
   - Go to https://aistudio.google.com/app/apikey
   - Click "Create API Key"
   - Copy the key

3. **SECRET_KEY:**
   ```powershell
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Copy the output into `.env`

#### Step 5: Set Up Database

**Option A: PostgreSQL (Production Setup)**

```powershell
# Create PostgreSQL database
# Using psql command line:
psql -U postgres
CREATE DATABASE justwatch;
\q

# Then run migrations:
alembic upgrade head
```

**Option B: SQLite (Development - Automatic)**

SQLite file is created automatically when you run the app. No setup needed.

#### Step 6: Run the Development Server

```powershell
# Navigate to src directory
cd src

# Start the development server
python -m uvicorn manage:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
Uvicorn running on http://127.0.0.1:8000
Press CTRL+C to quit
```

#### Step 7: Verify Installation

Open your browser and go to:
- **Interactive API Docs:** http://localhost:8000/docs
- **Alternative API Docs:** http://localhost:8000/redoc
- **API Root:** http://localhost:8000

You should see the Swagger UI with all API endpoints listed.

### Testing the API

#### Health Check Endpoint

```powershell
curl http://localhost:8000/health
# Response: OK
```

#### Register a Test User

```powershell
curl -X POST http://localhost:8000/v1/auth/register/ `
  -H "Content-Type: application/json" `
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "Password123!",
    "confirm_password": "Password123!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

Response will include access_token and refresh_token.

#### Use Token for Protected Endpoints

```powershell
$token = "your-access-token-from-registration"

curl -X GET http://localhost:8000/v1/auth/user-me/ `
  -H "Authorization: Bearer $token"
```

### Running Tests

```powershell
# Navigate to src directory
cd src

# Run all tests
pytest -v

# Run specific test file
pytest tests/test_users.py -v

# Run with coverage report
pytest --cov=. -v
```

### Troubleshooting

**Issue: "ModuleNotFoundError: No module named 'fastapi'"**
- Solution: Ensure virtual environment activated and dependencies installed
  ```powershell
  .\.venv\Scripts\Activate.ps1
  pip install fastapi uvicorn
  ```

**Issue: "Connection refused" error when running app**
- Solution: Database not running or URL wrong
  - Check `.env` DATABASE_URL
  - For PostgreSQL, ensure service is running
  - For SQLite, ensure directory is writable

**Issue: "TMDB API key not working"**
- Solution: Verify API key in `.env` is correct
  - Test with: `curl "https://api.themoviedb.org/3/movie/550?api_key=YOUR_KEY"`
  - Should return JSON with movie data

**Issue: "Gemini API not responding"**
- Solution: Verify Gemini API key and model name
  - Check key at https://aistudio.google.com/app/apikey
  - Ensure `GEMINI_MODEL=gemini-2.0-flash` (or latest available)

### Environment-Specific Configuration

**Development (.env)**
```env
DEBUG=true
DATABASE_URL=sqlite+aiosqlite:///./database.db
# Log everything, allow all origins
```

**Production (.env.prod)**
```env
DEBUG=false
DATABASE_URL=postgresql+asyncpg://user:pass@prod-db:5432/justwatch
# More restrictive CORS, monitoring enabled
```

### Running on Different Hosts

```powershell
# Default (localhost only):
python -m uvicorn manage:app --reload

# Allow external connections:
python -m uvicorn manage:app --reload --host 0.0.0.0 --port 8000

# Custom port:
python -m uvicorn manage:app --reload --port 3000

# Production (no reload):
python -m uvicorn manage:app --host 0.0.0.0 --port 8000 --workers 4
```

### Database Migrations

When models change, create migration:

```powershell
# Auto-generate migration
alembic revision --autogenerate -m "describe your changes"

# Review the generated file in alembic/versions/

# Apply migration
alembic upgrade head

# Rollback to previous version if needed
alembic downgrade -1
```

---

## Conclusion

Just-Watch demonstrates a modern, production-ready FastAPI backend with:
- ✅ Async/await throughout for performance
- ✅ JWT authentication for security
- ✅ Rate limiting against abuse
- ✅ Intelligent caching to reduce external API calls
- ✅ AI integration for personalized recommendations
- ✅ Comprehensive error handling
- ✅ Scalable database design
- ✅ Type-safe with Pydantic validation
- ✅ Testing framework ready

The architecture separates concerns (models, services, routes) making it easy to extend with new features, add more AI capabilities, or scale to handle millions of users.

For questions or contributions, reach out to the development team.
