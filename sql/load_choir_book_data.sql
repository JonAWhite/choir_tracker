LOAD DATA LOCAL INFILE '/root/choir_tracker/data/choir_book.txt'
INTO TABLE choir_tracker.Songs 
FIELDS TERMINATED BY '|' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
