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
            X_adv_cnw = cnw.attack(confidence=args.cnw_confidence)
            ret_status, report_util = utility.evaluate_aes('cnw', classifier, X_adv_cnw, y_test, acc_benign,
                                                           sampling_idx, report_util)
        # Jacobian Saliency Map Attack.
        elif args.attack_evasion == 'jsma':
            jsma = JSMA(utility=utility, model=classifier, dataset=X_test)
            X_adv_jsma = jsma.attack(theta=args.theta, gamma=args.gamma)
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
            defence_classifier = at.fit(at_classifier,
                                        X_train,
                                        y_train,
                                        X_test,
                                        y_test,
                                        batch_size=args.adversarial_training_batch_size,
                                        epochs=args.adversarial_training_epochs,
                                        shuffle=args.adversarial_training_shuffle)

            # Save model.
            utility.save_model(defence_classifier, 'at_model.h5')

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

    # Show banner.
    show_banner(utility)

    # Parse arguments.
    parser = argparse.ArgumentParser(description='Adversarial Threat Detector.')
    parser.add_argument('--model_name', default='', type=str, help='Target model name.')
    parser.add_argument('--train_data_name', default='X_train.npz', type=str, help='Training dataset name.')
    parser.add_argument('--test_data_name', default='X_test.npz', type=str, help='Test dataset name.')
    parser.add_argument('--use_x_train_num', default=10000, type=int, help='Dataset number for X_train.')
    parser.add_argument('--use_x_test_num', default=1000, type=int, help='Dataset number for X_test.')
    parser.add_argument('--train_label_name', default='y_train.npz', type=str, help='Train label name.')
    parser.add_argument('--test_label_name', default='y_test.npz', type=str, help='Test label name.')
    parser.add_argument('--op_type', default='', choices=['attack', 'defence'], type=str, help='operation type.')

    # Attack.
    parser.add_argument('--attack_type', default='evasion',
                        choices=['data_poisoning', 'model_poisoning', 'evasion', 'exfiltration'],
                        type=str, help='Specify attack type.')

    parser.add_argument('--attack_data_poisoning', default='feature_collision',
                        choices=['feature_collision', 'convex_polytope', 'bullseye_polytope'],
                        type=str, help='Specify method of Data Poisoning Attack.')

    parser.add_argument('--attack_model_poisoning', default='node_injection',
                        choices=['node_injection', 'layer_injection'],
                        type=str, help='Specify method of Poisoning Attack.')

    parser.add_argument('--attack_evasion', default='fgsm', choices=['fgsm', 'cnw', 'jsma'],
                        type=str, help='Specify method of Evasion Attack.')
    parser.add_argument('--fgsm_epsilon', default=0.05, choices=[0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3],
                        type=float, help='Specify Eps for FGSM.')
    parser.add_argument('--cnw_confidence', default=0.5, choices=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                        type=float, help='Specify Confidence for C&W.')
    parser.add_argument('--jsma_theta', default=0.1, choices=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                        type=float, help='Specify Theta for JSMA.')
    parser.add_argument('--jsma_gamma', default=1.0, choices=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                        type=float, help='Specify Gamma for JSMA.')

    parser.add_argument('--attack_exfiltration', default='membership_inference',
                        choices=['membership_inference', 'label_only', 'inversion'],
                        type=str, help="Specify method of Exfiltration Attack.")

    # Defence.
    parser.add_argument('--defence_type', default='evasion',
                        choices=['data_poisoning', 'model_poisoning', 'evasion', 'exfiltration'],
                        type=str, help='Specify defence type.')

    parser.add_argument('--defence_evasion', default='adversarial_training',
                        choices=['adversarial_training', 'feature_squeezing', 'jpeg_compression'],
                        type=str, help='Specify defence method against Evasion Attack.')
    parser.add_argument('--adversarial_training_attack', default='fgsm', choices=['fgsm', 'cnw', 'jsma'],
                        type=str, help='Specify attack method for Adversarial Training.')
    parser.add_argument('--adversarial_training_ratio', default=0.5, choices=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
                        type=float, help='Specify ratio for Adversarial Training.')
    parser.add_argument('--adversarial_training_batch_size', default=128, choices=[32, 64, 128, 256, 512],
                        type=int, help='Specify batch size for Adversarial Training.')
    parser.add_argument('--adversarial_training_epochs', default=30, choices=[10, 20, 30, 40, 50],
                        type=int, help='Specify epochs for Adversarial Training.')
    parser.add_argument('--adversarial_training_shuffle', default=True, choices=[True, False],
                        type=bool, help='Specify shuffle for Adversarial Training.')

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
    report_util.make_report_dir()
    sampling_idx = utility.random_sampling(data_size=len(X_test), sample_num=report_util.adv_sample_num)
    benign_sample_list = report_util.make_image(X_test, 'benign', sampling_idx)

    # Data to report's template.
    report_util.template_target['model_path'] = model_path
    report_util.template_target['dataset_path'] = x_test_path
    report_util.template_target['label_path'] = y_test_path
    report_util.template_target['dataset_num'] = len(X_test)
    for (sample_path, elem) in zip(benign_sample_list, report_util.template_target['dataset_img'].keys()):
        report_util.template_target['dataset_img'][elem] = sample_path

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

        # Execute scanning.
        ret_status, report_util = attack(utility, args, classifier, X_test, y_test, report_util)

        # Create ipynb report.
        report_ipynb.report_util = report_util
        report_ipynb.lang = args.lang
        report_util = report_ipynb.create_report()

        # Create HTML report.
        report_html.report_util = report_util
        report_html.lang = args.lang
        report_html.create_report()
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
