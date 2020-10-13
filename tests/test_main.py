import pytest
from fastapi.testclient import TestClient

from crawler_api.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_return_404_for_invalid_url(client):
    response = client.post('/not-found')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


def test_return_405_for_method_not_allowed(client):
    response = client.get('/legal-process')
    assert response.status_code == 405
    assert response.json() == {'detail': 'Method Not Allowed'}


def test_request_body_validation_on_legal_process_url(client):
    data = {'number': '1234567-12.1234.1.12.1234'}
    response = client.post('/legal-process', json=data)
    assert response.status_code == 422
    expected_payload = {
        'detail': [
            {
                'loc': ['body', 'number'],
                'msg': 'Invalid Number. The check digit (DV) is not correct',
                'type': 'assertion_error'
            }
        ]
    }
    assert response.json() == expected_payload


def test_required_request_body_validation_on_legal_process_url(client):
    data = {}
    response = client.post('/legal-process', json=data)
    assert response.status_code == 422
    expected_payload = {
        'detail': [
            {
                'loc': ['body', 'number'],
                'msg': 'field required',
                'type': 'value_error.missing'
            }
        ]
    }
    assert response.json() == expected_payload
