import sqlite3
from uuid import uuid4 
import os.path

# TODO: Read these from a config file
INSTALL_PATH = '.'
DB = 'tags.db'	

class Tagger():

	def __init__(self):
		cmd_create_tags = """
		create table tags 
		(
		id char(40), 
		tag_name varchar(128),
		primary key (id)
		)"""

		cmd_create_paths = """
		create table paths 
		(
		id char(40), 
		path varchar(512),
		primary key (id)
		)"""

		cmd_create_tagpaths = """
		create table tagpaths 
		(
		id char(40), 
		tag_id char(40),
		path_id char(40),
		primary key (id),
		foreign key (tag_id) references tags(id),
		foreign key (path_id) references paths(id)
		)"""

		db_path = os.path.join(INSTALL_PATH, DB)
		if not os.path.isfile(db_path):
			self.conn = sqlite3.connect(db_path)
			self.cursor = conn.cursorsor()
			self.cursor.execute(cmd_create_tags)
			self.cursor.execute(cmd_create_paths)
			self.cursor.execute(cmd_create_tagpaths)
		else:
			self.conn = sqlite3.connect(db_path)
			self.cursor = self.conn.cursor()

		

	def get_or_insert_tag(self, tag_name):
		try:
			self.cursor.execute('select id from tags where tag_name = ?', (tag_name.lower(), ))
			results = self.cursor.fetchall()
			if len(results) == 0:
				tag_id = str(uuid4())
				self.cursor.execute('insert into tags values (?, ?)', (tag_id, tag_name.lower()))
				self.conn.commit()
				return tag_id
			else:
				return results[0][0]
		except Exception, e:
			raise

	def get_or_insert_path(self, file_path):
		try:
			self.cursor.execute('select id from paths where path = ?', (file_path.lower(), ))
			results = self.cursor.fetchall()
			if len(results) == 0:
				path_id = str(uuid4())
				self.cursor.execute('insert into paths values (?, ?)', (path_id, file_path.lower()))
				self.conn.commit()
				return path_id
			else:
				return results[0][0]
		except Exception, e:
			raise

	def tag_file(self, tag_name, path):
		tag_id = self.get_or_insert_tag(tag_name)
		path_id = self.get_or_insert_path(path)

		if tag_id is not None and path_id is not None:
			tagpath_id = str(uuid4())
			self.cursor.execute('insert into tagpaths values (?, ?, ?)', (tagpath_id, tag_id.lower(), path_id.lower()))
			self.conn.commit()
			return tagpath_id
		
	# Requires absolute path
	def list_tags_on_file(self, file_path):
		"""List all the tags on a given file"""
		cmd = """
		select tag_name from tags where id in (
			select tag_id from tagpaths 
			join paths on tagpaths.path_id = paths.id 
			where paths.path = ?)
		"""
		try:
			self.cursor.execute(cmd, (file_path, ))
			for tag in self.cursor.fetchall():
				print tag
		except:
			raise

	def list_files_with_tags(self, tag_name):
		cmd = """
		select path from paths where id in (
			select path_id from tagpaths 
			join tags on tagpaths.tag_id = tags.id 
			where tags.tag_name = ?)
		"""
		try:
			self.cursor.execute(cmd, (tag_name, ))
			for path in self.cursor.fetchall():
				print path
		except:
			raise

	def list_all_tags(self):
		cmd = "select tag_name from tags"
		try:
			self.cursor.execute(cmd)
			for tag in self.cursor.fetchall():
				print tag
		except:
			raise	

	def remove_tags(self, tag_name, files):
		pass
		# """Removes tags from the given file list"""
		# cmd = """"
		# 	Delete from tags
		# """
		# try:
		# 	self.cursor.execute('SELECT TAG_NAME FROM TAGS WHERE FILE_NAME=?', file_name)
		# except:
		# 	raise