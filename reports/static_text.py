#!/usr/bin/env python
# -*- coding:utf-8 -*-
import enum


# Summary.
class Summary(enum.Enum):
    # Executive Summary.
    summary_executive_rank = "Weak"
    summary_executive_rank_ja = "非常に脆弱です。"
    summary_executive_text = "Your classifier is vulnerable to Evasion Attacks. An adversary can input an Adversarial Examples into your classifier and cause it to misclassify into the class intended by the adversary."
    summary_executive_text_ja = "あなたのAIは回避攻撃に脆弱です。攻撃者は細工した入力データ（敵対的サンプル）をAIに与えることで、入力データを攻撃者の意図したクラスに誤分類させることができます。"

    # Data Poisoning.
    summary_data_poisoning = "あなたのAIはデータ汚染攻撃に脆弱です。攻撃者は細工したデータをAIの学習データに注入することで、AIの推論を操作することができます。"
    summary_data_poisoning_ja = "あなたのAIはデータ汚染攻撃に脆弱です。攻撃者は細工したデータをAIの学習データに注入することで、AIの推論を操作することができます。"

    # Model Poisoning.
    summary_model_poisoning = "あなたのAIはデータ汚染攻撃に脆弱です。攻撃者は細工したデータをAIの学習データに注入することで、AIの推論を操作することができます。"
    summary_model_poisoning_ja = "あなたのAIはモデル汚染攻撃に脆弱です。攻撃者は細工したノード・層を事前学習モデルに注入することで、AIの推論操作または任意のシステムコマンドを実行することができます。"

    # Evasion.
    summary_evasion = "Your classifier is vulnerable to Evasion Attacks. An adversary can input an Adversarial Examples into your classifier and cause it to misclassify into the class intended by the adversary."
    summary_evasion_ja = "あなたのAIは回避攻撃に脆弱です。攻撃者は細工した入力データ（敵対的サンプル）をAIに与えることで、入力データを攻撃者の意図したクラスに誤分類させることができます。"

    # Evasion.
    summary_exfiltration = "あなたのAIは抽出攻撃に脆弱です。攻撃者はAIへの入出力情報を観察することで、AI内部のデータを窃取することができます。"
    summary_exfiltration_ja = "あなたのAIは抽出攻撃に脆弱です。攻撃者はAIへの入出力情報を観察することで、AI内部のデータを窃取することができます。"


# Common parts.
class Common(enum.Enum):
    # Title, Introduction.
    md_report_title = "# ATD Scan report."
    md_1_1_title = "## Summary"
    md_1_1_title_ja = "## サマリ"
    md_1_1_text = "This report is a scanned result of the Adversarial Threat Detector."
    md_1_1_text_ja = "このレポートは、Adversarial Threat Detectorのスキャン結果レポートです。"

    md_1_2_title = "## Replay the vulnerabilities."
    md_1_2_title_ja = "## 脆弱性の再現"
    md_1_2_text = "Replay the detected vulnerabilities."
    md_1_2_text_ja = "検出した脆弱性を再現します。"

    # Preparation.
    md_2_title = "## Preparation."
    md_2_title_ja = "## 事前準備"

    md_2_text = "Import libraries required to replay the vulnerability and load your classifier to be verified."
    md_2_text_ja = "脆弱性の再現に必要となるライブラリのインポートや、検証対象AIの読み込みなどを行います。"

    md_2_1_title = "### Import libraries."
    md_2_1_title_ja = "### ライブラリのインポート"

    md_2_1_text = """Import the libraries required for verification.  
    In this section, you will use Keras to build the classifier, so you will import the Keras classes.  
    You will also import ART, a library for vulnerability verification.  
    """
    md_2_1_text_ja = """検証に必要なライブラリをインポートします。  
    ここでは、TensorFlowに組み込まれているKerasを使用して画像分類器を構築するため、Kerasのクラスをインポートします。  
    また、脆弱性検証を行うためのライブラリ「ART」などもインポートします。  
    """

    cd_2_1_code = """# Import libraries.
import os
import random
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from art.estimators.classification import KerasClassifier
tf.compat.v1.disable_eager_execution()

print('Done')"""
    cd_2_1_code_ja = """# 必要なライブラリのインポート
import os
import random
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from art.estimators.classification import KerasClassifier
tf.compat.v1.disable_eager_execution()

print('Done')"""

    md_2_2_title = "### Load dataset."
    md_2_2_title_ja = "### データセットのロード"

    md_2_2_text = "Load the test data (normal data) of the classifier to be verified.  "
    md_2_2_text_ja = "検証対象となるAIのテストデータ（ノーマルデータ）を読み込みます。  "

    cd_2_2_code = """# Load dataset.
X_test = np.load('{0}')
X_test = X_test[X_test.files[0]][:{1}]

# Load data labels.
y_test = np.load('{2}')
y_test = y_test[y_test.files[0]][:{1}]
    
print('Done.')"""
    cd_2_2_code_ja = """# データセットのロード
X_test = np.load('{0}')
X_test = X_test[X_test.files[0]][:{1}]

# データラベルのロード
y_test = np.load('{2}')
y_test = y_test[y_test.files[0]][:{1}]

print('Done.')"""

    md_2_3_title = "### Load the classifier to be verified."
    md_2_3_title_ja = "### 検証対象AIのロード"

    md_2_3_text = "Load the classifier to be verified."
    md_2_3_text_ja = "検証対象のAIを読み込みます。"

    cd_2_3_code = """# Load classifier.
model = load_model('{0}')
model.summary()

print('Done.')"""
    cd_2_3_code_ja = """# モデルのロード
model = load_model('{0}')
model.summary()

    print('Done.')"""

    md_2_4_title = "### Evaluation of the classifier's accuracy."
    md_2_4_title_ja = "### AIの精度評価"

    md_2_4_text = "You will use the test data `X_test` to evaluate the inference accuracy of the loaded classifier."
    md_2_4_text_ja = "テストデータ`X_test`を使用し、読み込んだAIの推論精度を評価します。"

    cd_2_4_code = """# Evaluation of the classifier's accuracy.
predictions = model.predict(X_test)
accuracy = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
print('Accuracy on benign test example: {}%'.format(accuracy * 100))

print('Done.')"""
    cd_2_4_code_ja = """# AIの精度評価
predictions = model.predict(X_test)
accuracy = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
print('Accuracy on benign test example: {}%'.format(accuracy * 100))

print('Done.')"""


# Evasion Attacks.
class EvasionAttack(enum.Enum):
    md_ae_title = "## Evasion Attacks"
    md_ae_title_ja = "## 回避攻撃（Evasion Attacks）"

    md_ae_text = "The Evasion Attack is an attack that causes the target classifier to misclassify the Adversarial Examples into the class intended by the adversary."
    md_ae_text_ja = "回避攻撃は、標的分類器に敵対的サンプルを入力し、これを攻撃者が意図したクラスに誤分類させる攻撃です。"

    md_ae_fgsm_1_title = "### Execution of FGSM."
    md_ae_fgsm_1_title_ja = "### FGSMの実行"

    md_ae_fgsm_1_text = "You use the Adversarial Examples created by ATD to replay the vulnerability."
    md_ae_fgsm_1_text_ja = "ATDが作成したAdversarial Examplesを使用し、脆弱性を再現（確認）します。"

    md_ae_fgsm_2_title = "#### Load Adversarial Examples."
    md_ae_fgsm_2_title_ja = "#### Adversarial Examplesのロード"

    cd_ae_fgsm_2_code = """# Load Adversarial Examples.
X_adv = np.load('{}')
X_adv = X_adv['adv']

print('Done.')"""
    cd_ae_fgsm_2_code_ja = """# 敵対的サンプルのロード。
X_adv = np.load('{}')
X_adv = X_adv['adv']

print('Done.')"""

    md_ae_fgsm_3_title = "#### Data Visualization."
    md_ae_fgsm_3_title_ja = "#### データの可視化"

    cd_ae_fgsm_3_code = """# Select 25 samples.
show_normal = []
show_AEs = []
for _ in range(5 * 5):
    idx = random.randint(0, {0}-1)
    show_AEs.append(X_adv[idx])
    show_normal.append(X_test[idx])

print('Done.')"""
    cd_ae_fgsm_3_code_ja = """# 25枚のサンプルを選択
show_normal = []
show_AEs = []
for _ in range(5 * 5):
    idx = random.randint(0, {0}-1)
    show_AEs.append(X_adv[idx])
    show_normal.append(X_test[idx])

print('Done.')"""

    md_ae_fgsm_4_title = "#### Visualization of normal data."
    md_ae_fgsm_4_title_ja = "#### 正常データの可視化"

    cd_ae_fgsm_4_code = """# 正常データの可視化
for idx, image in enumerate(show_normal):
    plt.subplot(5, 5, idx + 1)
    plt.imshow(image)

print('Done.')"""
    cd_ae_fgsm_4_code_ja = """# Visualization of normal data.
for idx, image in enumerate(show_normal):
    plt.subplot(5, 5, idx + 1)
    plt.imshow(image)

print('Done.')"""

    md_ae_fgsm_5_title = "#### Visualization of Adversarial Examples."
    md_ae_fgsm_5_title_ja = "#### 敵対的サンプルの可視化"

    cd_ae_fgsm_5_code = """# Visualization of Adversarial Examples.
for idx, image in enumerate(show_AEs):
    plt.subplot(5, 5, idx + 1)
    plt.imshow(image)

print('Done.')"""
    cd_ae_fgsm_5_code_ja = """# 敵対的サンプルの可視化
for idx, image in enumerate(show_AEs):
    plt.subplot(5, 5, idx + 1)
    plt.imshow(image)

print('Done.')"""

    md_ae_fgsm_6_title = "#### Accuracy evaluation for Adversarial Examples."
    md_ae_fgsm_6_title_ja = "#### 敵対的サンプルの精度評価"

    cd_ae_fgsm_6_code = """# Evaluating the inference accuracy of your classifiers using Adversarial Examples.
predictions = model.predict(X_adv)
accuracy = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
print('Accuracy on Adversarial Examples: {}%'.format(accuracy*100))
    
print('Done.')"""
    cd_ae_fgsm_6_code_ja = """# 敵対的サンプルを使用して画像分類器の推論精度を評価。
predictions = model.predict(X_adv)
accuracy = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
print('Accuracy on Adversarial Examples: {}%'.format(accuracy*100))

print('Done.')"""

    md_ae_fgsm_7_title = "## Countermeasures."
    md_ae_fgsm_7_title_ja = "## 対策"

    md_ae_fgsm_7_text = """There are multiple countermeasures against Adversarial Examples.  
Defense in depth is important because there are attack methods that can defeat individual countermeasures.   
Examples of countermeasures are as follows.  

* Data Augmentation  
* [Defensive distillation](https://arxiv.org/abs/1511.04508)  
* Ensemble Method  
* [Feature Squeezing](https://arxiv.org/abs/1704.01155)  
* [Detecting Adversarial Examples with AI](https://arxiv.org/abs/1705.09064)  
* [Adversarial Training](https://arxiv.org/abs/1705.07204)  
"""
    md_ae_fgsm_7_text_ja = """敵対的サンプルに対する様々な防御手法が提案されています。  
個々の防御手法を破る攻撃手法も研究が進んでいるため、多層防御の観点が重要です。  
以下に対策の一例を列挙します。  

* Data Augmentation（データ拡張）  
* [ネットワークの蒸留](https://arxiv.org/abs/1511.04508)  
* アンサンブルメソッド  
* [Feature Squeezing（特徴量の絞り込み）](https://arxiv.org/abs/1704.01155)  
* [AIによる検出](https://arxiv.org/abs/1705.09064)  
* [Adversarial Training（敵対的学習）](https://arxiv.org/abs/1705.07204)  
"""
