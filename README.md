# Vertex Weight Viewer for Blender

Advanced vertex weight overlay tool designed.
Displays active vertex weights and total weight sums directly in the 3D viewport, with support for weight limit warnings.

<img width="1584" height="867" alt="image" src="https://github.com/user-attachments/assets/4eeddaf0-99f9-4392-adba-c5a8a82a2f36" />

## ✨ Features

- **Real-time Overlay**: Displays vertex weights directly on the mesh in Edit Mode and Weight Paint Mode.
- **Dual Display**:
  - **Active Weight**: Shows the weight of the currently selected vertex group (Default: Yellow).
  - **Total Weight**: Shows the normalized sum of all weights on the vertex (Default: Cyan). Essential for checking normalization (should be 1.0).
- **Influence Limit Warning**:
  - Highlights vertices that exceed a specified number of bone influences (e.g., > 4 bones).
  - Critical for optimizing assets for game engines like Unity, Unreal Engine, or VRChat.
  - Customizable threshold and warning color (Default: Red).
- **Customization**:
  - Adjust font sizes and colors for all elements.
  - Toggle elements on/off individually.
- **Blender Support**: Compatible with Blender 4.0+ and 5.0+.

## 📦 Installation

1. Download the `vertex_weight_viewer.py` file.
2. Open Blender.
3. Go to `Edit > Preferences > Add-ons`.
4. Click **Install...** and select the downloaded file.
5. Enable the checkbox for **3D View: Vertex Weight Viewer**.

## 🚀 Usage

1. Select a Mesh object.
2. Enter **Weight Paint Mode** or **Edit Mode**.
3. Open the **Sidebar (N-Panel)** in the 3D Viewport.
4. Navigate to the **Item** tab.
5. In the **Weight Viewer** panel:
   - Check **Show Overlay** to enable the tool.
   - Adjust **Active/Total Weight** visibility preferences.
   - Enable **Influence Limit Warning** and set your **Max Bones** limit (e.g., 4) to detect overflow.

## ⚙️ Configuration

- **Show Overlay**: Main toggle for the addon.
- **Show Total Weight**: Toggle display of the sum of weights.
- **Display Settings**:
  - **Active Weight**: Font size and color for the selected group's weight.
  - **Total Weight**: Font size and color for the total weight sum.
- **Influence Limit Warning**:
  - **Max Bones**: Integer threshold. Vertices influenced by more bones than this number will be highlighted.
  - Warning color applies to the text when the limit is exceeded.

## 📝 Requirements

- Blender 5.0+ (Tested on 5.0.1).

## 📄 License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details.

---

# Vertex Weight Viewer for Blender (日本語)

高機能ウェイトオーバーレイツールです。
アクティブな頂点ウェイトと、ウェイトの合計値を3Dビューポート上に直接表示します。ウェイト数制限の警告機能も搭載しています。

![Vertex Weight Viewer Demo](https://github.com/akiRAM2/vertex-weight-viewer/assets/demo_image.png)

## ✨ 機能

- **リアルタイムオーバーレイ**: 編集モードおよびウェイトペイントモードで、メッシュ上に直接ウェイト値を表示します。
- **デュアル表示**:
  - **Active Weight (アクティブウェイト)**: 現在選択している頂点グループのウェイトを表示します（デフォルト：黄色）。
  - **Total Weight (合計ウェイト)**: 頂点に割り当てられた全ウェイトの合計を表示します（デフォルト：シアン）。正規化（合計1.0）の確認に必須です。
- **影響数制限の警告 (Influence Limit Warning)**:
  - 指定したボーン数（例：4本）を超えて影響を受けている頂点をハイライト表示します。
  - Unity、Unreal Engine、VRChatなどのゲームエンジン向けアセットの最適化に重要です。
  - 閾値と警告色はカスタマイズ可能です（デフォルト：赤）。
- **カスタマイズ**:
  - 全要素のフォントサイズと色を調整可能。
  - 各要素の表示/非表示を個別に切り替え可能。
- **Blenderサポート**: Blender 4.0以降および5.0以降に対応。

## 📦 インストール方法

1. `vertex_weight_viewer.py` ファイルをダウンロードします。
2. Blenderを開きます。
3. `編集 (Edit) > プリファレンス (Preferences) > アドオン (Add-ons)` に移動します。
4. **インストール... (Install...)** をクリックし、ダウンロードしたファイルを選択します。
5. **3D View: Vertex Weight Viewer** のチェックボックスを有効にします。

## 🚀 使い方

1. メッシュオブジェクトを選択します。
2. **ウェイトペイントモード** または **編集モード** に入ります。
3. 3Dビューポートで **サイドバー (N-Panel)** を開きます（ショートカット：`N`）。
4. **Item** タブに移動します。
5. **Weight Viewer** パネルで以下を操作します：
   - **Show Overlay** をチェックしてツールを有効にします。
   - **Active/Total Weight** の表示設定を調整します。
   - **Influence Limit Warning** を有効にし、**Max Bones**（制限数）を設定して、オーバーフローしている頂点を検出します。

## ⚙️ 設定項目

- **Show Overlay**: アドオンのメインスイッチ。
- **Show Total Weight**: ウェイト合計値の表示切り替え。
- **Display Settings**:
  - **Active Weight**: 選択中のグループウェイトのフォントサイズと色。
  - **Total Weight**: 合計ウェイトのフォントサイズと色。
- **Influence Limit Warning**:
  - **Max Bones**: 整数の閾値。この数より多くのボーンから影響を受けている頂点がハイライトされます。
  - 警告色は、制限を超えた数値のテキストに適用されます。

## 📝 必要要件

- Blender 5.0以降 (5.0.1で動作確認済み)

## 📄 ライセンス

このプロジェクトは GPL-3.0 ライセンスの下で公開されています。詳細は LICENSE ファイルをご確認ください。
