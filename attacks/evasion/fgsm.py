#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import configparser
from art.attacks.evasion import FastGradientMethod

# Type of printing.
OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.


# Fast Gradient Signed Method.
class FGSM:
    def __init__(self, utility, model, dataset):
        # Read config.ini.
        full_path = os.path.dirname(os.path.abspath(__file__))
        config = configparser.ConfigParser()
        config.read(os.path.join(full_path, 'config.ini'))
        self.utility = utility

        # Set target model and dataset.
        self.model = model
        self.dataset = dataset

    # Create Adversarial Examples.
    def attack(self, eps=0.05):
        # Create Adversarial Examples using FGSM.
        self.utility.print_message(NOTE, 'Creating Adversarial Examples using FGSM.')
        attack = FastGradientMethod(estimator=self.model, eps=eps)
        X_adv = attack.generate(x=self.dataset)
        return X_adv
