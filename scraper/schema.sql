CREATE TABLE article (
	id INT NOT NULL AUTO_INCREMENT,
	date_created DATETIME,
	source_url VARCHAR(255) UNIQUE,
 	source VARCHAR(4),
 	PRIMARY KEY(id)
	);