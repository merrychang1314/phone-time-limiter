```ini
[app]
title = PhoneLimiter
package.name = phonelimiter
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.permissions = INTERNET
android.api = 30
android.minapi = 21
android.ndk = 23b
android.sdk = 30
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
