import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer
import gpio_control

WAKE_WORD = "你好小灯"
MODEL_PATH = "g:/smart_lamp_project/smart_lamp_project/vosk-model-small-cn-0.22"
SAMPLE_RATE = 16000

controller = gpio_control.GPIOController()

def parse_intent(text):
    """
    简单意图解析：返回'on'/'off'/'brightness'/'none'
    """
    if "打开" in text or "开灯" in text:
        return "on"
    if "关闭" in text or "关灯" in text:
        return "off"
    if "亮度" in text:
        # 解析亮度百分比
        import re
        m = re.search(r"(\d+)", text)
        if m:
            return ("brightness", int(m.group(1)))
        return "brightness"
    return "none"

def handle_intent(intent):
    if intent == "on":
        print("执行：开灯")
        controller.turn_on()
    elif intent == "off":
        print("执行：关灯")
        controller.turn_off()
    elif isinstance(intent, tuple) and intent[0] == "brightness":
        value = intent[1]
        print(f"执行：设置亮度 {value}%")
        controller.set_brightness(value)
    elif intent == "brightness":
        print("请说出亮度百分比，例如“亮度50”")
    else:
        print("未识别到有效指令")

def main():
    print("加载模型中...")
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)
    recognizer.SetWords(True)
    q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(status, flush=True)
        q.put(bytes(indata))

    print("请说唤醒词：“你好小灯” ...")
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize = 8000, dtype='int16',
                          channels=1, callback=callback):
        listening = False
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get("text", "")
                if not listening:
                    if WAKE_WORD in text:
                        print("唤醒成功，请说出指令...")
                        listening = True
                else:
                    if text.strip() == "":
                        continue
                    print("识别到指令：", text)
                    intent = parse_intent(text)
                    handle_intent(intent)
                    print("等待唤醒词“你好小灯” ...")
                    listening = False

if __name__ == "__main__":
    main()