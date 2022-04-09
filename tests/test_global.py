"""Global tests"""


def test_root(client):
    """Root query test"""
    res = client.get("/")
    assert res.status_code == 200
    assert res.json().get("message") == "Hello there :) Available queries -> /posts /users /rate"
