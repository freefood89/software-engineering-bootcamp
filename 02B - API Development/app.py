import connexion
from flask import jsonify

def get_profile():
    return jsonify({
    	'id': 'lol',
    	'name': 'Ren'
    })

if __name__ == '__main__':
    app = connexion.FlaskApp(__name__, port=5000)
    app.add_api('example.yaml')
    app.run()