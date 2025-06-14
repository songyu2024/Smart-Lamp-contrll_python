# sensor_mock.py
import random
import time

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
