CREATE TABLE Prison(
    Branch_ID INTEGER PRIMARY KEY,
    Prison_Location VARCHAR(100),
    Prison_Guard_Name VARCHAR(100),
    Prison_GUARD_PhnNumber VARCHAR(10)
);

CREATE TABLE Incharge(
    Incharge_ID INTEGER PRIMARY KEY,
    Incharge_Name VARCHAR(20),
    Age INTEGER,
    Post INTEGER,
    Workplace VARCHAR(100)
);


CREATE TABLE Prisoner( 
    Prisoner_id INTEGER PRIMARY KEY,
    Prisoner_name VARCHAR(100),
    Age INTEGER,
    Cell_Number VARCHAR(10),
    Incharge_ID INTEGER,
    Branch_ID INTEGER,
    CONSTRAINT fk2 FOREIGN KEY (Branch_ID) REFERENCES Prison(Branch_ID),
    CONSTRAINT fk4 FOREIGN KEY (Incharge_ID) REFERENCES Incharge(Incharge_ID)
);


-- CREATE TABLE Prisoner_details(
--     Prisoner_id INTEGER,
--     Prisoner_name VARCHAR(100),
--     Incharge_ID INTEGER,
--     Age INTEGER,
--     Address VARCHAR(100),
--     HEIGHT INTEGER,
--     WEIGHT INTEGER,
--     CRIME_COMMITED VARCHAR(20),
--     DATE_OF_IMPRSNMNT VARCHAR(9),
--     MNTHS_SNTNCD_IN_JAIL INTEGER,
    
--     CONSTRAINT fk3 FOREIGN KEY (Prisoner_id) REFERENCES Prisoner(Prisoner_id)
-- );

INSERT INTO Prison VALUES (1,'Delhi Central','Rajesh J','9205785202');
INSERT INTO Prison VALUES (2,'Delhi Central','Roshan K','9292453216');
INSERT INTO Prison VALUES (3,'Delhi Main','Amit S','9506100184');
INSERT INTO Prison VALUES (4,'Delhi Central','Rajesh J','8723969242');
INSERT INTO Prison VALUES (5,'Delhi Tihar Jail','Mahesh ','8699190711');
INSERT INTO Prison VALUES (6,'Mumbai Central','Kumar J','9906519356');
INSERT INTO Prison VALUES (7,'Mumbai Metro','Yash F','9906519356');
INSERT INTO Prison VALUES (8,'Chennai Central JAIL','Harshan I','8205785202');
INSERT INTO Prison VALUES (9,'Salem Central','Raja S','7611870554');
INSERT INTO Prison VALUES (10,'Kolkata Main','Rose M','9205785202');
INSERT INTO Prison VALUES (11,'Delhi Main','Yash Gabriel Raj L','9205785202');



-- insert into prisoner VALUES(345,'Madhan OP',24,'B14',112345,43)

INSERT INTO Incharge VALUES(1001, 'Chotta Bheem', 46, 2001, 'Block 01');
INSERT INTO Incharge VALUES(1002, 'Chutki', 20, 2002, 'Block 02');
INSERT INTO Incharge VALUES(1003, 'Kalia', 46, 2001, 'Block 01');
INSERT INTO Incharge VALUES(1004, 'Dholu', 55, 2003, 'Block 02');
INSERT INTO Incharge VALUES(1005, 'Bholu', 76, 2004, 'Block 03');
INSERT INTO Incharge VALUES(1006, 'Jaggu', 46, 2005, 'Block 04');
INSERT INTO Incharge VALUES(1007, 'Indumati', 40, 2005, 'Block 01');
INSERT INTO Incharge VALUES(1008, 'Boomer', 26, 2004, 'Block 03');
INSERT INTO Incharge VALUES(1009, 'Harshan', 36, 2006, 'Block 03');
INSERT INTO Incharge VALUES(1010, 'Pandu Rangan', 19, 2007, 'Block 01');
INSERT INTO Incharge VALUES(1011, 'Srikrishna', 46, 2007, 'Block 05');
INSERT INTO Incharge VALUES(1012, 'Harish', 46, 2008, 'Block 01');
INSERT INTO Incharge VALUES(1013, 'Pal Pandian', 46, 2009, 'Block 02');
INSERT INTO Incharge VALUES(1014, 'Bladeu Ravi', 46, 2009, 'Block 05');




insert into prisoner VALUES(345,'Madhan OP',24,'B14',1014,10);
insert into prisoner VALUES(346,'Manmadan',40,'B14',1014,9);
insert into prisoner VALUES(347,'Robert Bhaagyasree Kaul',34,'B14',1003,8);
insert into prisoner VALUES(348,'Jackie Kalyan Sarin',67,'B14',1004,7);
insert into prisoner VALUES(349,'Namita Sastry Shankar R',21,'B14',1004,11);
insert into prisoner VALUES(350,'Dhanush',20,'B14',1001,1);
insert into prisoner VALUES(351,'Bahubali',34,'B14',1002,3);
insert into prisoner VALUES(352,'Julie',31,'B14',1006,4);
insert into prisoner VALUES(353,'Raghuvareb',80,'B14',1009,5);
insert into prisoner VALUES(354,'Joseph',29,'B14',1004,10);
insert into prisoner VALUES(355,'Binita Jhaveri Shindu',36,'B14',1010,10);
