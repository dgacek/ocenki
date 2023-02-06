# Ocenki for Spotify

Web application for rating Spotify albums.  
SPA with session-based auth.  
Backend in Flask; frontend in Svelte and served through Jinja.

## App concept

- User can search for an album, search results are pulled from the Spotify API
- Ratings for each album are stored in a database, attached to the album's Spotify ID 

## Getting Started
Requirements: Python >= 3.11, pip, Node.js >= 18.13, npm
```sh
$ python -m venv env
$ source env/bin/activate  --  on Windows use this instead: & env/Scripts/Activate.ps1
$ pip install -r requirements.txt

$ npm install
$ npm run build
```

### Run locally
```sh
$ python app.py
```

### Run locally in a Docker container
```sh
$ docker build -t ocenki .
$ docker run -dp 5000:5000 --name ocenki ocenki
```

### Deploy on Fly.io
```sh
$ flyctl launch
```

If ran locally, the app is available at [http://localhost:5000/](http://localhost:5000/)
