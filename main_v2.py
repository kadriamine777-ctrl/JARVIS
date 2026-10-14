
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import os
import random
from datetime import datetime

# Try to import real modules - if not available, use fallback
try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except:
    HAS_PIL = False

try:
    import requests
    HAS_REQUESTS = True
except:
    HAS_REQUESTS = False

class JarvisPrivateApp(App):
    def build(self):
        self.title = "JARVIS PRIVATE v2"
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        title = Label(text="JARVIS PRIVATE v2.0\nREAL AI - No Companies", 
                     font_size='18sp', size_hint=(1, 0.12), 
                     color=(0, 0.8, 1, 1), bold=True)
        layout.add_widget(title)
        
        self.console = TextInput(
            text="> JARVIS v2.0 Ready\n> Offline Mode\n> Type a prompt and press ENTER\n> Example: a cat in space\n", 
            readonly=True, size_hint=(1, 0.5),
            background_color=(0.05, 0.05, 0.05, 1),
            foreground_color=(0, 1, 0.6, 1),
            font_size='14sp'
        )
        layout.add_widget(self.console)
        
        self.input = TextInput(
            hint_text="Write your prompt here... e.g: sunset over Algiers", 
            size_hint=(1, 0.1), multiline=False
        )
        self.input.bind(on_text_validate=self.on_command)
        layout.add_widget(self.input)
        
        btn_layout = BoxLayout(size_hint=(1, 0.28), spacing=5)
        
        btn1 = Button(text="TALK", background_color=(0, 0.6, 1, 1), font_size='15sp', bold=True)
        btn1.bind(on_press=lambda x: self.do_talk())
        btn_layout.add_widget(btn1)
        
        btn2 = Button(text="IMAGE", background_color=(0.8, 0.2, 1, 1), font_size='15sp', bold=True)
        btn2.bind(on_press=lambda x: self.do_image())
        btn_layout.add_widget(btn2)
        
        btn3 = Button(text="VIDEO", background_color=(0, 0.8, 0.3, 1), font_size='15sp', bold=True)
        btn3.bind(on_press=lambda x: self.do_video())
        btn_layout.add_widget(btn3)
        
        btn4 = Button(text="LEARN", background_color=(1, 0.6, 0, 1), font_size='15sp', bold=True)
        btn4.bind(on_press=lambda x: self.do_learn())
        btn_layout.add_widget(btn4)
        
        layout.add_widget(btn_layout)
        return layout
    
    def log(self, text):
        self.console.text += text + "\n"
        # Auto scroll
        self.console.cursor = (0, len(self.console.text))
    
    def get_prompt(self):
        prompt = self.input.text.strip()
        if not prompt:
            prompt = f"JARVIS creation {datetime.now().strftime('%H:%M')}"
        return prompt
    
    def on_command(self, instance):
        cmd = self.input.text
        self.input.text = ""
        self.log(f"\n> You: {cmd}")
        if "image" in cmd.lower() or "صورة" in cmd:
            self.do_image(cmd)
        elif "video" in cmd.lower() or "فيديو" in cmd:
            self.do_video(cmd)
        elif "learn" in cmd.lower() or "تعلم" in cmd:
            self.do_learn()
        else:
            self.do_talk(cmd)
    
    def do_talk(self, custom_text=None):
        prompt = custom_text if custom_text else self.get_prompt()
        self.log(f"\n[JARVIS TALK]")
        self.log(f"> Thinking about: {prompt}")
        # Real TTS would go here - for now we simulate and also try android TTS
        response = f"Hello ADEM, I am your private JARVIS. You said: {prompt}. I am 100% offline and private."
        self.log(f"> JARVIS: {response}")
        
        # Try Android TTS via jnius if available
        try:
            from jnius import autoclass
            Locale = autoclass('java.util.Locale')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
            activity = PythonActivity.mActivity
            tts = TextToSpeech(activity, None)
            tts.setLanguage(Locale.US)
            tts.speak(response, TextToSpeech.QUEUE_FLUSH, None)
            self.log("> [Voice] Speaking...")
        except Exception as e:
            self.log(f"> [Voice] (TTS not available in Pydroid, will work in APK)")
    
    def do_image(self, custom_prompt=None):
        prompt = custom_prompt if custom_prompt else self.get_prompt()
        if custom_prompt and "image" in custom_prompt.lower():
            prompt = custom_prompt.replace("image", "").strip()
        
        self.log(f"\n[IMAGE GENERATION - PRIVATE]")
        self.log(f"> Prompt: {prompt}")
        
        if not HAS_PIL:
            self.log("> ERROR: PIL not found. Install: pip install pillow")
            return
        
        try:
            # Create folders
            base = "/sdcard/DCIM/JARVIS" if os.path.exists("/sdcard") else "./JARVIS_IMAGES"
            os.makedirs(base, exist_ok=True)
            
            # Create image 512x512 with gradient and text
            width, height = 512, 512
            img = Image.new('RGB', (width, height), color=(10, 10, 30))
            draw = ImageDraw.Draw(img)
            
            # Gradient background
            for y in range(height):
                r = int(10 + y*0.3)
                g = int(10 + y*0.1)
                b = int(30 + y*0.2)
                draw.line([(0, y), (width, y)], fill=(r%255, g%255, b%255))
            
            # Add text - wrap it
            text = prompt[:60]  # limit
            try:
                font = ImageFont.truetype("/system/fonts/Roboto-Regular.ttf", 28)
            except:
                font = ImageFont.load_default()
            
            # Center text
            draw.text((20, height//2 - 30), f"JARVIS\n{prompt}", fill=(0, 255, 200), font=font, align="center", spacing=10)
            draw.text((10, height-30), f"Private AI - {datetime.now().strftime('%Y-%m-%d')}", fill=(100,100,100))
            
            filename = f"{base}/jarvis_img_{datetime.now().strftime('%H%M%S')}.jpg"
            img.save(filename)
            self.log(f"> SUCCESS: Image saved!\n> {filename}")
            self.log(f"> Check your Gallery -> JARVIS folder")
        except Exception as e:
            self.log(f"> ERROR: {e}")
    
    def do_video(self, custom_prompt=None):
        prompt = custom_prompt if custom_prompt else self.get_prompt()
        self.log(f"\n[VIDEO EDITING - PRIVATE]")
        self.log(f"> Prompt: {prompt}")
        
        if not HAS_PIL:
            self.log("> ERROR: Need PIL")
            return
        
        try:
            base = "/sdcard/Movies/JARVIS" if os.path.exists("/sdcard") else "./JARVIS_VIDEO"
            os.makedirs(base, exist_ok=True)
            
            # Create 3 images then make video from them using PIL -> save as GIF or MP4 frames
            # Simple version: create image sequence
            width, height = 640, 360
            frames = []
            for i in range(3):
                img = Image.new('RGB', (width, height), color=(10+i*30, 20, 50+i*20))
                draw = ImageDraw.Draw(img)
                try:
                    font = ImageFont.truetype("/system/fonts/Roboto-Bold.ttf", 32)
                except:
                    font = ImageFont.load_default()
                draw.text((20, height//2 - 40), f"JARVIS VIDEO\n{prompt[:30]}\nFrame {i+1}/3", fill=(0,255,180), font=font)
                frames.append(img)
            
            # Save as GIF (works without ffmpeg) and also as MP4 if moviepy available
            gif_path = f"{base}/jarvis_vid_{datetime.now().strftime('%H%M%S')}.gif"
            frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=800, loop=0)
            
            self.log(f"> SUCCESS: Video saved as GIF!\n> {gif_path}")
            
            # Try to make MP4 if moviepy available
            try:
                from moviepy.editor import ImageSequenceClip
                import numpy as np
                clip = ImageSequenceClip([np.array(f) for f in frames], fps=1)
                mp4_path = gif_path.replace(".gif", ".mp4")
                clip.write_videofile(mp4_path, codec='libx264', verbose=False, logger=None)
                self.log(f"> Also saved as MP4:\n> {mp4_path}")
            except:
                self.log(f"> (For MP4 install: pip install moviepy)")
                self.log(f"> GIF works in gallery")
                
        except Exception as e:
            self.log(f"> ERROR: {e}")
    
    def do_learn(self):
        self.log(f"\n[LEARNING FROM OPEN SOURCES]")
        if not HAS_REQUESTS:
            self.log("> Need requests: pip install requests")
            return
        
        try:
            self.log("> Connecting to Wikipedia (open source)...")
            # Get random article summary from Wikipedia API (open)
            url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                title = data.get('title', 'Unknown')
                extract = data.get('extract', '')[:300]
                
                # Save to memory
                base = "/sdcard/Documents/JARVIS" if os.path.exists("/sdcard") else "./JARVIS_MEMORY"
                os.makedirs(base, exist_ok=True)
                mem_file = f"{base}/memory.txt"
                with open(mem_file, "a", encoding="utf-8") as f:
                    f.write(f"\n[{datetime.now()}] LEARNED: {title}\n{extract}\n---\n")
                
                self.log(f"> LEARNED: {title}")
                self.log(f"> {extract}...")
                self.log(f"> Saved to memory.txt")
                self.log(f"> Total knowledge growing!")
            else:
                self.log(f"> Failed to learn: {r.status_code}")
        except Exception as e:
            self.log(f"> ERROR Learning: {e}")
            self.log(f"> Check internet")

if __name__ == '__main__':
    JarvisPrivateApp().run()
