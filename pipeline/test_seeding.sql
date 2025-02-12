INSERT INTO developer (developer_name)
VALUES ('treyarch');

INSERT INTO publisher (publisher_name)
VALUES ('ubisoft');

INSERT INTO game (game_title, release_date, game_image, age_rating)
VALUES ('Black ops', NOW(), 'url', 18);

INSERT INTO game_platform_assignment (game_id, platform_id, platform_score, platform_price, platform_discount)
VALUES (2, 2, 10, 10, 0);