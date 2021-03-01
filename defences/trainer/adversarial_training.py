#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import configparser
from art.defences.trainer import AdversarialTrainer

# Type of printing.
OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.


# Adversarial Training.
class Adversarial_Training:
    def __init__(self, utility, model, dataset):
        # Read config.ini.
        full_path = os.path.dirname(os.path.abspath(__file__))
        config = configparser.ConfigParser()
        config.read(os.path.join(full_path, 'config.ini'))
        self.utility = utility

        # Set target model and dataset.
        self.model = model
        self.dataset = dataset

    # Creating Adversarial Training instance.
    def trainer(self, classifier, attacks, ration=0.5):
        # Creating Adversarial Training instance.
        return AdversarialTrainer(classifier=classifier, attacks=attacks, ratio=ration)

    # Create Adversarial Examples.
    def fit(self, classifier, X_train, y_train, X_test, y_test, batch_size=512, epochs=30, shuffle=True):
        # Execute Adversarial Training.
        self.utility.print_message(NOTE, 'Executing Adversarial Training.')
        classifier.fit(X_train, y_train,
                       batch_size=512,
                       nb_epochs=30,
                       validation_data=(X_test, y_test),
                       shuffle=True)

        return classifier
