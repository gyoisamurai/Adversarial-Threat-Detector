#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import configparser
import pandas as pd
import jinja2

# Type of printing.
OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.


# Create report.
class HtmlReport:
    def __init__(self, utility, report_utility):
        self.utility = utility
        self.report_util = report_utility

        # Read config file.
        config = configparser.ConfigParser()
        self.file_name = os.path.basename(__file__)
        self.full_path = os.path.dirname(os.path.abspath(__file__))
        self.root_path = os.path.join(self.full_path, '../')
        config.read(os.path.join(self.root_path, 'config.ini'))

        # Saved list for Adversarial Examples.
        self.save_adv_list = []

    # Create report.
    def create_report(self, poisoning=False, evasion=False, inference = False):
        # Setting template.
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.report_util.base_path))
        template = env.get_template(self.report_util.template)
        pd.set_option('display.max_colwidth', -1)
        html = template.render()
        report_full_path = os.path.join(self.report_util.report_path, self.report_util.report_name)

        # Flush html to report.
        with open(report_full_path, 'w') as fout:
            fout.write(html)
        self.utility.print_message(WARNING, 'Created report: {}'.format(report_full_path))
