from fastapi import FastAPI, status, HTTPException
from enum import Enum
from typing import Optional
from pydantic import BaseModel

app = FastAPI(
    title='Automation demo project',
    description='Showcasing my ability to create a simple REST API Server that can handle blog posts.'
)


class Category(Enum):
    TRAVEL = 'travel'
    FOOD = 'food'
    OTHER = 'other'


class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: bool = True
    category: Category
    rating: Optional[float] = None


posts = [
    Post(id=0, title='Best beaches in Florida', content='Check out these awesome beaches!',
         category=Category.TRAVEL, published=False, rating=4.5),
    Post(id=1, title='Best restaurants in Florida', content='Check out these awesome restaurants!',
         category=Category.FOOD, published=True, rating=3.0)
]


def find_post(uid):
    for post in posts:
        if post.id == uid:
            return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post with id {uid} was not found!')


@app.get('/posts/{uid}', responses={404: {'description': 'Post not found!'}})
async def get_post(uid: int):
    post = find_post(uid)
    return {'data': post}


@app.get('/posts')
async def get_posts():
    return {'data': posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_post(new_post: Post):
    new_post.id = posts[-1].id + 1
    posts.append(new_post)
    return {'data': new_post}


@app.put('/posts/{uid}', responses={404: {'description': 'Post not found!'}})
async def update_post(uid: int, update_data: Post):
    post = find_post(uid=uid)
    for post_key in post.__dict__.keys():
        setattr(post, post_key, getattr(update_data, post_key))
    return {'data': post}


@app.delete('/posts/{uid}', status_code=status.HTTP_204_NO_CONTENT, responses={404: {'description': 'Post not found!'}})
async def delete_post(uid: int):
    post = find_post(uid)
    posts.remove(post)
