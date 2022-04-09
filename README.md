# Social media API
API that allows users to exchange posts on
social media simulation

## Try out yourself!
API is deployed on heroku: <br/>
https://social-media-api-verevkin.herokuapp.com/posts <br/>
Interactive documentation: <br/>
https://social-media-api-verevkin.herokuapp.com/docs

## Preview, examples
- #### Fetch published posts <br/>
```GET https://social-media-api-verevkin.herokuapp.com/posts```
```json
[{
    "Post": {
        "title": "Wassup",
        "content": "Who want to chat?",
        "published": true,
        "id": 2,
        "created_at": "2022-04-09T13:13:26.930493+00:00",
        "owner": {
            "id": 1,
            "email": "sandychatter@gmail.com",
            "created_at": "2022-04-03T20:14:56.543206+00:00"
        }
    },
    "likes": 4
}, {
    "Post": {
        "title": "Hi, it's my first post",
        "content": "Happy to be here!",
        "published": true,
        "id": 1,
        "created_at": "2022-04-04T12:27:40.618115+00:00",
        "owner": {
            "id": 3,
            "email": "RonLoveCode1989@gmail.com",
            "created_at": "2022-04-01T20:30:40.231458+00:00"
        }
    },
    "likes": 2
}]
```
- #### Create new user <br/>
```POST https://social-media-api-verevkin.herokuapp.com/users``` 
```json
{
  "email": "user@example.com",
  "password": "MyPassword123?!"
}
```
- #### User login <br/>
```POST https://social-media-api-verevkin.herokuapp.com/users/login```<br/>
input:
```json
{
  "username": "user@example.com",
  "password": "MyPassword123?!"
}
```
output:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2NDk1MTc0MTJ9.uIbF5LHfy_AJZ2SLhCTvEXlhMtMLDjUhc9ROsiKypDo",
  "token_type": "bearer"
}
```
- #### Create post <br/>
```POST https://social-media-api-verevkin.herokuapp.com/posts```<br/>
```json
{
    "title": "I love tigers",
    "content": "Tigers are great",
    "published": true
}
```
- #### Rate post <br/>
```POST https://social-media-api-verevkin.herokuapp.com/rate```<br/>
```json
{
  "post_id": 3,
  "dir": 1
}
```


## Used technologies
- FastAPI framework
- PostgreSQl database
- SQLAlchemy ORM
- Alembic as database migration tool
- OAuth2 and JWTokens for users authentication
- Each query and api feature provided with pytest tests
- Application is fully automized for CI/CD workflow with GitHub actions
- Application is dockerized and deployed on heroku

## Planned features
- Dislike feature (direction: -1, youtube answer)
- Show amount of likes and posts created by user

###### *Aleksandr Verevkin 2022*
