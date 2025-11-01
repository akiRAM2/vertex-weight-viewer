# Vertex Weight Viewer / 頂点ウェイトビューワー

<img width="795" height="534" alt="image" src="https://github.com/user-attachments/assets/444f6da4-e39b-4b65-bf08-f11a1e847073" />
<img width="1481" height="993" alt="image" src="https://github.com/user-attachments/assets/4cc3563d-85de-45d6-9a4d-c4bbc552b0cd" />

A Blender addon that displays vertex group weights as numerical overlays in weight paint and edit modes.

ウェイトペイントモードとEditモード中に、頂点グループのウェイト値を数値オーバーレイとして表示するBlenderアドオンです。

## Features / 機能

✨ **Dual Display System** - Shows active vertex group (large) + total weight (small) simultaneously  
�️ **Flexible Display Control** - Toggle total weight display on/off as needed  
�🎨 **Individual Customization** - Separate font sizes and colors for each display type  
🔄 **Multi-Mode Support** - Works in both Weight Paint and Edit modes  
⚡ **Auto-Activation** - Automatically displays on Blender startup and file loads  
🎯 **Smart Display** - Shows only non-zero values for clean visualization  
📋 **Easy Controls** - Simple toggles and organized UI panel options

**デュアル表示システム** - アクティブ頂点グループ（大）+ 合計ウェイト（小）を同時表示  
**柔軟な表示制御** - 必要に応じて合計ウェイト表示をオン/オフ切り替え  
**個別カスタマイズ** - それぞれの表示タイプで異なるフォントサイズと色を設定  
**マルチモードサポート** - ウェイトペイントモードとEditモードの両方で動作  
**自動アクティベーション** - Blender起動時とファイル読み込み時に自動表示  
**スマート表示** - 0より大きい値のみ表示してクリーンな視覚化を実現  
**簡単操作** - シンプルな切り替えと整理されたUIパネルオプション

## Installation / インストール

1. Download the `vertex_weight_viewer.py` file / `vertex_weight_viewer.py` ファイルをダウンロード
2. Open Blender and go to Edit > Preferences > Add-ons / Blenderを開き、編集 > プリファレンス > アドオンへ移動
3. Click "Install..." and select the downloaded file / 「インストール...」をクリックしてダウンロードしたファイルを選択
4. Enable the addon by checking the checkbox next to "Vertex Weight Viewer" / 「Vertex Weight Viewer」の隣のチェックボックスをオンにしてアドオンを有効化

**Note:** If the addon doesn't work after initial installation, try pressing N key to open the sidebar menu and click "Show Overlay" to toggle the display.

**注意:** 初回インストール時に動作しない場合は、Nキーのメニューから「Show Overlay」を押して切り替えてみてください。

## Usage / 使用方法

1. Select a mesh object with vertex groups / 頂点グループを持つメッシュオブジェクトを選択
2. Enter Weight Paint or Edit mode / ウェイトペイントモードまたはEditモードに入る
3. Open the sidebar (N key) and go to the "Item" tab to find the "Weight Viewer" panel / サイドバー（Nキー）を開いて「Item」タブの「Weight Viewer」パネルを探す
4. Toggle "Show Overlay" to display vertex weights / 「Show Overlay」をオンにして頂点ウェイトを表示
5. **Optional**: Toggle "Show Total Weight" to enable/disable total weight display / **オプション**: 「Show Total Weight」で合計ウェイト表示をオン/オフ切り替え
6. **Adjust font sizes**: Set "Active Vertex Group Size" and optionally "Total Weight Size" / **フォントサイズ調整**: 「Active Vertex Group Size」と必要に応じて「Total Weight Size」を設定
7. **Customize colors**: Set different colors for active group and total weight displays / **色のカスタマイズ**: アクティブグループと合計ウェイト表示それぞれに異なる色を設定

## Requirements / 動作環境

- Blender 4.0 or later (including 5.0+) / Blender 4.0以降（5.0+を含む）

## License / ライセンス

This project is licensed under the GNU General Public License v3.0 or later - see the [LICENSE](LICENSE) file for details.

このプロジェクトはGNU General Public License v3.0以降の下でライセンスされています - 詳細は [LICENSE](LICENSE) ファイルをご覧ください。

## Contributing / コントリビューション

Feel free to fork this repository and make your own improvements!

フォークはご自由にどうぞ！

## Credits / クレジット

This addon was written entirely by GitHub Copilot.

このアドオンはGitHub Copilotによって全て書かれました。
