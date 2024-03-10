-- public.instagram_posts_test definition

-- Drop table

-- DROP TABLE public.instagram_posts_test;

CREATE TABLE public.instagram_posts_test (
	id serial4 NOT NULL,
	username varchar NULL,
	id_post varchar NOT NULL,
	input_url varchar NULL,
	"type" varchar NULL,
	short_code varchar NULL,
	caption varchar NULL,
	url varchar NULL,
	comments_count int4 NULL,
	dimensions_height int4 NULL,
	dimensions_width int4 NULL,
	display_url varchar NULL,
	video_url varchar NULL,
	alt varchar NULL,
	likes_count int4 NULL,
	video_view_count int4 NULL,
	video_play_count int4 NULL,
	"timestamp" timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	location_name varchar NULL,
	location_id varchar NULL,
	owner_full_name varchar NULL,
	owner_username varchar NULL,
	owner_id varchar NULL,
	product_type varchar NULL,
	video_duration float8 NULL,
	is_sponsored bool NULL,
	music_info json NULL,
	hashtags json NULL,
	mentions json NULL,
	images json NULL,
	child_posts json NULL,
	tagged_users json NULL,
	coauthor_producers json NULL,
	created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	error varchar NULL,
	client varchar NULL,
	updated_at timestamp NULL,
	deleted_at timestamp NULL,

	CONSTRAINT instagram_posts_test_pkey PRIMARY KEY (id)
);