import datetime
import re
import time
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, BigInteger
from sqlalchemy.orm import relationship, validates
from flask_appbuilder import Model
from sqlalchemy.dialects.mysql import VARCHAR, TEXT, TIME, ENUM
from sqlalchemy import Enum, Interval, Time

mindate = datetime.date(datetime.MINYEAR, 1, 1)

class TrueFalseDefault(Enum):
	TestTrue = 1
	TestFalse = 0
	TestDefault = -1

class jdbc_connections(Model):
	__bind_key__ = 'DBImport'

	dbalias = Column(String(256), nullable=False, primary_key=True)
	private_key_path = Column(String(128), nullable=True)
	public_key_path = Column(String(128), nullable=True)
	jdbc_url = Column(String(1024), nullable=False)
	credentials = Column(String(1024), nullable=True)
	datalake_source = Column(String(256), nullable=True)
	force_string = Column(Integer, ForeignKey('true_false_default_01.id'), nullable=False, default=1)
	force_string_ref = relationship("true_false_default_01")
#	force_string = Column(Integer, nullable=False, default=-1)
#	force_string = Column(Enum("0", "1", name="TrueFalseDefault"), default="TestTrue")
#	force_string = Column(Enum("TestTrue", "TestFalse", name="TrueFalseDefault"))
#	force_string = Column(Enum(0, 1, name="TrueFalseDefault"))
#	force_string = Column(ENUM(-1, 0, 1))
	create_datalake_import = Column(Integer, ForeignKey('true_false_default_02.id'), nullable=False, default=1)
	create_datalake_import_ref = relationship("true_false_default_02")
#	create_datalake_import = Column(Integer, nullable=False, default=1) 
#	timewindow_start = Column(Time, nullable=True)
	timewindow_start = Column(String(20), nullable=True)
	timewindow_stop = Column(String(20), nullable=True)
	operator_notes = Column(TEXT, nullable=True)

	def __repr__(self):
		return self.dbalias

	@validates('timewindow_start', 'timewindow_stop')
	def validate_time(self, key, timeWindow):
		try:
			time.strptime(timeWindow, '%H:%M:%S')
			return timeWindow
		except ValueError:
			return None
#		if timeWindow == "":
#			return None
#		if not re.match("^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]$", timeWindow):
#			return None
#		return timeWindow

	@validates('operator_notes')
	def validate_operator_notes(self, key, operator_notes):
		if len(operator_notes) > 5:
			operator_notes = operator_notes[:5]
		return operator_notes

class import_tables(Model):
	__bind_key__ = 'DBImport'
	hive_db = Column(String(256), nullable=False)
	hive_table = Column(String(256), nullable=False)
	table_id = Column(Integer, nullable=False, primary_key=True)
	dbalias = Column(String(256), ForeignKey('jdbc_connections.dbalias'), nullable=False)
	dbalias_ref = relationship("jdbc_connections")
	source_schema = Column(String(256), nullable=False)
	source_table = Column(String(256), nullable=False)
	import_type = Column(String(32), ForeignKey('import_type.id'), nullable=False, default='full')
	import_type_ref = relationship("import_type")
	last_update_from_source = Column(DateTime, nullable=True)
	sqoop_sql_where_addition = Column(String(1024), nullable=True)
	nomerge_ingestion_sql_addition = Column(String(2048), nullable=True)
	include_in_airflow = Column(Integer, ForeignKey('true_false_04.id'), nullable=False, default=1)
	include_in_airflow_ref = relationship("true_false_04")
	airflow_priority = Column(Integer, nullable=True)
	validate_import = Column(Integer, ForeignKey('true_false_01.id'), nullable=False, default=1)
	validate_import_ref = relationship("true_false_01")
	validate_diff_allowed = Column(BigInteger, nullable=False, default=-1)
	truncate_hive = Column(Integer, ForeignKey('true_false_03.id'), nullable=False, default=1)
	truncate_hive_ref = relationship("true_false_03")
	mappers = Column(Integer, nullable=False, default=-1)
	soft_delete_during_merge = Column(Integer, ForeignKey('true_false_05.id'), nullable=False, default=0)
	soft_delete_during_merge_ref = relationship("true_false_05")
	source_rowcount = Column(BigInteger, nullable=True)
	hive_rowcount = Column(BigInteger, nullable=True)
	incr_mode = Column(String(16), ForeignKey('incr_mode.id'), nullable=False, default="none")
	incr_mode_ref = relationship("incr_mode")
	incr_column = Column(String(256), nullable=True)
	incr_minvalue = Column(String(32), nullable=True)
	incr_maxvalue = Column(String(32), nullable=True)
	incr_minvalue_pending = Column(String(32), nullable=True)
	incr_maxvalue_pending = Column(String(32), nullable=True)
	pk_column_override = Column(String(1024), nullable=True)
	pk_column_override_mergeonly = Column(String(1024), nullable=True)
	hive_merge_heap = Column(Integer, nullable=True)
	concatenate_hive_table = Column(Integer, nullable=False, default=-1)
	sqoop_query = Column(TEXT, nullable=True)
	sqoop_options = Column(TEXT, nullable=True)
	sqoop_last_size = Column(BigInteger, nullable=True)
	sqoop_last_rows = Column(BigInteger, nullable=True)
	sqoop_last_execution = Column(BigInteger, nullable=True)
	sqoop_use_generated_sql = Column(Integer, ForeignKey('true_false_default_02.id'), nullable=False, default=-1)
	sqoop_use_generated_sql_ref = relationship("true_false_default_02")
	sqoop_allow_text_splitter = Column(Integer, ForeignKey('true_false_02.id'), nullable=False, default=0)
	sqoop_allow_text_splitter_ref = relationship("true_false_02")
	force_string = Column(Integer, ForeignKey('true_false_default_01.id'), nullable=False, default=-1)
	force_string_ref = relationship("true_false_default_01")
	comment = Column(TEXT, nullable=True)
	generated_hive_column_definition = Column(TEXT, nullable=True)
	generated_sqoop_query = Column(TEXT, nullable=True)
	generated_sqoop_options = Column(TEXT, nullable=True)
	generated_pk_columns = Column(TEXT, nullable=True)
	generated_foreign_keys = Column(TEXT, nullable=True)
	datalake_source = Column(String(256), nullable=True)
	operator_notes = Column(TEXT, nullable=True)

	def __repr__(self):
#		return self.table_id
		return "%s.%s" % (self.hive_db, self.hive_table)

class import_columns(Model):
	__bind_key__ = 'DBImport'
	table_id = Column(Integer, ForeignKey("import_tables.table_id"), nullable=False)
	table_id_ref = relationship("import_tables")
	column_id = Column(Integer, nullable=False, primary_key=True)
	column_order = Column(Integer, nullable=True)
	column_name = Column(String(256), nullable=False)
	hive_db = Column(String(256), nullable=True)
	hive_table = Column(String(256), nullable=True)
	source_column_name = Column(String(256), nullable=False)
	column_type = Column(String(2048), nullable=False)
	source_column_type = Column(String(2048), nullable=False)
	source_database_type = Column(String(256), nullable=True)
	sqoop_column_type = Column(String(256), nullable=True)
	force_string = Column(Integer, ForeignKey('true_false_default_01.id'), nullable=False, default=-1)
	force_string_ref = relationship("true_false_default_01")
	include_in_import = Column(Integer, ForeignKey('true_false_01.id'), nullable=False, default=1)
	include_in_import_ref = relationship("true_false_01")
	source_primary_key = Column(Integer, nullable=True)
	last_update_from_source = Column(DateTime, nullable=False)
	comment = Column(TEXT, nullable=True)
	operator_notes = Column(TEXT, nullable=True)

	def __repr__(self):
		return self.column_name

class import_type(Model):
	__bind_key__ = 'memory'
	id = Column(String(32), primary_key=True)
	name = Column(String(50), unique=True, nullable=False)

	def __repr__(self):
		return self.name

class incr_mode(Model):
	__bind_key__ = 'memory'
	id = Column(String(16), primary_key=True)
	name = Column(String(50), unique=True, nullable=False)

	def __repr__(self):
		return self.name

class true_false_01(Model):
	__bind_key__ = 'memory'
	id = Column(Integer, primary_key=True)
	name = Column(String(50), unique=True, nullable=False)

	def __repr__(self):
		return self.name

class true_false_02(Model):
	__bind_key__ = 'memory'
	id = Column(Integer, primary_key=True)
	name = Column(String(50), unique=True, nullable=False)

	def __repr__(self):
		return self.name

class true_false_03(Model):
	__bind_key__ = 'memory'
	id = Column(Integer, primary_key=True)
	name = Column(String(50), unique=True, nullable=False)

	def __repr__(self):
		return self.name

class true_false_04(Model):
	__bind_key__ = 'memory'
	id = Column(Integer, primary_key=True)
	name = Column(String(50), unique=True, nullable=False)

	def __repr__(self):
		return self.name

class true_false_05(Model):
	__bind_key__ = 'memory'
	id = Column(Integer, primary_key=True)
	name = Column(String(50), unique=True, nullable=False)

	def __repr__(self):
		return self.name

class true_false_default_01(Model):
	__bind_key__ = 'memory'
	id = Column(Integer, primary_key=True)
	name = Column(String(50), unique=True, nullable=False)

	def __repr__(self):
		return self.name

class true_false_default_02(Model):
	__bind_key__ = 'memory'
	id = Column(Integer, primary_key=True)
	name = Column(String(50), unique=True, nullable=False)

	def __repr__(self):
		return self.name

