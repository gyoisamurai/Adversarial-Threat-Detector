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
    def __init__(self, utility):
        self.utility = utility
        self.report_util = None

        # Read config file.
        config = configparser.ConfigParser()
        self.file_name = os.path.basename(__file__)
        self.full_path = os.path.dirname(os.path.abspath(__file__))
        self.root_path = os.path.join(self.full_path, '../')
        config.read(os.path.join(self.root_path, 'config.ini'))

        # Language for report.
        self.lang = ''

        # model/dataset path.
        self.model_path = ''
        self.dataset_path = ''
        self.label_path = ''
        self.dataset_num = 0

    # Create common part.
    def create_common(self, nb):
        self.utility.print_message(OK, 'Creating common part...')
        # Introduction.
        if self.lang == 'en':
            nb['cells'] = [
                nbformat.v4.new_markdown_cell(Common.md_report_title.value),
                nbformat.v4.new_markdown_cell(Common.md_1_1_title.value),
                nbformat.v4.new_markdown_cell(Common.md_1_1_text.value),
                nbformat.v4.new_markdown_cell(Common.md_1_2_title.value),
                nbformat.v4.new_markdown_cell(Common.md_1_2_text.value)
            ]
        else:
            nb['cells'] = [
                nbformat.v4.new_markdown_cell(Common.md_report_title.value),
                nbformat.v4.new_markdown_cell(Common.md_1_1_title_ja.value),
                nbformat.v4.new_markdown_cell(Common.md_1_1_text_ja.value),
                nbformat.v4.new_markdown_cell(Common.md_1_2_title_ja.value),
                nbformat.v4.new_markdown_cell(Common.md_1_2_text_ja.value)
            ]

        # Preparation
        if self.lang == 'en':
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
        else:
            nb['cells'].extend([nbformat.v4.new_markdown_cell(Common.md_2_title_ja.value),
                                nbformat.v4.new_markdown_cell(Common.md_2_text_ja.value),
                                nbformat.v4.new_markdown_cell(Common.md_2_1_title_ja.value),
                                nbformat.v4.new_markdown_cell(Common.md_2_1_text_ja.value),
                                nbformat.v4.new_code_cell(Common.cd_2_1_code_ja.value),
                                nbformat.v4.new_markdown_cell(Common.md_2_2_title_ja.value),
                                nbformat.v4.new_markdown_cell(Common.md_2_2_text_ja.value),
                                nbformat.v4.new_code_cell(Common.cd_2_2_code_ja.value.format(self.dataset_path,
                                                                                             self.dataset_num,
                                                                                             self.label_path)),
                                nbformat.v4.new_markdown_cell(Common.md_2_3_title_ja.value),
                                nbformat.v4.new_markdown_cell(Common.md_2_3_text_ja.value),
                                nbformat.v4.new_code_cell(Common.cd_2_3_code_ja.value.format(self.model_path)),
                                nbformat.v4.new_markdown_cell(Common.md_2_4_title_ja.value),
                                nbformat.v4.new_markdown_cell(Common.md_2_4_text_ja.value),
                                nbformat.v4.new_code_cell(Common.cd_2_4_code_ja.value),
                                ])

        self.utility.print_message(OK, 'Done creating common part.')
        return nb

    # Create evasion (FGSM) part.
    def create_evasion_fgsm(self, nb, aes_path):
        self.utility.print_message(OK, 'Creating Evasion (FGSM) part...')

        # FGSM.
        if self.lang == 'en':
            nb['cells'].extend([nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_title.value),
                                nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_text.value),
                                nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_fgsm_1_title.value),
                                nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_fgsm_1_text.value),
                                nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_fgsm_2_title.value),
                                nbformat.v4.new_code_cell(EvasionAttack.cd_ae_fgsm_2_code.value.format(aes_path)),
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
        else:
            nb['cells'].extend([nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_title_ja.value),
                                nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_text_ja.value),
                                nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_fgsm_1_title_ja.value),
                                nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_fgsm_1_text_ja.value),
                                nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_fgsm_2_title_ja.value),
                                nbformat.v4.new_code_cell(EvasionAttack.cd_ae_fgsm_2_code_ja.value.format(aes_path)),
                                nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_fgsm_3_title_ja.value),
                                nbformat.v4.new_code_cell(
                                    EvasionAttack.cd_ae_fgsm_3_code_ja.value.format(self.dataset_num)),
                                nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_fgsm_4_title_ja.value),
                                nbformat.v4.new_code_cell(EvasionAttack.cd_ae_fgsm_4_code_ja.value),
                                nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_fgsm_5_title_ja.value),
                                nbformat.v4.new_code_cell(EvasionAttack.cd_ae_fgsm_5_code_ja.value),
                                nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_fgsm_6_title_ja.value),
                                nbformat.v4.new_code_cell(EvasionAttack.cd_ae_fgsm_6_code_ja.value),
                                nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_fgsm_7_title_ja.value),
                                nbformat.v4.new_markdown_cell(EvasionAttack.md_ae_fgsm_7_text_ja.value),
                                ])

        self.utility.print_message(OK, 'Done Evasion (FGSM) part...')
        return nb

    # Create report.
    def create_report(self):
        self.utility.print_message(NOTE, 'Creating report...')
        nb = nbformat.v4.new_notebook()

        # Report Setting.
        self.model_path = self.report_util.template_target['model_path']
        self.dataset_path = self.report_util.template_target['dataset_path']
        self.label_path = self.report_util.template_target['label_path']
        self.dataset_num = self.report_util.template_target['dataset_num']

        # Create common part.
        nb = self.create_common(nb)

        # Create replay part.
        report_name = ''
        report_full_path = ''
        if self.report_util.template_data_poisoning['exist']:
            self.utility.print_message(WARNING, 'Not implementation.')
        elif self.report_util.template_model_poisoning['exist']:
            self.utility.print_message(WARNING, 'Not implementation.')
        elif self.report_util.template_evasion['exist']:
            if self.report_util.template_evasion['fgsm']['exist']:
                # Create FGSM.
                report_name = 'evasion_fgsm.ipynb'
                nb = self.create_evasion_fgsm(nb, self.report_util.template_evasion['fgsm']['aes_path'])
                report_full_path = os.path.join(self.report_util.report_path, report_name)
                with open(report_full_path, 'w') as fout:
                    nbformat.write(nb, fout)
                self.report_util.template_evasion['fgsm']['ipynb_path'] = report_full_path
            if self.report_util.template_evasion['cnw']['exist']:
                # Create C&W.
                self.utility.print_message(WARNING, 'Not implementation.')
            if self.report_util.template_evasion['jsma']['exist']:
                # Create JSMA.
                self.utility.print_message(WARNING, 'Not implementation.')
        elif self.report_util.template_exfiltration['exist']:
            self.utility.print_message(WARNING, 'Not implementation.')

        self.utility.print_message(NOTE, 'Done creating report.')
        return self.report_util, report_name
