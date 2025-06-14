from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.image import Image, AsyncImage
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle, Ellipse, Rectangle
from gpio_control import GPIOController
import requests
from io import BytesIO
from PIL import Image as PILImage
import random
from kivy.graphics.texture import Texture
from PIL import ImageFilter
from kivy.clock import Clock
from kivy.graphics import Fbo, ClearColor, ClearBuffers
import os
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
import threading
from kivy.uix.modalview import ModalView

FONT_PATH = "front/AaLanTingTiShi-LuoBiRuShen-2.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

EMOJI_FONT_PATH = "front/NotoEmoji-VariableFont_wght.ttf"
LIGHT_OFF_IMG = "assets/light_off.png"
LIGHT_ON_IMG = "assets/light_on.png"

Window.size = (1024, 600)

def get_main_color_from_url(url):
    # 下载图片
    response = requests.get(url)
    img = PILImage.open(BytesIO(response.content)).convert('RGB')
    # 缩小图片加快处理
    img = img.resize((50, 50))
    # 获取所有像素
    pixels = list(img.getdata())
    # 统计出现最多的颜色
    main_color = max(set(pixels), key=pixels.count)
    return main_color  # (r, g, b)

class ModernSlider(Slider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_width = 40
        self.thumb_radius = 25
        self.border_padding = 25
        self.corner_radius = 25
        self.gradient_texture = None
        self.create_gradient()
        self._need_blur_update = True

        self.bind(pos=self._on_geom_change, size=self._on_geom_change)
        self.bind(value=self._on_value_change)

    def _on_geom_change(self, *args):
        self._need_blur_update = True
        self.redraw()

    def _on_value_change(self, *args):
        self.redraw(update_blur=False)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self._need_blur_update = True
            self.redraw()
        return super().on_touch_up(touch)

    def redraw(self, update_blur=True):
        self.canvas.after.clear()
        with self.canvas.after:
            Color(1, 1, 1, 0.35)
            RoundedRectangle(
                pos=(self.x - self.border_padding, self.center_y - self.background_width / 2 - self.border_padding),
                size=(self.width + self.border_padding * 2 + 40, self.background_width + self.border_padding * 2),
                radius=[self.corner_radius] * 4
            )
            Color(0.8, 0.8, 0.8, 0.3)
            RoundedRectangle(
                pos=(self.x - self.border_padding, self.center_y - self.background_width / 2 - self.border_padding),
                size=(self.width + self.border_padding * 2 + 40, self.background_width + self.border_padding * 2),
                radius=[self.corner_radius] * 4
            )
            Color(1, 1, 1, 0.7)
            RoundedRectangle(
                pos=(self.x, self.center_y - self.background_width / 2),
                size=(self.width, self.background_width),
                radius=[self.corner_radius] * 4
            )
            if self.gradient_texture:
                Color(1, 1, 1, 1)
                RoundedRectangle(
                    pos=(self.x, self.center_y - self.background_width / 2),
                    size=(self.value_normalized * self.width, self.background_width),
                    radius=[self.corner_radius, 0, 0, self.corner_radius],
                    texture=self.gradient_texture
                )
            Color(1, 1, 1, 1)
            Ellipse(
                pos=(self.value_pos[0] - self.thumb_radius, self.center_y - self.thumb_radius),
                size=(self.thumb_radius * 2, self.thumb_radius * 2)
            )

    def create_gradient(self):
        from kivy.graphics.texture import Texture
        w, h = 256, 1
        buf = bytearray()
        # 紫色 (162,89,255) 到 橙色 (255,183,77)
        r1, g1, b1 = 162, 89, 255
        r2, g2, b2 = 255, 183, 77
        for i in range(w):
            t = i / (w - 1)
            r = int(r1 + (r2 - r1) * t)
            g = int(g1 + (g2 - g1) * t)
            b = int(b1 + (b2 - b1) * t)
            buf += bytes([r, g, b, 255])
        texture = Texture.create(size=(w, h), colorfmt='rgba')
        texture.blit_buffer(bytes(buf), colorfmt='rgba', bufferfmt='ubyte')
        self.gradient_texture = texture


class BlurBox(FloatLayout):
    def __init__(self, width=200, height=200, radius=25, **kwargs):
        super().__init__(**kwargs)
        self.box_width = width
        self.box_height = height
        self.radius = radius
        self.blur_texture = None
        self.bind(pos=self.redraw, size=self.redraw)
        Clock.schedule_once(lambda dt: self.redraw(), 0.1)

    def create_blur_texture(self):
        from kivy.graphics import Fbo, ClearColor, ClearBuffers, Rectangle
        # 获取父级的背景图片控件
        bg_img = None
        parent = self.parent
        while parent:
            if hasattr(parent, "bg_img"):
                bg_img = parent.bg_img
                break
            parent = getattr(parent, "parent", None)
        if not bg_img or not bg_img.texture:
            self.blur_texture = None
            return

        w, h = self.box_width, self.box_height
        abs_x = self.to_window(self.x, self.y)[0]
        abs_y = self.to_window(self.x, self.y)[1]
        bg_pos = bg_img.pos
        bg_size = bg_img.size

        fbo = Fbo(size=(w, h))
        with fbo:
            ClearColor(1, 1, 1, 0)
            ClearBuffers()
            Rectangle(
                texture=bg_img.texture,
                pos=(bg_pos[0] - abs_x, bg_pos[1] - abs_y),
                size=bg_size
            )
        fbo.draw()
        data = fbo.texture.pixels
        img = PILImage.frombytes('RGBA', fbo.size, data)
        img = img.filter(ImageFilter.GaussianBlur(radius=16))
        texture = Texture.create(size=img.size, colorfmt='rgba')
        texture.blit_buffer(img.tobytes(), colorfmt='rgba', bufferfmt='ubyte')
        texture.flip_vertical()
        self.blur_texture = texture

    def redraw(self, *args):
        self.create_blur_texture()
        self.canvas.clear()
        with self.canvas:
            if self.blur_texture:
                RoundedRectangle(
                    texture=self.blur_texture,
                    pos=self.pos,
                    size=(self.box_width, self.box_height),
                    radius=[self.radius] * 4
                )
            Color(1, 1, 1, 0.35)
            RoundedRectangle(
                pos=self.pos,
                size=(self.box_width, self.box_height),
                radius=[self.radius] * 4
            )
            Color(0.8, 0.8, 0.8, 0.3)
            RoundedRectangle(
                pos=self.pos,
                size=(self.box_width, self.box_height),
                radius=[self.radius] * 4
            )


class RoundImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allow_stretch = True
        self.keep_ratio = False
        with self.canvas.before:
            Color(1, 1, 1, 0)  # 透明背景
            # 只保留左下和右下圆角，左上和右上为0
            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[0, 0, 25, 25]  # 左上,右上,右下,左下
            )
        self.bind(pos=self._update_bg, size=self._update_bg)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class LampControlUI(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.light_on = False
        self.gpio_controller = GPIOController()  # 初始化 GPIO 控制器

         # 设置本地图片为默认背景
        self.bg_img = AsyncImage(
            source="Deafult_wallpaper.jpg",  # 默认壁纸
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0}
        )
        self.add_widget(self.bg_img)

        # 灯图标毛玻璃（用BlurBox控件）
        self.blur_box = BlurBox(
            width=100,
            height=100,
            radius=25,
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.5}  # 修改为0.5
        )
        self.add_widget(self.blur_box)

        self.light_img = Image(
            source=LIGHT_OFF_IMG,
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.5}  # 修改为0.5
        )
        self.add_widget(self.light_img)

        self.light_btn = Button(
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.5},  # 修改为0.5
            background_color=[0, 0, 0, 0],
            border=(0, 0, 0, 0)
        )
        self.light_btn.bind(on_release=self.toggle_light)
        self.add_widget(self.light_btn)

        # 创建水平布局，包含滑块和亮度 Emoji
        slider_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(0.8, None),
            height=80,
            pos_hint={"center_x": 0.5, "y": 0.1},
            spacing=10
        )

        # 添加滑块
        self.slider = ModernSlider(
            min=0, max=100, value=0,
            size_hint=(1, 1)
        )
        self.slider.bind(value=self.on_slider_change)
        slider_layout.add_widget(self.slider)

        # 用 FloatLayout 包裹 emoji，实现xy方向偏移
        emoji_layout = FloatLayout(size_hint=(None, None), size=(50, 80))
        self.max_icon = Label(
            text="🔆",
            font_size=32,
            font_name=EMOJI_FONT_PATH,
            size_hint=(None, None),
            size=(50, 50),
            color=(0.5, 0.5, 0.5, 1),
        )
        # 让emoji在x方向右移10像素，y方向上移20像素
        self.max_icon.pos = (870, (80-50)//2 + 60)
        emoji_layout.add_widget(self.max_icon)
        slider_layout.add_widget(emoji_layout)

        self.add_widget(slider_layout)

        # 灯图标毛玻璃边框（正方形，25px圆角，中心与灯图标一致，图层仅次于灯图标）
        self.light_blur_texture = None

        from kivy.graphics import Color, RoundedRectangle  # <--- 加在这里

        with self.canvas.before:
            # 毛玻璃底层
            self.light_blur_border = RoundedRectangle(
                size=(100, 100),  # 由200改为100
                pos=(0, 0),
                radius=[25],
                texture=None
            )
            Color(1, 1, 1, 0.35)
            self.light_blur_overlay = RoundedRectangle(
                size=(100, 100),  # 由200改为100
                pos=(0, 0),
                radius=[25]
            )

        # 绑定事件
        self.light_img.bind(center=self.update_light_blur, size=self.update_light_blur)
        Window.bind(on_resize=lambda *a: self.update_light_blur())
        self.bg_img.bind(on_texture=lambda *a: self.update_light_blur())
        Clock.schedule_once(lambda dt: self.update_light_blur(), 0)

        # 强制初始刷新滑块（关键修复）
        Clock.schedule_once(lambda dt: self.slider.redraw(), 0.1)

        # 监听背景图片加载完成
        self.bg_img.bind(on_texture=self.on_bg_loaded)

        # 第3秒自动刷新一次界面（强制刷新毛玻璃和滑块等）
        Clock.schedule_once(lambda dt: self.force_refresh_ui(), 3.0)

        self.wallpaper_mode = "simple"  # simple 或 acg
        self.macosbliss_dir = "macosbliss"
        self.macosbliss_imgs = [
            os.path.join(self.macosbliss_dir, f)
            for f in os.listdir(self.macosbliss_dir)
            if f.lower().endswith(('.png', '.jpg', '.jpeg'))
        ]

        # 计算进度条的y轴和滑块毛玻璃的高度
        slider_y = 0.1  # 进度条的pos_hint["y"]，与slider_layout一致
        slider_blur_height = self.slider.background_width + self.slider.border_padding * 2  # 取滑块毛玻璃高度

        # 切换壁纸按钮毛玻璃底板，大小与滑块毛玻璃一致
        self.switch_blur_box = BlurBox(
            width=60,  # 宽度保持60
            height=slider_blur_height,  # 高度与滑块毛玻璃一致
            radius=25,
            size_hint=(None, None),
            size=(60, slider_blur_height),
            pos_hint={"right": 0.98, "y": 0.092}  # ↓下移2px
        )
        self.add_widget(self.switch_blur_box)

        # 切换壁纸按钮，宽度60，高度与毛玻璃一致，图片自动拉伸但保持比例
        self.switch_btn = RoundImageButton(
            source="assets/swich_wallpaper.png",
            size_hint=(None, None),
            size=(60, slider_blur_height),
            pos_hint={"right": 0.98, "y": 0.0967}  # ↓下移2px
        )
        self.switch_btn.allow_stretch = True
        self.switch_btn.keep_ratio = True  # 保持比例
        self.switch_btn.bind(on_release=self.switch_wallpaper_mode)
        self.add_widget(self.switch_btn)

        # 让毛玻璃和按钮位置同步
        def sync_blur_box_pos(*args):
            self.switch_blur_box.pos = self.switch_btn.pos
        self.switch_btn.bind(pos=sync_blur_box_pos, size=sync_blur_box_pos)
        Clock.schedule_once(lambda dt: sync_blur_box_pos(), 0.1)

        # 刷新毛玻璃
        self.bg_img.bind(on_texture=lambda *a: self.switch_blur_box.redraw())
        Window.bind(on_resize=lambda *a: self.switch_blur_box.redraw())

        # 添加时间毛玻璃框和时间Label
        self.time_blur_box = BlurBox(
            width=480,
            height=90,
            radius=25,
            size_hint=(None, None),
            size=(480, 90),
        )
        self.add_widget(self.time_blur_box)

        self.time_label = Label(
            text="[size=100][color=FFFFFF]{hour}[/color][/size][size=40][color=00eaff][i] h [/i][/color][/size]"
                 "[size=100][color=FFFFFF]{minute}[/color][/size][size=40][color=00eaff][i] min [/i][/color][/size]"
                 "[size=100][color=FFFFFF]{second}[/color][/size][size=40][color=00eaff][i] s[/i][/color][/size]",
            font_name="front/DS-Digital/DS-DIGI-1.ttf",
            markup=True,
            size_hint=(None, None),
            size=(700, 120),
            halign="center",
            valign="middle"
        )
        self.add_widget(self.time_label)

        def update_time_pos(*args):
            win_w, win_h = Window.size
            # 1/4高度再上移30px
            y = win_h * 0.75 + 30 - self.time_blur_box.box_height / 2
            x = (win_w - self.time_blur_box.box_width) / 2
            self.time_blur_box.pos = (x, y)
            # label居中对齐
            label_y = win_h * 0.75 + 30 - self.time_label.height / 2
            label_x = (win_w - self.time_label.width) / 2
            self.time_label.pos = (label_x, label_y)

        Window.bind(size=update_time_pos)
        Clock.schedule_once(lambda dt: update_time_pos(), 0)

        # 定时刷新时间
        def update_time_label(dt):
            import time
            t = time.localtime()
            self.time_label.text = (
                f"[size=100][color=FFFFFF]{t.tm_hour:02d}[/color][/size][size=40][color=00eaff][i] h [/i][/color][/size]"
                f"[size=100][color=FFFFFF]{t.tm_min:02d}[/color][/size][size=40][color=00eaff][i] min [/i][/color][/size]"
                f"[size=100][color=FFFFFF]{t.tm_sec:02d}[/color][/size][size=40][color=00eaff][i] s[/i][/color][/size]"
            )
        Clock.schedule_interval(update_time_label, 1)
        update_time_label(0)
        # 记录长按状态
        self._timebox_touch_time = None

        # 绑定事件
        self.time_blur_box.bind(on_touch_down=self._on_timebox_touch_down)
        self.time_blur_box.bind(on_touch_up=self._on_timebox_touch_up)

    def _on_timebox_touch_down(self, instance, touch):
        if self.time_blur_box.collide_point(*touch.pos) and touch.button == 'left':
            self._timebox_touch_time = Clock.schedule_once(self._show_exam_countdown, 1.0)  # 1秒为长按

    def _on_timebox_touch_up(self, instance, touch):
        if self._timebox_touch_time:
            self._timebox_touch_time.cancel()
            self._timebox_touch_time = None

    def _show_exam_countdown(self, dt):
        app = App.get_running_app()
        app.switch_to_exam_screen(self.bg_img.source)

    def toggle_light(self, instance):
        self.light_on = not self.light_on
        if self.light_on:
            self.light_img.source = LIGHT_ON_IMG
            self.gpio_controller.turn_on()  # 调用 GPIO 打开灯
        else:
            self.light_img.source = LIGHT_OFF_IMG
            self.gpio_controller.turn_off()  # 调用 GPIO 关闭灯

    def on_slider_change(self, instance, value):
        if self.light_on:  # 只有灯打开时才调整亮度
            self.gpio_controller.set_brightness(int(value))  # 调用 GPIO 设置亮度

    def refresh_bg(self, instance):
        # 只用API获取壁纸，强制刷新（加随机参数）
        url = f"https://api.vvhan.com/api/wallpaper/acg?rand={random.randint(1, 9999999)}"
        self.bg_img.source = url

    def set_simple_wallpaper(self):
        # 只用API获取简约壁纸（主线程直接设置）
        url = f"https://api.vvhan.com/api/wallpaper/acg?rand={random.randint(1, 9999999)}"
        self.bg_img.source = url
        self.bg_img.reload()

    def set_acg_wallpaper(self):
        # 只用API获取二次元壁纸（主线程直接设置）
        url = f"https://api.vvhan.com/api/wallpaper/acg?rand={random.randint(1, 9999999)}"
        self.bg_img.source = url
        self.bg_img.reload()

    def create_light_blur_texture(self):
        # 将模糊处理放到子线程
        def blur_task():
            bg_img = self.bg_img
            if not bg_img.texture:
                self.light_blur_texture = None
                return
            w, h = 200, 200
            cx, cy = self.light_img.center
            abs_x = int(cx - w / 2)
            abs_y = int(cy - h / 2)
            bg_pos = bg_img.pos
            bg_size = bg_img.size
            fbo = Fbo(size=(w, h))
            with fbo:
                ClearColor(1, 1, 1, 0)
                ClearBuffers()
                Rectangle(
                    texture=bg_img.texture,
                    pos=(bg_pos[0] - abs_x, bg_pos[1] - abs_y),
                    size=bg_size
                )
            fbo.draw()
            data = fbo.texture.pixels
            img = PILImage.frombytes('RGBA', fbo.size, data)
            img = img.filter(ImageFilter.GaussianBlur(radius=16))
            texture = Texture.create(size=img.size, colorfmt='rgba')
            texture.blit_buffer(img.tobytes(), colorfmt='rgba')
            texture.flip_vertical()
            # 回到主线程更新UI
            def update_ui(dt):
                self.light_blur_texture = texture
                self.light_blur_border.texture = texture
            Clock.schedule_once(update_ui)
        threading.Thread(target=blur_task, daemon=True).start()

    def update_bg_size(self, instance, value):
        # 获取窗口宽度和高度
        window_width, window_height = Window.size
        texture_width, texture_height = self.bg_img.texture_size

        # 计算图片的宽高比和窗口的宽高比
        texture_ratio = texture_width / texture_height
        window_ratio = window_width / window_height

       
        self.max_icon.center_y = self.slider.center_y + 100  # 上移 20px

    def on_bg_loaded(self, instance, value):
        # 延迟 0.2 秒确保布局完成
        Clock.schedule_once(lambda dt: self.slider.redraw(), 0.2)
        if hasattr(self, "slider"):
            # 记录上一次的尺寸和位置
            self._last_slider_geom = (0, 0, 0, 0)
            def try_redraw_slider(*args):
                geom = (self.slider.x, self.slider.y, self.slider.width, self.slider.height)
                # 只有尺寸和位置都有效且和上次不同才刷新
                if self.slider.width > 0 and self.slider.height > 0 and geom != self._last_slider_geom:
                    self._last_slider_geom = geom
                    self.slider.redraw()
            # 持续监听
            self.slider.bind(size=try_redraw_slider, pos=try_redraw_slider)
            # 也可以延迟多次主动刷新，确保捕获到最终布局
            for i in range(1, 6):
                Clock.schedule_once(lambda dt: self.slider.redraw(), i * 0.5)

    def force_refresh_ui(self):
        # 强制刷新灯毛玻璃
        if hasattr(self, "light_img"):
            # 触发灯毛玻璃的刷新
            if hasattr(self, "light_img") and hasattr(self, "bg_img"):
                # 触发 update_light_blur
                try:    
                    self.light_img.dispatch('on_pos')
                except Exception:
                    pass
            # 直接调用 update_light_blur（如果在 __init__ 作用域内定义则用 self. 绑定）
            if hasattr(self, "update_light_blur"):
                self.update_light_blur()
            else:
                # 如果是局部函数，直接再调一次
                try:
                    self.update_light_blur()
                except Exception:
                    pass
        # 强制刷新滑块毛玻璃
        if hasattr(self, "slider"):
            self.slider.redraw()

    def update_light_blur(self, *args):
        cx, cy = self.light_img.center
        pos = (cx - 50, cy - 50)  # 由100改为50
        self.create_light_blur_texture()
        self.light_blur_border.pos = pos
        self.light_blur_border.texture = self.light_blur_texture
        self.light_blur_overlay.pos = pos

    def create_light_blur_texture(self):
        bg_img = self.bg_img
        if not bg_img.texture:
            self.light_blur_texture = None
            return
        w, h = 200, 200
        cx, cy = self.light_img.center
        abs_x = int(cx - w / 2)
        abs_y = int(cy - h / 2)
        bg_pos = bg_img.pos
        bg_size = bg_img.size
        fbo = Fbo(size=(w, h))
        with fbo:
            ClearColor(1, 1, 1, 0)
            ClearBuffers()
            Rectangle(
                texture=bg_img.texture,
                pos=(bg_pos[0] - abs_x, bg_pos[1] - abs_y),
                size=bg_size
            )
        fbo.draw()
        data = fbo.texture.pixels
        img = PILImage.frombytes('RGBA', fbo.size, data)
        img = img.filter(ImageFilter.GaussianBlur(radius=16))
        texture = Texture.create(size=img.size, colorfmt='rgba')
        texture.blit_buffer(img.tobytes(), colorfmt='rgba')
        texture.flip_vertical()
        self.light_blur_texture = texture

    def switch_wallpaper_mode(self, instance):
        if self.wallpaper_mode == "acg":
            self.wallpaper_mode = "simple"
            self.switch_btn.text = "切换二次元壁纸"
            self.set_simple_wallpaper()
        else:
            self.wallpaper_mode = "acg"
            self.switch_btn.text = "切换简约壁纸"
            self.set_acg_wallpaper()
        # 每次切换壁纸后都重新处理毛玻璃
        self.update_light_blur()
        # 1秒后拉长窗口y轴
        Clock.schedule_once(self._stretch_window_y_temporarily, 0.8)

    def _stretch_window_y_temporarily(self, dt):
        old_height = Window.height
        Window.size = (Window.width, Window.height + 1)
        # 0.05秒后恢复原高度
        Clock.schedule_once(lambda dt: self._restore_window_height(old_height), 0.05)

    def _restore_window_height(self, old_height):
        Window.size = (Window.width, old_height)

    def set_simple_wallpaper(self):
        # 只用API获取简约壁纸（主线程直接设置）
        url = f"https://t.alcy.cc/moe?rand={random.randint(1, 9999999)}"
        self.bg_img.source = url
        self.bg_img.reload()

    def set_acg_wallpaper(self):
        # 只用API获取二次元壁纸（主线程直接设置）
        url = f"https://t.alcy.cc/fj?rand={random.randint(1, 9999999)}"
        self.bg_img.source = url
        self.bg_img.reload()

    def auto_switch_wallpaper(self, dt):
        if self.wallpaper_mode == "simple":
            self.set_simple_wallpaper()
        else:
            self.set_acg_wallpaper()

class ExamCountdownPopup(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (700, 250)
        self.background_color = (0, 0, 0, 0.7)
        self.auto_dismiss = True

        self.label = Label(
            text="",
            font_size=60,
            markup=True,
            halign="center",
            valign="middle"
        )
        self.add_widget(self.label)
        self.update_countdown()
        Clock.schedule_interval(lambda dt: self.update_countdown(), 1)

    def update_countdown(self):
        import datetime
        now = datetime.datetime.now()
        # 2026年高考假设为6月7日8:00
        exam_time = datetime.datetime(2026, 6, 7, 8, 0, 0)
        delta = exam_time - now
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.label.text = (
            f"[b][size=120][color=FFFFFF]{days}[/color][/size][size=60][color=00eaff] D [/color][/size]"
            f"[size=120][color=FFFFFF]{hours:02d}[/color][/size][size=60][color=00eaff] h [/color][/size]"
            f"[size=60][color=FFFFFF]{minutes:02d} min {seconds:02d} s[/color][/size][/b]\n"
            f"[size=48][color=FFFFFF]距离 2026高考[/color][/size]"
        )

class ExamCountdownScreen(FloatLayout):
    def __init__(self, bg_img_source, **kwargs):
        super().__init__(**kwargs)
        # 背景图
        self.bg_img = AsyncImage(
            source=bg_img_source,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0}
        )
        self.add_widget(self.bg_img)

        # 毛玻璃边框，尺寸包裹倒计时和副标题
        self.blur_box = BlurBox(
            width=1000,
            height=320,
            radius=40,
            size_hint=(None, None),
            size=(1000, 320),
        )
        self.add_widget(self.blur_box)

        # “距离 2026高考”副标题（放到上面）
        self.title_label = Label(
            text="[b][color=FFFFFF]距离 2026高考[/color][/b]",
            font_name=FONT_PATH,
            markup=True,
            font_size=64,
            size_hint=(None, None),
            size=(900, 80),
            halign="center",  # ← 这里改为 center
            valign="middle"
        )
        self.add_widget(self.title_label)

        # 高考倒计时主数字（放到下面）
        self.countdown_label = Label(
            text="",
            font_name="front/DS-Digital/DS-DIGI-1.ttf",
            markup=True,
            size_hint=(None, None),
            size=(900, 160),
            halign="center",
            valign="middle"
        )
        self.add_widget(self.countdown_label)

        # 一言毛玻璃框，圆角25px
        self.hitokoto_blur_box = BlurBox(
            width=900,
            height=60,
            radius=25,  # 圆角25px
            size_hint=(None, None),
            size=(900, 60),
        )
        self.add_widget(self.hitokoto_blur_box)

        # 一言Label，毛玻璃下方
        self.hitokoto_label = Label(
            text="",
            font_name="front/AaLanTingTiShi-LuoBiRuShen-2.ttf",
            italic=True,
            markup=True,
            font_size=32,
            size_hint=(None, None),
            size=(900, 60),
            halign="center",
            valign="middle"
        )
        self.add_widget(self.hitokoto_label)
        # 定时刷新倒计时
        Clock.schedule_interval(self.update_countdown, 1)
        self.update_countdown(0)

        # 动态定位
        Window.bind(size=self.update_layout)
        Clock.schedule_once(lambda dt: self.update_layout(), 0)

        # 获取一言
        Clock.schedule_once(lambda dt: self.fetch_hitokoto(), 0)

        # 长按毛玻璃返回主界面
        self._touch_time = None
        self.blur_box.bind(on_touch_down=self._on_blurbox_touch_down)
        self.blur_box.bind(on_touch_up=self._on_blurbox_touch_up)

    def _on_blurbox_touch_down(self, instance, touch):
        if self.blur_box.collide_point(*touch.pos) and touch.button == 'left':
            self._touch_time = Clock.schedule_once(self._return_main, 1.0)  # 1秒为长按

    def _on_blurbox_touch_up(self, instance, touch):
        if self._touch_time:
            self._touch_time.cancel()
            self._touch_time = None

    def _return_main(self, dt):
        app = App.get_running_app()
        app.switch_to_main_screen()

    def update_layout(self, *args):
        win_w, win_h = Window.size
        # 毛玻璃居中，略微上移
        box_w, box_h = self.blur_box.box_width, self.blur_box.box_height
        box_x = (win_w - box_w) / 2
        box_y = win_h * 0.5 - box_h / 2 + 30
        self.blur_box.pos = (box_x, box_y)
        # 副标题居中（上面）
        title_w, title_h = self.title_label.size
        self.title_label.pos = (win_w / 2 - title_w / 2, box_y + box_h - title_h - 30)
        # 倒计时数字居中（下面）
        label_w, label_h = self.countdown_label.size
        self.countdown_label.pos = (win_w / 2 - label_w / 2, box_y + 40)
        # 一言毛玻璃紧贴主毛玻璃下方，居中
        hitokoto_blur_w, hitokoto_blur_h = self.hitokoto_blur_box.box_width, self.hitokoto_blur_box.box_height
        self.hitokoto_blur_box.pos = (win_w / 2 - hitokoto_blur_w / 2, box_y - hitokoto_blur_h - 20)
        # 一言Label与毛玻璃重合
        self.hitokoto_label.pos = self.hitokoto_blur_box.pos

    def update_countdown(self, dt):
        import datetime
        now = datetime.datetime.now()
        exam_time = datetime.datetime(2026, 6, 7, 8, 0, 0)
        delta = exam_time - now
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        # 数字部分用DS-DIGI-1.ttf，字母用苹方，单位全蓝色
        self.countdown_label.text = (
            f"[size=120][color=FFFFFF]{days}[/color][/size]"
            f"[size=60][font={FONT_PATH}][color=00eaff] D [/color][/font][/size]"
            f"[size=120][color=FFFFFF]{hours:02d}[/color][/size]"
            f"[size=60][font={FONT_PATH}][color=00eaff] h [/color][/font][/size]"
            f"[size=120][color=FFFFFF]{minutes:02d}[/color][/size]"
            f"[size=60][font={FONT_PATH}][color=00eaff] min [/color][/font][/size]"
            f"[size=120][color=FFFFFF]{seconds:02d}[/color][/size]"
            f"[size=60][font={FONT_PATH}][color=00eaff] s [/color][/font][/size]"
        )

    def fetch_hitokoto(self):
        import threading, requests
        def get_and_set():
            try:
                resp = requests.get("https://v1.hitokoto.cn/?encode=text", timeout=5)
                text = resp.text.strip()
            except Exception:
                text = "获取一言失败"
            # 斜体+小号+居中
            self.hitokoto_label.text = f"[i]{text}[/i]"
        threading.Thread(target=get_and_set, daemon=True).start()

    def on_back(self, instance):
        app = App.get_running_app()
        app.switch_to_main_screen()

class LampApp(App):
    def build(self):
        from kivy.uix.floatlayout import FloatLayout
        self.root_layout = FloatLayout()
        self.main_screen = LampControlUI()
        self.root_layout.add_widget(self.main_screen)
        return self.root_layout

    def switch_to_exam_screen(self, bg_img_source):
        self.exam_screen = ExamCountdownScreen(bg_img_source)
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.exam_screen)

    def switch_to_main_screen(self):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.main_screen)

if __name__ == "__main__":
    LampApp().run()