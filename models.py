from sqlalchemy import Column, BigInteger, String, Integer, Boolean, ForeignKey, DateTime, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class InstagramPost(Base):
    __tablename__ = 'instagram_posts_test'

    id = Column(String, primary_key=True)
    inputUrl = Column(String)
    type = Column(String)
    shortCode = Column(String)
    caption = Column(String)
    url = Column(String)
    commentsCount = Column(Integer)
    dimensionsHeight = Column(Integer)
    dimensionsWidth = Column(Integer)
    displayUrl = Column(String)
    videoUrl = Column(String, nullable=True)
    alt = Column(String, nullable=True)
    likesCount = Column(Integer)
    videoViewCount = Column(Integer, nullable=True)
    videoPlayCount = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    locationName = Column(String, nullable=True)
    locationId = Column(String, nullable=True)
    ownerFullName = Column(String)
    ownerUsername = Column(String)
    ownerId = Column(String)
    productType = Column(String)
    videoDuration = Column(Float, nullable=True)
    isSponsored = Column(Boolean)
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
