# Adversarial-Threat-Detector
[English page](./README.md)  

### Topics
2021年04月：ATD用のWebインタフェース「**GyoiBoard**」をリリースしました！  
　->[詳細はこちら](https://github.com/gyoisamurai/GyoiBoard)  
2021年03月：アジア最大級のハッカーカンファレンスである**Black Hat ASIA 2021**にて、Adversarial Threat Detectorを発表します！  
　->[詳細はこちら](https://www.blackhat.com/asia-21/arsenal/schedule/#adversarial-threat-detector-22628)  

<font size=4><b>Adversarial Threat DetectorはAI開発を<font color="red">安全</font>にします。</b></font>

[![Demo movie on youtube](https://img.youtube.com/vi/5jGbYJGO84A/0.jpg)](https://www.youtube.com/watch?v=5jGbYJGO84A)

近年、ディープラーニング技術の発展により、顔認証や防犯カメラ（異常検知）、そして自動運転技術など、ディープラーニングを使用したシステムが普及しています。その一方で、ディープラーニングのアルゴリズムの脆弱性を突く攻撃手法の研究も急速に進んでいます。例えば、システムへの入力データを細工することで、これを攻撃者が意図したクラスに誤分類させる回避攻撃や、システムが学習したデータを推論する抽出攻撃などがあります。これらの攻撃に適切に対処していない場合、顔認証が突破されて不正侵入を許したり、学習データが推論されることで情報漏えいが発生するなど、重大なインシデントに繋がることになります。  

そこで私達は、**Adversarial Threat Detector (a.k.a. ATD)と呼ばれる、ディープラーニング・ベースの分類器の脆弱性を自動検知する脆弱性スキャナーをリリースしました**。  

ATDは、「脆弱性の発見（Scanning & Detection）」→「開発者の脆弱性の理解（Understand）」→「脆弱性の修正（Fix）」→「修正確認（Re-Scanning）」のサイクルを回すことで、単に脆弱性を検知するだけでなく、開発者の方々の脆弱性への理解を深めることで、あなたの分類器の安全確保に貢献します。  

なお、ATDは、機械学習システムへの脅威を纏めた「[Adversarial Threat Matrix](https://github.com/mitre/advmlthreatmatrix)」に沿って開発を進めています。また、現在のところ脆弱性の検出や防御には、機械学習のためのセキュリティ・ライブラリである「[Adversarial Robustness Toolbox (ART)](https://github.com/Trusted-AI/adversarial-robustness-toolbox)」を使用しています。現在のATDはベータ版ですが、月に１回のペースで機能を拡張していきますので、定期的にリリース情報をご確認いただけると幸いです。  

##### ATDのセキュア・サイクル
<div align="center">
  <center>
  <img src="./img/atd_concept.jpg" width="400">
  <figcaption><b></b></figcaption>
  </center>
  <br>
</div>

#### 1. 脆弱性の発見（Scanning & Detection）  
ATDは、**分類器に対する様々な攻撃を全自動で実行し、脆弱性を検知**します。  

<div align="center">
  <center>
  <img src="./img/atd_scanning.png">
  <figcaption><b>脆弱性スキャン</b></figcaption>
  </center>
  <br>
</div>

脆弱性スキャン対象の分類器やデータセット、攻撃手法などを引数で指定するだけで、脆弱性の有無を検証することができます。  

#### 2. 開発者の脆弱性の理解（Understanding）  
脆弱性が検知された場合、ATDは**対策レポート（HTML）と脆弱性の再現環境（ipynb）を生成**します。  
開発者は、対策レポートと再現環境を参照することで、**脆弱性に関する理解を深めることができます**。  

* 対策レポート（HTML形式）  
<div align="center">
  <center>
  <img src="./img/scan_report_samples.png">
  <figcaption><b>HTML形式のレポート</b></figcaption>
  </center>
  <br>
</div>

開発者は、検出された脆弱性の概要や対策を参照することで、脆弱性に対処する方法を知ることができます。  
サンプルレポートは[こちら](https://gyoisamurai.github.io/Adversarial-Threat-Detector/reports/sample/)。  

* 脆弱性の再現環境（ipynb形式）  
<div align="center">
  <center>
  <img src="./img/ipynb_samples.png">
  <figcaption><b>Jupyter Notebook形式のレポート</b></figcaption>
  </center>
  <br>
</div>

ATDが自動生成したipynbをJupyter Notebookで読み込むことで、分類器に対する攻撃手順を一つずつ確認することができます。これにより、脆弱性を深く理解することができます。  
サンプルのNotebookは[こちら](https://github.com/gyoisamurai/Adversarial-Threat-Detector/blob/main/reports/sample/sample_ipynb.ipynb).  

#### 3. 脆弱性の修正（Fix）  
ATDは、検知された**脆弱性を自動で修正**します。  
現在のATDは、回避攻撃に対する防御手法の一つである「敵対的学習（Adversarial Training）」に対応しています。  
**※他の防御手法は順次対応していきます。**

#### 4. 修正確認（Re-Scanning）  
ATDは、脆弱性が修正されたAIに対し、修正確認の再スキャンを実行します。  

## サポート状況
#### 分類器種別
ATDの現バージョンは、`tf.keras`で構築された**画像分類器**に対応しています。  
他の分類器は今後サポートしていく予定です。

|識別器|画像分類器|文書分類器|その他の分類器|
|:--|:--|:--|:--|
|Keras|supported|-|-|
|TensorFlow|-|-|-|
|TensorFlow v2|-|-|-|
|PyTorch|-|-|-|
|Scikit-learn|-|-|-|

#### 攻撃種別  
ATDの現バージョンは**回避攻撃**に対応しています。  
他の攻撃手法は今後サポートしていく予定です。  

|攻撃種別|画像分類器|文書分類器|その他の分類器|
|:--|:--:|:--:|:--:|
|データ汚染攻撃|6月頃対応予定-|-|-|
|モデル汚染攻撃|-|-|-|
|回避攻撃|supported|-|-|
|抽出攻撃|5月頃対応予定-|-|-|

## Road Map
ATDは１ヶ月おきに新機能をリリースしていく予定です。  
今後の開発スケジュールは以下の通りです。  

* 2021/01: 回避攻撃の実装（完了）  
* 2021/02: 脆弱性修正機能、修正確認機能の実装（一部完了）  
* 2021/05: 抽出攻撃の実装  
* 2021/06: データ汚染検知の実装
* 2021/07: モデル汚染検知の実装  
* 2021/08〜: Keras以外のモデル / 画像分類器以外への対応  

## Installation
1. ATDのリポジトリを`git clone`します。  
```
root@kali:~# git clone https://github.com/gyoisamurai/Adversarial-Threat-Detector
```

2. `pip3`をインストールします。  
```
root@kali:~# apt-get update
root@kali:~# apt-get install python3-pip
```

3. ATDの実行に必要なライブラリをインストールします。  
```
root@kali:~# cd Adversarial-Threat-Detector
root@kali:~/Adversarial-Threat-Detector# pip3 install -r requirements.txt
```

## Usage
ATDの引数を変えることで、様々な脆弱性スキャンを実行することができます。  

|注意|
|:---|
|ATDの現バージョンは、回避攻撃に対応しています。他の攻撃手法は今後対応する予定です。|

```
usage: atd.py [-h] [--target_id TARGET_ID] [--scan_id SCAN_ID] [--model_name MODEL_NAME]
              [--train_data_name TRAIN_DATA_NAME] [--test_data_name TEST_DATA_NAME]
              [--use_x_train_num USE_X_TRAIN_NUM] [--use_x_test_num USE_X_TEST_NUM]
              [--train_label_name TRAIN_LABEL_NAME] [--test_label_name TEST_LABEL_NAME]
              [--op_type {attack,defence,test}]
              [--attack_type {data_poisoning,model_poisoning,evasion,exfiltration}]
              [--attack_data_poisoning {feature_collision,convex_polytope,bullseye_polytope}]
              [--attack_model_poisoning {node_injection,layer_injection}]
              [--attack_evasion {fgsm,cnw,jsma}] [--fgsm_epsilon {0.01,0.05,0.1,0.15,0.2,0.25,0.3}]
              [--fgsm_eps_step {0.1,0.2,0.3,0.4,0.5}] [--fgsm_targeted]
              [--fgsm_batch_size FGSM_BATCH_SIZE]
              [--cnw_confidence {0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0}]
              [--cnw_batch_size CNW_BATCH_SIZE]
              [--jsma_theta {0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0}]
              [--jsma_gamma {0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0}]
              [--jsma_batch_size JSMA_BATCH_SIZE]
              [--attack_exfiltration {membership_inference,label_only,inversion}]
              [--defence_type {data_poisoning,model_poisoning,evasion,exfiltration}]
              [--defence_evasion {adversarial_training,feature_squeezing,jpeg_compression}]
              [--adversarial_training_attack {fgsm,cnw,jsma}]
              [--adversarial_training_ratio {0.1,0.2,0.3,0.4,0.5,0.6,0.7}]
              [--adversarial_training_batch_size {32,64,128,256,512}]
              [--adversarial_training_epochs {10,20,30,40,50}] [--adversarial_training_shuffle]
              [--lang {en,ja}]

Adversarial Threat Detector.

optional arguments:
  -h, --help            show this help message and exit
  --target_id TARGET_ID
                        Target's identifier for GyoiBoard.
  --scan_id SCAN_ID     Scan's identifier for GyoiBoard.
  --model_name MODEL_NAME
                        Target model name.
  --train_data_name TRAIN_DATA_NAME
                        Training dataset name.
  --test_data_name TEST_DATA_NAME
                        Test dataset name.
  --use_x_train_num USE_X_TRAIN_NUM
                        Dataset number for X_train.
  --use_x_test_num USE_X_TEST_NUM
                        Dataset number for X_test.
  --train_label_name TRAIN_LABEL_NAME
                        Train label name.
  --test_label_name TEST_LABEL_NAME
                        Test label name.
  --op_type {attack,defence,test}
                        operation type.
  --attack_type {data_poisoning,model_poisoning,evasion,exfiltration}
                        Specify attack type.
  --attack_data_poisoning {feature_collision,convex_polytope,bullseye_polytope}
                        Specify method of Data Poisoning Attack.
  --attack_model_poisoning {node_injection,layer_injection}
                        Specify method of Poisoning Attack.
  --attack_evasion {fgsm,cnw,jsma}
                        Specify method of Evasion Attack.
  --fgsm_epsilon {0.01,0.05,0.1,0.15,0.2,0.25,0.3}
                        Specify Epsilon for FGSM.
  --fgsm_eps_step {0.1,0.2,0.3,0.4,0.5}
                        Specify Epsilon step for FGSM.
  --fgsm_targeted       Specify targeted evasion for FGSM.
  --fgsm_batch_size FGSM_BATCH_SIZE
                        Specify batch size for FGSM.
  --cnw_confidence {0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0}
                        Specify Confidence for C&W.
  --cnw_batch_size CNW_BATCH_SIZE
                        Specify batch size for CnW.
  --jsma_theta {0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0}
                        Specify Theta for JSMA.
  --jsma_gamma {0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0}
                        Specify Gamma for JSMA.
  --jsma_batch_size JSMA_BATCH_SIZE
                        Specify batch size for JSMA.
  --attack_exfiltration {membership_inference,label_only,inversion}
                        Specify method of Exfiltration Attack.
  --defence_type {data_poisoning,model_poisoning,evasion,exfiltration}
                        Specify defence type.
  --defence_evasion {adversarial_training,feature_squeezing,jpeg_compression}
                        Specify defence method against Evasion Attack.
  --adversarial_training_attack {fgsm,cnw,jsma}
                        Specify attack method for Adversarial Training.
  --adversarial_training_ratio {0.1,0.2,0.3,0.4,0.5,0.6,0.7}
                        Specify ratio for Adversarial Training.
  --adversarial_training_batch_size {32,64,128,256,512}
                        Specify batch size for Adversarial Training.
  --adversarial_training_epochs {10,20,30,40,50}
                        Specify epochs for Adversarial Training.
  --adversarial_training_shuffle
                        Specify shuffle for Adversarial Training.
  --lang {en,ja}        Specify language of report.
```

### チュートリアル
#### 攻撃
##### 回避攻撃（FGSM）
```
root@kali:~/Adversarial-Threat-Detector# python3 atd.py --op_type attack --model_name "[full path]"/model.h5 --test_data_name "[full path]"/X_test.npz --test_label_name "[full path]"/y_test.npz --use_x_test_num 100 --attack_type evasion --attack_evasion fgsm --fgsm_epsilon 0.05
```

##### 回避攻撃（C&W）
```
root@kali:~/Adversarial-Threat-Detector# python3 atd.py --op_type attack --model_name "[full path]"/model.h5 --test_data_name "[full path]"/X_test.npz --test_label_name "[full path]"/y_test.npz --use_x_test_num 100 --attack_type evasion --attack_evasion cnw
```

##### 回避攻撃（JSMA）
```
root@kali:~/Adversarial-Threat-Detector# python3 atd.py --op_type attack --model_name "[full path]"/model.h5 --test_data_name "[full path]"/X_test.npz --test_label_name "[full path]"/y_test.npz --use_x_test_num 100 --attack_type evasion --attack_evasion jsma
```

#### 防御
##### 敵対的学習（Adversarial Training）
```
root@kali:~/Adversarial-Threat-Detector# python3 atd.py --op_type defence --model_name "[path]"/model.h5 --train_data_name "[path]"/X_train.npz --train_label_name "[path]"/y_train.npz --test_data_name "[path]"/X_test.npz --test_label_name "[path]"/y_test.npz --use_x_train_num 50000 --use_x_test_num 10000 --defence_type evasion --defence_evasion adversarial_training --adversarial_training_attack fgsm --adversarial_training_ratio 0.5 --adversarial_training_batch_size 128 --adversarial_training_epochs 10 --adversarial_training_shuffle
```

## Demo
私達が用意したデモ用のモデルとデータセットを使用してATDをデモ実行することができます。  

1. `tf.keras`で構築した学習済みの画像分類器をダウンロードします。  
```
root@kali:~/Adversarial-Threat-Detector# wget "https://drive.google.com/uc?export=download&id=1zFNn8EBHR_xewFW3-IhXkfdEop0gYUbu" -O demo_model.h5
```

2. デモに使用するデータセット（CIFAR10）をダウンロードします。  
```
root@kali:~/Adversarial-Threat-Detector# wget "https://drive.google.com/uc?export=download&id=1zJyB4zUDK22oU55rwTdbKMy0p3rOfuBw" -O X_test.npz
root@kali:~/Adversarial-Threat-Detector# wget "https://drive.google.com/uc?export=download&id=1SUuXdebgMjUOMT8I-e5vFC8oMIVcDz5P" -O y_test.npz
```

3. ダウンロードしたファイル（`demo_model.h5`,`X_test.npz`,`y_test.npz`）を`targets`ディレクトリに移動します。  
```
root@kali:~/Adversarial-Threat-Detector# mv demo_model.h5 X_test.npz y -O X_test.npz y_test.npz ./targets/
```

4. ATDを実行します。  
```
root@kali:~/Adversarial-Threat-Detector# python3 atd.py --op_type attack --model_name ./targets/model.h5 --test_data_name ./targets/X_test.npz --test_label_name ./targets/y_test.npz --use_x_test_num 100 --attack_type evasion --attack_evasion fgsm --fgsm_epsilon 0.05
..snip..
[!] Created report: ~/Adversarial-Threat-Detector/reports/../reports/20210217151416_scan/scan_report.html
atd.py Done!!
```

5. `reports`ディレクトリ以下に生成されたスキャンレポートをチェックします。  
```
root@kali:~/Adversarial-Threat-Detector# firefox reports/20210217151416_scan/scan_report.html
root@kali:~/Adversarial-Threat-Detector# jupyter notebook reports/20210217151416_scan/evasion_fgsm.ipynb
```

## Licence
[MIT License](https://github.com/gyoisamurai/Adversarial-Threat-Detector/blob/main/LICENSE)

## Contact us
* Email  
[gyoiler3@gmail.com](mailto:gyoiler3@gmail.com)  
