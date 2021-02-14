#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import time
import argparse
import configparser

# ATD modules.
from attacks.evasion import FGSM, CarliniL2, JSMA
from reports import ReportUtility, HtmlReport, IpynbReport
from util import Utilty

# Type of printing.
OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.


# Display banner.
def show_banner(utility):
    banner = """
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 █████╗ ██████╗ ██╗   ██╗███████╗██████╗ ███████╗ █████╗ ██████╗ ██╗ █████╗ ██╗     
██╔══██╗██╔══██╗██║   ██║██╔════╝██╔══██╗██╔════╝██╔══██╗██╔══██╗██║██╔══██╗██║     
███████║██║  ██║██║   ██║█████╗  ██████╔╝███████╗███████║██████╔╝██║███████║██║     
██╔══██║██║  ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██╔══██║██╔══██╗██║██╔══██║██║     
██║  ██║██████╔╝ ╚████╔╝ ███████╗██║  ██║███████║██║  ██║██║  ██║██║██║  ██║███████╗
╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝
            ████████╗██╗  ██╗██████╗ ███████╗ █████╗ ████████╗                      
            ╚══██╔══╝██║  ██║██╔══██╗██╔════╝██╔══██╗╚══██╔══╝                      
               ██║   ███████║██████╔╝█████╗  ███████║   ██║                         
               ██║   ██╔══██║██╔══██╗██╔══╝  ██╔══██║   ██║                         
               ██║   ██║  ██║██║  ██║███████╗██║  ██║   ██║                         
               ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝                         
    ██████╗ ███████╗████████╗███████╗ ██████╗████████╗ ██████╗ ██████╗              
    ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗             
    ██║  ██║█████╗     ██║   █████╗  ██║        ██║   ██║   ██║██████╔╝             
    ██║  ██║██╔══╝     ██║   ██╔══╝  ██║        ██║   ██║   ██║██╔══██╗             
    ██████╔╝███████╗   ██║   ███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║             
    ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝      (beta)

  Powered by Adversarial Robustness Toolbox (ART)
  https://github.com/Trusted-AI/adversarial-robustness-toolbox
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
""" + 'by ' + os.path.basename(__file__)
    utility.print_message(NONE, banner)
    show_credit(utility)
    time.sleep(utility.banner_delay)


# Show credit.
def show_credit(utility):
    credit = u"""
       =[ Adversarial Threat Detector v0.0.1-beta                              ]=
+ -- --=[ Author  : Isao Takaesu (@bbr_bbq)                                    ]=--
+ -- --=[ Website : https://github.com/gyoisamurai/Adversarial-Threat-Detector ]=--
    """
    utility.print_message(NONE, credit)


# main.
if __name__ == '__main__':
    file_name = os.path.basename(__file__)
    full_path = os.path.dirname(os.path.abspath(__file__))

    utility = Utilty()
    report_util = ReportUtility(utility)
    report_html = HtmlReport(utility)
    report_ipynb = IpynbReport(utility)
    utility.write_log(20, '[In] Adversarial Threat Detector [{}].'.format(file_name))

    # Show banner.
    show_banner(utility)

    # Parse arguments.
    parser = argparse.ArgumentParser(description='Adversarial Threat Detector.')
    parser.add_argument('--model_name', default='', type=str, help='Target model name.')
    parser.add_argument('--dataset_name', default='', type=str, help='Dataset name.')
    parser.add_argument('--use_dataset_num', default=100, type=int, help='Dataset number for test.')
    parser.add_argument('--label_name', default='', type=str, help='Label name.')
    parser.add_argument('--attack_type', default='evasion', choices=['all', 'data_poisoning', 'model_poisoning',
                                                                     'evasion', 'exfiltration'],
                        type=str, help='Specify attack type.')
    parser.add_argument('--data_poisoning_method', default='fc', choices=['fc', 'cp'],
                        type=str, help='Specify method of Data Poisoning Attack.')
    parser.add_argument('--model_poisoning_method', default='node_injection',
                        choices=['node_injection', 'layer_injection'],
                        type=str, help='Specify method of Poisoning Attack.')
    parser.add_argument('--evasion_method', default='fgsm', choices=['all', 'fgsm', 'cnw', 'jsma'],
                        type=str, help='Specify method of Evasion Attack.')
    parser.add_argument('--exfiltration_method', default='mi', choices=['mi', 'label_only', 'inversion'],
                        type=str, help="Specify method of Exfiltration Attack.")
    parser.add_argument('--lang', default='en', choices=['en', 'ja'], type=str, help='Specify language of report.')
    args = parser.parse_args()
    print(args)

    #  Read config.ini.
    config = configparser.ConfigParser()
    config.read(os.path.join(full_path, 'config.ini'))

    # Load target model.
    ret_status, model_path, model = utility.load_model(args.model_name)
    if ret_status is False:
        utility.write_log(20, '[Out] Adversarial Threat Detector [{}].'.format(file_name))
        sys.exit(0)

    # Load dataset.
    ret_status, dataset_path, label_path, X_test, y_test = utility.load_dataset(args.dataset_name, args.label_name, args.use_dataset_num)
    if ret_status is False:
        utility.write_log(20, '[Out] Adversarial Threat Detector [{}].'.format(file_name))
        sys.exit(0)

    # Report setting.
    report_util.make_report_dir()
    sampling_idx = utility.random_sampling(data_size=len(X_test), sample_num=report_util.adv_sample_num)
    benign_sample_list = report_util.make_image(X_test, 'benign', sampling_idx)

    # Data to report's template.
    report_util.template_target['model_path'] = model_path
    report_util.template_target['dataset_path'] = dataset_path
    report_util.template_target['label_path'] = label_path
    report_util.template_target['dataset_num'] = len(X_test)
    for (sample_path, elem) in zip(benign_sample_list, report_util.template_target['dataset_img'].keys()):
        report_util.template_target['dataset_img'][elem] = sample_path

    # Scan setting.
    ret_status, classifier = utility.wrap_classifier(model, X_test)
    if ret_status is False:
        utility.write_log(20, '[Out] Adversarial Threat Detector [{}].'.format(file_name))
        sys.exit(0)

    # Accuracy on Benign Examples.
    ret_status, acc_benign = utility.evaluate(classifier, X_test=X_test, y_test=y_test)
    if ret_status is False:
        utility.write_log(20, '[Out] Adversarial Threat Detector [{}].'.format(file_name))
        sys.exit(0)
    else:
        utility.print_message(OK, 'Accuracy on Benign Examples : {}%'.format(acc_benign * 100))
        report_util.template_target['accuracy'] = '{}%'.format(acc_benign * 100)

    # Evaluate all attacks.
    if args.attack_type == 'all':
        utility.print_message(WARNING, 'Not implementation: {}'.format(args.attack_type))
    # Evaluate Data Poisoning Attacks.
    elif args.attack_type == 'data_poisoning':
        utility.print_message(WARNING, 'Not implementation: {}'.format(args.attack_type))
    # Evaluate Model Poisoning Attacks.
    elif args.attack_type == 'model_poisoning':
        utility.print_message(WARNING, 'Not implementation: {}'.format(args.attack_type))
    # Evaluate Evasion Attacks.
    elif args.attack_type == 'evasion':
        report_util.template_evasion['exist'] = True
        # All methods.
        if args.evasion_method == 'all':
            # FGSM.
            fgsm = FGSM(utility=utility, model=classifier, dataset=X_test)
            X_adv_fgsm = fgsm.attack(eps=0.05)
            ret_status, report_util = utility.evaluate_aes('fgsm', classifier, X_adv_fgsm, y_test, acc_benign,
                                                           sampling_idx, report_util)

            # C&W.
            cnw = CarliniL2(utility=utility, model=classifier, dataset=X_test)
            X_adv_cnw = cnw.attack(confidence=0.5)
            ret_status, report_util = utility.evaluate_aes('cnw', classifier, X_adv_cnw, y_test, acc_benign,
                                                           sampling_idx, report_util)

            # JSMA.
            jsma = JSMA(utility=utility, model=classifier, dataset=X_test)
            X_adv_jsma = jsma.attack(theta=0.1, gamma=1.0)
            ret_status, report_util = utility.evaluate_aes('jsma', classifier, X_adv_jsma, y_test, acc_benign,
                                                           sampling_idx, report_util)
        # Fast Gradient Signed Method.
        if args.evasion_method == 'fgsm':
            fgsm = FGSM(utility=utility, model=classifier, dataset=X_test)
            X_adv_fgsm = fgsm.attack(eps=0.05)
            ret_status, report_util = utility.evaluate_aes('fgsm', classifier, X_adv_fgsm, y_test, acc_benign,
                                                           sampling_idx, report_util)
        # Carlini and Wagner Attack.
        elif args.evasion_method == 'cnw':
            cnw = CarliniL2(utility=utility, model=classifier, dataset=X_test)
            X_adv_cnw = cnw.attack(confidence=0.5)
            ret_status, report_util = utility.evaluate_aes('cnw', classifier, X_adv_cnw, y_test, acc_benign,
                                                           sampling_idx, report_util)
        # Jacobian Saliency Map Attack.
        elif args.evasion_method == 'jsma':
            jsma = JSMA(utility=utility, model=classifier, dataset=X_test)
            X_adv_jsma = jsma.attack(theta=0.1, gamma=1.0)
            ret_status, report_util = utility.evaluate_aes('jsma', classifier, X_adv_jsma, y_test, acc_benign,
                                                           sampling_idx, report_util)
    # Evaluate Exfiltration Attacks.
    elif args.attack_type == 'exfiltration':
        utility.print_message(WARNING, 'Not implementation: {}'.format(args.attack_type))

    # Create ipynb report.
    report_ipynb.report_util = report_util
    report_ipynb.lang = args.lang
    report_util = report_ipynb.create_report()

    # Create HTML report.
    report_html.report_util = report_util
    report_html.lang = args.lang
    report_html.create_report()

    print(os.path.basename(__file__) + ' Done!!')
    utility.write_log(20, '[Out] Adversarial Threat Detector [{}].'.format(file_name))
