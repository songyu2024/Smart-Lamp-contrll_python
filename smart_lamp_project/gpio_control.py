# gpio_control.py

import config

if not config.GPIO_ENABLED:
    import sensor_mock as gpio_backend
else:
    gpio_backend = None  # 实际部署时替换为真实GPIO控制

class GPIOController:
    def __init__(self):
        self.brightness = config.DEFAULT_BRIGHTNESS
        self.light_on = False

    def turn_on(self):
        self.light_on = True
        if config.GPIO_ENABLED:
            # 真实GPIO操作
            # gpio_backend.set_gpio_output(config.GPIO_PIN, True)
            pass
        else:
            gpio_backend.set_gpio_output(config.GPIO_PIN, True)
        print("[GPIO] 灯已打开")

    def turn_off(self):
        self.light_on = False
        if config.GPIO_ENABLED:
            # 真实GPIO操作
            # gpio_backend.set_gpio_output(config.GPIO_PIN, False)
            pass
        else:
            gpio_backend.set_gpio_output(config.GPIO_PIN, False)
        print("[GPIO] 灯已关闭")

    def set_brightness(self, value):
        self.brightness = value
        if config.GPIO_ENABLED:
            # 真实GPIO操作
            # gpio_backend.set_pwm_duty_cycle(config.GPIO_PIN, value)
            pass
        else:
            gpio_backend.set_pwm_duty_cycle(config.GPIO_PIN, value)
        print(f"[GPIO] 设置亮度为 {value}%")
