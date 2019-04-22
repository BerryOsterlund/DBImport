from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from flask_appbuilder import AppBuilder, expose, BaseView, has_access
from flask import render_template
from webadmin import appbuilder, db
from wtforms.validators import DataRequired, EqualTo
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.forms import DynamicForm
from flask_appbuilder import SimpleFormView
from flask_babel import lazy_gettext as _
from flask import flash
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
# from .models import ContactGroup, Gender, Contact, jdbc_connections, true_false_default
# from .models import ContactGroup, Gender, Contact, jdbc_connections, import_tables, true_false_default01, true_false_default02
from .models import *
from sqlalchemy.orm import validates

import calendar
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count

@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

class importColumnsView(ModelView):
	datamodel = SQLAInterface(import_columns)
	base_permissions = ['can_edit', 'can_list', 'can_show', 'can_delete']

	list_columns = ['column_name', 'column_type', 'include_in_import_ref']

	label_columns = {
		'hive_db':'Hive Database', 
		'hive_table':'Hive Table', 
		'include_in_import_ref':'Include column in import',
		'comment':'Column comment from source table',
		'source_column_name':'Column name on source system',
		'source_column_type':'Column type on source system',
		'source_database_type':'Database type',
		'sqoop_column_type':'Override column type in Sqoop',
		'force_string_ref':'Force all char columns to string in Hive',
	}

	show_fieldsets = [
		('General', {'fields': ['hive_db', 'hive_table', 'column_name', 'column_type', 'include_in_import_ref', 'comment', 'last_update_from_source' ]}),
		( 'Documentation', {'fields': ['operator_notes']}),
		('Source', {'fields': ['source_column_name', 'source_column_type', 'source_database_type' ], 'expanded': False}),
		('Sqoop', {'fields': ['sqoop_column_type' ], 'expanded': False}),
		('Hive', {'fields': ['force_string_ref' ], 'expanded': False}) ]

	edit_fieldsets = [
		('General', {'fields': [ 'include_in_import_ref']}),
		( 'Documentation', {'fields': ['operator_notes']}),
		('Sqoop', {'fields': ['sqoop_column_type' ], 'expanded': False}),
		('Hive', {'fields': ['force_string_ref' ], 'expanded': False}) ]

	add_fieldsets = edit_fieldsets
#   table_id = Column(Integer, ForeignKey("import_tables.table_id"), nullable=False)
#   table_id_ref = relationship("import_tables")
#   column_id = Column(Integer, nullable=False, primary_key=True)
#   column_order = Column(Integer, nullable=True)
#   column_name = Column(String(256), nullable=False)
#   hive_db = Column(String(256), nullable=True)
#   hive_table = Column(String(256), nullable=True)
#   source_column_name = Column(String(256), nullable=False)
#   column_type = Column(String(2048), nullable=False)
#   source_column_type = Column(String(2048), nullable=False)
#   source_database_type = Column(String(256), nullable=True)
#   sqoop_column_type = Column(String(256), nullable=True)
#   force_string = Column(Integer, nullable=False, default=-1)
#   include_in_import = Column(Integer, nullable=False, default=1)
#   source_primary_key = Column(Integer, nullable=True)
#   last_update_from_source = Column(DateTime, nullable=False)
#   comment = Column(TEXT, nullable=True)
#   operator_notes = Column(TEXT, nullable=True)


class importTablesView(ModelView):
	datamodel = SQLAInterface(import_tables)

	label_columns = {
		'dbalias_ref':'Connection name', 
		'hive_db':'Hive Database', 
		'hive_table':'Hive Table', 
		'import_type_ref':'Import method',
		'force_string_ref':'Force all char columns to string in Hive',
		'validate_import_ref':'Validate the import',
		'validate_diff_allowed':'How many rows are the validation allowed to diff? (-1 for auto calculation)',
		'incr_mode_ref':'Incremental mode',
		'incr_column':'Incremental column',
		'comment':'Table comment from source table',
		'mappers':'Number of parallel SQL sessions (-1 for auto)',
		'sqoop_use_generated_sql_ref':'Use the generated SQL to query the source system',
		'sqoop_allow_text_splitter_ref':'Allow split on text columns',
		'truncate_hive_ref':'Truncate Hive Target table before loading it',
		'include_in_airflow_ref':'Include table in Airflow DAG',
		'soft_delete_during_merge_ref':'In Merge operations, should the rows be marked as deleted instead of actually delete them',
		'pk_column_override_mergeonly':'Override Primary Key in Merge operations with these columns (comma separeted list of columns)',
		'nomerge_ingestion_sql_addition':'Add this to the SQL when copying from import to target table. Not used in Merge operations',
		'pk_column_override':'Override Primary Key (comma separeted list of columns)',
		'sqoop_sql_where_addition':'Where statement to use in Sqoop',
	}

	list_columns = ['hive_db', 'hive_table', 'import_type']

	show_fieldsets = [
		('General', {'fields': ['hive_db', 'hive_table', 'import_type_ref', 'dbalias_ref', 'source_schema', 'source_table', 'last_update_from_source', 'validate_import_ref', 'validate_diff_allowed', 'incr_mode_ref', 'incr_column' ]}),
		( 'Documentation', {'fields': ['operator_notes']}),
		('Sqoop', {'fields': ['sqoop_sql_where_addition', 'mappers', 'sqoop_query', 'sqoop_options', 'sqoop_use_generated_sql_ref', 'sqoop_allow_text_splitter_ref', 'generated_sqoop_query', 'generated_sqoop_options' ], 'expanded': False}),
		('Hive', {'fields': ['truncate_hive_ref', 'pk_column_override', 'force_string_ref', 'datalake_source', 'comment', 'nomerge_ingestion_sql_addition', 'generated_hive_column_definition', 'generated_pk_columns' ], 'expanded': False}),
		('Airflow', {'fields': ['include_in_airflow_ref', 'airflow_priority'], 'expanded': False}),
		('Merge', {'fields': ['hive_merge_heap', 'pk_column_override_mergeonly', 'soft_delete_during_merge_ref'], 'expanded': False}) ]

	edit_fieldsets = [
		('General', {'fields': ['hive_db', 'hive_table', 'import_type_ref', 'dbalias_ref', 'source_schema', 'source_table', 'validate_import_ref', 'validate_diff_allowed', 'incr_mode_ref', 'incr_column' ]}),
		('Documentation', {'fields': ['operator_notes']}),
		('Sqoop', {'fields': ['sqoop_sql_where_addition', 'mappers', 'sqoop_query', 'sqoop_options', 'sqoop_use_generated_sql_ref', 'sqoop_allow_text_splitter_ref' ], 'expanded': False}),
		('Hive', {'fields': ['truncate_hive_ref', 'pk_column_override', 'force_string_ref', 'datalake_source', 'nomerge_ingestion_sql_addition' ], 'expanded': False}),
		('Airflow', {'fields': ['include_in_airflow_ref', 'airflow_priority'], 'expanded': False}),
		('Merge', {'fields': ['hive_merge_heap', 'pk_column_override_mergeonly', 'soft_delete_during_merge_ref'], 'expanded': False}) ]

	add_fieldsets = edit_fieldsets

	related_views = [importColumnsView]

class JDBCConnectionsView(ModelView):
#	@has_access
	datamodel = SQLAInterface(jdbc_connections)

	label_columns = {
		'dbalias':'Connection name', 
		'jdbc_url':'JDBC URL', 
		'datalake_source':'datalake_source column value',
		'force_string_ref':'Force all char columns to string in Hive',
		'create_datalake_import_ref':'Create datalake_import column?',
		'timewindow_start':'Time Window Start',
		'timewindow_stop':'Time Window Stop',
	}

	search_columns = ['dbalias', 'jdbc_url', 'create_datalake_import_ref', 'force_string_ref', 'operator_notes']
	list_columns = ['dbalias', 'operator_notes']

	show_fieldsets = [
		('Connection Details', {'fields': ['dbalias', 'jdbc_url']}),
		('Import config', {'fields': ['datalake_source', 'force_string_ref', 'create_datalake_import_ref', 'timewindow_start', 'timewindow_stop']}),
		('Documentation', {'fields': ['operator_notes']}) ]

	edit_fieldsets = [
		('Connection Details', {'fields': ['dbalias', 'jdbc_url']}),
		('Import config', {'fields': ['datalake_source', 'force_string_ref', 'create_datalake_import_ref', 'timewindow_start', 'timewindow_stop']}),
		('Documentation', {'fields': ['operator_notes']}) ]

	add_fieldsets = [
		('Connection Details', {'fields': ['dbalias', 'jdbc_url']}),
		('Import config', {'fields': ['datalake_source', 'force_string_ref', 'create_datalake_import_ref', 'timewindow_start', 'timewindow_stop']}),
		('Documentation', {'fields': ['operator_notes']}) ]

	related_views = [importTablesView]
#	validators_columns = {'timewindow_start':[EqualTo('timewindow_stop',
#		message='fields must match')]}

#	def validate_timewindow_start(form, field):
#		if(field.data) > 2:
#			raise ValidationError("Longer than 2")

class importTypeChartView(GroupByChartView):
    datamodel = SQLAInterface(import_tables)
    chart_title = 'Import Types in use'

    definitions = [
        {
				'label': 'Import types',
            'group': 'import_type',
            'series': [(aggregate_count, 'import_type')]
        }
    ]

def fill_import_type():
	db.session.add(import_type(id="full", name="Full import"))
	db.session.add(import_type(id="full_direct", name="Full import (directly to Hive for old DBImport)"))
	db.session.add(import_type(id="full_merge_direct", name="Full import with merge"))
	db.session.add(import_type(id="full_merge_direct_history", name="Full import with merge and History table"))
	db.session.add(import_type(id="incr", name="Incremental import"))
	db.session.add(import_type(id="incr_merge_delete", name="Incremental import with merge"))
	db.session.add(import_type(id="incr_merge_delete_history", name="Incremental import with merge and History table"))
	db.session.add(import_type(id="incr_merge_direct", name="Incremental import with merge (old version)"))
	db.session.commit()

def fill_incr_mode():
	db.session.add(incr_mode(id="none", name='None'))
	db.session.add(incr_mode(id="append", name='Append'))
	db.session.add(incr_mode(id="last_modified", name='Last modified'))
	db.session.commit()

def fill_true_false_01():
	db.session.add(true_false_01(id=0, name='False'))
	db.session.add(true_false_01(id=1, name='True'))
	db.session.commit()

def fill_true_false_02():
	db.session.add(true_false_02(id=0, name='False'))
	db.session.add(true_false_02(id=1, name='True'))
	db.session.commit()

def fill_true_false_03():
	db.session.add(true_false_03(id=0, name='False'))
	db.session.add(true_false_03(id=1, name='True'))
	db.session.commit()

def fill_true_false_04():
	db.session.add(true_false_04(id=0, name='False'))
	db.session.add(true_false_04(id=1, name='True'))
	db.session.commit()

def fill_true_false_05():
	db.session.add(true_false_05(id=0, name='False'))
	db.session.add(true_false_05(id=1, name='True'))
	db.session.commit()

def fill_true_false_default_01():
	db.session.add(true_false_default_01(id=-1, name='Default'))
	db.session.add(true_false_default_01(id=0, name='False'))
	db.session.add(true_false_default_01(id=1, name='True'))
	db.session.commit()

def fill_true_false_default_02():
	db.session.add(true_false_default_02(id=-1, name='Default'))
	db.session.add(true_false_default_02(id=0, name='False'))
	db.session.add(true_false_default_02(id=1, name='True'))
	db.session.commit()

db.create_all()

appbuilder.add_view(JDBCConnectionsView,
	"Database connections",
	icon = "fa-database",
	category = "Common",
	category_icon = "fa-cog")

appbuilder.add_view(importTablesView,
	"Tables",
	icon = "fa-table",
	category = "Import",
	category_icon = "fa-level-down")

appbuilder.add_view(importColumnsView,
	"Columns",
	icon = "fa-columns",
	category = "Import",
	category_icon = "fa-level-down")

appbuilder.add_separator("Import")

appbuilder.add_view(importTypeChartView,
	"Import Types",
	icon = "fa-dashboard",
	category = "Import",
	category_icon = "fa-level-down")

fill_import_type()
fill_incr_mode()
fill_true_false_01()
fill_true_false_02()
fill_true_false_03()
fill_true_false_04()
fill_true_false_05()
fill_true_false_default_01()
fill_true_false_default_02()


