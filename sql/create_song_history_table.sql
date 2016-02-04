CREATE TABLE choir_tracker.Song_History
(
ID varchar(4),
Date DATE, 
DirectorID varchar(4), 
OrganistID varchar(4), 
EventID varchar(4), 
PRIMARY KEY (ID),
INDEX dir_ind (DirectorID),
FOREIGN KEY (DirectorID)
    REFERENCES Choir_Directors(id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
FOREIGN KEY (OrganistID)
    REFERENCES Organists(id)
    ON UPDATE CASCADE ON DELETE RESTRICT
);
