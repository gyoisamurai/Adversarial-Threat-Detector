#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import configparser
from art.attacks.evasion import CarliniL2Method

# Type of printing.
OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.


# Carlini and Wagner L_2 Attack.
class CarliniL2:
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
    def attack(self, confidence=0.0, batch_size=1):
        # Create Adversarial Examples using Carlini and Wagner L_2 Attack.
        self.utility.print_message(NOTE, 'Creating Adversarial Examples using Carlini and Wagner L_2 Attack.')
        attack = CarliniL2Method(classifier=self.model,
                                 confidence=confidence,
                                 targeted=False,
                                 learning_rate=0.01,
                                 binary_search_steps=10,
                                 max_iter=10,
                                 initial_const=0.01,
                                 max_halving=5,
                                 max_doubling=5,
                                 batch_size=batch_size,
                                 verbose=True)
        X_adv = attack.generate(x=self.dataset)
        return X_adv
