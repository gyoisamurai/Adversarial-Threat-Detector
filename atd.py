#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time
import argparse
import configparser

# ATD modules.
from attacks.evasion import FGSM, CarliniL2, JSMA
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
    utility.write_log(20, '[In] Adversarial Threat Detector [{}].'.format(file_name))

    # Show banner.
    show_banner(utility)

    # Parse arguments.
    parser = argparse.ArgumentParser(description='Adversarial Threat Detector.')
    parser.add_argument('--model_name', default='', type=str, help='Target model name.')
    parser.add_argument('--dataset_name', default='', type=str, help='Dataset name.')
    parser.add_argument('--label_name', default='', type=str, help='Label name.')
    parser.add_argument('--attack_type', default='evasion', choices=['all', 'poisoning', 'evasion', 'inference'],
                        type=str, help='Specify attack type.')
    parser.add_argument('--poisoning_method', default='fc', choices=['fc', 'cp'],
                        type=str, help='Specify method of Poisoning Attack.')
    parser.add_argument('--evasion_method', default='fgsm', choices=['fgsm', 'cnw', 'jsma'],
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
    X_test, y_test = utility.load_dataset(args.dataset_name, args.label_name)

    # Evaluate evasion attacks.
    if args.attack_type == 'all':
        utility.print_message(WARNING, 'Not implementation: {}'.format(args.attack_type))
    # Poisoning Attacks.
    elif args.attack_type == 'poisoning':
        utility.print_message(WARNING, 'Not implementation: {}'.format(args.attack_type))
    # Evasion Attacks.
    elif args.attack_type == 'evasion':
        # Fast Gradient Signed Method.
        if args.evasion_method == 'fgsm':
            classifier = utility.wrap_classifier(model, X_test)
            evasion = FGSM(utility=utility, model=classifier, dataset=X_test)
            X_adv = evasion.attack(eps=0.05)
            utility.evaluate(classifier, X_adv=X_adv, X_test=X_test, y_test=y_test)
        # Carlini and Wagner Attack.
        elif args.evasion_method == 'cnw':
            classifier = utility.wrap_classifier(model, X_test)
            evasion = CarliniL2(utility=utility, model=classifier, dataset=X_test)
            X_adv = evasion.attack(confidence=0.5)
            utility.evaluate(classifier, X_adv=X_adv, X_test=X_test, y_test=y_test)
        # Jacobian Saliency Map Attack.
        elif args.evasion_method == 'jsma':
            classifier = utility.wrap_classifier(model, X_test)
            evasion = JSMA(utility=utility, model=classifier, dataset=X_test)
            X_adv = evasion.attack(theta=0.1, gamma=1.0)
            utility.evaluate(classifier, X_adv=X_adv, X_test=X_test, y_test=y_test)
    # Inference Attacks.
    elif args.attack_type == 'inference':
        utility.print_message(WARNING, 'Not implementation: {}'.format(args.attack_type))

    print(os.path.basename(__file__) + ' Done!!')
    utility.write_log(20, '[Out] Adversarial Threat Detector [{}].'.format(file_name))
