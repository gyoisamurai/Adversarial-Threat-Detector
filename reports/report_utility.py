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
            self.template_ja = config['Report']['template_name_ja']
            self.adv_sample_num = 5
        except Exception as e:
            self.utility.print_message(FAIL, 'Reading config.ini is failure : {}'.format(e))
            self.utility.write_log(40, 'Reading config.ini is failure : {}'.format(e))
            sys.exit(1)

        # Saved path of Adversarial Examples.
        self.adv_image_path = ''

        # Define report contents.
        self.template_target = {'rank': '', 'summary': '', 'model_path': '', 'dataset_path': '', 'label_path': '',
                                'dataset_num': 0, 'accuracy': '',
                                'dataset_img': {'img1': '', 'img2': '', 'img3': '', 'img4': '', 'img5': ''}}
        self.template_data_poisoning = {'exist': False, 'consequence': 'Secure', 'summary': '',
                                        'fc': {'exist': False, 'date': '', 'consequence': '', 'ipynb_path': ''},
                                        'cp': {'exist': False, 'date': '', 'consequence': '', 'ipynb_path': ''}}
        self.template_model_poisoning = {'exist': False, 'consequence': 'Secure', 'summary': '',
                                         'node_injection': {'exist': False, 'date': '', 'consequence': '', 'ipynb_path': ''},
                                         'layer_injection': {'exist': False, 'date': '', 'consequence': '', 'ipynb_path': ''}}
        self.template_evasion = {'exist': False, 'consequence': 'Secure', 'summary': '', 'accuracy': '',
                                 'fgsm': {'exist': False, 'date': '', 'consequence': 'Secure',
                                          'ipynb_path': '', 'aes_path': '',
                                          'ae_img': {'img1': '', 'img2': '', 'img3': '', 'img4': '', 'img5': ''}},
                                 'cnw': {'exist': False, 'date': '', 'consequence': 'Secure',
                                         'ipynb_path': '', 'aes_path': '',
                                         'ae_img': {'img1': '', 'img2': '', 'img3': '', 'img4': '', 'img5': ''}},
                                 'jsma': {'exist': False, 'date': '', 'consequence': 'Secure',
                                          'ipynb_path': '', 'aes_path': '',
                                          'ae_img': {'img1': '', 'img2': '', 'img3': '', 'img4': '', 'img5': ''}}}
        self.template_exfiltration = {'exist': False, 'consequence': 'Secure', 'summary': '',
                                      'mi': {'exist': False, 'date': '', 'consequence': '', 'ipynb_path': ''},
                                      'label_only_mi': {'exist': False, 'date': '', 'consequence': '', 'ipynb_path': ''},
                                      'model_inversion': {'exist': False, 'date': '', 'consequence': '', 'ipynb_path': ''}}

    # Make report directory.
    def make_report_dir(self):
        # Make directory.
        self.report_path = self.report_path.replace('*', self.utility.get_current_date(indicate_format='%Y%m%d%H%M%S'))
        self.adv_image_path = os.path.join('.', 'img')
        os.makedirs(self.report_path, exist_ok=False)
        os.makedirs(os.path.join(self.report_path, self.adv_image_path), exist_ok=False)
        return self.report_path

    # Make image file for Adversarial Examples.
    def make_image(self, X_adv, method, sampling_idx):
        save_path_list = []
        for count_idx, adv_idx in enumerate(sampling_idx):
            save_path_list.append(self.utility.save_adv_images(count_idx,
                                                               method,
                                                               X_adv[adv_idx],
                                                               self.report_path,
                                                               self.adv_image_path))
        return save_path_list
