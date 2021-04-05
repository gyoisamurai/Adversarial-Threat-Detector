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
from defences.trainer.adversarial_training import Adversarial_Training
from util import Utilty
from sql import DbControl

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


# Attacks.
def attack(utility, args, classifier, X_test, y_test, report_util):
    ret_status = True

    # Evaluate Data Poisoning Attacks.
    if args.attack_type == 'data_poisoning':
        utility.print_message(WARNING, 'Not implementation: {}'.format(args.attack_type))
    # Evaluate Model Poisoning Attacks.
    elif args.attack_type == 'model_poisoning':
        utility.print_message(WARNING, 'Not implementation: {}'.format(args.attack_type))
    # Evaluate Evasion Attacks.
    elif args.attack_type == 'evasion':
        report_util.template_evasion['exist'] = True

        # Fast Gradient Signed Method.
        if args.attack_evasion == 'fgsm':
            fgsm = FGSM(utility=utility, model=classifier, dataset=X_test)
            fgsm_attack = fgsm.evasion(eps=args.fgsm_epsilon)
            X_adv_fgsm = fgsm.attack(fgsm_attack)
            ret_status, report_util = utility.evaluate_aes('fgsm', classifier, X_adv_fgsm, y_test, acc_benign,
                                                           sampling_idx, report_util)
        # Carlini and Wagner Attack.
        elif args.attack_evasion == 'cnw':
            cnw = CarliniL2(utility=utility, model=classifier, dataset=X_test)
            X_adv_cnw = cnw.attack(confidence=args.cnw_confidence, batch_size=args.cnw_batch_size)
            ret_status, report_util = utility.evaluate_aes('cnw', classifier, X_adv_cnw, y_test, acc_benign,
                                                           sampling_idx, report_util)
        # Jacobian Saliency Map Attack.
        elif args.attack_evasion == 'jsma':
            jsma = JSMA(utility=utility, model=classifier, dataset=X_test)
            X_adv_jsma = jsma.attack(theta=args.jsma_theta, gamma=args.jsma_gamma, batch_size=args.jsma_batch_size)
            ret_status, report_util = utility.evaluate_aes('jsma', classifier, X_adv_jsma, y_test, acc_benign,
                                                           sampling_idx, report_util)
    # Evaluate Exfiltration Attacks.
    elif args.attack_type == 'exfiltration':
        utility.print_message(WARNING, 'Not implementation: {}'.format(args.attack_type))

    return ret_status, report_util


# Defences.
def defence(utility, args, classifier, X_train, y_train, X_test, y_test, report_util):
    ret_status = True

    # Defence against Data Poisoning Attacks.
    if args.defence_type == 'data_poisoning':
        utility.print_message(WARNING, 'Not implementation: {}'.format(args.defence_type))
    # Defence against Model Poisoning Attacks.
    elif args.defence_type == 'model_poisoning':
        utility.print_message(WARNING, 'Not implementation: {}'.format(args.defence_type))
    # Defence againstEvasion Attacks.
    elif args.defence_type == 'evasion':
        # Adversarial Training.
        if args.defence_evasion == 'adversarial_training':
            attacks = None
            if args.adversarial_training_attack == 'fgsm':
                fgsm = FGSM(utility=utility, model=classifier, dataset=X_test)
                attacks = fgsm.evasion(eps=args.fgsm_epsilon)
            elif args.adversarial_training_attack == 'cnw':
                attacks = CarliniL2(utility=utility, model=classifier, dataset=X_test)
            else:
                attacks = JSMA(utility=utility, model=classifier, dataset=X_test)

            at = Adversarial_Training(utility)
            at_classifier = at.trainer(classifier, attacks, ratio=args.adversarial_training_ratio)
            at.fit(at_classifier,
                   X_train,
                   y_train,
                   X_test,
                   y_test,
                   batch_size=args.adversarial_training_batch_size,
                   epochs=args.adversarial_training_epochs,
                   shuffle=args.adversarial_training_shuffle)

            # Save model.
            utility.save_model(classifier, 'at_model.h5')

        # Feature Squeezing.
        elif args.defence_evasion == 'feature_squeezing':
            utility.print_message(WARNING, 'Not implementation: {}'.format(args.defence_evasion))
        # JPEG Compression.
        elif args.defence_evasion == 'jpeg_compression':
            utility.print_message(WARNING, 'Not implementation: {}'.format(args.defence_evasion))
    # Defence against Exfiltration Attacks.
    elif args.defence_type == 'exfiltration':
        utility.print_message(WARNING, 'Not implementation: {}'.format(args.defence_type))

    return ret_status, report_util


# main.
if __name__ == '__main__':
    file_name = os.path.basename(__file__)
    full_path = os.path.dirname(os.path.abspath(__file__))

    utility = Utilty()
    report_util = ReportUtility(utility)
    report_html = HtmlReport(utility)
    report_ipynb = IpynbReport(utility)
    utility.write_log(20, '[In] Adversarial Threat Detector [{}].'.format(file_name))

    # Initialize Database.
    utility.sql = DbControl(utility)

    # Show banner.
    show_banner(utility)

    # Parse arguments.
    parser = argparse.ArgumentParser(description='Adversarial Threat Detector.')
    parser.add_argument('--target_id', default='', type=int, help='Target\'s identifier for GyoiBoard.')
    parser.add_argument('--scan_id', default='', type=str, help='Scan\'s identifier for GyoiBoard.')
    parser.add_argument('--model_name', default='', type=str, help='Target model name.')
    parser.add_argument('--train_data_name', default='X_train.npz', type=str, help='Training dataset name.')
    parser.add_argument('--test_data_name', default='X_test.npz', type=str, help='Test dataset name.')
    parser.add_argument('--use_x_train_num', default=10000, type=int, help='Dataset number for X_train.')
    parser.add_argument('--use_x_test_num', default=1000, type=int, help='Dataset number for X_test.')
    parser.add_argument('--train_label_name', default='y_train.npz', type=str, help='Train label name.')
    parser.add_argument('--test_label_name', default='y_test.npz', type=str, help='Test label name.')
    parser.add_argument('--op_type', default='', choices=['attack', 'defence'], type=str, help='operation type.')

    # Attack.
    parser.add_argument('--attack_type', default='',
                        choices=['data_poisoning', 'model_poisoning', 'evasion', 'exfiltration'],
                        type=str, help='Specify attack type.')

    parser.add_argument('--attack_data_poisoning', default='',
                        choices=['feature_collision', 'convex_polytope', 'bullseye_polytope'],
                        type=str, help='Specify method of Data Poisoning Attack.')

    parser.add_argument('--attack_model_poisoning', default='',
                        choices=['node_injection', 'layer_injection'],
                        type=str, help='Specify method of Poisoning Attack.')

    parser.add_argument('--attack_evasion', default='', choices=['fgsm', 'cnw', 'jsma'],
                        type=str, help='Specify method of Evasion Attack.')
    parser.add_argument('--fgsm_epsilon', default=0.05, choices=[0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3],
                        type=float, help='Specify Epsilon for FGSM.')
    parser.add_argument('--fgsm_eps_step', default=0.1, choices=[0.1, 0.2, 0.3, 0.4, 0.5],
                        type=float, help='Specify Epsilon step for FGSM.')
    parser.add_argument('--fgsm_targeted', action='store_true', help='Specify targeted evasion for FGSM.')
    parser.add_argument('--fgsm_batch_size', default=32, type=int, help='Specify batch size for FGSM.')
    parser.add_argument('--cnw_confidence', default=0.0, choices=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                        type=float, help='Specify Confidence for C&W.')
    parser.add_argument('--cnw_batch_size', default=1, type=int, help='Specify batch size for CnW.')
    parser.add_argument('--jsma_theta', default=0.1, choices=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                        type=float, help='Specify Theta for JSMA.')
    parser.add_argument('--jsma_gamma', default=1.0, choices=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                        type=float, help='Specify Gamma for JSMA.')
    parser.add_argument('--jsma_batch_size', default=1, type=int, help='Specify batch size for JSMA.')

    parser.add_argument('--attack_exfiltration', default='',
                        choices=['membership_inference', 'label_only', 'inversion'],
                        type=str, help="Specify method of Exfiltration Attack.")

    # Defence.
    parser.add_argument('--defence_type', default='',
                        choices=['data_poisoning', 'model_poisoning', 'evasion', 'exfiltration'],
                        type=str, help='Specify defence type.')

    parser.add_argument('--defence_evasion', default='',
                        choices=['adversarial_training', 'feature_squeezing', 'jpeg_compression'],
                        type=str, help='Specify defence method against Evasion Attack.')
    parser.add_argument('--adversarial_training_attack', default='', choices=['fgsm', 'cnw', 'jsma'],
                        type=str, help='Specify attack method for Adversarial Training.')
    parser.add_argument('--adversarial_training_ratio', default=0.5, choices=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
                        type=float, help='Specify ratio for Adversarial Training.')
    parser.add_argument('--adversarial_training_batch_size', default=128, choices=[32, 64, 128, 256, 512],
                        type=int, help='Specify batch size for Adversarial Training.')
    parser.add_argument('--adversarial_training_epochs', default=30, choices=[10, 20, 30, 40, 50],
                        type=int, help='Specify epochs for Adversarial Training.')
    parser.add_argument('--adversarial_training_shuffle', action='store_true',
                        help='Specify shuffle for Adversarial Training.')

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

    # Load test data.
    ret_status, x_test_path, y_test_path, X_test, y_test = utility.load_dataset(args.test_data_name,
                                                                                args.test_label_name,
                                                                                args.use_x_test_num)

    if ret_status is False:
        utility.write_log(20, '[Out] Adversarial Threat Detector [{}].'.format(file_name))
        sys.exit(0)

    # Report setting.
    report_path = report_util.make_report_dir()
    sampling_idx = utility.random_sampling(data_size=len(X_test), sample_num=report_util.adv_sample_num)
    benign_sample_list = report_util.make_image(X_test, 'benign', sampling_idx)

    # Data to report's template.
    report_util.template_target['model_path'] = model_path
    report_util.template_target['dataset_path'] = x_test_path
    report_util.template_target['label_path'] = y_test_path
    report_util.template_target['dataset_num'] = len(X_test)
    for (sample_path, elem) in zip(benign_sample_list, report_util.template_target['dataset_img'].keys()):
        report_util.template_target['dataset_img'][elem] = sample_path

    # Insert scan record.
    if args.scan_id != '':
        # Set attack's method.
        attack_method = ''
        if args.attack_type == 'data_poisoning':
            attack_method = args.attack_data_poisoning
        elif args.attack_type == 'model_poisoning':
            attack_method = args.attack_model_poisoning
        elif args.attack_type == 'evasion':
            attack_method = args.attack_evasion
            utility.insert_new_scan_record_evasion(args.target_id, args.scan_id, attack_method)
            if args.attack_evasion == 'fgsm':
                # Insert values to FGSM table.
                utility.insert_new_scan_record_fgsm(args.target_id,
                                                    args.scan_id,
                                                    args.fgsm_epsilon,
                                                    args.fgsm_eps_step,
                                                    args.fgsm_targeted,
                                                    args.fgsm_batch_size)
            elif args.attack_evasion == 'cnw':
                # Insert values to CnW table.
                utility.insert_new_scan_record_cnw(args.target_id,
                                                   args.scan_id,
                                                   args.cnw_confidence,
                                                   args.cnw_batch_size)
            elif args.attack_evasion == 'jsma':
                # Insert values to JSMA table.
                utility.insert_new_scan_record_jsma(args.target_id,
                                                    args.scan_id,
                                                    args.jsma_theta,
                                                    args.jsma_gamma,
                                                    args.jsma_batch_size)
        elif args.attack_type == 'exfiltration':
            attack_method = args.attack_exfiltration

        # Set defence's method.
        # TODO: ディフェンスタイプを設定すること。
        defence_method = ''
        if args.defence_type == 'data_poisoning':
            defence_method = args.attack_data_poisoning
        elif args.defence_type == 'model_poisoning':
            defence_method = args.attack_model_poisoning
        elif args.defence_type == 'evasion':
            defence_method = args.attack_evasion
        elif args.defence_type == 'exfiltration':
            defence_method = args.attack_exfiltration

        # Insert values to Common table.
        utility.insert_new_scan_record(args.target_id,
                                       args.scan_id,
                                       'Scanning',
                                       args.model_name,
                                       args.train_data_name,
                                       args.use_x_train_num,
                                       args.train_label_name,
                                       args.test_data_name,
                                       args.use_x_test_num,
                                       args.test_label_name,
                                       args.op_type,
                                       args.attack_type,
                                       attack_method,
                                       args.defence_type,
                                       defence_method,
                                       utility.get_current_date(),
                                       args.lang)

    # Preparation.
    ret_status, classifier = utility.wrap_classifier(model, X_test)
    if ret_status is False:
        utility.write_log(20, '[Out] Adversarial Threat Detector [{}].'.format(file_name))
        sys.exit(0)

    # Attack or Defence.
    if args.op_type == 'attack':
        # Accuracy on Benign Examples.
        ret_status, acc_benign = utility.evaluate(classifier, X_test=X_test, y_test=y_test)
        if ret_status is False:
            utility.write_log(20, '[Out] Adversarial Threat Detector [{}].'.format(file_name))
            sys.exit(0)
        else:
            utility.print_message(OK, 'Accuracy on Benign Examples : {}%'.format(acc_benign * 100))
            report_util.template_target['accuracy'] = '{}%'.format(acc_benign * 100)
            utility.update_accuracy(args.scan_id, acc_benign * 100)

        # Execute scanning.
        ret_status, report_util = attack(utility, args, classifier, X_test, y_test, report_util)

        # Create ipynb report.
        report_ipynb.report_util = report_util
        report_ipynb.lang = args.lang
        report_util, report_ipynb_name = report_ipynb.create_report()

        # Create HTML report.
        report_html.report_util = report_util
        report_html.lang = args.lang
        report_html.create_report()

        # Update tables.
        if args.scan_id != '':
            # Update scan status, rank, summary, report path so on.
            utility.update_status(args.scan_id, 'Done')
            utility.update_rank_summary(args.scan_id,
                                        report_html.report_util.template_target['rank'],
                                        report_html.report_util.template_target['summary'])
            utility.update_report_path(args.scan_id,
                                       report_path,
                                       report_html.report_util.report_name,
                                       report_ipynb_name)
            utility.update_exec_end_date(args.scan_id, utility.get_current_date())

            if args.attack_type == 'data_poisoning':
                # TODO: Data Poisoningのレコードを追加すること。
                # Insert values to data poisoning table.
                utility.print_message(WARNING, 'Not implementation: {}'.format(args.attack_type))
            elif args.attack_type == 'model_poisoning':
                # TODO: Model Poisoningのレコードを追加すること。
                # Insert values to model poisoning table.
                utility.print_message(WARNING, 'Not implementation: {}'.format(args.attack_type))
            elif args.attack_type == 'evasion':
                utility.update_consequence_evasion(args.scan_id,
                                                   report_html.report_util.template_evasion['consequence'],
                                                   report_html.report_util.template_evasion['summary'],
                                                   report_html.report_util.template_evasion['accuracy'])
            elif args.attack_type == 'exfiltration':
                # TODO: Exfiltrationのレコードを追加すること。
                # Insert values to exfiltration table.
                utility.print_message(WARNING, 'Not implementation: {}'.format(args.attack_type))
    elif args.op_type == 'defence':
        # Load test data.
        ret_status, _, _, X_train, y_train = utility.load_dataset(args.train_data_name,
                                                                  args.train_label_name,
                                                                  args.use_x_train_num)

        if ret_status is False:
            utility.write_log(20, '[Out] Adversarial Threat Detector [{}].'.format(file_name))
            sys.exit(0)

        defence(utility, args, classifier, X_train, y_train, X_test, y_test, report_util)
    else:
        utility.print_message(WARNING, 'Invalid operation type: {}'.format(args.op_type))
        sys.exit(0)

    print(os.path.basename(__file__) + ' Done!!')
    utility.write_log(20, '[Out] Adversarial Threat Detector [{}].'.format(file_name))
