#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time
import argparse
import configparser

# ATD modules.
from attacks.evasion import FGSM, CarliniL2, JSMA
from reports.create_report import CreateReport
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
    report = CreateReport(utility)
    utility.write_log(20, '[In] Adversarial Threat Detector [{}].'.format(file_name))

    # Show banner.
    show_banner(utility)

    # Parse arguments.
    parser = argparse.ArgumentParser(description='Adversarial Threat Detector.')
    parser.add_argument('--model_name', default='', type=str, help='Target model name.')
    parser.add_argument('--dataset_name', default='', type=str, help='Dataset name.')
    parser.add_argument('--use_dataset_num', default=100, type=int, help='Dataset number for test.')
    parser.add_argument('--label_name', default='', type=str, help='Label name.')
    parser.add_argument('--attack_type', default='evasion', choices=['all', 'poisoning', 'evasion', 'inference'],
                        type=str, help='Specify attack type.')
    parser.add_argument('--poisoning_method', default='fc', choices=['fc', 'cp'],
                        type=str, help='Specify method of Poisoning Attack.')
    parser.add_argument('--evasion_method', default='fgsm', choices=['all', 'fgsm', 'cnw', 'jsma'],
                        type=str, help='Specify method of Evasion Attack.')
    parser.add_argument('--inference_method', default='mi', choices=['mi', 'label_only'],
                        type=str, help="Specify method of Membership Inference Attack.")
    args = parser.parse_args()
    print(args)

    #  Read config.ini.
    config = configparser.ConfigParser()
    config.read(os.path.join(full_path, 'config.ini'))

    # Load target model and dataset.
    model = utility.load_model(args.model_name)
    X_test, y_test = utility.load_dataset(args.dataset_name, args.label_name, args.use_dataset_num)
    report.make_report_dir()
    sampling_idx = utility.random_sampling(data_size=len(X_test), sample_num=report.adv_sample_num)
    report.make_image(X_test, 'benign', sampling_idx)

    # Wrap classifier.
    classifier = utility.wrap_classifier(model, X_test)

    # Evaluate evasion attacks.
    if args.attack_type == 'all':
        utility.print_message(WARNING, 'Not implementation: {}'.format(args.attack_type))
    # Poisoning Attacks.
    elif args.attack_type == 'poisoning':
        utility.print_message(WARNING, 'Not implementation: {}'.format(args.attack_type))
    # Evasion Attacks.
    elif args.attack_type == 'evasion':
        # Accuracy on Benign Examples.
        accuracy = utility.evaluate(classifier, X_test=X_test, y_test=y_test)
        utility.print_message(OK, 'Accuracy on Benign Examples : {}%'.format(accuracy * 100))

        # All methods.
        if args.evasion_method == 'all':
            # FGSM.
            evasion = FGSM(utility=utility, model=classifier, dataset=X_test)
            X_adv_fgsm = evasion.attack(eps=0.05)
            acc_fgsm = utility.evaluate(classifier, X_test=X_adv_fgsm, y_test=y_test)
            utility.print_message(WARNING, 'Accuracy on AEs (FGSM)      : {}%'.format(acc_fgsm * 100))
            report.make_image(X_adv_fgsm, 'fgsm', sampling_idx)

            # CnW.
            evasion = CarliniL2(utility=utility, model=classifier, dataset=X_test)
            X_adv_cnw = evasion.attack(confidence=0.5)
            acc_cnw = utility.evaluate(classifier, X_test=X_adv_cnw, y_test=y_test)
            utility.print_message(WARNING, 'Accuracy on AEs (C&W)       : {}%'.format(acc_cnw * 100))
            report.make_image(X_adv_cnw, 'cnw', sampling_idx)

            # JSMA.
            evasion = JSMA(utility=utility, model=classifier, dataset=X_test)
            X_adv_jsma = evasion.attack(theta=0.1, gamma=1.0)
            acc_jsma = utility.evaluate(classifier, X_test=X_adv_jsma, y_test=y_test)
            utility.print_message(WARNING, 'Accuracy on AEs (JSMA)      : {}%'.format(acc_jsma * 100))
            report.make_image(X_adv_jsma, 'jsma', sampling_idx)
        # Fast Gradient Signed Method.
        if args.evasion_method == 'fgsm':
            evasion = FGSM(utility=utility, model=classifier, dataset=X_test)
            X_adv_fgsm = evasion.attack(eps=0.05)
            acc_fgsm = utility.evaluate(classifier, X_test=X_adv_fgsm, y_test=y_test)
            utility.print_message(WARNING, 'Accuracy on AEs (FGSM)      : {}%'.format(acc_fgsm * 100))
            report.make_image(X_adv_fgsm, 'fgsm', sampling_idx)
        # Carlini and Wagner Attack.
        elif args.evasion_method == 'cnw':
            evasion = CarliniL2(utility=utility, model=classifier, dataset=X_test)
            X_adv_cnw = evasion.attack(confidence=0.5)
            acc_cnw = utility.evaluate(classifier, X_test=X_adv_cnw, y_test=y_test)
            utility.print_message(WARNING, 'Accuracy on AEs (C&W)       : {}%'.format(acc_cnw * 100))
            report.make_image(X_adv_cnw, 'cnw', sampling_idx)
        # Jacobian Saliency Map Attack.
        elif args.evasion_method == 'jsma':
            evasion = JSMA(utility=utility, model=classifier, dataset=X_test)
            X_adv_jsma = evasion.attack(theta=0.1, gamma=1.0)
            acc_jsma = utility.evaluate(classifier, X_test=X_adv_jsma, y_test=y_test)
            utility.print_message(WARNING, 'Accuracy on AEs (JSMA)      : {}%'.format(acc_jsma * 100))
            report.make_image(X_adv_jsma, 'jsma', sampling_idx)
    # Inference Attacks.
    elif args.attack_type == 'inference':
        utility.print_message(WARNING, 'Not implementation: {}'.format(args.attack_type))

    # Create report.
    report.create_report()

    print(os.path.basename(__file__) + ' Done!!')
    utility.write_log(20, '[Out] Adversarial Threat Detector [{}].'.format(file_name))
