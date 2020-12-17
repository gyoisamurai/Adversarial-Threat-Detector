#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import configparser

# Type of printing.
OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.


# Utility.
class ReportUtility:
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
            self.base_path = os.path.join(self.root_path, config['Report']['base_path'])
            self.report_path = os.path.join(self.base_path, config['Report']['report_path'])
            self.report_name = config['Report']['report_name']
            self.template = config['Report']['template_name']
            self.adv_sample_num = int(config['Report']['adv_sample_num'])
        except Exception as e:
            self.utility.print_message(FAIL, 'Reading config.ini is failure : {}'.format(e))
            self.utility.write_log(40, 'Reading config.ini is failure : {}'.format(e))
            sys.exit(1)

        # Saved list for Adversarial Examples.
        self.save_adv_list = []
        self.adv_image_path = ''

    # Make report directory.
    def make_report_dir(self):
        # Make directory.
        self.report_path = self.report_path.replace('*', self.utility.get_current_date(indicate_format='%Y%m%d%H%M%S'))
        self.adv_image_path = os.path.join(self.report_path, 'img')
        os.makedirs(self.report_path, exist_ok=False)
        os.makedirs(self.adv_image_path, exist_ok=False)

    # Make image file for Adversarial Examples.
    def make_image(self, X_adv, method, sampling_idx):
        for count_idx, adv_idx in enumerate(sampling_idx):
            self.save_adv_list.append(self.utility.save_adv_images(count_idx, method, X_adv[adv_idx], self.report_path))
