#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import configparser
import pandas as pd
import numpy as np
import jinja2

# Type of printing.
OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.


# Create report.
class CreateReport:
    def __init__(self, utility):
        self.utility = utility
        # Read config file.
        config = configparser.ConfigParser()
        self.file_name = os.path.basename(__file__)
        self.full_path = os.path.dirname(os.path.abspath(__file__))
        self.root_path = os.path.join(self.full_path, '../')
        config.read(os.path.join(self.root_path, 'config.ini'))

        try:
            self.report_file_name = ''
            self.report_dir = os.path.join(self.root_path, config['Report']['report_path'])
            self.report_path = os.path.join(self.report_dir, config['Report']['report_name'])
            self.template_path = os.path.join(self.report_dir, config['Report']['report_name'])
        except Exception as e:
            self.utility.print_message(FAIL, 'Reading config.ini is failure : {}'.format(e))
            self.utility.write_log(40, 'Reading config.ini is failure : {}'.format(e))
            sys.exit(1)

    # Create report
    def create_report(self, fqdn, port):
        # Setting template.
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.report_dir))
        template = env.get_template(self.template_path)
        pd.set_option('display.max_colwidth', -1)
        html = template.render({'title': 'ATD Report', 'items': items})
        self.report_path = self.report_path.replace('*', self.utility.get_current_date(indicate_format='%Y%m%d%H%M%S'))

        with open(self.report_path, 'w') as fout:
            fout.write(html)
