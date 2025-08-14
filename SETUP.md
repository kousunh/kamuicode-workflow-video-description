# Video Text Enhancer Workflow セットアップガイド

## 前提条件

- GitHubアカウント
- Gemini API有効化
- （オプション）GitHub Personal Access Token

## ステップ1: Google Gemini APIキーの取得

1. [Google AI Studio](https://makersuite.google.com/app/apikey)にアクセス
2. 「Get API key」をクリック
3. 新しいAPIキーを作成またはプロジェクトを選択
4. 生成されたAPIキーをコピー

## ステップ2: GitHubリポジトリの準備

### 2.1 リポジトリのクローン
```bash
# このリポジトリをクローン
git clone https://github.com/kousunh/kamuicode-workflow-video-description.git
cd kamuicode-workflow-video-description
```

### 2.2 ディレクトリ構成の確認
クローン後のディレクトリ構成：
```
kamuicode-workflow-video-description/
├── .github/
│   └── workflows/
│       ├── CCA-video-text-enhancer.yml    # Claude Code Action版ワークフロー
│       ├── Gemini-video-text-enhancer.yml # Gemini CLI Action版ワークフロー
│       └── re-edit-video.yml              # 再編集ワークフローファイル
├── scripts/
│   └── gemini_analyzer.py    # 汎用動画/画像分析スクリプト
├── modules/
│   ├── claude-code-image-generator/       # CCA画像生成モジュール
│   ├── claude-code-music-generator/       # CCA音楽生成モジュール
│   ├── gemini-cli-title-image-generator/  # Gemini画像生成モジュール
│   ├── gemini-cli-music-generator/        # Gemini音楽生成モジュール
│   ├── ffmpeg-add-music/                  # 音楽追加モジュール
│   ├── ffmpeg-text-overlay/               # テキストオーバーレイモジュール
│   ├── ffmpeg-title-generator/            # タイトル動画生成モジュール
│   ├── ffmpeg-video-concat/               # 動画結合モジュール
│   └── workflow-summary-generator/        # サマリー生成モジュール
├── settings/                               # 各種設定ファイル
│   ├── ClaudeCodeAction/                  # CCA用設定
│   ├── ffmpeg-settings.yml                # FFmpeg設定
│   ├── ffmpeg-settings-readme.md          # FFmpeg設定説明
│   ├── video-analysis-prompts.md          # 動画分析プロンプト
│   ├── image-generation-prompt.md         # 画像生成プロンプト
│   └── music-generation-prompt.md         # 音楽生成プロンプト
├── videos/
│   └── README.md                           # 動画ディレクトリの説明
├── README.md
├── SETUP.md
└── LICENSE
```

### 2.3 ワークフローファイルの配置
自分のリポジトリにワークフローを設定する場合：

```bash
# ワークフローファイルがすでに.github/workflowsにある場合はコピー不要
# 使用したいワークフローを選択してコピー：

# Claude Code Action版を使用する場合：
cp CCA-video-text-enhancer.yml .github/workflows/

# または、Gemini CLI Action版を使用する場合：
cp Gemini-video-text-enhancer.yml .github/workflows/

# 再編集ワークフロー（共通）
cp re-edit-video.yml .github/workflows/

# サンプル動画を配置（任意）
cp your-video.mp4 videos/
```

## ⚠️ 重要な設定事項

### ワークフロー別の設定要件

#### Claude Code Action版の場合
- Claude Code Actionのサブスクリプションプランによる設定、またはClaude APIが必要です
- KAMUI CODEへのアクセスはClaude Code Action経由で行われます
- `.mcp.json`ファイルは`settings/ClaudeCodeAction/`に配置済み
- GitHub Actionsワークフロー実行時に、GitHub Secretsの値を使用してMCP URLが自動的に展開されます

##### Claude Code Actionの設定方法（サブスクリプションプラン利用）

**OAuthトークンの自動セットアップ（推奨）**

1. **Claude Codeでセットアップコマンドを実行**
   ```bash
   /install-github-app
   ```

2. **自動的に実行される処理**
   - Claude Code ActionがあなたのGitHubリポジトリにプルリクエストを作成
   - プルリクエストには以下が含まれます：
     - 必要なGitHub Secretsの設定
     - `claude.yml`ワークフローファイル（Issue/PR用）

3. **プルリクエストをマージ**
   - 内容を確認してマージすると、以下が自動設定されます：
     - `CLAUDE_CODE_OAUTH_TOKEN`: GitHub Secretsに自動登録
     - `claude.yml`: Issue/PR用のワークフロー
   - これでClaude Code Actionが使用可能になります

4. **設定完了の確認**
   - GitHub Secretsに`CLAUDE_CODE_OAUTH_TOKEN`が追加されていることを確認
   - このトークンはCCA-video-text-enhancer.ymlで使用されます

**注意事項**
- `/install-github-app`で作成される`claude.yml`は、Issue/PRからClaude Code Actionを呼び出す際に使用
- `CCA-video-text-enhancer.yml`の実行には直接関係ありませんが、削除する必要はありません
- リポジトリの管理者権限が必要です

#### Gemini CLI Action版の場合
- `.gemini/settings.json`ファイルは**手動で作成する必要はありません**
- GitHub Actionsワークフロー実行時に、GitHub Secretsの値を使用して自動的に生成されます

### 必須設定

#### 両ワークフロー共通
- `GEMINI_API_KEY`: Gemini APIキー（動画分析用）
- `PAT_TOKEN`: GitHub Personal Access Token（PR自動作成用、オプション）

#### Claude Code Action版の追加設定

**サブスクリプションプランを使用する場合：**
- `CLAUDE_CODE_OAUTH_TOKEN`: `/install-github-app`コマンドで自動設定されるOAuthトークン
  
  ※手動でトークンを生成する場合は`claude setup-token`コマンドを使用

**APIキーを使用する場合：**
- `ANTHROPIC_API_KEY`: Anthropic APIキー

**KAMUI CODE接続用：**
- `T2I_KAMUI_IMAGEN4_FAST_URL`: Imagen4 FastのKAMUI CODEサーバーURL
- `T2M_KAMUI_LYRIA_URL`: Google LyriaのKAMUI CODEサーバーURL

※これらのURLはセキュリティ保護のためGitHub Secretsで管理し、`settings/ClaudeCodeAction/.mcp.json`内では環境変数として参照されます

#### Gemini CLI Action版の追加設定
- `T2I_KAMUI_IMAGEN4_FAST_URL`: Imagen4 FastのMCPサーバーURL
- `T2M_KAMUI_LYRIA_URL`: Google LyriaのMCPサーバーURL

**セキュリティ上の利点**:
- KAMUI CODEのMCPサーバーURLは機密情報としてGitHub Secretsで安全に管理されます
- リポジトリにコミットされることがないため、公開リポジトリでも安全に使用できます
- Claude Code Action版: `settings/ClaudeCodeAction/.mcp.json`内で環境変数として参照
- Gemini CLI Action版: ワークフロー実行時に`.gemini/settings.json`を動的生成

### AI生成ツールについて

両ワークフローともKAMUI CODEのツールを使用します：
- **画像生成**: Imagen4 Fast
- **音楽生成**: Google Lyria

アクセス方法の違い：
- **Claude Code Action版**: 
  - Claude Code Action経由でKAMUI CODEにアクセス
  - 設定ファイル: `settings/ClaudeCodeAction/.mcp.json`
  - URLはGitHub Secretsで管理（セキュリティ保護）
- **Gemini CLI Action版**: 
  - Gemini CLI経由でKAMUI CODEにアクセス
  - 設定ファイル: `.gemini/settings.json`（ワークフロー実行時に自動生成）
  - URLはGitHub Secretsで管理（セキュリティ保護）

## ステップ3: GitHubシークレットの設定

1. GitHubリポジトリページで「Settings」タブをクリック
2. 左メニューから「Secrets and variables」→「Actions」を選択
3. 「New repository secret」をクリック

### 必須シークレット（両ワークフロー共通）
- **Name**: `GEMINI_API_KEY`
- **Secret**: 取得したGemini APIキー

### Claude Code Action版のみ必要

#### サブスクリプションプランの場合：
- **Name**: `CLAUDE_CODE_OAUTH_TOKEN`
- **Secret**: `/install-github-app`コマンドで自動設定、または`claude setup-token`で生成

#### APIキーの場合：
- **Name**: `ANTHROPIC_API_KEY`
- **Secret**: Anthropicから取得したAPIキー
こちらを利用する場合、ワークフローをAPIキーを使うように編集しなければなりません。現在は上記のサブスクリプションプランのOAuthトークンを使うようになっています。

#### KAMUI CODE接続用：
- **Name**: `T2I_KAMUI_IMAGEN4_FAST_URL`
- **Secret**: KAMUI CODE MCPサーバーのImagen4 FastエンドポイントURL
- **Name**: `T2M_KAMUI_LYRIA_URL`
- **Secret**: KAMUI CODE MCPサーバーのGoogle LyriaエンドポイントURL


- **Name**: `T2I_KAMUI_IMAGEN4_FAST_URL`
- **Secret**: KAMUI CODE MCPサーバーのImagen4 FastエンドポイントURL
- **Name**: `T2M_KAMUI_LYRIA_URL`
- **Secret**: KAMUI CODE MCPサーバーのGoogle LyriaエンドポイントURL

### オプションシークレット（PR自動作成用）
- **Name**: `PAT_TOKEN`
- **Secret**: GitHub Personal Access Token

⚠️ **セキュリティ上の注意**: 
- APIキーやトークンを直接ワークフローファイルに記載しないでください
- 必ずGitHub Secretsを使用してください

#### Personal Access Tokenの作成方法：
1. GitHub → Settings → Developer settings → Personal access tokens
2. 「Generate new token」をクリック
3. 必要な権限を選択：
   - `repo`（フルアクセス）
   - `workflow`
4. トークンを生成してコピー

## ステップ4: 動画ファイルの追加

```bash
# 動画ファイルをvideosディレクトリにコピー
cp /path/to/your/video.mp4 videos/

# コミットしてプッシュ
git add videos/your-video.mp4
git commit -m "Add sample video"
git push origin main
```

**注意**: Pythonパッケージのインストールは不要です。GitHub Actions環境で自動的にインストールされます。

## ステップ5: ワークフローの実行

### 手動実行
1. GitHubリポジトリの「Actions」タブを開く
2. 左サイドバーから使用するワークフローを選択：
   - 「CCA-Video Text Enhancer」（Claude Code Action版）
   - 「Gemini-Video Text Enhancer」（Gemini CLI Action版）
3. 「Run workflow」ボタンをクリック
4. パラメータを入力：
   - **video_path**: 
     - `auto-select`（最新の動画を自動選択）
     - または具体的なパス（例：`videos/sample.mp4`）
   - **edit_title**: カスタムタイトル（オプション）
   - **text_position**: テキスト表示位置（auto/左上/上/右上/左下/下/右下）
   - **generate_title_image**: AI背景画像生成（true/false、デフォルトtrue）
   - **generate_background_music**: AI背景音楽生成（true/false、デフォルトtrue）
5. 「Run workflow」をクリックして実行

## ステップ6: 結果の確認

### ワークフロー実行中
- Actionsタブで進行状況を確認
- 各ステップのログを確認可能

### 実行完了後
1. 自動的に新しいブランチが作成される
2. プルリクエストが作成される（PAT_TOKEN設定時）
3. PRページで生成された成果物を確認

## よくある質問

### Q: ワークフローが表示されない
A: `.github/workflows/`ディレクトリにYAMLファイルが正しく配置されているか確認してください。

### Q: 「auto-select」が動作しない
A: `videos/`ディレクトリに動画ファイルが存在することを確認してください。

### Q: Gemini APIキーのエラーが出る
A: APIキーが正しく設定されているか、API制限に達していないか確認してください。

### Q: AI画像/音楽生成がエラーになる

#### Claude Code Action版の場合
A: 以下を確認してください：
- `CLAUDE_CODE_OAUTH_TOKEN`が正しく設定されているか
- Claude Code Actionの設定ファイル
- KAMUI CODEのMCP URLの設定
- API制限とレートリミット

#### Gemini CLI Action版の場合
A: GitHub Secretsに`T2I_KAMUI_IMAGEN4_FAST_URL`と`T2M_KAMUI_LYRIA_URL`が正しく設定されているか確認してください。

### Q: 高速に処理したい
A: AI生成機能を無効にしてください（`generate_title_image`と`generate_background_music`を`false`に設定）。

## Re-Edit Video ワークフローの使用方法

### 概要
既存の編集済み動画を再編集するためのワークフローです。`video-text-enhancer.yml`で生成されたブランチ内のフォルダにある分析結果、タイトル画像、背景音楽を活用して、最終動画を再編集できます。

### 実行手順
1. GitHubリポジトリの「Actions」タブを開く
2. 左サイドバーから「Re-Edit Existing Video」を選択
3. 「Run workflow」ボタンをクリック
4. パラメータを入力：
   - **text_position**: テキスト表示位置（default/左上/上/右上/左下/下/右下）
   - **add_title_image**: 既存のタイトル画像を使用（チェックボックス）
   - **add_background_music**: 既存の背景音楽を使用（チェックボックス）
5. 「Run workflow」をクリックして実行

### 動作の詳細
- 最新のmovie-editフォルダを自動検出
- mainブランチでフォルダが見つからない場合、最新のvideo-editブランチを自動検索
- 既存のreport.mdまたはre-edit-report.mdからビデオ情報を読み取り
- 選択されたオプションに基づいて動画を再編集

## カスタマイズ設定

### FFmpeg設定
タイトルや説明テキストのスタイル設定は、`settings/ffmpeg-settings-readme.md`を参照してください。

### プロンプト設定
各種AI生成のプロンプトは以下のファイルで管理されています：
- **動画分析**: `settings/video-analysis-prompts.md`
- **画像生成**: `settings/image-generation-prompt.md`
- **音楽生成**: `settings/music-generation-prompt.md`

## トラブルシューティング

### 画像・音楽が生成されない

#### Claude Code Action版
- `CLAUDE_CODE_OAUTH_TOKEN`の設定を確認（`claude setup-token`で再生成）
- Claude Code Actionの設定ファイルが正しく配置されているか確認
- KAMUI CODEのMCP URLがGitHub Secretsに正しく設定されているか確認
- ワークフローの画像・音楽生成ジョブの詳細ログを確認
- Claude APIのレートリミットで止まっている可能性があります

#### Gemini CLI Action版
- ワークフローの画像・音楽生成ジョブの詳細ログを確認してください
- Gemini CLI Actionのレートリミットで止まっている可能性があります
- GitHub Secretsの`T2I_KAMUI_IMAGEN4_FAST_URL`と`T2M_KAMUI_LYRIA_URL`が正しく設定されているか確認してください

### Re-Edit Videoでフォルダが見つからない
- mainブランチで実行している場合、自動的に最新のvideo-editブランチを検索します
- 特定のブランチで作業したい場合は、そのブランチを選択してワークフローを実行してください

## サポート

問題が発生した場合は、以下を確認してください：
1. Actionsタブのワークフローログ
2. 各ステップの詳細ログ
3. GitHubリポジトリのIssuesセクション