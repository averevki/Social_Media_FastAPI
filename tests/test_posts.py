import pytest

from app import schemas


def test_get_all_posts(authorized_client, add_test_posts):
    res = authorized_client.get("/posts/")
    assert res.status_code == 200
    assert len(res.json()) == len(add_test_posts)
    assert_schema = [schemas.PostResponse(**post) for post in res.json()]


def test_get_not_existing_post(authorized_client, add_test_posts):
    res = authorized_client.get("/posts/99999999")
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


@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_delete_post(authorized_client, user, add_test_posts, post_id):
    res = authorized_client.delete(f"/posts/{post_id}")
    assert res.status_code == 204


@pytest.mark.parametrize("post_id", [4, 120, 9999999])
def test_delete_not_existing_post(authorized_client, user, add_test_posts, post_id):
    res = authorized_client.delete(f"/posts/{post_id}")
    assert res.status_code == 404
