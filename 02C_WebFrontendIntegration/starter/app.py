import connexion
from flask import jsonify, send_from_directory, url_for
import boto3

BUCKET_NAME = ''
UPLOAD_FOLDER = ''
AWS_PROFILE = ''

session = boto3.Session(profile_name=AWS_PROFILE)
s3 = session.client('s3')

def serve_ui():
    return send_from_directory('public', 'index.html')

def serve_static(filename):
    response = send_from_directory('public', filename)
    response.direct_passthrough = False
    return response

def get_profile():
    return jsonify({
        'id': 'lol',
        'name': 'Ren'
    })

def get_image_upload_url(filename):
    url = s3.generate_presigned_url(
        # Implement
    )

    return jsonify({
        'upload_url': url
    })

if __name__ == '__main__':
    app = connexion.FlaskApp(__name__, port=5000)
    app.add_api('example.yaml')
    app.run(debug=True)