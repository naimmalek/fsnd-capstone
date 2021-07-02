from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS

from database.models import setup_db, Actors, Movies
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config['DEBUG'] = True
    setup_db(app)
    CORS(app)

    @app.route('/')
    def home():
        return "Welcome to Udacity Casting Agency"

    @app.route('/health')
    def health():
        return jsonify({'health': 'Running!!'})

    # ROUTES
    @app.route('/actors')
    @requires_auth("get:actors")
    def get_actors(payload):
        actors = Actors.query.all()
        if not actors:
            abort(404)
        actors = [i.format() for i in actors]
        return jsonify({
            'success': True,
            'actors': actors
        })

    @app.route('/movies')
    @requires_auth("get:movies")
    def get_movies(payload):
        movies = Movies.query.all()
        if not movies:
            abort(404)
        movies = [i.format() for i in movies]
        return jsonify({
            'success': True,
            'movies': movies
        })

    @app.route("/movies/<int:id>")
    @requires_auth("get:movies-detail")
    def get_movies_detail(payload, id):
        movie = Movies.query.get(id)
        if not movie:
            abort(404)
        result = {
            "success": True,
            "movie": movie.format()
        }
        return jsonify(result)

    @app.route("/actors/<int:id>")
    @requires_auth("get:actors-detail")
    def get_actor_detail(payload, id):
        actor = Actors.query.get(id)
        if not actor:
            abort(404)
        result = {
            "success": True,
            "actor": actor.format()
        }
        return jsonify(result)

    @app.route("/actors/<int:id>", methods=['DELETE'])
    @requires_auth("delete:actors")
    def delete_actor(token, id):
        actor = Actors.query.get(id)
        if not actor:
            abort(404)
        try:
            Actors.delete(actor)
        except Exception as e:
            print('delete_actor error', e)
            abort(422)

        result = {
            "success": True,
        }
        return jsonify(result)

    @app.route("/movies/<int:id>", methods=['DELETE'])
    @requires_auth("delete:movies")
    def delete_movie(token, id):
        movies = Movies.query.get(id)
        if not movies:
            abort(404)
        try:
            Movies.delete(movies)
        except Exception as e:
            print('delete_movie error', e)
            abort(422)

        result = {
            "success": True,
        }
        return jsonify(result)

    @app.route("/actors", methods=['POST'])
    @requires_auth("post:actors")
    def add_actors(token):
        if request.data:
            request_data = json.loads(request.data.decode('utf-8'))
            actors = []
            try:
                new_act = Actors(full_name=request_data['full_name'],
                                 date_of_birth=json.dumps(request_data['date_of_birth']))
                Actors.insert(new_act)
                actors = list(map(Actors.format, Actors.query.all()))
            except Exception as e:
                print('add_actors error', e)
                abort(422)

            result = {
                "success": True,
                "actors": actors
            }
            return jsonify(result)

    @app.route("/movies", methods=['POST'])
    @requires_auth("post:movies")
    def add_movies(token):
        if request.data:
            request_data = json.loads(request.data.decode('utf-8'))
            movies = []
            try:
                new_movies = Movies(title=request_data['title'], release_year=request_data['release_year'],
                                    duration=request_data['duration'], imdb_rating=request_data['imdb_rating'])
                if request_data["cast"]:
                    actors = Actors.query.filter(Actors.full_name.in_(request_data["cast"])).all()
                    new_movies.cast = actors
                    new_movies.insert()
                else:
                    new_movies.insert()
                movies = list(map(Movies.format, Movies.query.all()))
            except Exception as e:
                print('add_movies error', e)
                abort(422)

            result = {
                "success": True,
                "movies": movies
            }
            return jsonify(result)

    @app.route("/actors/<int:id>", methods=['PATCH'])
    @requires_auth("patch:actors")
    def patch_actors(token, id):
        request_data = json.loads(request.data.decode('utf-8'))
        actor_data = Actors.query.get(id)

        if not actor_data:
            abort(404)

        if 'full_name' in request_data:
            setattr(actor_data, 'full_name', request_data['full_name'])
        if 'date_of_birth' in request_data:
            setattr(actor_data, 'date_of_birth', request_data['date_of_birth'])
        actors = []
        try:
            Actors.update(actor_data)
            actors = list(map(Actors.format, Actors.query.all()))
        except Exception as e:
            print('patch_actors error', e)
            abort(422)

        result = {
            "success": True,
            "actors": actors
        }
        return jsonify(result)

    @app.route("/movies/<int:id>", methods=['PATCH'])
    @requires_auth("patch:movies")
    def patch_movies(token, id):
        request_data = json.loads(request.data.decode('utf-8'))
        movie_data = Movies.query.get(id)
        if not movie_data:
            abort(404)

        if 'title' in request_data:
            setattr(movie_data, 'title', request_data['title'])
        if 'release_year' in request_data:
            setattr(movie_data, 'release_year', request_data['release_year'])
        if 'duration' in request_data:
            setattr(movie_data, 'duration', request_data['duration'])
        if 'imdb_rating' in request_data:
            setattr(movie_data, 'imdb_rating', request_data['imdb_rating'])
        if 'cast' in request_data:
            actors = Actors.query.filter(Actors.full_name.in_(request_data["cast"])).all()
            print('actors', actors)
            movie_data.cast = actors

        movies = []
        try:
            Movies.update(movie_data)
            movies = list(map(Movies.format, Movies.query.all()))
        except Exception as e:
            print('patch_movies error', e)
            abort(422)

        result = {
            "success": True,
            "movies": movies
        }
        return jsonify(result)

    # Error Handling
    @app.errorhandler(400)
    @app.errorhandler(401)
    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(405)
    @app.errorhandler(422)
    @app.errorhandler(500)
    def error_handler(error):
        return jsonify({
            'success': False,
            'error': error.code,
            'message': error.description
        }), error.code

    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify(e.error), e.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

# db_drop_and_create_all()
