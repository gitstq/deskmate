<div align="center">

# 🐾 DeskMate

### 跨平台桌面虛擬伴侶 | Cross-Platform Desktop Virtual Companion

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![Tests](https://img.shields.io/badge/tests-27%20passed-brightgreen.svg)]()
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

**[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md)**

---

</div>

## 🎉 專案介紹

**DeskMate** 是一款輕量級、跨平台的桌面虛擬伴侶工具。牠在你的桌面上養一隻可愛的虛擬寵物，陪伴你工作、學習，同時內建番茄鐘專注計時器和系統資源監控，讓桌面不再孤單。

### ✨ 靈感來源

靈感來自 GitHub Trending 上的 `desktop-fly`（macOS 桌面 3D 果蠅）專案。我們在此基礎上做了全面的差異化升級：

- 🌍 **跨平台支援**：不再儘限於 macOS，完美執行 Windows / macOS / Linux
- 🎨 **多角色選擇**：貓 / 狗 / 兔 / 狐 四種寵物，各有獨特外觀與動畫
- 🖼️ **程式化繪製**：所有角色使用 QPainter 純程式碼繪製，**零外部圖片素材**，包體極小
- 🍅 **實用功能**：內建番茄鐘、系統監控，不只是好看，更能提升效率
- ⚙️ **高度可客製**：縮放、寵物切換、功能開關，一切盡在掌控

### 🎯 解決的痛點

- 長時間面對螢幕工作感到孤單，需要一個可愛的陪伴
- 番茄鐘工具太枯燥，缺乏趣味性和持續使用動力
- 系統監控工具太重，只想輕量查看 CPU / 記憶體狀態
- 桌面寵物工具要嘛平台受限，要嘛依賴大量外部素材

---

## ✨ 核心特性

### 🐾 四種可愛寵物角色

| 角色 | 特點 | 標誌性動作 |
|------|------|-----------|
| 🐱 **小貓咪** | 橘色毛髮，俏皮尾巴 | 搖尾巴、舔爪子 |
| 🐶 **小狗狗** | 棕色垂耳，熱情活潑 | 搖尾巴、吐舌頭 |
| 🐰 **小兔子** | 雪白絨毛，長耳朵 | 耳朵擺動、蹦跳 |
| 🦊 **小狐狸** | 橘紅皮毛，金色豎瞳 | 大尾巴搖擺、火焰特效 |

### 🎭 豐富的狀態與動畫

- **8 種狀態**：待機 / 行走 / 睡眠 / 進食 / 玩耍 / 開心 / 難過 / 好奇
- **智慧狀態機**：根據飽食度、快樂度、精力值自動切換行為
- **流暢動畫**：60fps 重新整理，呼吸、眨眼、行走、搖尾一應俱全
- **對話氣泡**：寵物會根據狀態說出有趣的台詞

### 🍅 內建番茄鐘

- ⏱️ 自訂工作 / 休息時長（預設 25 分鐘工作 + 5 分鐘休息）
- 📊 即時倒數計時顯示，進度條可視化
- 🔔 完成提醒，寵物會為你慶祝
- 📈 自動統計完成的番茄數

### 💻 輕量級系統監控

- 📊 即時顯示 CPU 使用率
- 🧠 即時顯示記憶體使用率
- 🪶 Linux 下直接讀取 `/proc` 零依賴，其他平台可選 psutil
- 🎨 半透明懸浮資訊條，不遮擋工作

### 🖼️ 透明置頂視窗

- 👻 完全透明背景，寵物彷彿浮在桌面上
- 📌 始終置頂，不會被其他視窗遮擋
- 🖱️ 拖曳移動，想放哪裡放哪裡
- 🖱️ 左鍵撫摸、雙擊玩耍、右鍵選單

### 🔧 系統托盤整合

- 📥 最小化到托盤，不佔工作列
- 🎛️ 托盤選單快速切換寵物、控制番茄鐘
- 🔔 系統通知提醒
- 👁️ 一鍵顯示 / 隱藏寵物

---

## 🚀 快速開始

### 📋 環境需求

- **Python**: 3.8 或更高版本
- **作業系統**: Windows 10+ / macOS 10.14+ / Linux (需支援 X11/Wayland)
- **依賴**: PyQt5 5.15+

### 📦 安裝步驟

#### 方式一：pip 安裝（推薦）

```bash
# 複製倉庫
git clone https://github.com/gitstq/deskmate.git
cd deskmate

# 安裝依賴
pip install -r requirements.txt

# 安裝為命令列工具
pip install -e .
```

#### 方式二：直接執行

```bash
git clone https://github.com/gitstq/deskmate.git
cd deskmate
pip install PyQt5
python -m deskmate.main
```

### ▶️ 啟動執行

```bash
# 啟動 DeskMate
deskmate

# 或使用模組方式
python -m deskmate.main

# 指定寵物啟動
deskmate --pet fox --name 小火

# 列出所有可用寵物
deskmate --list-pets

# 查看版本
deskmate --version
```

啟動後，寵物會出現在螢幕右下角，右鍵寵物開啟選單進行互動！

---

## 📖 詳細使用指南

### 🖱️ 互動操作

| 操作 | 效果 |
|------|------|
| **左鍵單擊** | 撫摸寵物，快樂度 +10 |
| **左鍵雙擊** | 和寵物玩耍，快樂度 +25 |
| **左鍵拖曳** | 移動寵物到任意位置 |
| **右鍵單擊** | 開啟功能選單 |
| **托盤左鍵** | 顯示 / 隱藏寵物 |

### 🍖 寵物餵養與照顧

透過右鍵選單可以進行以下操作：

- **🍖 餵食**：飽食度 +30，寵物進入進食狀態
- **🎾 玩耍**：快樂度 +25，精力 -10，寵物開心蹦跳
- **🤚 撫摸**：快樂度 +10，寵物露出享受表情
- **😴 睡覺**：精力 +40，寵物進入睡眠狀態（會出現 Zzz）
- **🧼 清潔**：清潔度恢復滿，寵物閃閃發光

寵物的四項屬性會隨時間緩慢下降，記得定期照顧哦！

### 🍅 番茄鐘使用

1. 右鍵寵物 → 「🍅 開始專注」啟動番茄鐘
2. 寵物頭頂出現倒數計時狀態列，紅色表示工作中，綠色表示休息中
3. 工作結束後自動進入休息，寵物會彈出慶祝對話
4. 可隨時暫停 / 停止 / 跳過休息

自訂時長：
```bash
deskmate  # 啟動後編輯 ~/.deskmate/config.json
```
```json
{
  "pomodoro_work_minutes": 25,
  "pomodoro_break_minutes": 5
}
```

### 💻 系統監控

- 啟用後，寵物左上角顯示半透明資訊條：`💻 CPU 23%  MEM 56%`
- Linux 下直接讀取 `/proc/stat` 和 `/proc/meminfo`，零額外依賴
- Windows / macOS 下如安裝 psutil 可獲得更精確資料
- 可在設定中關閉：`"enable_system_monitor": false`

### 🔍 縮放調整

右鍵選單 → 「🔍 縮放」可選 75% / 100% / 125% / 150%，適配不同解析度螢幕。

### ⚙️ 設定檔

設定檔位於 `~/.deskmate/config.json`，所有設定均可手動編輯：

```json
{
  "pet_species": "cat",
  "pet_name": "Mate",
  "scale": 1.0,
  "always_on_top": true,
  "enable_pomodoro": true,
  "pomodoro_work_minutes": 25,
  "pomodoro_break_minutes": 5,
  "enable_system_monitor": true,
  "sound_enabled": false,
  "language": "zh_CN"
}
```

### 🎬 執行截圖

> 📸 在此處新增執行截圖 / Add screenshots here

---

## 💡 設計思路與迭代規劃

### 🏗️ 技術架構

```
deskmate/
├── deskmate/
│   ├── __init__.py          # 版本資訊
│   ├── main.py              # GUI 主入口
│   ├── cli.py               # 命令列入口
│   ├── pet.py               # 寵物基類 + 狀態機
│   ├── window.py            # 透明桌面視窗 + 渲染
│   ├── tray.py              # 系統托盤整合
│   ├── pets/                # 寵物角色定義
│   │   ├── cat.py           # 🐱 小貓咪
│   │   ├── dog.py           # 🐶 小狗狗
│   │   ├── bunny.py         # 🐰 小兔子
│   │   └── fox.py           # 🦊 小狐狸
│   └── utils/               # 工具模組
│       ├── config.py        # JSON 設定管理
│       ├── pomodoro.py      # 番茄鐘計時器
│       └── system_monitor.py # 系統資源監控
├── tests/                   # 單元測試（27 個）
├── build.sh                 # 跨平台打包腳本
├── requirements.txt         # 依賴清單
└── setup.py                 # 安裝設定
```

### 🎯 技術選型原因

| 技術 | 選擇原因 |
|------|---------|
| **Python** | 跨平台、開發效率高、生態豐富 |
| **PyQt5** | 成熟穩定、支援透明視窗 / 系統托盤 / 高DPI、社群活躍 |
| **QPainter 程式化繪製** | 零外部素材、包體小、可無限縮放不失真、易於客製 |
| **JSON 設定** | 人類可讀、易於編輯、無額外依賴 |
| **/proc 直讀** | Linux 下零依賴取得系統資訊，無需安裝 psutil |

### 🗺️ 後續迭代計畫

- [ ] 🎵 新增音效支援（寵物叫聲、互動回饋音）
- [ ] 🌙 深色 / 淺色主題自適應
- [ ] 🎨 更多寵物角色（熊貓、倉鼠、龍等）
- [ ] 👗 寵物皮膚 / 裝扮系統
- [ ] 📊 番茄鐘資料統計與週報
- [ ] 🌐 多語言介面（日 / 韓 / 西）
- [ ] 🖼️ 寵物互動動畫增強（追逐滑鼠、躲避點擊）
- [ ] 📱 行動端適配
- [ ] 🔄 開機自啟動設定

### 🤝 社群貢獻方向

- 新增寵物角色（參考 `CONTRIBUTING.md`）
- 翻譯文件到更多語言
- 回報 Bug 和功能建議
- 最佳化動畫效果和效能

---

## 📦 打包與部署指南

### 🐧 Linux 打包

```bash
# 安裝打包工具
pip install pyinstaller

# 執行打包腳本
chmod +x build.sh
./build.sh linux

# 產物位於 release/linux/
# DeskMate-1.0.0-linux-x86_64
```

### 🍎 macOS 打包

```bash
pip install pyinstaller
chmod +x build.sh
./build.sh macos

# 產物位於 release/macos/
# DeskMate-1.0.0-macos
```

### 🪟 Windows 打包

```bash
pip install pyinstaller
build.sh windows

# 或在 PowerShell 中
pyinstaller --name DeskMate --windowed --onefile deskmate/main.py

# 產物位於 dist/DeskMate.exe
```

### 📋 相容環境

| 平台 | 最低版本 | 透明視窗 | 系統托盤 |
|------|---------|---------|---------|
| Windows | 10 | ✅ | ✅ |
| macOS | 10.14 (Mojave) | ✅ | ✅ |
| Linux (X11) | 任意主流發行版 | ✅（需合成器） | ✅ |
| Linux (Wayland) | 任意主流發行版 | ⚠️ 部分支援 | ✅ |

> ⚠️ **Linux 注意**：透明視窗需要桌面環境啟用合成器（Compositor）。GNOME/KDE 預設啟用，部分輕量視窗管理員需手動設定。

---

## 🤝 貢獻指南

我們歡迎所有形式的貢獻！請參考 [CONTRIBUTING.md](CONTRIBUTING.md) 了解詳細規範。

### 📝 提交規範

遵循 Angular 提交資訊規範：

```
feat: 新增功能
fix: 修復問題
docs: 文件更新
style: 程式碼格式
refactor: 程式碼重構
test: 測試相關
chore: 構建/工具
```

### 🧪 執行測試

```bash
python -m pytest tests/ -v
# 或
python -m unittest discover tests/ -v
```

---

## 📄 開源協議說明

本專案基於 **MIT 協議** 開源，詳見 [LICENSE](LICENSE)。

你可以自由地使用、複製、修改、合併、發佈、分發、再授權和銷售本軟體的副本，只需在所有副本中包含原始版權聲明和許可聲明。

---

<div align="center">

**如果 DeskMate 給你帶來了快樂，請給個 ⭐ Star 支持一下！**

Made with ❤️ by DeskMate Team

</div>
