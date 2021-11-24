
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.sql.functions import func

from ..database import get_db
from .. import models, schemas, oauth2


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 2,
    search: Optional[str] = ""
):

    # cursor.execute("""SELECT * FROM posts""")
    # post = cursor.fetchall()


    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).\
        join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).\
        group_by(models.Post.id).\
        filter(models.Post.title.contains(search)).\
        limit(limit).\
        offset(skip).\
        all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: id = Depends(oauth2.get_current_user)
):

    # cursor.execute(
    #     """INSERT INTO posts (title, content, published)
    #     VALUES (%s, %s, %s) RETURNING * """,
    #     (post.title, post.content, post.published)
    # )
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(owner_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # returning *

    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int, db: Session = Depends(get_db),
    current_user: id = Depends(oauth2.get_current_user)
):

    # cursor.execute(
    #     """SELECT * FROM posts WHERE id = %s """, (str(id))
    # )
    # post = cursor.fetchone()

    # post = db.query(models.Post).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).\
        join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).\
        group_by(models.Post.id).\
        filter(models.Post.id == id).\
        first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, db: Session = Depends(get_db),
    current_user: id = Depends(oauth2.get_current_user)
):

    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s returning * """,
    #     (str(id))
    # )
    # deleted_post = cursor.fetchone()
    # conn.commit()

    deleted_query = db.query(models.Post).filter(models.Post.id == id)

    deleted_post = deleted_query.first()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")

    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to performed requested action")

    deleted_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: id = Depends(oauth2.get_current_user)
):
    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s
    #     WHERE id = %s
    #     RETURNING *""",
    #     (post.title, post.content, post.published, id)
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    updated_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = updated_query.first()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")

    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to performed requested action")

    updated_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return updated_query.first()
