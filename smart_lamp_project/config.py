# config.py

import datetime
import random
import time

# --------------------
# 字体路径
# --------------------
FONT_PATH_DS_DIGI = "front/DS-Digital/DS-DIGI-1.ttf"
FONT_PATH_MS_YAHEI = "C:/Windows/Fonts/msyh.ttc"  # 微软雅黑

# --------------------
# 字体大小
# --------------------
FONT_SIZE_CLOCK = 240
FONT_SIZE_COUNTDOWN_NUMBER = 120
FONT_SIZE_COUNTDOWN_UNIT = 48
FONT_SIZE_COUNTDOWN_TITLE = 48
FONT_SIZE_HITOKOTO = 28

# --------------------
# 颜色配置
# --------------------
BACKGROUND_COLOR = "white"
TEXT_COLOR = "#222"
SLIDER_COLOR = "#4CAF50"
CLOCK_TEXT_COLOR = "#222"
COUNTDOWN_NUMBER_COLOR = "#222"
COUNTDOWN_UNIT_COLOR = "#00eaff"
COUNTDOWN_UNIT_GLOW = "#ffffff"
COUNTDOWN_TITLE_GLOW = "#fff"
HITOKOTO_COLOR = "#888"

# --------------------
# 图标路径
# --------------------
ICON_ON_PATH = "assets/light_on.png"
ICON_OFF_PATH = "assets/light_off.png"

# --------------------
# 倒计时配置
# --------------------
EXAM_DATE = "2025-06-07"  # 高考日期

def get_exam_countdown():
    """返回距离高考的天、小时、分钟"""
    now = datetime.datetime.now()
    target = datetime.datetime.strptime(EXAM_DATE, "%Y-%m-%d")
    delta = target - now
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    return days, hours, minutes

FONT_SIZE = 36
COUNTDOWN_IMAGE_SIZE = (300, 100)

# --------------------
# GPIO 配置
# --------------------
GPIO_ENABLED = False  # 本地调试时关闭，部署时改为 True
GPIO_PIN = 12

# --------------------
# 亮度设置
# --------------------
DEFAULT_BRIGHTNESS = 0  # 0-100 范围

# --------------------
# 传感器模拟与GPIO控制整合
# --------------------
# 传感器模拟
_last_temp = 25.0
_last_humi = 50.0
_last_update = 0

def _update_sensor():
    global _last_temp, _last_humi, _last_update
    now = time.time()
    # 每60秒更新一次
    if now - _last_update > 60:
        _last_temp = round(random.uniform(22.0, 30.0), 1)
        _last_humi = round(random.uniform(40.0, 70.0), 1)
        _last_update = now

def read_temperature_sensor():
    """模拟读取温度（摄氏度），1分钟更新一次"""
    _update_sensor()
    return _last_temp

def read_humidity_sensor():
    """模拟读取湿度（%），1分钟更新一次"""
    _update_sensor()
    return _last_humi

def set_gpio_output(pin, state):
    print(f"[Mock GPIO] 设置引脚 {pin} 为 {'高电平' if state else '低电平'}")

def set_pwm_duty_cycle(pin, duty_cycle):
    print(f"[Mock PWM] 设置引脚 {pin} 占空比为 {duty_cycle}%")

def cleanup():
    """模拟 GPIO 清理操作"""
    print("[Mock GPIO] 清理 GPIO 引脚")

# GPIO控制类
class GPIOController:
    def __init__(self):
        self.brightness = DEFAULT_BRIGHTNESS
        self.light_on = False

    def turn_on(self):
        self.light_on = True
        if GPIO_ENABLED:
            # 真实GPIO操作
            # set_gpio_output(GPIO_PIN, True)
            pass
        else:
            set_gpio_output(GPIO_PIN, True)
        print("[GPIO] 灯已打开")

    def turn_off(self):
        self.light_on = False
        if GPIO_ENABLED:
            # 真实GPIO操作
            # set_gpio_output(GPIO_PIN, False)
            pass
        else:
            set_gpio_output(GPIO_PIN, False)
        print("[GPIO] 灯已关闭")

    def set_brightness(self, value):
        self.brightness = value
        if GPIO_ENABLED:
            # 真实GPIO操作
            # set_pwm_duty_cycle(GPIO_PIN, value)
            pass
        else:
            set_pwm_duty_cycle(GPIO_PIN, value)
        print(f"[GPIO] 设置亮度为 {value}%")
