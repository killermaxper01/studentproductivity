[app]
title = Student Productivity App
package.name = studentproductivity
package.domain = com.yourdomain
source.include_exts = py,png,jpg,kv,json,ttf,otf
version = 1.0
requirements = python3,kivy,kivymd,plyer,requests,android
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, RECEIVE_BOOT_COMPLETED, VIBRATE, POST_NOTIFICATIONS, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, WAKE_LOCK, FOREGROUND_SERVICE
android.api = 34
android.minapi = 21
android.ndk = 23b
android.ndk_version = 23b
android.gradle_dependencies = com.google.android.gms:play-services-ads:22.2.0
android.enable_androidx = True
android.allow_cleartext = True
android.arch = arm64-v8a,armeabi-v7a,x86_64
android.compile_options = -O2
p4a.branch = master
p4a.fork = kivy/python-for-android
android.compile_sdk = 34
android.build_tools_version = 34.0.0
android.gradle_dependencies = com.android.support:support-compat:28.0.0
android.manifest_intent_filters = "intent-filter android:host=* android:scheme=http android:scheme=https"
android.services = NOTIFICATION
android.meta_data = android.support.VERSION:28.0.0
android.hardware.accelerated = True
android.allow_backup = True
android.backup_rules = res/xml/backup_rules.xml
android.keystore = debug.keystore
android.preserve_artifacts = True
android.release = True
android.wakelock = True
android.foreground_service_type = mediaPlayback
android.disable_optimizations = False
android.enable_resource_optimizer = True
android.extra_manifest_xml = <uses-feature android:name="android.hardware.touchscreen" android:required="true"/>

[buildozer]
log_level = 2
warn_on_root = 1

[buildozer.extensions]
android.presplash_color = #FFFFFF
android.presplash_path = res/drawable/presplash.png
android.icon = res/drawable/icon.png
android.adaptive_icon_foreground = res/drawable/icon_foreground.png
android.adaptive_icon_background = res/drawable/icon_background.png
android.disable_customization = False
