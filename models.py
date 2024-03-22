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
    # musicInfo = Column(JSON, nullable=True)
    # hashtags = Column(JSON)
    # mentions = Column(JSON)
    # images = Column(JSON, nullable=True)
    # childPosts = Column(JSON, nullable=True)
    # taggedUsers = Column(JSON, nullable=True)
    # coauthorProducers = Column(JSON, nullable=True)

    # comments = relationship("Comment", backref="instagram_posts_test")

class InstagramProfile(Base):
    __tablename__ = 'instagram_profiles_test'

    input_url = Column(String, primary_key=True)
    id = Column(String)
    username = Column(String)
    url = Column(String)
    full_name = Column(String)
    biography = Column(String)
    external_url = Column(String)
    external_url_shimmed = Column(String)
    followers_count = Column(Integer)
    follows_count = Column(Integer)
    has_channel = Column(Boolean)
    highlight_reel_count = Column(Integer)
    is_business_account = Column(Boolean)
    joined_recently = Column(Boolean)
    business_category_name = Column(String)
    private = Column(Boolean)
    verified = Column(Boolean)
    profile_pic_url = Column(String)
    profile_pic_url_hd = Column(String)
    igtv_video_count = Column(Integer)
    related_profiles = Column(String)  # Assuming this is a string representation of related profiles
    latest_igtv_videos = Column(String)  # Assuming this is a string representation of latest IGTV videos
    posts_count = Column(Integer)  # Renamed from `postsCount` to follow Python naming conventions
    latest_posts = Column(String)  # Assuming this is a string representation of latest posts
    error = Column(String)


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
