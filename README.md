<div align="center">

# 🐾 DeskMate

### 跨平台桌面虚拟伴侣 | Cross-Platform Desktop Virtual Companion

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![Tests](https://img.shields.io/badge/tests-27%20passed-brightgreen.svg)]()
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

**[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md)**

---

</div>

## 🎉 项目介绍

**DeskMate** 是一款轻量级、跨平台的桌面虚拟伴侣工具。它在你的桌面上养一只可爱的虚拟宠物，陪伴你工作、学习，同时内置番茄钟专注计时器和系统资源监控，让桌面不再孤单。

### ✨ 灵感来源

灵感来自 GitHub Trending 上的 `desktop-fly`（macOS 桌面 3D 果蝇）项目。我们在此基础上做了全面的差异化升级：

- 🌍 **跨平台支持**：不再局限于 macOS，完美运行 Windows / macOS / Linux
- 🎨 **多角色选择**：猫 / 狗 / 兔 / 狐 四种宠物，各有独特外观与动画
- 🖼️ **程序化绘制**：所有角色使用 QPainter 纯代码绘制，**零外部图片素材**，包体极小
- 🍅 **实用功能**：内置番茄钟、系统监控，不只是好看，更能提升效率
- ⚙️ **高度可定制**：缩放、宠物切换、功能开关，一切尽在掌控

### 🎯 解决的痛点

- 长时间面对屏幕工作感到孤单，需要一个可爱的陪伴
- 番茄钟工具太枯燥，缺乏趣味性和持续使用动力
- 系统监控工具太重，只想轻量查看 CPU / 内存状态
- 桌面宠物工具要么平台受限，要么依赖大量外部素材

---

## ✨ 核心特性

### 🐾 四种可爱宠物角色

| 角色 | 特点 | 标志性动作 |
|------|------|-----------|
| 🐱 **小猫咪** | 橘色毛发，俏皮尾巴 | 摇尾巴、舔爪子 |
| 🐶 **小狗狗** | 棕色垂耳，热情活泼 | 摇尾巴、吐舌头 |
| 🐰 **小兔子** | 雪白绒毛，长耳朵 | 耳朵摆动、蹦跳 |
| 🦊 **小狐狸** | 橘红皮毛，金色竖瞳 | 大尾巴摇摆、火焰特效 |

### 🎭 丰富的状态与动画

- **8 种状态**：待机 / 行走 / 睡眠 / 进食 / 玩耍 / 开心 / 难过 / 好奇
- **智能状态机**：根据饱食度、快乐度、精力值自动切换行为
- **流畅动画**：60fps 刷新，呼吸、眨眼、行走、摇尾一应俱全
- **对话气泡**：宠物会根据状态说出有趣的台词

### 🍅 内置番茄钟

- ⏱️ 自定义工作 / 休息时长（默认 25 分钟工作 + 5 分钟休息）
- 📊 实时倒计时显示，进度条可视化
- 🔔 完成提醒，宠物会为你庆祝
- 📈 自动统计完成的番茄数

### 💻 轻量级系统监控

- 📊 实时显示 CPU 使用率
- 🧠 实时显示内存使用率
- 🪶 Linux 下直接读取 `/proc` 零依赖，其他平台可选 psutil
- 🎨 半透明悬浮信息条，不遮挡工作

### 🖼️ 透明置顶窗口

- 👻 完全透明背景，宠物仿佛浮在桌面上
- 📌 始终置顶，不会被其他窗口遮挡
- 🖱️ 拖拽移动，想放哪里放哪里
- 🖱️ 左键抚摸、双击玩耍、右键菜单

### 🔧 系统托盘集成

- 📥 最小化到托盘，不占任务栏
- 🎛️ 托盘菜单快速切换宠物、控制番茄钟
- 🔔 系统通知提醒
- 👁️ 一键显示 / 隐藏宠物

---

## 🚀 快速开始

### 📋 环境要求

- **Python**: 3.8 或更高版本
- **操作系统**: Windows 10+ / macOS 10.14+ / Linux (需支持 X11/Wayland)
- **依赖**: PyQt5 5.15+

### 📦 安装步骤

#### 方式一：pip 安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/gitstq/deskmate.git
cd deskmate

# 安装依赖
pip install -r requirements.txt

# 安装为命令行工具
pip install -e .
```

#### 方式二：直接运行

```bash
git clone https://github.com/gitstq/deskmate.git
cd deskmate
pip install PyQt5
python -m deskmate.main
```

### ▶️ 启动运行

```bash
# 启动 DeskMate
deskmate

# 或使用模块方式
python -m deskmate.main

# 指定宠物启动
deskmate --pet fox --name 小火

# 列出所有可用宠物
deskmate --list-pets

# 查看版本
deskmate --version
```

启动后，宠物会出现在屏幕右下角，右键宠物打开菜单进行交互！

---

## 📖 详细使用指南

### 🖱️ 交互操作

| 操作 | 效果 |
|------|------|
| **左键单击** | 抚摸宠物，快乐度 +10 |
| **左键双击** | 和宠物玩耍，快乐度 +25 |
| **左键拖拽** | 移动宠物到任意位置 |
| **右键单击** | 打开功能菜单 |
| **托盘左键** | 显示 / 隐藏宠物 |

### 🍖 宠物喂养与照顾

通过右键菜单可以进行以下操作：

- **🍖 喂食**：饱食度 +30，宠物进入进食状态
- **🎾 玩耍**：快乐度 +25，精力 -10，宠物开心蹦跳
- **🤚 抚摸**：快乐度 +10，宠物露出享受表情
- **😴 睡觉**：精力 +40，宠物进入睡眠状态（会出现 Zzz）
- **🧼 清洁**：清洁度恢复满，宠物闪闪发光

宠物的四项属性会随时间缓慢下降，记得定期照顾哦！

### 🍅 番茄钟使用

1. 右键宠物 → 「🍅 开始专注」启动番茄钟
2. 宠物头顶出现倒计时状态栏，红色表示工作中，绿色表示休息中
3. 工作结束后自动进入休息，宠物会弹出庆祝对话
4. 可随时暂停 / 停止 / 跳过休息

自定义时长：
```bash
deskmate  # 启动后编辑 ~/.deskmate/config.json
```
```json
{
  "pomodoro_work_minutes": 25,
  "pomodoro_break_minutes": 5
}
```

### 💻 系统监控

- 启用后，宠物左上角显示半透明信息条：`💻 CPU 23%  MEM 56%`
- Linux 下直接读取 `/proc/stat` 和 `/proc/meminfo`，零额外依赖
- Windows / macOS 下如安装 psutil 可获得更精确数据
- 可在配置中关闭：`"enable_system_monitor": false`

### 🔍 缩放调整

右键菜单 → 「🔍 缩放」可选 75% / 100% / 125% / 150%，适配不同分辨率屏幕。

### ⚙️ 配置文件

配置文件位于 `~/.deskmate/config.json`，所有设置均可手动编辑：

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

### 🎬 运行截图

> 📸 在此处添加运行截图 / Add screenshots here

---

## 💡 设计思路与迭代规划

### 🏗️ 技术架构

```
deskmate/
├── deskmate/
│   ├── __init__.py          # 版本信息
│   ├── main.py              # GUI 主入口
│   ├── cli.py               # 命令行入口
│   ├── pet.py               # 宠物基类 + 状态机
│   ├── window.py            # 透明桌面窗口 + 渲染
│   ├── tray.py              # 系统托盘集成
│   ├── pets/                # 宠物角色定义
│   │   ├── cat.py           # 🐱 小猫咪
│   │   ├── dog.py           # 🐶 小狗狗
│   │   ├── bunny.py         # 🐰 小兔子
│   │   └── fox.py           # 🦊 小狐狸
│   └── utils/               # 工具模块
│       ├── config.py        # JSON 配置管理
│       ├── pomodoro.py      # 番茄钟计时器
│       └── system_monitor.py # 系统资源监控
├── tests/                   # 单元测试（27 个）
├── build.sh                 # 跨平台打包脚本
├── requirements.txt         # 依赖清单
└── setup.py                 # 安装配置
```

### 🎯 技术选型原因

| 技术 | 选择原因 |
|------|---------|
| **Python** | 跨平台、开发效率高、生态丰富 |
| **PyQt5** | 成熟稳定、支持透明窗口 / 系统托盘 / 高DPI、社区活跃 |
| **QPainter 程序化绘制** | 零外部素材、包体小、可无限缩放不失真、易于定制 |
| **JSON 配置** | 人类可读、易于编辑、无额外依赖 |
| **/proc 直读** | Linux 下零依赖获取系统信息，无需安装 psutil |

### 🗺️ 后续迭代计划

- [ ] 🎵 添加音效支持（宠物叫声、交互反馈音）
- [ ] 🌙 深色 / 浅色主题自适应
- [ ] 🎨 更多宠物角色（熊猫、仓鼠、龙等）
- [ ] 👗 宠物皮肤 / 装扮系统
- [ ] 📊 番茄钟数据统计与周报
- [ ] 🌐 多语言界面（日 / 韩 / 西）
- [ ] 🖼️ 宠物互动动画增强（追逐鼠标、躲避点击）
- [ ] 📱 移动端适配
- [ ] 🔄 开机自启动配置

### 🤝 社区贡献方向

- 新增宠物角色（参考 `CONTRIBUTING.md`）
- 翻译文档到更多语言
- 报告 Bug 和功能建议
- 优化动画效果和性能

---

## 📦 打包与部署指南

### 🐧 Linux 打包

```bash
# 安装打包工具
pip install pyinstaller

# 执行打包脚本
chmod +x build.sh
./build.sh linux

# 产物位于 release/linux/
# DeskMate-1.0.0-linux-x86_64
```

### 🍎 macOS 打包

```bash
pip install pyinstaller
chmod +x build.sh
./build.sh macos

# 产物位于 release/macos/
# DeskMate-1.0.0-macos
```

### 🪟 Windows 打包

```bash
pip install pyinstaller
build.sh windows

# 或在 PowerShell 中
pyinstaller --name DeskMate --windowed --onefile deskmate/main.py

# 产物位于 dist/DeskMate.exe
```

### 📋 兼容环境

| 平台 | 最低版本 | 透明窗口 | 系统托盘 |
|------|---------|---------|---------|
| Windows | 10 | ✅ | ✅ |
| macOS | 10.14 (Mojave) | ✅ | ✅ |
| Linux (X11) | 任意主流发行版 | ✅（需合成器） | ✅ |
| Linux (Wayland) | 任意主流发行版 | ⚠️ 部分支持 | ✅ |

> ⚠️ **Linux 注意**：透明窗口需要桌面环境启用合成器（Compositor）。GNOME/KDE 默认启用，部分轻量窗口管理器需手动配置。

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！请参考 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细规范。

### 📝 提交规范

遵循 Angular 提交信息规范：

```
feat: 新增功能
fix: 修复问题
docs: 文档更新
style: 代码格式
refactor: 代码重构
test: 测试相关
chore: 构建/工具
```

### 🧪 运行测试

```bash
python -m pytest tests/ -v
# 或
python -m unittest discover tests/ -v
```

---

## 📄 开源协议说明

本项目基于 **MIT 协议** 开源，详见 [LICENSE](LICENSE)。

你可以自由地使用、复制、修改、合并、发布、分发、再授权和销售本软件的副本，只需在所有副本中包含原始版权声明和许可声明。

---

<div align="center">

**如果 DeskMate 给你带来了快乐，请给个 ⭐ Star 支持一下！**

Made with ❤️ by DeskMate Team

</div>
