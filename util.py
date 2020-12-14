#!/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import string
import random
import configparser
import numpy as np
from datetime import datetime
from PIL import Image
from logging import getLogger, FileHandler, Formatter

# TensorFlow.
import tensorflow as tf
from tensorflow.keras.models import load_model
tf.compat.v1.disable_eager_execution()

# ART.
from art.estimators.classification import KerasClassifier

# Printing colors.
OK_BLUE = '\033[94m'      # [*]
NOTE_GREEN = '\033[92m'   # [+]
FAIL_RED = '\033[91m'     # [-]
WARN_YELLOW = '\033[93m'  # [!]
ENDC = '\033[0m'
PRINT_OK = OK_BLUE + '[*]' + ENDC
PRINT_NOTE = NOTE_GREEN + '[+]' + ENDC
PRINT_FAIL = FAIL_RED + '[-]' + ENDC
PRINT_WARN = WARN_YELLOW + '[!]' + ENDC

# Type of printing.
OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.


# Utility class.
class Utilty:
    def __init__(self):
        # Read config.ini.
        full_path = os.path.dirname(os.path.abspath(__file__))
        config = configparser.ConfigParser()
        config.read(os.path.join(full_path, 'config.ini'))

        try:
            self.banner_delay = float(config['Common']['banner_delay'])
            self.report_date_format = config['Common']['date_format']
            self.log_dir = os.path.join(full_path, config['Common']['log_path'])
            os.makedirs(self.log_dir, exist_ok=True)
            self.log_file = config['Common']['log_file']
            self.log_path = os.path.join(self.log_dir, self.log_file)
            self.target_dir = os.path.join(full_path, config['Common']['target_path'])
            os.makedirs(self.target_dir, exist_ok=True)
        except Exception as e:
            self.print_message(FAIL, 'Reading config.ini is failure : {}'.format(e))
            sys.exit(1)

        # Setting logger.
        self.logger = getLogger('Adversarial Threat Detector')
        self.logger.setLevel(20)
        file_handler = FileHandler(self.log_path)
        self.logger.addHandler(file_handler)
        formatter = Formatter('%(levelname)s,%(message)s')
        file_handler.setFormatter(formatter)

    # Print metasploit's symbol.
    def print_message(self, type, message):
        if os.name == 'nt':
            if type == NOTE:
                print('[+] ' + message)
            elif type == FAIL:
                print('[-] ' + message)
            elif type == WARNING:
                print('[!] ' + message)
            elif type == NONE:
                print(message)
            else:
                print('[*] ' + message)
        else:
            if type == NOTE:
                print(PRINT_NOTE + ' ' + message)
            elif type == FAIL:
                print(PRINT_FAIL + ' ' + message)
            elif type == WARNING:
                print(PRINT_WARN + ' ' + message)
            elif type == NONE:
                print(NOTE_GREEN + message + ENDC)
            else:
                print(PRINT_OK + ' ' + message)

    # Print exception messages.
    def print_exception(self, e, message):
        self.print_message(WARNING, 'type:{}'.format(type(e)))
        self.print_message(WARNING, 'args:{}'.format(e.args))
        self.print_message(WARNING, '{}'.format(e))
        self.print_message(WARNING, message)

    # Load model.
    def load_model(self, model_name):
        model_path = os.path.join(self.target_dir, model_name)
        if os.path.exists(model_path) is False:
            self.print_message(FAIL, 'Model path not Found: {}'.format(model_path))
            return None
        else:
            model = load_model(model_path)
            self.print_message(OK, 'Loaded target model: {}'.format(model_path))
            return model

    # Load dataset/label from npz.
    def load_dataset(self, dataset_name, label_name, use_dataset_num):
        dataset_path = os.path.join(self.target_dir, dataset_name)
        label_path = os.path.join(self.target_dir, label_name)
        if os.path.exists(dataset_path) is False or os.path.exists(label_path) is False:
            self.print_message(FAIL, 'Dataset or Label path not Found: {}/{}'.format(dataset_path, label_path))
            return None, None
        else:
            # Check dataset number.
            X_test = np.load(dataset_path)
            if len(X_test[X_test.files[0]]) < use_dataset_num:
                use_dataset_num = len(X_test[X_test.files[0]])

            self.print_message(OK, 'Loaded dataset: {} ({})'.format(dataset_path, X_test.files))
            y_test = np.load(label_path)
            self.print_message(OK, 'Loaded label: {} ({})'.format(label_path, y_test.files))
            return X_test[X_test.files[0]][:use_dataset_num], y_test[y_test.files[0]][:use_dataset_num]

    # Wrap classifier using ART.
    def wrap_classifier(self, model, X_test):
        mix_pixel_value = np.amin(X_test)
        max_pixel_value = np.amax(X_test)
        classifier = KerasClassifier(model=model,
                                     clip_values=(mix_pixel_value, max_pixel_value),
                                     use_logits=False)
        return classifier

    # Evaluate accuracy.
    def evaluate(self, model, X_test, y_test):
        preds = model.predict(X_test)
        accuracy = np.sum(np.argmax(preds, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
        return accuracy

    # Random sampling.
    def random_sampling(self, data_size=100, sample_num=5):
        sample_list = []
        for _ in range(sample_num):
            sample_list.append(random.randint(0, data_size - 1))
        return sample_list

    # Save Adversarial Examples.
    def save_adv_images(self, idx, method, X_adv, save_path):
        scale = 255.0 / np.max(X_adv)
        pil_img = Image.fromarray(np.uint8(X_adv * scale))
        save_full_path = os.path.join(save_path, 'adv_{}_{}.jpg'.format(method, idx+1))
        pil_img.save(save_full_path)
        return save_full_path

    # Write logs.
    def write_log(self, loglevel, message):
        self.logger.log(loglevel, self.get_current_date() + ' ' + message)

    # Create random string.
    def get_random_token(self, length):
        chars = string.digits + string.ascii_letters
        return ''.join([random.choice(chars) for _ in range(length)])

    # Get current date.
    def get_current_date(self, indicate_format=None):
        if indicate_format is not None:
            date_format = indicate_format
        else:
            date_format = self.report_date_format
        return datetime.now().strftime(date_format)

    # Transform date from string to object.
    def transform_date_object(self, target_date, format=None):
        if format is None:
            return datetime.strptime(target_date, self.report_date_format)
        else:
            return datetime.strptime(target_date, format)

    # Transform date from object to string.
    def transform_date_string(self, target_date):
        return target_date.strftime(self.report_date_format)

    # Check argument values.
    def check_arg_value(self, protocol, fqdn, port, path):
        # Check protocol.
        if protocol not in ['http', 'https']:
            self.print_message(FAIL, 'Invalid protocol : {}'.format(protocol))

        # Check IP address.
        if isinstance(fqdn, str) is False and isinstance(fqdn, int) is False:
            self.print_message(FAIL, 'Invalid IP address : {}'.format(fqdn))
            return False

        # Check port number.
        if port.isdigit() is False:
            self.print_message(FAIL, 'Invalid port number : {}'.format(port))
            return False
        elif (int(port) < 1) or (int(port) > 65535):
            self.print_message(FAIL, 'Invalid port number : {}'.format(port))
            return False

        # Check path.
        if isinstance(path, str) is False and isinstance(path, int) is False:
            self.print_message(FAIL, 'Invalid path : {}'.format(path))
            return False
        # elif path.startswith('/') is False or path.endswith('/') is False:
        elif path.startswith('/') is False:
            self.print_message(FAIL, 'Invalid path : {}'.format(path))
            return False

        return True
