# Video Text Enhancer Workflow セットアップガイド

## 前提条件

- GitHubアカウント
- Google Cloud ProjectとGemini API有効化
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
├── video-text-enhancer.yml    # ワークフローファイル
├── scripts/
│   └── gemini_analyzer.py    # 汎用動画/画像分析スクリプト
├── modules/
│   ├── ffmpeg-add-music/     # 音楽追加モジュール
│   ├── ffmpeg-text-overlay/  # テキストオーバーレイモジュール
│   ├── ffmpeg-title-generator/  # タイトル動画生成モジュール
│   ├── ffmpeg-video-concat/  # 動画結合モジュール
│   ├── gemini-cli-music-generator/  # AI音楽生成モジュール
│   └── gemini-cli-title-image-generator/  # AI画像生成モジュール
├── videos/
│   └── README.md             # 動画ディレクトリの説明
├── README.md
├── SETUP.md
├── module.md                 # モジュール詳細説明
└── LICENSE
```

### 2.3 ワークフローファイルの配置
自分のリポジトリにワークフローを設定する場合：

```bash
# ワークフローディレクトリを作成
mkdir -p .github/workflows

# ワークフローファイルをコピー
cp video-text-enhancer.yml .github/workflows/

# サンプル動画を配置（任意）
cp your-video.mp4 videos/
```

## ⚠️ 重要な設定事項

### kamuicode MCP設定

**重要**: `.gemini/settings.json`ファイルは**手動で作成する必要はありません**。GitHub Actionsワークフロー実行時に、GitHub Secretsの値を使用して自動的に生成されます。

**必須設定**:
- GitHubリポジトリのSecretsに以下の値を設定するだけで動作します：
  - `T2I_FAL_IMAGEN4_FAST_URL`: Imagen4 FastのMCPサーバーURL
  - `T2M_GOOGLE_LYRIA_URL`: Google LyriaのMCPサーバーURL
  - `GEMINI_API_KEY`: Gemini APIキー

**セキュリティ上の利点**:
- MCPサーバーのURLは機密情報としてGitHub Secretsで安全に管理されます
- リポジトリにコミットされることがないため、公開リポジトリでも安全に使用できます
- ワークフロー実行時にのみ、一時的に`.gemini/settings.json`が作成されます

**自動生成される設定ファイルの内容**:
```json
{
  "mcpServers": {
    "t2i-fal-imagen4-fast": {
      "httpUrl": "<T2I_FAL_IMAGEN4_FAST_URLの値>",
      "timeout": 300000
    },
    "t2m-google-lyria": {
      "httpUrl": "<T2M_GOOGLE_LYRIA_URLの値>",
      "timeout": 300000
    }
  },
  "coreTools": [
    "ReadFileTool",
    "WriteFileTool", 
    "EditFileTool",
    "ShellTool"
  ]
}
```
※ `<T2I_FAL_IMAGEN4_FAST_URLの値>`と`<T2M_GOOGLE_LYRIA_URLの値>`には、GitHub Secretsに設定した実際のURLが挿入されます

### MCPツールの限定設定

**重要**: 全てのMCPツールを設定すると、gemini特有の問題で利用できないツールがある場合にエラーになります。（Gemini CLI actionがSettings.jsonを読み込む際に、MCPツールの有効性を全部確認しているようです。）

このワークフローでは以下のツールのみを使用：
- Imagen4 Fast（画像生成）
- Google Lyria（音楽生成）

### 権限設定

ワークフローファイルには以下の権限設定が必要です：

```yaml
permissions:
  contents: write
  pull-requests: write
```

## ステップ3: GitHubシークレットの設定

1. GitHubリポジトリページで「Settings」タブをクリック
2. 左メニューから「Secrets and variables」→「Actions」を選択
3. 「New repository secret」をクリック

### 必須シークレット
- **Name**: `GEMINI_API_KEY`
- **Secret**: 取得したGemini APIキー
- **Name**: `T2I_FAL_IMAGEN4_FAST_URL`
- **Secret**: kamuicode MCPサーバーのImagen4 FastエンドポイントURL（上記settings.jsonの`t2i-fal-imagen4-fast-url`に設定するURL）
- **Name**: `T2M_GOOGLE_LYRIA_URL`
- **Secret**: kamuicode MCPサーバーのGoogle LyriaエンドポイントURL（上記settings.jsonの`t2m-google-lyria-url`に設定するURL）

### オプションシークレット（PR自動作成用）
- **Name**: `PAT_TOKEN`
- **Secret**: GitHub Personal Access Token

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
2. 左サイドバーから「Video Text Enhancer」を選択
3. 「Run workflow」ボタンをクリック
4. パラメータを入力：
   - **video_path**: 
     - `auto-select`（最新の動画を自動選択）
     - または具体的なパス（例：`videos/sample.mp4`）
   - **edit_title**: カスタムタイトル（オプション）
   - **description_prompt**: 説明文生成の追加指示（オプション）
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

## サポート

問題が発生した場合は、以下を確認してください：
1. Actionsタブのワークフローログ
2. 各ステップの詳細ログ
3. GitHubリポジトリのIssuesセクション