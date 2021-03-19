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
    def __init__(self, utility):
        # Read config.ini.
        full_path = os.path.dirname(os.path.abspath(__file__))
        config = configparser.ConfigParser()
        config.read(os.path.join(full_path, 'config.ini'))
        self.utility = utility

    # Creating Adversarial Training instance.
    def trainer(self, classifier, attacks, ratio=0.5):
        # Creating Adversarial Training instance.
        return AdversarialTrainer(classifier=classifier, attacks=attacks, ratio=ratio)

    # Create Adversarial Examples.
    def fit(self, classifier, X_train, y_train, X_test, y_test, batch_size=512, epochs=30, shuffle=True):
        # Execute Adversarial Training.
        self.utility.print_message(NOTE, 'Executing Adversarial Training.')
        classifier.fit(X_train, y_train,
                       batch_size=batch_size,
                       nb_epochs=epochs,
                       validation_data=(X_test, y_test),
                       shuffle=shuffle)

        return classifier
