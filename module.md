# GitHub Actions Modules Documentation

このドキュメントでは、video-text-enhancerワークフローで使用される全モジュールの使い方を説明します。

## 1. ffmpeg-add-music
背景音楽を動画に追加するモジュール

### 必須入力
- `video-path`: 入力動画ファイルパス
- `music-path`: 音楽ファイルパス（mp3またはwav）
- `output-path`: 出力ファイルパス

### オプション入力
- `volume`: 音楽の音量（0.0-1.0、デフォルト: 0.3）

### 出力
- `video-generated`: 音楽付き動画生成の成功可否（true/false）

### 使用例
```yaml
- uses: ./modules/ffmpeg-add-music
  with:
    video-path: "folder/video.mp4"
    music-path: "folder/music/background.mp3"
    volume: '0.3'
    output-path: "folder/final.mp4"
```

## 2. ffmpeg-text-overlay
動画にテキストオーバーレイを適用するモジュール

### 必須入力
- `video-path`: 入力動画ファイルパス
- `descriptions-json`: 説明文JSONファイルのパス（timestamp, text, duration等を含む）
- `output-path`: 出力ファイルパス

### オプション入力
- `fontfile`: フォントファイルのパス（デフォルト: NotoSansCJK）

### 出力
- `video-generated`: オーバーレイ動画生成の成功可否（true/false）

### 使用例
```yaml
- uses: ./modules/ffmpeg-text-overlay
  with:
    video-path: "folder/input.mp4"
    descriptions-json: "folder/analysis/descriptions.json"
    output-path: "folder/output.mp4"
```

## 3. ffmpeg-title-generator
タイトル動画を生成するモジュール

### 必須入力
- `title`: タイトルテキスト
- `duration`: 動画の長さ（秒）
- `output-path`: 出力ファイルパス

### オプション入力
- `background-image`: 背景画像のパス
- `resolution`: 解像度（デフォルト: 1920x1080）
- `fontfile`: フォントファイルのパス
- `fontsize`: フォントサイズ（デフォルト: 72）
- `fontcolor`: フォント色（デフォルト: white）

### 出力
- `video-generated`: タイトル動画生成の成功可否（true/false）

### 使用例
```yaml
- uses: ./modules/ffmpeg-title-generator
  with:
    title: "動画タイトル"
    duration: '5'
    background-image: "folder/title-image/background.jpg"
    output-path: "folder/title.mp4"
```

## 4. ffmpeg-video-concat
2つの動画を結合するモジュール

### 必須入力
- `video1-path`: 最初の動画ファイルパス（通常はタイトル）
- `video2-path`: 2番目の動画ファイルパス（通常は本編）
- `video1-duration`: 最初の動画の長さ（秒）- 音声遅延の計算用
- `output-path`: 出力ファイルパス

### 出力
- `video-generated`: 結合動画生成の成功可否（true/false）

### 使用例
```yaml
- uses: ./modules/ffmpeg-video-concat
  with:
    video1-path: "folder/title.mp4"
    video2-path: "folder/main.mp4"
    video1-duration: '5'
    output-path: "folder/combined.mp4"
```

## 5. gemini-cli-title-image-generator
AI（Gemini + Imagen4）で画像を生成するモジュール

### 必須入力
- `branch-name`: 作業ブランチ名
- `folder-name`: 出力フォルダー名
- `generation-prompt`: Geminiエージェントに渡すプロンプト全体
- `GEMINI_API_KEY`: Gemini API Key
- `T2I_KAMUI_IMAGEN4_FAST_URL`: Text-to-Image API URL

### オプション入力
- `output-path`: 生成された画像の保存パス（デフォルト: title-image/background.jpg）
- `commit-message`: Gitコミットメッセージ（デフォルト: 🖼️ Add generated image）

### 出力
- `image-generated`: 画像生成の成功可否（true/false）

### 使用例
```yaml
- uses: ./modules/gemini-cli-title-image-generator
  with:
    branch-name: ${{ needs.setup-branch.outputs.branch-name }}
    folder-name: ${{ needs.setup-branch.outputs.folder-name }}
    generation-prompt: |
      🖼️ **タイトル画像生成タスク**
      
      タイトル「${{ needs.analyze-video.outputs.title }}」に基づいた背景画像を生成してください。
      
      1. `mkdir -p ${{ needs.setup-branch.outputs.folder-name }}/title-image`
      2. タイトルに合った高品質な背景画像のプロンプトを作成（英語で、cinematic style, professional lighting等を含む）
      3. `mcp__t2i-kamui-imagen4-fast__imagen4_fast_submit`で生成開始
      4. `mcp__t2i-kamui-imagen4-fast__imagen4_fast_status`で完了確認（最大30回、5秒間隔）
      5. `mcp__t2i-kamui-imagen4-fast__imagen4_fast_result`でURL取得
      6. **必須**: `curl -L -o "$(pwd)/${{ needs.setup-branch.outputs.folder-name }}/title-image/background.jpg" "$IMAGE_URL"`でダウンロード
      7. ファイルサイズが1KB未満なら再試行
      8. generation-info.jsonに生成情報を保存
    GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
    T2I_KAMUI_IMAGEN4_FAST_URL: ${{ secrets.T2I_KAMUI_IMAGEN4_FAST_URL }}
```

## 6. gemini-cli-music-generator  
AI（Gemini + Google Lyria）で音楽を生成するモジュール

### 必須入力
- `branch-name`: 作業ブランチ名
- `folder-name`: 出力フォルダー名
- `generation-prompt`: Geminiエージェントに渡すプロンプト全体
- `GEMINI_API_KEY`: Gemini API Key
- `T2M_KAMUI_LYRIA_URL`: Text-to-Music API URL

### オプション入力
- `output-path`: 生成された音楽の保存パス（デフォルト: music/background.mp3）
- `commit-message`: Gitコミットメッセージ（デフォルト: 🎵 Add generated music）

### 出力
- `music-generated`: 音楽生成の成功可否（true/false）

### 使用例
```yaml
- uses: ./modules/gemini-cli-music-generator
  with:
    branch-name: ${{ needs.setup-branch.outputs.branch-name }}
    folder-name: ${{ needs.setup-branch.outputs.folder-name }}
    generation-prompt: |
      🎵 **背景音楽生成タスク**
      
      タイトル「${{ needs.analyze-video.outputs.title }}」に合った背景音楽を生成してください。
      
      1. `mkdir -p ${{ needs.setup-branch.outputs.folder-name }}/music`
      2. 動画のトーンに合った音楽ジャンルを選択（ambient, cinematic等）
      3. `mcp__t2m-kamui-lyria__lyria_submit`で生成開始（short, 20-second, ambient music）
      4. `mcp__t2m-kamui-lyria__lyria_status`で完了確認（最大30回、5秒間隔）
      5. `mcp__t2m-kamui-lyria__lyria_result`でURL取得
      6. **必須**: `curl -L -o "$(pwd)/${{ needs.setup-branch.outputs.folder-name }}/music/background.mp3" "$MUSIC_URL"`でダウンロード
      7. ファイルサイズが50KB未満なら再試行
      8. generation-info.jsonに生成情報を保存
    GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
    T2M_KAMUI_LYRIA_URL: ${{ secrets.T2M_KAMUI_LYRIA_URL }}
```

## 7. gemini_analyzer.py (Pythonスクリプト)
動画や画像を汎用的に分析するPythonスクリプト

### 必須引数
- `file_path`: 分析する動画または画像ファイルのパス

### オプション引数
- `--prompt`: カスタムプロンプト（デフォルト: 動画を分析して内容を説明）
- `--output`: 出力ファイルパス（指定しない場合は標準出力）
- `--format`: 出力形式（json, text, markdown、デフォルト: json）
- `--model`: 使用するGeminiモデル（デフォルト: gemini-2.0-flash-exp）
- `--verbose`: 詳細なログ出力

### 環境変数
- `GEMINI_API_KEY`: Gemini API Key（必須）

### 使用例

#### 動画タイトル分析
```bash
python scripts/gemini_analyzer.py videos/input.mp4 \
  --prompt "この動画の内容を分析し、適切なタイトルを提案してください。応答は以下のJSON形式で返してください：{\"title\": \"提案するタイトル\", \"reason\": \"タイトルの理由\"}" \
  --output folder/analysis/title.json \
  --format json
```

#### 動画説明文生成
```bash
python scripts/gemini_analyzer.py videos/input.mp4 \
  --prompt "動画の重要な瞬間を特定し、説明文を生成してください。タイムスタンプ形式（MM:SS）で、各瞬間に6秒程度の説明文を付けてください。" \
  --output folder/analysis/descriptions.json \
  --format json
```

#### 動画サマリー生成
```bash
python scripts/gemini_analyzer.py videos/input.mp4 \
  --prompt "この動画の詳細な要約を作成してください。主要なトピック、重要なポイント、全体的な印象を含めてください。" \
  --output folder/analysis/summary.md \
  --format markdown
```

#### 画像分析
```bash
python scripts/gemini_analyzer.py images/photo.jpg \
  --prompt "この画像の内容を詳しく説明してください。" \
  --format text
```

### 出力形式
- **json**: 構造化されたJSONデータ
- **text**: プレーンテキスト
- **markdown**: Markdown形式のドキュメント

### エラーハンドリング
- ファイルが存在しない場合はエラー終了
- API呼び出しが失敗した場合は詳細なエラーメッセージを出力
- 大きすぎるファイル（200MB以上）は警告を表示

## 8. claude-code-image-generator
Claude Code Actionを使用して画像を生成するモジュール

### 必須入力
- `claude-code-oauth-token`: Claude Code OAuthトークン
- `env-var-value`: ツールURL（GitHubシークレットから）
- `title`: 画像のタイトル
- `folder-name`: 保存先フォルダー名
- `image-prompt`: 画像生成プロンプト

### オプション入力
- `mcp-config-file`: MCP設定ファイルパス（デフォルト: settings/ClaudeCodeAction/.mcp.json）
- `tool-name`: MCPツール名（デフォルト: t2i-kamui-imagen4-fast）
- `env-var-name`: 環境変数名（デフォルト: T2I_KAMUI_IMAGEN4_FAST_URL）
- `output-directory`: 出力ディレクトリ（デフォルト: title-image）

### 出力
- `image-generated`: 画像生成の成功可否（true/false）

### 使用例
```yaml
- uses: ./modules/claude-code-image-generator
  with:
    claude-code-oauth-token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
    env-var-value: ${{ secrets.T2I_KAMUI_IMAGEN4_FAST_URL }}
    title: "動画タイトル"
    folder-name: "folder"
    image-prompt: "cinematic landscape with professional lighting"
```

## 9. claude-code-music-generator
Claude Code Actionを使用して音楽を生成するモジュール

### 必須入力
- `claude-code-oauth-token`: Claude Code OAuthトークン
- `env-var-value`: ツールURL（GitHubシークレットから）
- `title`: 音楽のタイトル
- `folder-name`: 保存先フォルダー名
- `music-prompt`: 音楽生成プロンプト

### オプション入力
- `mcp-config-file`: MCP設定ファイルパス（デフォルト: settings/ClaudeCodeAction/.mcp.json）
- `tool-name`: MCPツール名（デフォルト: t2m-kamui-lyria）
- `env-var-name`: 環境変数名（デフォルト: T2M_KAMUI_LYRIA_URL）
- `output-directory`: 出力ディレクトリ（デフォルト: music）

### 出力
- `music-generated`: 音楽生成の成功可否（true/false）

### 使用例
```yaml
- uses: ./modules/claude-code-music-generator
  with:
    claude-code-oauth-token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
    env-var-value: ${{ secrets.T2M_KAMUI_LYRIA_URL }}
    title: "動画タイトル"
    folder-name: "folder"
    music-prompt: "ambient cinematic background music"
```

## 10. mcp-tool-extractor
MCP設定ファイルから特定のツールを抽出するモジュール

### 必須入力
- `input-file`: 入力MCPファイル名（例: 2.mcp.json）
- `output-file`: 出力MCPファイル名（例: extracted.mcp.json）
- `tool-names`: 抽出するツール名（カンマ区切り）

### オプション入力
- `replace-env-vars`: 環境変数を置換するか（デフォルト: true）
- `T2I_FAL_WAN_V22_A14B_URL`: t2i-kamui-wan-v2-2-a14b用シークレット
- `T2V_FAL_WAN_V22_5B_FAST_URL`: t2v-kamui-wan-v2-2-5b-fast用シークレット
- `T2I_FAL_QWEN_IMAGE_URL`: t2i-kamui-qwen-image用シークレット
- `T2I_KAMUI_IMAGEN4_FAST_URL`: t2i-kamui-imagen4-fast用シークレット
- `T2M_GOOGLE_LYRIA_URL`: t2m-kamui-lyria用シークレット

### 出力
- `extraction-success`: ツール抽出の成功状態
- `extracted-tools`: 抽出されたツールのリスト

### 使用例
```yaml
- uses: ./modules/mcp-tool-extractor
  with:
    input-file: "settings/ClaudeCodeAction/.mcp.json"
    output-file: ".mcp.json"
    tool-names: "t2i-kamui-imagen4-fast,t2m-kamui-lyria"
    replace-env-vars: "true"
    T2I_KAMUI_IMAGEN4_FAST_URL: ${{ secrets.T2I_KAMUI_IMAGEN4_FAST_URL }}
    T2M_GOOGLE_LYRIA_URL: ${{ secrets.T2M_KAMUI_LYRIA_URL }}
```

### 特徴
- 複数のMCPツールを選択的に抽出可能
- 環境変数プレースホルダーの自動置換
- JSON構文の検証機能
- GitHub Actionsワークフローへの統合が容易

## 共通の注意事項

1. **パス指定**: 全てのパスは作業ディレクトリからの相対パスで指定
2. **シークレット**: API URLやキーはGitHub Secretsに保存し、`${{ secrets.SECRET_NAME }}`で参照
3. **エラーハンドリング**: 各モジュールは成功/失敗を出力として返すので、後続の処理で確認可能
4. **レート制限対策**: gemini-cliモジュールは自動的に2回までリトライ（60秒待機）
5. **.gemini/ディレクトリ**: gemini-cliモジュールは一時的に.gemini/settings.jsonを作成しますが、処理終了後に自動削除されます
6. **Claude Code Action**: claude-code-image-generatorとclaude-code-music-generatorモジュールはClaude Code OAuthトークンが必要
7. **MCP設定**: mcp-tool-extractorを使用してMCP設定から必要なツールのみを抽出し、環境変数を安全に置換