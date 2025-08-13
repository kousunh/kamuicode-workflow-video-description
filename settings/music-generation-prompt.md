# 背景音楽生成プロンプト

## 概要
動画用の背景音楽を生成するためのプロンプトです。Gemini CLIとGoogle Lyria APIを使用して、タイトルと内容に適した15-30秒の短い音楽を生成します。

## プロンプト
```
🎵 **音楽生成タスク**

タイトル「${TITLE}」と内容「${DESCRIPTIONS_SUMMARY}」に基づいた15-30秒の短い音楽を生成してください。

1. `mkdir -p ${FOLDER_NAME}/music`
2. 英語で音楽プロンプトを作成（例: "A short 20-second ambient music"）
3. `mcp__t2m-kamui-lyria__lyria_submit`で生成開始
4. `mcp__t2m-kamui-lyria__lyria_status`で完了確認（最大30回、5秒間隔）
5. `mcp__t2m-kamui-lyria__lyria_result`でURL取得
6. **必須**: `curl -L -f --retry 3 -o "$(pwd)/${FOLDER_NAME}/music/background.wav" "$MUSIC_URL"`でダウンロード
7. ファイルサイズが50KB未満なら再試行
8. generation-info.jsonに生成情報を保存
```

## 音楽生成のガイドライン

### 推奨音楽スタイル
- **ambient**: 環境音楽、雰囲気重視
- **upbeat**: 明るく活気のある
- **calm**: 穏やかで落ち着いた
- **energetic**: エネルギッシュな
- **minimal**: ミニマルな構成
- **cinematic**: 映画的な壮大さ

### プロンプト例
1. **料理動画の場合**:
   ```
   A short 20-second upbeat and cheerful cooking background music with light percussion and acoustic guitar
   ```

2. **技術解説動画の場合**:
   ```
   A short 25-second minimal electronic ambient music with soft synth pads for technology tutorial
   ```

3. **旅行動画の場合**:
   ```
   A short 30-second adventurous and inspiring world music with ethnic instruments
   ```

## 処理フロー
1. **ディレクトリ作成**: musicフォルダを作成
2. **プロンプト生成**: タイトルと内容から英語のプロンプトを作成
3. **音楽生成開始**: Google Lyria APIに生成リクエスト
4. **ステータス確認**: 最大30回まで5秒間隔で完了を確認
5. **URL取得**: 生成された音楽のURLを取得
6. **ダウンロード**: curlコマンドで音楽ファイルをダウンロード（3回まで再試行）
7. **サイズ確認**: 50KB未満の場合は再生成
8. **情報保存**: 生成情報をJSONファイルに保存

## カスタマイズ方法
- **長さを変更**: `15-30秒`を他の長さに変更（例: `10-20秒`）
- **ジャンルを指定**: `ambient`を`jazz`, `classical`, `electronic`などに変更
- **楽器を指定**: `piano solo`, `string quartet`, `synthesizer`などを追加
- **テンポを指定**: `slow tempo (60 BPM)`, `medium tempo (120 BPM)`などを追加
- **雰囲気を詳細に**: `mysterious`, `romantic`, `dramatic`などの形容詞を追加

## 注意事項
- 必ず英語でプロンプトを作成してください
- 生成される音楽は.wav形式です
- ファイルサイズが50KB未満の場合は生成失敗とみなされます
- 最大30回のステータス確認で完了しない場合はタイムアウトします