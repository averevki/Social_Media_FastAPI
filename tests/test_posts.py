"""Posts query tests"""
import pytest

from app import schemas


def test_get_all_posts(authorized_client, add_test_posts):
    res = authorized_client.get("/posts/")
    assert res.status_code == 200
    assert len(res.json()) == len(add_test_posts)
    assert_schema = [schemas.PostResponse(**post) for post in res.json()]


def test_get_my_posts(authorized_client, user, add_test_posts):
    res = authorized_client.get("/posts/my")
    assert res.status_code == 200
    assert len(res.json()) == len(add_test_posts) - 1


def test_get_my_posts_unauthorized(client, add_test_posts):
    res = client.get("/posts/my")
    assert res.status_code == 401
    assert res.json()["detail"] == "Not authenticated"


def test_get_latest_post(client, add_test_posts):
    res = client.get("/posts/latest")
    assert res.status_code == 200
    latest_post = schemas.PostResponse(**res.json())
    assert latest_post.Post.title == add_test_posts[-1].title
    assert latest_post.Post.content == add_test_posts[-1].content
    assert latest_post.Post.owner.id == add_test_posts[-1].owner_id

@pytest.mark.parametrize("post_id", [30, 120, 99999])
def test_get_not_existing_post(authorized_client, add_test_posts, post_id):
    res = authorized_client.get(f"/posts/{post_id}")
    assert res.status_code == 404
    res = authorized_client.get(f"/posts/{len(add_test_posts) + 1}")
    assert res.status_code == 404


@pytest.mark.parametrize("post_number", [0, 1, 2])
def test_get_post_by_id(authorized_client, add_test_posts, post_number):
    res = authorized_client.get(f"/posts/{add_test_posts[post_number].id}")
    assert res.status_code == 200
    post = schemas.PostResponse(**res.json())       # passive response structure check
    assert post.Post.id == add_test_posts[post_number].id
    assert post.Post.title == add_test_posts[post_number].title
    assert post.Post.content == add_test_posts[post_number].content


@pytest.mark.parametrize("published", [True, False])
def test_create_post_unauthorized(client, add_test_posts, published):
    res = client.post(f"/posts/", json={"title": "Anonymous title",
                                        "content": "Anonymous content",
                                        "published": published})
    assert res.status_code == 401
    assert res.json()["detail"] == "Not authenticated"

@pytest.mark.parametrize("title, content, published", [
    ("New post", "About me", True),
    ("Post title here", "Post content there", True),
    ("Hi, I'm Anton", "Nice to meet you!", False),
])
def test_create_new_post(authorized_client, user, add_test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title,
                                                  "content": content,
                                                  "published": published})
    assert res.status_code == 201
    new_post = schemas.Post(**res.json())   # passive response structure validation
    assert new_post.title == title
    assert new_post.content == content
    assert new_post.published == published
    assert new_post.owner.id == user["id"]
    assert new_post.owner.email == user["email"]


def test_create_new_post_default_published(authorized_client, user, add_test_posts):
    res = authorized_client.post("/posts/", json={"title": "Hi, my name is",
                                                  "content": "Slimshady"})
    assert res.status_code == 201
    new_post = schemas.Post(**res.json())   # passive response structure validation
    assert new_post.title == "Hi, my name is"
    assert new_post.content == "Slimshady"
    assert new_post.published is True       # test default published True
    assert new_post.owner.id == user["id"]
    assert new_post.owner.email == user["email"]


@pytest.mark.parametrize("post_id", [0, 1, 2, 3])
def test_delete_post_unauthorized(client, add_test_posts, post_id):
    res = client.delete(f"/posts/{post_id}")
    assert res.status_code == 401
    assert res.json()["detail"] == "Not authenticated"


@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_delete_post(authorized_client, add_test_posts, post_id):
    res = authorized_client.delete(f"/posts/{post_id}")
    assert res.status_code == 204


def test_delete_foreign_post(authorized_client, add_test_posts):
    res = authorized_client.delete(f"/posts/{add_test_posts[3].id}")
    assert res.status_code == 403
    assert res.json()["detail"] == "unauthorized action"


@pytest.mark.parametrize("post_id", [30, 120, 9999999])
def test_delete_not_existing_post(authorized_client, add_test_posts, post_id):
    res = authorized_client.delete(f"/posts/{post_id}")
    assert res.status_code == 404


@pytest.mark.parametrize("post_id", [1, 2, 3, 4])
def test_update_post_unauthorized(client, add_test_posts, post_id):
    res = client.put(f"/posts/{post_id}")
    assert res.status_code == 401
    assert res.json()["detail"] == "Not authenticated"


@pytest.mark.parametrize("title, content, published", [
    ("Updated post1", "Some content", True),
    ("Updated post2", "More content", False)
])
def test_update_post(authorized_client, user, add_test_posts, title, content, published):
    res = authorized_client.put(f"/posts/{add_test_posts[0].id}", json={"title": title,
                                                                        "content": content,
                                                                        "published": published})
    assert res.status_code == 200
    post_response = schemas.PostResponse(**res.json())      # passive response scheme check
    assert post_response.Post.id == 1
    assert post_response.Post.title == title
    assert post_response.Post.content == content
    assert post_response.Post.published == published
    assert post_response.Post.owner.id == user["id"]


def test_update_foreign_post(authorized_client, add_test_posts):
    res = authorized_client.put(f"/posts/{add_test_posts[3].id}", json={"title": "Random title",
                                                                        "content": "Random text",
                                                                        "published": False})
    assert res.status_code == 403
    assert res.json()["detail"] == "unauthorized action"


@pytest.mark.parametrize("post_id", [30, 120, 9999999])
def test_update_not_existing_post(authorized_client, add_test_posts, post_id):
    res = authorized_client.put(f"/posts/{post_id}", json={"title": "Random title",
                                                           "content": "Random text",
                                                           "published": False})
    assert res.status_code == 404
    assert res.json()["detail"] == f"post was not found (id: {post_id})"
