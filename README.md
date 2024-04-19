# Spotify_backend_system

"""
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
      - FLASK_APP=app.py
      - DATABASE_URL=postgresql://user:password@db:5432/music_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    networks:
      - flask_app_network

  db:
    image: postgres
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=music_db
    networks:
      - flask_app_network

  redis:
    image: redis
    networks:
      - flask_app_network

networks:
  flask_app_network:
    driver: bridge

"""

### Api Functions And Endpoints:-

Endpoints:

User Authentication:
/register: Register a new user.
/login: User login to get authentication token.
/logout: User logout to invalidate authentication token.
Music Catalog:
/songs: List all songs in the catalog.
/songs/{id}: Get details of a specific song by ID.
/albums: List all albums in the catalog.
/albums/{id}: Get details of a specific album by ID.
/artists: List all artists in the catalog.
/artists/{id}: Get details of a specific artist by ID.
User Playlists:
/playlists: List all playlists of the authenticated user.
/playlists/{id}: Get details of a specific playlist by ID.
/playlists/{id}/songs: List songs in a specific playlist.
/playlists/create: Create a new playlist for the authenticated user.
/playlists/{id}/add-song: Add a song to a specific playlist.
/playlists/{id}/remove-song: Remove a song from a specific playlist.
Functionality:

User Authentication:

Users can register with a username, email, and password.
Users can log in to obtain an authentication token.
Users can log out to invalidate their authentication token.
Music Catalog:

Users can browse songs, albums, and artists.
Users can view details of specific songs, albums, and artists.
User Playlists:

Authenticated users can create playlists.
Authenticated users can add songs to their playlists.
Authenticated users can remove songs from their playlists.
Users:

Regular User:
Can browse music catalog.
Can create playlists, add songs, and remove songs from their playlists.
Admin User:
Same functionalities as regular user.
Additionally, can perform administrative tasks such as adding, editing, or deleting songs, albums, and artists from the catalog.


### dockerfile foe web
FROM python:3.9-slim
WORKDIR /app
COPY requiremnets.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requiremnets.txt
COPY . .
EXPOSE 5000
CMD ["flask","run","--host","0.0.0.0"]