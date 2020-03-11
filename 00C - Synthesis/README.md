# 00B - Persisting Data

Persistence is typically necessary for any application and comes in many forms such as File Systems, Document Stores, Key Value Stores and so on. Here we explore how to use a Relational Database with an SQL interface using an Object Relational Mapping (ORM) tool.

You will write a program that will declaratively configure the database with an table for images, insert a row into it and print the rows.

## Parts

The builtin python function `input()`

The database engine `SQLite` ([docs](https://www.sqlite.org/index.html)) will be used to track the mapping between images and thumbnails.

The python module `SQLAlchemy` ([docs](https://www.sqlalchemy.org/)) will be used to help you interact with the SQLite.

## Specification

Write a program that prompts the user for a filename and inserts that into the database.

Write a program that prompts the user for a filename and uses `filter_by`  to find all the row items with that filename.

## Appendix

### ORM for images table

The following can be used to define and create a table. 

```python
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Image(Base):
	__tablename__ = 'images'

	id = Column(Integer, primary_key=True)
	filename = Column(String)

	def __repr__(self):
		return "Image<id={id}, filename='{filename}'>".format(
			id=self.id, 
			filename=self.filename
		)

engine = create_engine('sqlite+pysqlite:///local.db')
Base.metadata.create_all(engine)
```

### Writing to SQLite

```python
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite+pysqlite:///local.db')
Session = sessionmaker(bind=engine)
session = Session()

image = Image(filename='test.jpg')
session.add(image)
session.commit()
```