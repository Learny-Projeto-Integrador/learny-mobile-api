import os
import sys

import mongomock
import pymongo
import pytest

os.environ["DB_NAME"] = "test_learny"
os.environ["JWT_SECRET_KEY"] = "test-secret-key"
os.environ.pop("DB_USER", None)
os.environ.pop("DB_PASSWORD", None)
os.environ.pop("DB_HOST", None)

pymongo.MongoClient = mongomock.MongoClient
try:
    import flask_pymongo
    flask_pymongo.MongoClient = mongomock.MongoClient
except ImportError:
    pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from api import app as flask_app, mongo  # noqa: E402


@pytest.fixture(scope="session")
def app():
    flask_app.config["TESTING"] = True
    flask_app.config["JWT_SECRET_KEY"] = "test-secret-key"
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db():
    return mongo.db


@pytest.fixture(autouse=True)
def _clean_db():
    """Limpa todas as coleções antes de cada teste."""
    for col in mongo.db.list_collection_names():
        mongo.db[col].drop()
    yield
    for col in mongo.db.list_collection_names():
        mongo.db[col].drop()


@pytest.fixture
def make_parent(db):
    from bson import ObjectId
    from werkzeug.security import generate_password_hash

    def _make(**overrides):
        doc = {
            "_id": ObjectId(),
            "username": "testparent",
            "password": generate_password_hash("password123"),
            "name": "Test Parent",
            "email": "parent@example.com",
            "selectedChild": "",
            "profilePicture": "",
            "birthDate": None,
        }
        doc.update(overrides)
        db.parents.insert_one(doc)
        return doc

    return _make


@pytest.fixture
def make_child(db):
    from bson import ObjectId
    from werkzeug.security import generate_password_hash

    def _make(parent_id=None, **overrides):
        doc = {
            "_id": ObjectId(),
            "username": "testchild",
            "password": generate_password_hash("kidpass"),
            "name": "Test Child",
            "profilePicture": "",
            "audioActive": True,
            "rankingActive": True,
            "parent": parent_id,
            "birthDate": None,
        }
        doc.update(overrides)
        db.children.insert_one(doc)
        return doc

    return _make


@pytest.fixture
def parent_token(app, make_parent):
    from flask_jwt_extended import create_access_token

    parent = make_parent()
    with app.app_context():
        token = create_access_token(
            identity=str(parent["_id"]),
            additional_claims={
                "user": {
                    "username": parent["username"],
                    "name": parent["name"],
                    "type": "parent",
                }
            },
        )
    return token, parent


@pytest.fixture
def child_token(app, make_child):
    from flask_jwt_extended import create_access_token

    child = make_child()
    with app.app_context():
        token = create_access_token(
            identity=str(child["_id"]),
            additional_claims={
                "user": {
                    "username": child["username"],
                    "name": child["name"],
                    "type": "child",
                }
            },
        )
    return token, child


@pytest.fixture
def auth_header():
    def _build(token):
        return {"Authorization": f"Bearer {token}"}

    return _build
