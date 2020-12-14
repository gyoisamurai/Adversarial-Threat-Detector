#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import configparser
from art.attacks.evasion import SaliencyMapMethod

# Type of printing.
OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.


# Jacobian Saliency Map Attack.
class JSMA:
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
    def attack(self, theta=0.1, gamma=1.0):
        # Create Adversarial Examples using JSMA.
        self.utility.print_message(WARNING, 'Creating Adversarial Examples using JSMA.')
        attack = SaliencyMapMethod(classifier=self.model,
                                   theta=theta,
                                   gamma=gamma,
                                   batch_size=1,
                                   verbose=True)
        X_adv = attack.generate(x=self.dataset)
        return X_adv
