-- public.instagram_posts_profiles_test definition

-- Drop table

-- DROP TABLE public.instagram_posts_profiles_test;

CREATE TABLE public.instagram_posts_profiles_test (
	input_url text NULL,
	id text NULL,
	username text NULL,
	url text NULL,
	full_name text NULL,
	biography text NULL,
	external_url text NULL,
	external_url_shimmed text NULL,
	followers_count int8 NULL,
	follows_count int8 NULL,
	has_channel bool NULL,
	highlight_reel_count int8 NULL,
	is_business_account bool NULL,
	joined_recently bool NULL,
	business_category_name text NULL,
	private bool NULL,
	verified bool NULL,
	profile_pic_url text NULL,
	profile_pic_url_hd text NULL,
	igtv_video_count int8 NULL,
	"postsCount" int8 NULL,
	created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP
);