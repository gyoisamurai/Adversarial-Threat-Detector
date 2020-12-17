#!/usr/bin/env python
# -*- coding:utf-8 -*-
import enum


# Common parts.
class Common(enum.Enum):
    # Title, Introduction.
    md_report_title = "# ATD Scan report（開発者向け（仮））.  "
    md_1_1_title = "## サマリ"
    md_1_1_text = """このレポートは、Adversarial Threat Detectorのスキャン結果レポートです。  
    これはテストです。これはテストです。これはテストです。  
    """

    md_1_2_title = "## 脆弱性の再現"
    md_1_2_text = """検出した脆弱性を再現します。  
        これはテストです。これはテストです。これはテストです。  
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
import random
import matplotlib.pyplot as plt
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
X_test = np.load('{0}')
X_test = X_test[X_test.files[0]][:{1}]

# データラベルのロード
y_test = np.load('{2}')
y_test = y_test[y_test.files[0]][:{1}]
    
print('Done.')"""
    md_2_3_title = "### 検証対象AIのロード"
    md_2_3_text = "検証対象のAIを読み込みます。"
    cd_2_3_code = """# モデルのロード
model = load_model('{0}')
model.summary()

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
    md_ae_fgsm_1_title = "### FGSMの実行"
    md_ae_fgsm_1_text = "ATDが作成したAdversarial Examplesを使用し、脆弱性を再現（確認）します。"
    md_ae_fgsm_2_title = "#### Adversarial Examplesのロード"
    cd_ae_fgsm_2_code = """# 敵対的サンプルのロード。
X_adv = np.load('{}')
X_adv = X_adv['adv']

print('Done.')"""
    md_ae_fgsm_3_title = "#### データの可視化"
    cd_ae_fgsm_3_code = """# 25枚のサンプルを選択
show_normal = []
show_AEs = []
for _ in range(5 * 5):
    idx = random.randint(0, {0}-1)
    show_AEs.append(X_adv[idx])
    show_normal.append(X_test[idx])

print('Done.')"""
    md_ae_fgsm_4_title = "#### 正常データの可視化"
    cd_ae_fgsm_4_code = """# 正常データの可視化
for idx, image in enumerate(show_normal):
    plt.subplot(5, 5, idx + 1)
    plt.imshow(image)

print('Done.')"""
    md_ae_fgsm_5_title = "#### 敵対的サンプルの可視化"
    cd_ae_fgsm_5_code = """# 敵対的サンプルの可視化
for idx, image in enumerate(show_AEs):
    plt.subplot(5, 5, idx + 1)
    plt.imshow(image)

print('Done.')"""
    md_ae_fgsm_6_title = "#### 敵対的サンプルの精度評価"
    cd_ae_fgsm_6_code = """# 敵対的サンプルを使用して画像分類器の推論精度を評価。
predictions = model.predict(X_adv)
accuracy = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
print('Accuracy on Adversarial Examples: {}%'.format(accuracy*100))
    
print('Done.')"""

    md_ae_fgsm_7_title = "## 対策"
    md_ae_fgsm_7_text = "これはテストです。これはテストです。これはテストです。"
