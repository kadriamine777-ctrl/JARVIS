[app]
title = JARVIS PRIVATE
package.name = jarvisprivate
package.domain = com.adem.jarvisprivate

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 2.0
requirements = python3,kivy,Pillow,requests,moviepy,numpy
source.main = main_v2.py

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,RECORD_AUDIO,CAMERA,ACCESS_NETWORK_STATE,WRITE_MEDIA_IMAGES
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.private_storage = False
