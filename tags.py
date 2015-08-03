import sqlite3
from uuid import uuid4 

# TODO: Read these from a config file
INSTALL_PATH = '~'
DB = 'tags.db'	

def get_or_insert_tag(cursor, tag_name):
	try:
		cursor.execute('SELECT ID FROM TAGS WHERE TAG_NAME = ?', tag_name.lower())
		results = cursor.fetchall()
		if len(results) == 0:
			id = uuid4()
			cursor.execute('INSERT INTO TAGS VALUES (?, ?)', (id, tag_name.lower()))
			cursor.commit()
			return id
		else:
			return results[0][0]
	except Exception, e:
		return None

def get_or_insert_path(cursor, file_path):
	try:
		cursor.execute('SELECT ID FROM PATHS WHERE FILE_PATH = ?', file_path.lower())
		results = cursor.fetchall()
		if len(results) == 0:
			id = uuid4()
			cursor.execute('INSERT INTO PATHS VALUES (?, ?)', (id, file_path.lower()))
			cursor.commit()
			return id
		else:
			return results[0][0]
	except Exception, e:
		return None

def tag_file(cursor, tag_name, path):
	tag_id = get_or_insert_tag(cursor, tag_name)
	path_id = get_or_insert_path(cursor, path)

	

def list_tags(cursor, file_name):
	"""List all the tags on a given file"""
	cmd = """
	SELECT TAG_NAME FROM TAGS WHERE TAG_NAME IN (
		SELECT TAG_ID FROM TAGPATHS WHERE )
	"""
	try:
		cursor.execute(, file_name)
	except:
		raise

def list_paths(cursor, tag_name):
	pass

def remove_tags(cursor, tag_name, files):
	"""Removes tags from the given file list"""
	cmd = """"
		Delete from tags
	"""
	try:
		cursor.execute('SELECT TAG_NAME FROM TAGS WHERE FILE_NAME=?', file_name)
	except:
		raise

def init():
	cmd_create_tags = """
	CREATE TABLE Tags 
	(
	id char(40), 
	tag_name varchar(128),
	PRIMARY KEY (id)
	)"""

	cmd_create_paths = """
	CREATE TABLE Paths 
	(
	id char(40), 
	path varchar(512),
	PRIMARY KEY (id)
	)"""

	cmd_create_tagpaths = """
	CREATE TABLE Tagpaths 
	(
	id char(40), 
	tag_id char(40),
	path_id char(40),
	PRIMARY KEY (id),
	FOREIGN KEY (tag_id) REFERENCES Tags(id),
	FOREIGN KEY (path_id) REFERENCES Paths(id)
	)"""

def end(conns):
	for conn in conns: 
		try:
			conn.close()
		except Exception, e:
			pass
