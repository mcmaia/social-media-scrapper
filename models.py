from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class InstagramPost(Base):
    __tablename__ = 'instagram_posts_test'
    id = Column(String, primary_key=True)
    username = Column(String)
    id_post = Column(String)
    input_url = Column(String)
    type = Column(String)
    short_code = Column(String)
    caption = Column(String)
    url = Column(String)
    comments_count = Column(Integer)
    dimensions_height = Column(Integer)
    dimensions_width = Column(Integer)
    display_url = Column(String)
    video_url = Column(String, nullable=True)
    alt = Column(String, nullable=True)
    likes_count = Column(Integer)
    video_view_count = Column(Integer, nullable=True)
    video_play_count = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    location_name = Column(String, nullable=True)
    location_id = Column(String, nullable=True)
    owner_full_name = Column(String)
    owner_username = Column(String)
    owner_id = Column(String)
    product_type = Column(String)
    video_duration = Column(Float, nullable=True)
    is_sponsored = Column(Boolean)
    error = Column(String, nullable=True)
    client = Column(String)
    created_at = Column(String)
    # musicInfo = Column(JSON, nullable=True)
    # hashtags = Column(JSON)
    # mentions = Column(JSON)
    # images = Column(JSON, nullable=True)
    # childPosts = Column(JSON, nullable=True)
    # taggedUsers = Column(JSON, nullable=True)
    # coauthorProducers = Column(JSON, nullable=True)

    # comments = relationship("Comment", backref="instagram_posts_test")

# class Comment(Base):
#     __tablename__ = 'comments'

#     id = Column(String, primary_key=True)
#     text = Column(String)
#     ownerUsername = Column(String)
#     ownerProfilePicUrl = Column(String)
#     timestamp = Column(DateTime, default=datetime.datetime.utcnow)
#     likesCount = Column(Integer)
#     repliesCount = Column(Integer, nullable=True)
#     instagram_post_id = Column(String, ForeignKey('instagram_posts.id'))

#     replies = relationship("Reply", backref="comment")

# class Reply(Base):
#     __tablename__ = 'replies'

#     id = Column(String, primary_key=True)
#     text = Column(String)
#     ownerUsername = Column(String)
#     ownerProfilePicUrl = Column(String)
#     timestamp = Column(DateTime, default=datetime.datetime.utcnow)
#     likesCount = Column(Integer)
#     comment_id = Column(String, ForeignKey('comments.id'))
