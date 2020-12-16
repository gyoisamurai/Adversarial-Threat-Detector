#!/usr/bin/env python
# -*- coding:utf-8 -*-
import enum


# Common parts.
class Common(enum.Enum):
    # Title, Introduction.
    md_report_title = "# Adversarial Threat Detector Scan report.  "
    md_1_title = "## はじめに"
    md_1_text = """このレポートは、Adversarial Threat Detectorのスキャン結果レポートです。  
    これはテストです。  
    """

    # Preparation.
    md_2_title = "## 事前準備"
    md_2_text = """必要なライブラリのインポートや検証対象AIの読み込みなどを行います。  
    """
    md_2_1_title = "### ライブラリのインポート"
    md_2_1_text = """検証に必要なライブラリをインポートします。  
    ここでは、TensorFlowに組み込まれているKerasを使用して画像分類器を構築するため、Kerasのクラスをインポートします。  
    また、脆弱性検証を行うためのライブラリ「ART」などもインポートします。  
    """
    cd_2_1_code = """# 必要なライブラリのインポート
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from art.estimators.classification import KerasClassifier
tf.compat.v1.disable_eager_execution()

print('Done')"""
    md_2_2_title = "### データセットのロード"
    md_2_2_text = """検証対象となるAIのテストデータ（ノーマルデータ）を読み込みます。  
    """
    cd_2_2_code = """# データセットのロード
X_test = np.load('{}')
X_test = X_test[X_test.files[0]]
    
# データラベルのロード
y_test = np.load('{}')
y_test = y_test[y_test.files[0]]
    
print('Done.')"""
    md_2_3_title = "### 検証対象AIのロード"
    md_2_3_text = "検証対象のAIを読み込みます。"
    cd_2_3_code = """# モデルのロード
model = load_model('{}')
    
print('Done.')"""
    md_2_4_title = "### AIの精度評価"
    md_2_4_text = "テストデータ`X_test`を使用し、読み込んだAIの推論精度を評価します。"
    cd_2_4_code = """# AIの精度評価
predictions = model.predict(X_test)
accuracy = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
print('Accuracy on benign test example: {}%'.format(accuracy * 100))

print('Done.')"""


# Evasion Attacks.
class EvasionAttack(enum.Enum):
    md_ae_title = "## Evasion Attacks"
    md_ae_text = "Evasion attacks is carefully perturbing the input samples at test time to have them misclassified."
    md_ae_fgsm_1_title = "### FGSMの実践"
    md_ae_fgsm_1_text = "ATDが作成したAdversarial Examplesを使用し、FGSMを実践します。"
    md_ae_fgsm_2_title = "#### Adversarial Examplesのロード"
    cd_ae_fgsm_2_code = """# 敵対的サンプルのロード。
X_adv = np.load('{}')

# 敵対的サンプルを使用して画像分類器の推論精度を評価。
predictions = model.predict(X_adv['adv'])
accuracy = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
print('Accuracy on Adversarial Exmaples: ', accuracy * 100 + '%')
    
print('Done.')"""
