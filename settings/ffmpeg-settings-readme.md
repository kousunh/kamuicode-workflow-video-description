# FFmpeg設定ファイル

このディレクトリには、動画処理で使用されるFFmpegの設定がYAML形式で保存されています。

## ファイル: ffmpeg-settings.yml

### タイトル画面生成の設定 (title:)

#### デフォルト設定
- **duration**: タイトル表示時間（秒）
- **fontsize**: フォントサイズ（デフォルト: 72）
- **color**: テキスト色（デフォルト: white）
- **bgcolor**: 背景色（デフォルト: black@0.8 = 80%不透明の黒）
- **position**: テキスト位置
  - x: 水平位置（中央揃え）
  - y: 垂直位置（中央から30px上）
- **shadow**: 影の設定
  - color: 影の色（black@0.8）
  - x, y: 影のオフセット（3px）
- **box**: テキストボックス
  - enable: 有効/無効（1/0）
  - color: ボックスの色
  - borderw: ボーダー幅

#### 背景画像使用時の設定
- フォントサイズが大きくなる（92）
- 背景が透明になる
- アウトライン（縁取り）が追加される

### テキストオーバーレイ（説明文）の設定 (text_overlay:)

#### デフォルト設定
- **fontsize**: フォントサイズ（デフォルト: 48）
- **fontcolor**: テキスト色（デフォルト: white）
- **box**: 背景ボックス
  - color: black@0.7（70%不透明の黒）
  - borderw: パディング（10px）
- **fade**: フェード効果
  - in_duration: フェードイン時間（0.5秒）
  - out_duration: フェードアウト時間（0.5秒）

#### 位置プリセット
6つの位置プリセットが用意されています：
- `top-left`: 左上
- `top-center`: 上中央
- `top-right`: 右上
- `bottom-left`: 左下
- `bottom-center`: 下中央
- `bottom-right`: 右下

#### その他の設定
- **video**: 動画エンコード設定
- **music**: 背景音楽の音量とフェード
- **video_concat**: 動画結合時の設定

## カスタマイズ例

### タイトルのフォントサイズを変更
```yaml
title:
  default:
    fontsize: 96
```

### テキストオーバーレイの背景を半透明の青に変更
```yaml
text_overlay:
  default:
    box:
      color: blue@0.5
```

### フェード時間を長くする
```yaml
text_overlay:
  default:
    fade:
      in_duration: 1.0
      out_duration: 1.0
```

## 色の指定方法
- 基本色: `white`, `black`, `red`, `blue`, `green`, `yellow`
- 透明度付き: `black@0.5`（50%不透明）
- 16進数: `#FFFFFF`（一部のみ対応）

## 注意事項
- フォントファイルのパスはシステムに依存します
- 透明度は@記号の後に0.0～1.0の値で指定
- 位置の計算式では`w`=動画幅、`h`=動画高、`text_w`=テキスト幅、`text_h`=テキスト高が使用可能