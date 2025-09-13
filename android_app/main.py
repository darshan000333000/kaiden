# android_app/main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
import threading, requests, base64, tempfile, os
from kivy.core.audio import SoundLoader

BACKEND = "http://<YOUR_SERVER_IP>:8000"  # replace with your server IP or domain

class KaidenUI(BoxLayout):
    status = StringProperty("Idle")
    output_text = StringProperty("")

    def send_text(self, text):
        self.status = "Sending..."
        def job():
            try:
                r = requests.post(f"{BACKEND}/ask", json={"text": text}, timeout=60)
                r.raise_for_status()
                data = r.json()
                self.output_text = data.get("text","(no text)")
                self.status = "Playing audio..."
                audio_b64 = data.get("audio_b64")
                if audio_b64:
                    audio_bytes = base64.b64decode(audio_b64)
                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    tmp.write(audio_bytes)
                    tmp.flush()
                    tmp.close()
                    sound = SoundLoader.load(tmp.name)
                    if sound:
                        sound.play()
                    else:
                        print("Failed to load audio")
                    # don't delete immediately; SoundLoader may need file
            except Exception as e:
                self.status = f"Error: {e}"
        threading.Thread(target=job, daemon=True).start()

class KaidenApp(App):
    def build(self):
        return KaidenUI()

if __name__ == "__main__":
    KaidenApp().run()
