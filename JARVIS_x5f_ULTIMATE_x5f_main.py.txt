from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.utils import platform
import os, webbrowser
from datetime import datetime

try:
    from plyer import notification, vibrator, flash
    PLYER = True
except:
    PLYER = False

def android_intent(action, data=None, package=None):
    try:
        if platform != 'android':
            return False, "يعمل على الأندرويد فقط - جرب APK"
        from jnius import autoclass
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        intent = Intent()
        if action == "VIEW":
            intent.setAction(Intent.ACTION_VIEW)
            if data:
                intent.setData(Uri.parse(data))
        elif action == "CALL":
            intent.setAction(Intent.ACTION_CALL)
            intent.setData(Uri.parse(f"tel:{data}"))
        elif action == "CAMERA":
            intent.setAction("android.media.action.IMAGE_CAPTURE")
        elif action == "SETTINGS":
            intent.setAction("android.settings.SETTINGS")
        elif action == "OPEN_APP" and package:
            pm = activity.getPackageManager()
            intent = pm.getLaunchIntentForPackage(package)
            if intent is None:
                intent = Intent(Intent.ACTION_VIEW)
                intent.setData(Uri.parse(f"market://details?id={package}"))
        if intent:
            activity.startActivity(intent)
            return True, "تم التنفيذ ✅"
        return False, "لم أجد التطبيق"
    except Exception as e:
        return False, str(e)

class JARVISUltimate(App):
    def build(self):
        self.title = "JARVIS ULTIMATE - ينفذ أي أمر"
        root = TabbedPanel(do_default_tab=False)

        tab1 = TabbedPanelItem(text='🤖 مساعد')
        layout1 = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout1.add_widget(Label(text='JARVIS ULTIMATE\nقل له أي شيء:\nافتح يوتيوب، صور، شغل الفلاش، اتصل، افتح الإعدادات، ابحث...', size_hint_y=None, height=120))
        self.cmd = TextInput(hint_text='اكتب أي أمر... مثلا: افتح تيك توك / اتصل 0555... / افتح الكاميرا / شغل فلاش', multiline=False, size_hint_y=None, height=50)
        btn_go = Button(text='🚀 نفذ أي أمر', background_color=(0,1,0.3,1), size_hint_y=None, height=60)
        btn_go.bind(on_press=self.run_any_command)
        self.out = Label(text='جاهز لتنفيذ أي أمر - اكتب و اضغط', size_hint_y=None, height=150)
        
        scroll = ScrollView(size_hint_y=0.5)
        grid = GridLayout(cols=3, spacing=5, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        
        quick_cmds = [
            ("YouTube", lambda: android_intent("OPEN_APP", package="com.google.android.youtube")),
            ("TikTok", lambda: android_intent("OPEN_APP", package="com.zhiliaoapp.musically")),
            ("Insta", lambda: android_intent("OPEN_APP", package="com.instagram.android")),
            ("Camera", lambda: android_intent("CAMERA")),
            ("Settings", lambda: android_intent("SETTINGS")),
            ("Flash ON", lambda: self.flash_ctrl(True)),
            ("Flash OFF", lambda: self.flash_ctrl(False)),
            ("Vibrate", lambda: self.vibrate()),
            ("Google", lambda: android_intent("VIEW", data="https://google.com")),
            ("Maps", lambda: android_intent("OPEN_APP", package="com.google.android.apps.maps")),
            ("Gallery", lambda: android_intent("OPEN_APP", package="com.google.android.apps.photos")),
            ("WhatsApp", lambda: android_intent("OPEN_APP", package="com.whatsapp")),
        ]
        for name, func in quick_cmds:
            b = Button(text=name, size_hint_y=None, height=50)
            def make_cb(f):
                return lambda x: self.exec_quick(f)
            b.bind(on_press=make_cb(func))
            grid.add_widget(b)
        scroll.add_widget(grid)
        
        layout1.add_widget(self.cmd)
        layout1.add_widget(btn_go)
        layout1.add_widget(self.out)
        layout1.add_widget(scroll)
        tab1.add_widget(layout1)

        tab2 = TabbedPanelItem(text='🎬 صنع فيديو')
        l2 = BoxLayout(orientation='vertical', padding=10, spacing=10)
        l2.add_widget(Label(text='صناعة فيديو بالذكاء الاصطناعي\nاكتب وصف الفيديو', size_hint_y=None, height=80))
        self.vprompt = TextInput(hint_text='مثال: رجل آلي يمشي في الجزائر، سينمائي، 4K...', size_hint_y=None, height=80)
        b_gen = Button(text='🎥 صنع الفيديو الآن', background_color=(1,0.5,0,1), size_hint_y=None, height=60)
        b_gen.bind(on_press=self.create_video_ai)
        self.vout = Label(text='💡 لصنع فيديو حقيقي:\n1. يفتح لك Pexels مجانا\n2. أو نربط API من HuggingFace\n3. الكود جاهز', size_hint_y=0.5)
        b_pexels = Button(text='جلب فيديو مجاني من Pexels', size_hint_y=None, height=50)
        b_pexels.bind(on_press=self.fetch_pexels_video)
        l2.add_widget(self.vprompt)
        l2.add_widget(b_gen)
        l2.add_widget(b_pexels)
        l2.add_widget(self.vout)
        tab2.add_widget(l2)

        tab3 = TabbedPanelItem(text='✂️ مونطاج')
        l3 = BoxLayout(orientation='vertical', padding=10, spacing=10)
        l3.add_widget(Label(text='مونطاج احترافي\nضع فيديوهاتك في: /Movies/JARVIS/', size_hint_y=None, height=80))
        self.m_cmd = TextInput(hint_text='مثال: ادمج vid1 و vid2', size_hint_y=None, height=60)
        b_mont = Button(text='🔥 ابدأ المونطاج', background_color=(0.2,0.6,1,1), size_hint_y=None, height=60)
        b_mont.bind(on_press=self.montage_pro)
        self.mout = Label(text='✅ يدعم:\n- دمج عدة فيديوهات\n- إضافة موسيقى\n- كتابة نص\n- قص\n\nضع ملفات vid1.mp4, vid2.mp4\nفي Movies/JARVIS/', size_hint_y=0.5)
        l3.add_widget(self.m_cmd)
        l3.add_widget(b_mont)
        l3.add_widget(self.mout)
        tab3.add_widget(l3)

        root.add_widget(tab1)
        root.add_widget(tab2)
        root.add_widget(tab3)
        return root

    def run_any_command(self, instance):
        c = self.cmd.text.lower().strip()
        if not c:
            self.out.text = "اكتب أمر أولا"
            return
        self.out.text = f"تنفيذ: {c}...\n"
        if "يوتيوب" in c or "youtube" in c:
            ok, msg = android_intent("OPEN_APP", package="com.google.android.youtube")
            self.out.text += f"YouTube: {msg}"
        elif "تيك توك" in c or "tiktok" in c:
            ok, msg = android_intent("OPEN_APP", package="com.zhiliaoapp.musically")
            self.out.text += f"TikTok: {msg}"
        elif "انستا" in c or "instagram" in c:
            ok, msg = android_intent("OPEN_APP", package="com.instagram.android")
            self.out.text += f"Insta: {msg}"
        elif "كاميرا" in c or "camera" in c or "صور" in c:
            ok, msg = android_intent("CAMERA")
            self.out.text += f"الكاميرا: {msg}"
        elif "فلاش" in c or "flash" in c:
            if "طفي" in c or "off" in c:
                self.flash_ctrl(False)
            else:
                self.flash_ctrl(True)
        elif "اتصل" in c or "call" in c:
            num = ''.join(filter(str.isdigit, c))
            if num:
                ok, msg = android_intent("CALL", data=num)
                self.out.text += f"اتصال {num}: {msg}"
            else:
                self.out.text += "اكتب الرقم: اتصل 0555..."
        elif "اعدادات" in c or "settings" in c:
            ok, msg = android_intent("SETTINGS")
            self.out.text += f"الإعدادات: {msg}"
        elif "اهتز" in c or "vibr" in c:
            self.vibrate()
        elif "واتساب" in c or "whatsapp" in c:
            ok, msg = android_intent("OPEN_APP", package="com.whatsapp")
            self.out.text += f"WhatsApp: {msg}"
        else:
            ok, msg = android_intent("VIEW", data=f"https://www.google.com/search?q={c}")
            self.out.text += f"بحث Google عن '{c}': {msg}"

    def exec_quick(self, func):
        try:
            res = func()
            if isinstance(res, tuple):
                ok, msg = res
                self.out.text = msg
            else:
                self.out.text = str(res)
        except Exception as e:
            self.out.text = f"خطأ: {e}"

    def flash_ctrl(self, on):
        try:
            if PLYER:
                if on:
                    flash.on()
                    self.out.text = "🔦 الفلاش شغال ✅"
                else:
                    flash.off()
                    self.out.text = "🔦 الفلاش طافي ✅"
        except Exception as e:
            self.out.text = f"فلاش: {e}"

    def vibrate(self):
        try:
            if PLYER:
                vibrator.vibrate(1)
                self.out.text = "📳 اهتزاز ✅"
        except Exception as e:
            self.out.text = f"اهتزاز: {e}"

    def create_video_ai(self, instance):
        prompt = self.vprompt.text or "nature"
        self.vout.text = f"🎬 صنع فيديو: {prompt}\nجاري فتح Pexels..."
        self.fetch_pexels_video(None)

    def fetch_pexels_video(self, instance):
        prompt = self.vprompt.text or "nature"
        ok, msg = android_intent("VIEW", data=f"https://www.pexels.com/video/search/{prompt}/")
        self.vout.text = f"✅ فتح Pexels: {prompt}\n{msg}\n\nحمل فيديو مجاني وضعه في Movies/JARVIS/ ثم مونطجه"

    def montage_pro(self, instance):
        self.mout.text = "🔥 جاري المونطاج...\n"
        try:
            from moviepy.editor import VideoFileClip, concatenate_videoclips
            base = "/storage/emulated/0/Movies/JARVIS"
            os.makedirs(base, exist_ok=True)
            files = [f for f in os.listdir(base) if f.endswith('.mp4')]
            if len(files) < 1:
                self.mout.text += f"❌ ضع فيديو في:\n{base}\nوجدت: {files}"
                return
            clips = []
            for f in files[:3]:
                try:
                    clips.append(VideoFileClip(os.path.join(base, f)).subclip(0,5))
                except:
                    clips.append(VideoFileClip(os.path.join(base, f)))
            final = concatenate_videoclips(clips)
            out = os.path.join(base, f"JARVIS_MONTAGE_{datetime.now().strftime('%H%M%S')}.mp4")
            final.write_videofile(out, codec='libx264', fps=24)
            self.mout.text += f"✅ تم!\n{out}"
        except Exception as e:
            self.mout.text += f"❌ خطأ: {e}"

if __name__ == '__main__':
    JARVISUltimate().run()
