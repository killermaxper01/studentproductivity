[app]
title = Student Productivity App
package.name = studentproductivity
package.domain = org.kivy.student
source.include_exts = py,png,jpg,kv,atlas,json
source.dir = .
version = 1.0
requirements = python3,kivy,kivymd,plyer,requests,json,android,urllib3,certifi,chardet,idna
orientation = portrait
fullscreen = 1

[buildozer]
log_level = 2
warn_on_root = 1

[app/android]
# Target API Level for Maximum Android Compatibility (Supports Android 14)
android.api = 34
android.minapi = 21
android.ndk_api = 23

# Enable AndroidX for Compatibility with Newer Libraries
android.enable_androidx = True

# Fix Gradle Build Issues on Android 13/14
android.gradle_dependencies = com.android.tools.build:gradle:8.0.2
android.p4a_whitelist = https://dl.google.com/dl/android/maven2/

# Use Modern NDK (Fixes Crashes on Android 12+)
android.ndk = 25c

# Permissions for Storage, Network, AI API Calls, and Notifications
android.permissions = INTERNET,ACCESS_NETWORK_STATE,MANAGE_EXTERNAL_STORAGE,POST_NOTIFICATIONS,FOREGROUND_SERVICE,WAKE_LOCK,VIBRATE

# Fix Storage Issues (Android 13+ Restrictions)
android.private_storage = True

# Keep Screen Awake During Study Timer
android.wakelock = True

# Enable Hardware Acceleration for Smooth UI
android.hardware.accelerated = True

# Set Default Screen Orientation
android.orientation = portrait

# Add Required Features (Enables Internet & Notifications)
android.features = android.hardware.touchscreen

# Disable Multisampling to Avoid Rendering Issues on Some Devices
android.p4a_extra_args = --no-multiarch

# Force 64-bit Support for Android 11+ (Fixes Compatibility)
android.archs = arm64-v8a
