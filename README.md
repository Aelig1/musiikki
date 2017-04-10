# musiikki REST API

REST API for adding, editing, fetching and deleting music metadata. Powered by Django.

Stores following information:
* Artist: name, genre, albums
* Album: name, artist, release year, tracklist
* Track: name, album, duration

Includes UI for testing HTTP requests and searching.

## Installation

The API is deployed in [musiikki.herokuapp.com](https://musiikki.herokuapp.com).
You can test it there

or

deploy locally with these steps:

1. Install [Python](https://www.python.org/) with [pip](https://pypi.python.org/pypi/pip/)
	* There's an option to install pip in Python Installer
	* Tested only on Python version 3.6
	* This guide assumes you have Python and pip in [PATH](https://en.wikipedia.org/wiki/PATH_(variable)) environment variable
2. Clone this reposity or download ZIP
	* Unzip into a folder
3. Install virtualenv
	* `pip install virtualenv` in command-line
4. Open command-line in the root file of the project. (Contains this file, README.md)
5. Create a virtual Python environment
	* `virtualenv venv` in command-line
6. Activate virtual environment
	* Windows: `venv\Scripts\activate`
	* others: `source venv/bin/activate`
	* Your command-line should have `(venv)` in the beginning of the line after this step
7. Install Django
	* `pip install -r requirements.txt`
8. Initialize Django project with the following commands
	* `python musiikki/manage.py collectstatic --no-input`
	* `python musiikki/manage.py makemigrations`
	* `python musiikki/manage.py migrate`
9. Run Django server
	* `python musiikki/manage.py runserver`
10. Open `localhost:8000` or `127.0.0.1:8000`in your web browser

## Usage

Requests:
* `GET /api/artists/` - Get all artists
* `GET /api/artists/id` - Get artist with id
* `GET /api/albums/` - Get all albums
* `GET /api/albums/id` - Get album with id
* `GET /api/tracks/` - Get all tracks
* `GET /api/tracks/id` - Get track with id

* `POST /api/artists/` - Add new artist (parameters: name, (genre))
* `POST /api/albums/` - Add new album (artist_id, album, (year))
* `POST /api/tracks/` - Add new track (album_id, track, (duration))

* `PUT /api/artists/id` - Replace artist with id (name, (genre))
* `PUT /api/albums/id` - Replace album with id (artist_id, album, (year))
* `PUT /api/tracks/id` - Replace track with id (album_id, track, (duration))

* `PATCH /api/artists/id` - Edit artist attribute with id ((name), (genre))
* `PATCH /api/albums/id` - Edit album attribute with id ((album), (year))
* `PATCH /api/tracks/id` - Edit track attribute with id ((track), (duration))

* `DELETE /api/artists/id` - Delete artist with id
* `DELETE /api/albums/id` - Delete album with id
* `DELETE /api/tracks/id` - Delete track with id

Search:
* `GET /api/search` - ((artist), (genre), (album), (track))
