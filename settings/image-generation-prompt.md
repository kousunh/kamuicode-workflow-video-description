# タイトル背景画像生成プロンプト

## 概要
動画のタイトル画面用の背景画像を生成するためのプロンプトです。Gemini CLIとImagen4 Fast APIを使用して、タイトルに適した高品質な背景画像を生成します。

## プロンプト
```
🖼️ **タイトル画像生成タスク**

タイトル「${TITLE}」に基づいた背景画像を生成してください。

1. `mkdir -p ${FOLDER_NAME}/title-image`
2. タイトルから高品質な背景画像のプロンプトを作成（英語で、cinematic, bokeh effect, warm color palette等を含む）
3. `mcp__t2i-fal-imagen4-fast__imagen4_fast_submit`で生成開始
4. `mcp__t2i-fal-imagen4-fast__imagen4_fast_status`で完了確認（最大20回）
5. `mcp__t2i-fal-imagen4-fast__imagen4_fast_result`でURL取得
6. 重要: 必ず`curl -L -o "$(pwd)/${FOLDER_NAME}/title-image/background.jpg" "$IMAGE_URL"`でダウンロード
7. generation-info.jsonに生成情報を保存
```

## 画像生成のガイドライン

### 推奨スタイル要素
- **cinematic**: 映画のような雰囲気
- **bokeh effect**: 背景のぼかし効果
- **warm color palette**: 暖色系の色調
- **high quality**: 高品質
- **4K resolution**: 高解像度
- **professional photography**: プロフェッショナルな写真風

### プロンプト例
タイトルが「簡単10分パスタレシピ」の場合：
```
A cinematic kitchen scene with warm lighting, pasta ingredients on a wooden table, shallow depth of field with bokeh effect, warm color palette, professional food photography, 4K resolution
```

## 処理フロー
1. **ディレクトリ作成**: title-imageフォルダを作成
2. **プロンプト生成**: タイトルから英語のプロンプトを作成
3. **画像生成開始**: Imagen4 Fast APIに生成リクエスト
4. **ステータス確認**: 最大20回まで完了を確認
5. **URL取得**: 生成された画像のURLを取得
6. **ダウンロード**: curlコマンドで画像をダウンロード
7. **情報保存**: 生成情報をJSONファイルに保存

## カスタマイズ方法
- **スタイルを変更**: `cinematic, bokeh effect, warm color palette`の部分を編集
- **解像度を変更**: `4K resolution`を他の解像度に変更
- **アスペクト比を指定**: プロンプトに`16:9 aspect ratio`などを追加
- **特定の色調**: `warm color palette`を`cool tones`や`monochrome`に変更
- **アートスタイル**: `minimalist`, `abstract`, `realistic`などを追加

## 注意事項
- 必ず英語でプロンプトを作成してください
- ダウンロードパスは絶対パスで指定してください
- 生成に失敗した場合は最大20回まで再試行されます