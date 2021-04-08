.read lab09data.sql

CREATE TABLE smallest_int AS
  SELECT time, smallest from students where smallest > 2  ORDER by smallest LIMIT 20;

CREATE TABLE matchmaker AS
  SELECT a.pet , a.song, a.color,b.color from students as a, students as b where a.pet = b.pet and a.song = b.song and  a.time < b.time;

CREATE TABLE parents AS
  SELECT "abraham" AS parent, "barack" AS child UNION
  SELECT "abraham"          , "clinton"         UNION
  SELECT "delano"           , "herbert"         UNION
  SELECT "fillmore"         , "abraham"         UNION
  SELECT "fillmore"         , "delano"          UNION
  SELECT "fillmore"         , "grover"          UNION
  SELECT "eisenhower"       , "fillmore";

CREATE TABLE dogs AS
  SELECT "abraham" AS name, "long" AS fur, 26 AS height UNION
  SELECT "barack"         , "short"      , 52           UNION
  SELECT "clinton"        , "long"       , 47           UNION
  SELECT "delano"         , "long"       , 46           UNION
  SELECT "eisenhower"     , "short"      , 35           UNION
  SELECT "fillmore"       , "curly"      , 32           UNION
  SELECT "grover"         , "short"      , 28           UNION
  SELECT "herbert"        , "curly"      , 31;

CREATE TABLE sizes AS
  SELECT "toy" AS size, 24 AS min, 28 AS max UNION
  SELECT "mini"       , 28       , 35        UNION
  SELECT "medium"     , 35       , 45        UNION
  SELECT "standard"   , 45       , 60;

-- Add your INSERT INTOs here
CREATE TABLE smallest_int_having AS
  SELECT time, smallest from students GROUP BY smallest HAVING count(*) < 2 ORDER by smallest;

CREATE TABLE sicp20favpets AS
  SELECT pet, count(*) from students GROUP BY pet ORDER by count(*) desc LIMIT 10;

CREATE TABLE sicp20dog AS
  SELECT pet, count(*) from students WHERE pet = "dog" GROUP BY pet  ORDER by count(*) desc LIMIT 10;