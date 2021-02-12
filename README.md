# Adversarial-Threat-Detector
Adversarial Threat Detector (a.k.a. ATD) は**AI開発者のための脆弱性スキャナー**です。  

ATDは「脆弱性の発見（Scanning & Detection）」→「開発者の脆弱性の理解（Understand）」→「脆弱性の修正（Fix）」→「修正確認（Re-Scanning）」のサイクルを回すことで、あなたのAIの安全確保に貢献します。  

<div align="center">
  <center>
  <img src="./img/atd_concept.jpg" width="400">
  <figcaption><b>ATDサイクル</b></figcaption>
  </center>
  <br>
</div>

#### 1. 脆弱性のスキャン・検知（Scanning & Detection）  
ATDは、**AIに対する様々な攻撃を全自動で実行し、脆弱性を検知**します。  

<div align="center">
  <center>
  <img src="./img/atd_scanning.png" width="800">
  <figcaption><b>脆弱性スキャン</b></figcaption>
  </center>
  <br>
</div>

脆弱性スキャン対象の分類器やデータセット、攻撃手法などを引数で指定するだけで、脆弱性の有無を検証することができます。  

#### 2. 脆弱性の理解（Understanding）  
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

検出された脆弱性の概要や対策を参照することで、脆弱性に対処する方法を知ることができます。  

* 脆弱性の再現環境（ipynb形式）  
<div align="center">
  <center>
  <img src="./img/ipynb_samples.png">
  <figcaption><b>Jupyter Notebook形式のレポート</b></figcaption>
  </center>
  <br>
</div>

ATDが自動生成したipynbをJupyter Notebookで読み込むことで、分類器に対する攻撃手順を一つずつ確認することができます。これにより、脆弱性を深く理解することができます。  

#### 3. 脆弱性の修正（Fix）  
ATDは、検知された**脆弱性を自動で修正**します。  

**※本機能は次期リリースで対応予定です。**  

#### 4. 修正確認（Re-Scanning）  
ATDは、脆弱性が修正されたAIに対し、修正確認の再スキャンを実行します。  

**※本機能は次期リリースで対応予定です。**  

## Overview

## Road Map


## Installation


## Usage


## Check Report


## Operation check environment


## Licence
[MIT License](https://github.com/gyoisamurai/Adversarial-Threat-Detector/blob/main/LICENSE)

## Contact us
takaesu235@gmail.com
