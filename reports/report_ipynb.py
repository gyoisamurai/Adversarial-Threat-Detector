#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import configparser
import nbformat
from .static_text import Common, EvasionAttack

# Type of printing.
OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.


# Create report.
class IpynbReport:
    def __init__(self, utility, report_util):
        self.utility = utility
        self.report_util = report_util

        # Read config file.
        config = configparser.ConfigParser()
        self.file_name = os.path.basename(__file__)
        self.full_path = os.path.dirname(os.path.abspath(__file__))
        self.root_path = os.path.join(self.full_path, '../')
        config.read(os.path.join(self.root_path, 'config.ini'))

        # model/dataset path.
        self.model_path = ''
        self.dataset_path = ''
        self.label_path = ''
        self.dataset_num = 0
        self.adv_path = ''

    # Create common part.
    def create_common(self, nb):
        self.utility.print_message(OK, 'Creating common part...')
        # Introduction.
        nb['cells'] = [
            nbformat.v4.new_markdown_cell(Common.md_report_title.value),
            nbformat.v4.new_markdown_cell(Common.md_1_1_title.value),
            nbformat.v4.new_markdown_cell(Common.md_1_1_text.value),
            nbformat.v4.new_markdown_cell(Common.md_1_2_title.value),
            nbformat.v4.new_markdown_cell(Common.md_1_2_text.value)
        ]

        # Preparation
        nb['cells'].extend([nbformat.v4.new_markdown_cell(Common.md_2_title.value),
                            nbformat.v4.new_markdown_cell(Common.md_2_text.value),
                            nbformat.v4.new_markdown_cell(Common.md_2_1_title.value),
                            nbformat.v4.new_markdown_cell(Common.md_2_1_text.value),
                            nbformat.v4.new_code_cell(Common.cd_2_1_code.value),
                            nbformat.v4.new_markdown_cell(Common.md_2_2_title.value),
                            nbformat.v4.new_markdown_cell(Common.md_2_2_text.value),
                            nbformat.v4.new_code_cell(Common.cd_2_2_code.value.format(self.dataset_path,
                                                                                      self.dataset_num,
                                                                                      self.label_path)),
                            nbformat.v4.new_markdown_cell(Common.md_2_3_title.value),
                            nbformat.v4.new_markdown_cell(Common.md_2_3_text.value),
                            nbformat.v4.new_code_cell(Common.cd_2_3_code.value.format(self.model_path)),
                            nbformat.v4.new_markdown_cell(Common.md_2_4_title.value),
                            nbformat.v4.new_markdown_cell(Common.md_2_4_text.value),
                            nbformat.v4.new_code_cell(Common.cd_2_4_code.value),
                            ])
        self.utility.print_message(OK, 'Done creating common part.')
        return nb

    # Create evasion (FGSM) part.
    def create_evasion_fgsm(self, nb):
        self.utility.print_message(OK, 'Creating Evasion (FGSM) part...')

        # FGSM.
        nb['cells'].extend([nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_title.value),
                            nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_text.value),
                            nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_fgsm_1_title.value),
                            nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_fgsm_1_text.value),
                            nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_fgsm_2_title.value),
                            nbformat.v4.new_code_cell(EvasionAttack.cd_ae_fgsm_2_code.value.format(self.adv_path)),
                            nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_fgsm_3_title.value),
                            nbformat.v4.new_code_cell(EvasionAttack.cd_ae_fgsm_3_code.value.format(self.dataset_num)),
                            nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_fgsm_4_title.value),
                            nbformat.v4.new_code_cell(EvasionAttack.cd_ae_fgsm_4_code.value),
                            nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_fgsm_5_title.value),
                            nbformat.v4.new_code_cell(EvasionAttack.cd_ae_fgsm_5_code.value),
                            nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_fgsm_6_title.value),
                            nbformat.v4.new_code_cell(EvasionAttack.cd_ae_fgsm_6_code.value),
                            nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_fgsm_7_title.value),
                            nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_fgsm_7_text.value),
                            ])

        self.utility.print_message(OK, 'Done Evasion (FGSM) part...')
        return nb

    # Create report.
    def create_report(self, poisoning=False, evasion=False, inference=False):
        self.utility.print_message(NOTE, 'Creating report...')
        nb = nbformat.v4.new_notebook()

        # Create common part.
        nb = self.create_common(nb)

        # Create replay part.
        if poisoning:
            self.utility.print_message(WARNING, 'Not implementation.')
        elif evasion:
            # Create FGSM.
            nb = self.create_evasion_fgsm(nb)

            # Create ipynb file for Evasion Attack.
            report_full_path = os.path.join(self.report_util.report_path, 'evasion_fgsm.ipynb')
            with open(report_full_path, 'w') as fout:
                nbformat.write(nb, fout)
        elif inference:
            self.utility.print_message(WARNING, 'Not implementation.')

        self.utility.print_message(NOTE, 'Done creating report.')
