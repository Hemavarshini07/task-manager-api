import os
import tempfile
import pytest
from app import app, db
from models import Task

@pytest.fixture
def client():
    db_fd, test_db = tempfile.mkstemp(suffix='.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + test_db
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(test_db)


def test_create_task(client):
    rv = client.post('/api/tasks', json={'title': 'Test task', 'description': 'desc'})
    assert rv.status_code == 201
    data = rv.get_json()
    assert data['task']['title'] == 'Test task'


def test_get_tasks(client):
    client.post('/api/tasks', json={'title': 't1'})
    client.post('/api/tasks', json={'title': 't2'})
    rv = client.get('/api/tasks')
    assert rv.status_code == 200
    payload = rv.get_json()
    assert payload['total'] == 2


def test_update_task(client):
    create = client.post('/api/tasks', json={'title': 't1'})
    task_id = create.get_json()['task']['id']
    rv = client.put(f'/api/tasks/{task_id}', json={'status': 'completed'})
    assert rv.status_code == 200
    assert rv.get_json()['task']['status'] == 'completed'


def test_delete_task(client):
    create = client.post('/api/tasks', json={'title': 't1'})
    task_id = create.get_json()['task']['id']
    rv = client.delete(f'/api/tasks/{task_id}')
    assert rv.status_code == 200
    assert client.get('/api/tasks').get_json()['total'] == 0
