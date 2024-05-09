import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_votes_unauthorized(client):
    response = client.get('/votes')
    assert response.status_code == 401

def test_votes_authorized(client):
    response = client.get('/votes', headers={'Authorization': 'Basic YWRtaW46c2VjcmV0'})
    assert response.status_code == 200
    assert b'Current Votes' in response.data

def test_vote_valid(client):
    votes_before = client.get('/api/getvotes').json
    response = client.post('/vote', data={'restaurant': 'ihop'}, 
                           headers={'Authorization': 'Basic YWRtaW46c2VjcmV0'})
    assert response.status_code == 302
    votes_after = client.get('/api/getvotes').json
    assert votes_after[2]['value'] == votes_before[2]['value'] + 1

def test_vote_invalid(client):
    votes_before = client.get('/api/getvotes').json
    response = client.post('/vote', data={'restaurant': 'invalid'}, 
                           headers={'Authorization': 'Basic YWRtaW46c2VjcmV0'})
    assert response.status_code == 302
    votes_after = client.get('/api/getvotes').json
    for i in range(len(votes_before)):
        assert votes_after[i]['value'] == votes_before[i]['value']
