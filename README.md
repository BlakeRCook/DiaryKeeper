This website is meant to store and keep posts about peoples daily lifes. Simply fill in all the feilds and and click the keep button to save the post.
the resource can be found in the **servhw3** folder. It is called **data.db**.
**data.db** contains all the **posts** saved from the users. Each **post** contains five elements:
1. Name
2. Age
3. Sentence (what the user writes about for their day)
4. Date
5. Ten (User rates their day out of 10)

The data was made through sqlite3 and the schema for the data base looks like this:
```sqlite3
CREATE TABLE fourm (
id INTEGER PRIMARY KEY,
name TEXT,
age TEXT,
sentence TEXT,
date TEXT,
ten TEXT);
```

The API implemented in my website consits of:
1. GET
2. POST
3. PUT
4. DELETE

**GET** has 2 functions one for retrieving all items and one to retrieve a single item.<br />
ex: (HTTP GET http://localhost:8080/messages)<br />
or<br />
ex: (HTTP GET http://localhost:8080/messages/1)<br />

**POST** creats a post and gives the post a unique id<br />
ex: (HTTP POST http://localhost:8080/messages)<br />

**PUT** edits one of the post<br />
ex: (HTTP PUT http://localhost:8080/messages/1)<br />

**DELETE** deletes a post<br />
ex: (HTTP DELETE http://localhost:8080/messages/1)<br /># f18-resourceful-Doctorhobo
