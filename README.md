# cd_rfid_player
cd player (rfid)

# できること
NFCタグを読み取って、関連付けられた音声ファイルを再生するCDプレイヤーもどき

# 構成

![image](https://github.com/omikujiv/cd_rfid_player/assets/128278435/b9d590ef-be11-4cb2-8dd4-6720f96383d3)


1. CDにNFCタグをくっつける
    * タグにCDのデータを置いてるパスを書き込む
2. ラズパイゼロにつけたRFID2ユニットで読み取る
    * CDデータのパスを入手 
3. ディレクトリ内の音楽を再生
    * スピーカーから出力
* ボタンから{Skip, Pause/Play, Stop}の操作をする

# 部品

* Raspberry Pi Zero WH
* RFIDモジュール
    * M5Stack用WS1850S搭載 RFID 2ユニット
    * https://www.switch-science.com/products/8301
    * 技適大丈夫そうで、安いユニットなので採用
* ボタン
    * タクトスイッチ
    * https://akizukidenshi.com/catalog/g/g109828/
    * 余ってたので採用
* スピーカー
    * USB-DAC
        * Logicool G430付属DAC
        * 余ってたので採用
    * スピーカー
        * ダイソースピーカーユニットなどAUX出力
* NCFタグ
    * NFCタグシール 円形無地27mm 
    * https://www.akiba-led.jp/product/1561

# ライセンス
* RFIDモジュール用
    * https://github.com/cpranzl/mfrc522_i2c
    * GPLライセンス

したがって当プログラムもGPLライセンスです
