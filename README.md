# 智能台灯控制系统 / Smart Lamp Control System / スマートランプ制御システム

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Kivy](https://img.shields.io/badge/Kivy-2.0+-green.svg)](https://kivy.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Raspberry%20Pi-lightgrey.svg)]()

</div>

<div align="center">

[🇨🇳 中文](#中文) | [🇺🇸 English](#english) | [🇯🇵 日本語](#日本語)

</div>

---

## 中文

### 📋 项目简介

这是一个基于Python和Kivy框架开发的智能台灯控制系统，具有现代化的毛玻璃UI界面和丰富的功能。支持语音控制、高考倒计时、动态壁纸等特性，特别适合学生和办公场景使用。

### ✨ 主要特性

#### 🎨 现代化界面
- **毛玻璃效果**：采用现代毛玻璃设计语言，界面优雅美观
- **动态背景**：支持API动态壁纸，可切换简约和二次元风格
- **响应式布局**：完美适配不同屏幕尺寸
- **流畅动画**：所有交互都有流畅的过渡动画

#### 💡 智能灯光控制
- **硬件控制**：支持GPIO控制真实台灯硬件
- **亮度调节**：0-100%精确亮度控制
- **开关控制**：点击式开关操作
- **PWM调光**：硬件级PWM调光支持

#### 🗣️ 语音控制
- **唤醒词识别**：支持"你好小灯"唤醒
- **中文语音识别**：基于Vosk模型的离线中文识别
- **智能意图解析**：支持开灯、关灯、亮度调节等语音指令
- **免联网操作**：完全离线语音识别

#### 📅 高考倒计时
- **精准倒计时**：实时显示距离2026年高考的剩余时间
- **数字时钟显示**：专业DS-Digital字体显示
- **一言励志**：每日励志语句和诗词展示
- **长按切换**：长按时间框切换到倒计时界面

#### 🌡️ 环境监测
- **温湿度监测**：支持温度和湿度传感器（可模拟）
- **实时更新**：每分钟自动更新传感器数据
- **智能模拟**：开发阶段支持传感器数据模拟

### 🏗️ 技术架构

```
Smart Lamp Control System
├── 用户界面层 (Kivy UI)
│   ├── 毛玻璃效果组件
│   ├── 动态背景管理
│   └── 响应式布局
├── 控制逻辑层 (Python Core)
│   ├── GPIO硬件控制
│   ├── 传感器数据处理
│   └── 配置管理
├── 语音识别层 (Vosk + SoundDevice)
│   ├── 唤醒词检测
│   ├── 语音识别引擎
│   └── 意图解析
└── 硬件抽象层 (GPIO/Mock)
    ├── 树莓派GPIO支持
    ├── PWM调光控制
    └── 传感器接口
```

### 📦 项目结构

```
smart_lamp_project/
├── main_kivy.py              # 主程序入口
├── config.py                 # 配置文件
├── gpio_control.py           # GPIO控制模块
├── sensor_mock.py            # 传感器模拟
├── voice_control.py          # 语音控制模块
├── assets/                   # 资源文件
│   ├── light_on.png          # 开灯图标
│   ├── light_off.png         # 关灯图标
│   ├── Countdown.png         # 倒计时图标
│   ├── loading.gif           # 加载动图
│   └── swich_wallpaper.png   # 切换壁纸图标
├── front/                    # 字体文件
│   ├── 苹方字体.ttf
│   ├── AaLanTingTiShi-LuoBiRuShen-2.ttf
│   ├── NotoEmoji-VariableFont_wght.ttf
│   └── DS-Digital/
├── macosbliss/               # 本地壁纸
│   ├── 01.png ~ 05.png
│   └── 6.jpg
├── vosk-model-small-cn-0.22/ # 中文语音模型
└── __pycache__/              # Python缓存
```

### 🚀 快速开始

#### 环境要求
- Python 3.8+
- Kivy 2.0+
- 支持的操作系统：Windows、Linux、Raspberry Pi OS

#### 安装依赖
```bash
# 克隆项目
git clone [your-repo-url]
cd smart_lamp_project

# 安装Python依赖
pip install kivy requests pillow sounddevice vosk

# 下载中文语音模型（可选）
# 将vosk-model-small-cn-0.22解压到项目根目录
```

#### 运行程序
```bash
# 启动主程序
python main_kivy.py

# 启动语音控制（可选）
python voice_control.py
```

### 🎮 使用指南

#### 基础操作
1. **开关灯**：点击中央灯泡图标
2. **调节亮度**：拖动底部彩色滑块
3. **切换壁纸**：点击右下角切换按钮
4. **查看倒计时**：长按时间框进入倒计时界面

#### 语音控制
1. 运行 `python voice_control.py`
2. 说出唤醒词："你好小灯"
3. 听到确认后说出指令：
   - "开灯" / "打开"
   - "关灯" / "关闭" 
   - "亮度50" / "设置亮度30"

#### 硬件部署
1. 修改 `config.py` 中的 `GPIO_ENABLED = True`
2. 连接继电器到指定GPIO引脚
3. 连接温湿度传感器（可选）
4. 部署到树莓派等设备

### 🔧 配置说明

#### 主要配置项 (config.py)
```python
# GPIO配置
GPIO_ENABLED = False        # 是否启用真实GPIO
GPIO_PIN = 12              # GPIO引脚号

# 字体配置
FONT_PATH_DS_DIGI = "front/DS-Digital/DS-DIGI-1.ttf"
FONT_PATH_MS_YAHEI = "C:/Windows/Fonts/msyh.ttc"

# 高考日期
EXAM_DATE = "2025-06-07"   # 可自定义目标日期

# 颜色主题
BACKGROUND_COLOR = "white"
TEXT_COLOR = "#222"
SLIDER_COLOR = "#4CAF50"
```

### 🌐 API接口

#### 背景壁纸API
- **风景壁纸**：`https://t.alcy.cc/fj`
- **二次元壁纸**：`https://t.alcy.cc/moe`
- **简约壁纸**：`https://t.alcy.cc/pc`

#### 一言API
- **主API**：`https://v1.hitokoto.cn/`
- **备用API**：`https://api.oick.cn/yiyan/api.php`

### 📱 界面预览

#### 主界面特性
- 🎨 毛玻璃质感的现代化设计
- 🌈 渐变色彩滑块
- 🖼️ 动态背景壁纸
- ⏰ 实时时钟显示
- 🌡️ 温湿度显示（可选）

#### 倒计时界面
- 📅 高考倒计时显示
- 💬 励志一言展示  
- 🎨 毛玻璃卡片设计
- 🔄 长按返回主界面

### 🔮 高級功能

#### 语音识别系统
- 基于Vosk的离线中文语音识别
- 支持自定义唤醒词
- 智能意图解析和执行
- 低延迟实时处理

#### 智能硬件控制
- GPIO继电器控制
- PWM精确调光
- 传感器数据采集
- 硬件状态反馈

### 🧪 开发与测试

#### 单元测试
```bash
# 运行GPIO控制测试
python import\ unittest.py

# 测试传感器模拟
python -c "import sensor_mock; print(sensor_mock.read_temperature_sensor())"
```

#### 开发模式
- `GPIO_ENABLED = False`：使用模拟GPIO，适合开发调试
- `GPIO_ENABLED = True`：使用真实GPIO，适合硬件部署

### 🛠️ 故障排除

#### 常见问题
1. **字体显示异常**：确保字体文件路径正确
2. **GPIO控制失败**：检查权限和硬件连接
3. **语音识别无响应**：确认麦克风权限和模型文件
4. **背景图片加载失败**：检查网络连接

#### Debug模式
```python
# 在config.py中启用调试模式
DEBUG_MODE = True
```

### 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

### 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 📞 支持与反馈

如有问题或建议，请通过以下方式联系：
- 提交 GitHub Issue
- [添加你的联系方式]

---

## English

### 📋 Project Overview

An intelligent desk lamp control system built with Python and Kivy framework, featuring modern frosted glass UI and rich functionality. Supports voice control, Gaokao countdown, dynamic wallpapers, and is perfect for students and office scenarios.

### ✨ Key Features

#### 🎨 Modern Interface
- **Frosted Glass Effect**: Modern frosted glass design language with elegant appearance
- **Dynamic Backgrounds**: API-powered dynamic wallpapers with simple and anime styles
- **Responsive Layout**: Perfect adaptation to different screen sizes
- **Smooth Animations**: Fluid transition animations for all interactions

#### 💡 Smart Lighting Control
- **Hardware Control**: GPIO control for real desk lamp hardware
- **Brightness Adjustment**: Precise 0-100% brightness control
- **On/Off Control**: Click-based switch operation
- **PWM Dimming**: Hardware-level PWM dimming support

#### 🗣️ Voice Control
- **Wake Word Recognition**: Supports "你好小灯" (Hello Lamp) wake word
- **Chinese Speech Recognition**: Offline Chinese recognition based on Vosk model
- **Smart Intent Parsing**: Supports voice commands for turning on/off and brightness adjustment
- **Offline Operation**: Complete offline speech recognition

#### 📅 Gaokao Countdown
- **Precise Countdown**: Real-time display of remaining time until Gaokao 2026
- **Digital Clock Display**: Professional DS-Digital font display
- **Daily Quotes**: Daily inspirational quotes and poetry
- **Long Press Toggle**: Long press time box to switch to countdown interface

#### 🌡️ Environmental Monitoring
- **Temperature & Humidity**: Support for temperature and humidity sensors (mockable)
- **Real-time Updates**: Automatic sensor data updates every minute
- **Smart Simulation**: Sensor data simulation support during development

### 🏗️ Technical Architecture

```
Smart Lamp Control System
├── UI Layer (Kivy UI)
│   ├── Frosted Glass Components
│   ├── Dynamic Background Management
│   └── Responsive Layout
├── Control Logic Layer (Python Core)
│   ├── GPIO Hardware Control
│   ├── Sensor Data Processing
│   └── Configuration Management
├── Speech Recognition Layer (Vosk + SoundDevice)
│   ├── Wake Word Detection
│   ├── Speech Recognition Engine
│   └── Intent Parsing
└── Hardware Abstraction Layer (GPIO/Mock)
    ├── Raspberry Pi GPIO Support
    ├── PWM Dimming Control
    └── Sensor Interface
```

### 🚀 Quick Start

#### Requirements
- Python 3.8+
- Kivy 2.0+
- Supported OS: Windows, Linux, Raspberry Pi OS

#### Install Dependencies
```bash
# Clone project
git clone [your-repo-url]
cd smart_lamp_project

# Install Python dependencies
pip install kivy requests pillow sounddevice vosk

# Download Chinese speech model (optional)
# Extract vosk-model-small-cn-0.22 to project root
```

#### Run Program
```bash
# Start main program
python main_kivy.py

# Start voice control (optional)
python voice_control.py
```

### 🎮 Usage Guide

#### Basic Operations
1. **Toggle Light**: Click central bulb icon
2. **Adjust Brightness**: Drag bottom colorful slider
3. **Switch Wallpaper**: Click bottom-right switch button
4. **View Countdown**: Long press time box to enter countdown interface

#### Voice Control
1. Run `python voice_control.py`
2. Say wake word: "你好小灯"
3. After confirmation, say commands:
   - "开灯" (Turn on) / "打开" (Open)
   - "关灯" (Turn off) / "关闭" (Close)
   - "亮度50" (Brightness 50) / "设置亮度30" (Set brightness 30)

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 日本語

### 📋 プロジェクト概要

PythonとKivyフレームワークで構築されたインテリジェントデスクランプ制御システムで、モダンなすりガラスUIと豊富な機能を備えています。音声制御、高考カウントダウン、動的壁紙をサポートし、学生やオフィスのシナリオに最適です。

### ✨ 主な機能

#### 🎨 モダンインターフェース
- **すりガラス効果**：エレガントな外観のモダンすりガラスデザイン言語
- **動的背景**：シンプルとアニメスタイルのAPI動的壁紙
- **レスポンシブレイアウト**：異なる画面サイズへの完璧な適応
- **スムーズアニメーション**：すべてのインタラクションに流れるような遷移アニメーション

#### 💡 スマート照明制御
- **ハードウェア制御**：実際のデスクランプハードウェアのGPIO制御
- **明度調整**：0-100%の精密な明度制御
- **オン/オフ制御**：クリックベースのスイッチ操作
- **PWM調光**：ハードウェアレベルのPWM調光サポート

#### 🗣️ 音声制御
- **ウェイクワード認識**：「你好小灯」ウェイクワードをサポート
- **中国語音声認識**：Voskモデルベースのオフライン中国語認識
- **スマート意図解析**：オン/オフと明度調整の音声コマンドをサポート
- **オフライン操作**：完全オフライン音声認識

#### 📅 高考カウントダウン
- **精密カウントダウン**：2026年高考までの残り時間をリアルタイム表示
- **デジタル時計表示**：プロフェッショナルDS-Digitalフォント表示
- **日々の名言**：日々の励ましの言葉と詩の表示
- **長押し切り替え**：時間ボックスを長押ししてカウントダウンインターフェースに切り替え

#### 🌡️ 環境監視
- **温湿度監視**：温度・湿度センサーのサポート（モック可能）
- **リアルタイム更新**：毎分自動センサーデータ更新
- **スマートシミュレーション**：開発段階でのセンサーデータシミュレーションサポート

### 🚀 クイックスタート

#### 要件
- Python 3.8+
- Kivy 2.0+
- サポートOS：Windows、Linux、Raspberry Pi OS

#### 依存関係のインストール
```bash
# プロジェクトのクローン
git clone [your-repo-url]
cd smart_lamp_project

# Python依存関係のインストール
pip install kivy requests pillow sounddevice vosk

# 中国語音声モデルのダウンロード（オプション）
# vosk-model-small-cn-0.22をプロジェクトルートに展開
```

#### プログラム実行
```bash
# メインプログラムの開始
python main_kivy.py

# 音声制御の開始（オプション）
python voice_control.py
```

### 📄 ライセンス

このプロジェクトはMITライセンスの下でライセンスされています - 詳細は[LICENSE](LICENSE)ファイルを参照してください。

---

<div align="center">

**🎓 すべての学習者を応援します！努力が夢への階段となりますように！**

*Made with ❤️ by [Your Name]*

</div>
