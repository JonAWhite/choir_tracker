LOAD DATA LOCAL INFILE '/root/choir_tracker/data/celebration_hymnal.txt'
INTO TABLE choir_tracker.Songs 
FIELDS TERMINATED BY '|' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
