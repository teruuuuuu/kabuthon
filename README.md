# 株価分析用プログラム

## 機能一覧
- クロール
- 通知

## クロール
- 新規上場会社情報
- 会社情報
- 4本値

#### 新規上場会社情報    
新規上場会社の情報をクロールします

#### 会社情報
brand_list.txtに記入している証券コードを対象に会社情報をクロールします

#### 4本値
brand_list.txtに記入している証券コードを対象に4本値をクロールします

## 通知
- 新規上場会社情報
- 会社情報
- 4本値のローソク足チャート

#### 新規上場会社情報
kabuthon/.envに設定しているslackの通知先に対して新規上場会社情報を通知します

#### 会社情報
kabuthon/.envに設定しているslackの通知先に対して会社情報を通知します

#### 4本値のローソク足チャート
kabuthon/.envに設定しているslackの通知先に対して4本値のローソク足チャートを通知します

## 設定
環境設定ファイル
kabuthon/.env    
kabuthon/.env.sampleにサンプルがあるのでkabuthon/.envにリネームして使います
> cp kabuthon/.env.sample kabuthon/.env
```buildoutcfg
DB_FILE = "SQLite保存先ファイル名"
SLACK_API_TOKEN = "通知先スラックAPIトークン"
SLACK_CHANNEL = "通知先スラックチャンネル"
```

監視対象企業設定
brand_list.txt.sampleにサンプルがあるのでbrand_list.txtにリネームして使います。
監視対象企業の証券コードのみを記入します
> cp brand_list.txt.sample brand_list.txt
```buildoutcfg
3382
4755
6861
6752
```

## 実行
ライブラリインストール
> pip install

オプション
```buildoutcfg
--setup DBの初期化
--crawl クロール実行
--notification 通知実行
```
実行例
> python kabuthon --setup --crawl --notification