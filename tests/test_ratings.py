"""Ratings query tests"""
import pytest

from app import models


@pytest.fixture
def rated_post(add_test_posts, db_session, user):
    new_vote = models.Rating(user_id=user["id"], post_id=add_test_posts[-1].id)
    db_session.add(new_vote)
    db_session.commit()


@pytest.mark.parametrize("post_id", [1, 2, 3, 4, 99])
def test_rate_post_unauthorized(client, add_test_posts, post_id):
    res = client.post("/rate/", json={"post_id": post_id,
                                      "dir": 1})
    assert res.status_code == 401
    assert res.json()["detail"] == "Not authenticated"


def test_rate_post(authorized_client, add_test_posts):
    res = authorized_client.post("/rate/", json={"post_id": add_test_posts[-1].id,
                                                 "dir": 1})
    assert res.status_code == 201
    assert res.json()["detail"] == "rating is saved"


def test_rate_post_twice(authorized_client, add_test_posts, rated_post):
    res = authorized_client.post("/rate/", json={"post_id": add_test_posts[-1].id,
                                                 "dir": 1})
    assert res.status_code == 409       # conflict
    assert res.json()["detail"] == "rating already exist"


@pytest.mark.parametrize("post_id, direction", [
    (1, 1),
    (3, 0)
])
def test_rate_your_own_post(authorized_client, add_test_posts, post_id, direction):
    res = authorized_client.post("/rate/", json={"post_id": post_id,
                                                 "dir": direction})
    assert res.status_code == 403
    assert res.json()["detail"] == "you can't rate your own post"


@pytest.mark.parametrize("post_id, direction", [(30, 1), (120, 0), (99999, 1)])
def test_rate_not_existing_post(authorized_client, add_test_posts, post_id, direction):
    res = authorized_client.post("/rate/", json={"post_id": post_id,
                                                 "dir": direction})
    assert res.status_code == 404
    assert res.json()["detail"] == f"post was not found (id: {post_id})"


def test_remove_post_rating(authorized_client, add_test_posts, rated_post):
    res = authorized_client.post("/rate/", json={"post_id": add_test_posts[-1].id,
                                                 "dir": 0})
    assert res.status_code == 201
    assert res.json()["detail"] == f"rating is saved"


def test_remove_not_existing_rating(authorized_client, add_test_posts):
    res = authorized_client.post("/rate/", json={"post_id": add_test_posts[-1].id,
                                                 "dir": 0})
    assert res.status_code == 404
    assert res.json()["detail"] == f"rating does not exist"
