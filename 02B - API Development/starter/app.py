import connexion
from flask import jsonify
import boto3

BUCKET_NAME = ''
UPLOAD_FOLDER = ''
AWS_PROFILE = ''

session = boto3.Session(profile_name=AWS_PROFILE)
s3 = session.client('s3')

def get_profile():
    return jsonify({
        'id': 'lol',
        'name': 'Ren'
    })

if __name__ == '__main__':
    app = connexion.FlaskApp(__name__, port=5000)
    app.add_api('example.yaml')
    app.run()