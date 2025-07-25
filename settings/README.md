# Settings Directory

このディレクトリには、動画処理ワークフローで使用されるプロンプトとFFmpeg設定ファイルが含まれています。

## ファイル一覧

### 1. video-analysis-prompts.md
動画分析フェーズで使用されるプロンプト設定（タイトル生成とテキストオーバーレイ）。
- タイトル生成：20文字以内の日本語タイトル
- テキストオーバーレイ：重要シーンへの説明テキスト（最大7-8個）
- 両方ともGemini Vision APIを使用

### 2. image-generation-prompt.md
タイトル画面の背景画像を生成するためのプロンプト設定。
- Imagen4 Fast APIを使用
- シネマティックなスタイルの画像生成
- 高品質4K解像度

### 3. music-generation-prompt.md
背景音楽を生成するためのプロンプト設定。
- Google Lyria APIを使用
- 15-30秒の短い音楽
- 動画の内容に合わせたスタイル

### 4. ffmpeg-settings.yml
FFmpegの詳細設定（YAML形式）。
- タイトル画面の設定（フォント、色、サイズ、エフェクト）
- テキストオーバーレイの設定（位置、フェード、背景）
- 動画エンコード設定
- 音楽ミックス設定

## 使用方法

各プロンプトファイルを編集することで、動画処理の挙動をカスタマイズできます。

### 例：タイトル生成を英語に変更する場合
`title-generation-prompt.md`を開き、以下の部分を変更：
```
条件：1. 20文字以内の日本語
↓
条件：1. 50文字以内の英語
```

### 例：テキストオーバーレイの数を増やす場合
`text-overlay-prompt.md`を開き、以下の部分を変更：
```
6. テキスト数は最大7-8個まで
↓
6. テキスト数は最大10-12個まで
```

## 注意事項
- プロンプトを変更する際は、JSON形式の出力指定を維持してください
- APIの制限事項を考慮してください（文字数制限、生成時間など）
- 変更後は必ずテストを実行して動作を確認してください