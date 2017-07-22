import pytest
import jobaddservice
from jobaddservice.database import db
from jobaddservice.oauth.models import Client
import json


@pytest.fixture
def client(request):
    """Configures the application and returns the test client."""
    jobaddservice.app.config['TESTING'] = True
    jobaddservice.app.config['SECRET_KEY'] = 'testing-key'

    db.drop_all(app=jobaddservice.app)
    db.create_all(app=jobaddservice.app)

    return jobaddservice.app.test_client()


def create_user(client, username, password):
    """Creates a new user given a username and password."""
    rv = client.post('/v1/oauth/', follow_redirects=True, data={
        'submit': 'Add User',
        'username': username,
        'password': password,
    })


def create_client(client):
    """Creates a new client."""
    rv = client.post('/v1/oauth/', follow_redirects=True, data={
        'submit': 'Add Client',
    })

    db.app = jobaddservice.app
    oauth_clients = Client.query.all()
    client_id = oauth_clients[0].client_id

    return client_id


def create_token(client, username, password, client_id):
    """Creates a new token given a username, password and client id."""
    rv = client.post('/v1/oauth/token', follow_redirects=True, data={
        'grant_type': 'password',
        'client_id': client_id,
        'username': username,
        'password': password
    })

    json_response = json.loads(rv.data)
    access_token = json_response['access_token']

    return access_token


def test_default_redirect(client):
    """Expects the default route to redirect to management."""
    rv = client.get('/', follow_redirects=True)
    assert 'Users' in rv.data
    assert 'Clients' in rv.data


def test_check(client):
    """Expects to obtain the authenticated user greeting."""
    create_user(client, 'userA', 'passA')
    client_id = create_client(client)
    access_token = create_token(client, 'userA', 'passA', client_id)

    rv = client.get('/v1/oauth/check', follow_redirects=True, headers={
        'Authorization': 'Bearer ' + access_token
    })

    assert 'userA' in rv.data


def test_get_job_index(client):
    """Expects to get and empty index."""
    create_user(client, 'userA', 'passA')
    client_id = create_client(client)
    access_token = create_token(client, 'userA', 'passA', client_id)

    rv = client.get('/v1/job', follow_redirects=True, headers={
        'Authorization': 'Bearer ' + access_token
    })

    assert '[]' in rv.data


def test_get_nonexistent_job(client):
    """Expects a not found error from a nonexistent item."""
    create_user(client, 'userA', 'passA')
    client_id = create_client(client)
    access_token = create_token(client, 'userA', 'passA', client_id)

    rv = client.get('/v1/job/1', follow_redirects=True, headers={
        'Authorization': 'Bearer ' + access_token
    })

    assert rv.status_code == 404
