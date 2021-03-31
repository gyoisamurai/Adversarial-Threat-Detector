#!/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import configparser
import sqlite3


# Type of printing.
OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.


# Database control class.
class DbControl:
    def __init__(self, utility):
        self.file_name = os.path.basename(__file__)
        self.full_path = os.path.dirname(os.path.abspath(__file__))
        self.utility = utility

        # Read config.ini.
        full_path = os.path.dirname(os.path.abspath(__file__))
        config = configparser.ConfigParser()
        config.read(os.path.join(full_path, 'config.ini'), encoding='utf-8')

        try:
            db_path = os.path.join(full_path, config['DB']['db_path'])
            os.makedirs(db_path, exist_ok=True)
            self.db_file = os.path.join(db_path, config['DB']['db_file'])
            self.con_timeout = int(config['DB']['con_timeout'])
            self.isolation_level = config['DB']['isolation_level']

            # Create or connect to database.
            self.conn = None
            if os.path.exists(self.db_file) is False:
                # Create table.
                self.db_initialize('scan_result')
            else:
                # Create connection.
                self.conn = sqlite3.connect(self.db_file,
                                            timeout=self.con_timeout,
                                            isolation_level=self.isolation_level)
        except Exception as e:
            self.utility.print_message(FAIL, 'Reading config.ini is failure : {}'.format(e))
            sys.exit(1)

        # Query templates.
        self.state_select = 'SELECT * FROM ScanResultTBL WHERE status = ?'
        self.state_select_id = 'SELECT * FROM ScanResultTBL WHERE scan_id = ?'
        self.state_insert = 'INSERT INTO ScanResultTBL (' \
                            'scan_id,' \
                            'status,' \
                            'rank,' \
                            'target_path,' \
                            'x_train_path,' \
                            'x_train_num,' \
                            'y_train_path,' \
                            'x_test_path,' \
                            'x_test_num,' \
                            'y_test_path,' \
                            'operation_type,' \
                            'attack_type,' \
                            'attack_method,' \
                            'defence_type,' \
                            'defence_method,' \
                            'exec_start_date,' \
                            'exec_end_date,' \
                            'report_path, ' \
                            'report_html,' \
                            'report_ipynb,' \
                            'lang) VALUES (?,?,"Weak",?,?,?,?,?,?,?,?,?,?,?,?,?,"","","","",?)'
        self.state_update_status = 'UPDATE ScanResultTBL SET status = ? WHERE scan_id = ?'
        self.state_update_exec_end_date = 'UPDATE ScanResultTBL SET exec_end_date = ? WHERE scan_id = ?'
        self.state_update_report_path = 'UPDATE ScanResultTBL ' \
                                        'SET ' \
                                        'report_path = ?,' \
                                        'report_html = ?,' \
                                        'report_ipynb = ?' \
                                        'WHERE scan_id = ?'
        self.state_delete = 'DELETE FROM ScanResultTBL WHERE scan_id = ?'
        self.state_delete_all = 'DELETE FROM ScanResultTBL'

    # Initialize Data base.
    def db_initialize(self, db_name):
        self.utility.write_log(20, '[In] Initialize Data base [{}].'.format(self.file_name))

        if db_name == 'scan_result':
            with sqlite3.connect(self.db_file,
                                 timeout=self.con_timeout,
                                 isolation_level=self.isolation_level) as conn:
                sql_query = ''
                try:
                    # Create table.
                    sql_query = 'CREATE TABLE IF NOT EXISTS ScanResultTBL(' \
                                'id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
                                'scan_id TEXT, ' \
                                'status TEXT, ' \
                                'rank TEXT, ' \
                                'target_path TEXT, ' \
                                'x_train_path TEXT, ' \
                                'x_train_num INTEGER, ' \
                                'y_train_path TEXT, '\
                                'x_test_path TEXT, '\
                                'x_test_num INTEGER, '\
                                'y_test_path TEXT, '\
                                'operation_type TEXT, '\
                                'attack_type TEXT, ' \
                                'attack_method TEXT, ' \
                                'defence_type TEXT, ' \
                                'defence_method TEXT, ' \
                                'exec_start_date TEXT, ' \
                                'exec_end_date TEXT, '\
                                'report_path, ' \
                                'report_html TEXT, ' \
                                'report_ipynb TEXT, ' \
                                'lang TEXT);'
                    conn.execute('begin transaction')
                    conn.execute(sql_query)
                    conn.commit()
                    self.conn = conn
                except Exception as e:
                    self.utility.print_message(FAIL, 'Could not create {} table: {}'.format(db_name, sql_query))
                    self.utility.print_exception(e, '')
                    self.utility.write_log(20, '[Out] Initialize Data base [{}].'.format(self.file_name))
                    sys.exit(1)
        else:
            self.utility.print_message(FAIL, 'Indicator {} is unknown.'.format(db_name))
            self.utility.write_log(20, '[Out] Initialize Data base [{}].'.format(self.file_name))
            sys.exit(1)

        self.utility.write_log(20, '[Out] Initialize Data base [{}].'.format(self.file_name))
        return

    # Execute INSERT query.
    def insert(self, conn, sql_query, params):
        self.utility.write_log(20, '[In] Execute INSERT query [{}].'.format(self.file_name))
        conn.execute('begin transaction')
        conn.execute(sql_query, params)
        conn.commit()
        self.utility.write_log(20, '[Out] Execute INSERT query [{}].'.format(self.file_name))

    # Execute UPDATE query.
    def update(self, conn, sql_query, params):
        self.utility.write_log(20, '[In] Execute UPDATE query [{}].'.format(self.file_name))
        conn.execute('begin transaction')
        conn.execute(sql_query, params)
        conn.commit()
        self.utility.write_log(20, '[Out] Execute UPDATE query [{}].'.format(self.file_name))

    # Execute DELETE query.
    def delete(self, conn, sql_query, params=()):
        self.utility.write_log(20, '[In] Execute DELETE query [{}].'.format(self.file_name))
        conn.execute('begin transaction')
        conn.execute(sql_query, params)
        conn.commit()
        self.utility.write_log(20, '[Out] Execute DELETE query [{}].'.format(self.file_name))

    # Execute SELECT query.
    def select(self, conn, sql_query, params=()):
        self.utility.write_log(20, '[In] Execute SELECT query [{}].'.format(self.file_name))
        cursor = conn.cursor()
        cursor.execute(sql_query, params)
        self.utility.write_log(20, '[Out] Execute SELECT query [{}].'.format(self.file_name))
        return cursor
