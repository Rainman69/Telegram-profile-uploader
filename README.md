# Telegram-profile-uploader
A Telegram automation script designed for Termux. It lets you set profile pictures, clone photos from other users or channels, and control operations via a private channel. Easy to run with Python and Telethon, it's ideal for managing Telegram profiles directly from your Android device.



راهنمای اجرای اسکریپت tgprof.py در Termux

Guide to Run tgprof.py Script in Termux


---

۱. نصب ترموکس و آماده‌سازی اولیه

Install Termux & Initial Setup

فارسی:

ابتدا برنامه‌ی Termux را از سایت F-Droid نصب کنید (نسخه‌ی Google Play پیشنهاد نمی‌شود).

سپس ترموکس را باز کرده و این دستورات را وارد کنید:


pkg update && pkg upgrade -y
pkg install python git -y

English:

First, download and install Termux from F-Droid (not Google Play).

Open Termux and run the following commands:


pkg update && pkg upgrade -y
pkg install python git -y


---

۲. نصب پیش‌نیازهای پایتون

Install Python Prerequisites

فارسی:
برای اجرای این اسکریپت به کتابخانه‌ی Telethon نیاز دارید. دستور زیر را وارد کنید:

pip install telethon

English:
This script requires the Telethon library. Run:

pip install telethon


---

۳. ذخیره و اجرای اسکریپت از مسیر دلخواه

Save & Run the Script from Any Location

فارسی:

ابتدا فایل tgprof.py را در هر پوشه‌ای که مایل هستید ذخیره کنید (برای مثال: Download یا scripts).

سپس در ترموکس، با استفاده از دستور cd وارد آن پوشه شوید. نمونه:


cd /data/data/com.termux/files/home/storage/downloads

حالا برای اجرای اسکریپت، دستور زیر را وارد کنید:


python tgprof.py

English:

Save the tgprof.py script in any folder you like (e.g., Download or scripts).

In Termux, navigate to that folder using cd. Example:


cd /data/data/com.termux/files/home/storage/downloads

Then run the script:


python tgprof.py


---

۴. ورود اولیه و دریافت مجوزها

Login and Initialization

فارسی:

در اولین اجرای اسکریپت، از شما خواسته می‌شود شماره‌ی تلفن خود را وارد کرده و کد تأیید تلگرام را وارد نمایید.

پس از ورود موفق، یک کانال خصوصی با نام tgprof Processing Channel به‌صورت خودکار ساخته می‌شود.


English:

On first run, you’ll be prompted to enter your Telegram phone number and verification code.

After successful login, a private channel named tgprof Processing Channel will be created automatically.



---

۵. نحوه استفاده از اسکریپت

How to Use the Script

فارسی:
برای کار با اسکریپت، پیام‌هایی به کانال ایجادشده ارسال کنید:

ارسال عکس: تصویر ارسال‌شده به‌عنوان عکس پروفایل شما تنظیم می‌شود.

ارسال دستوراتی مثل:

pause: توقف موقت

continue: ادامه

stop: توقف کامل


ارسال عبارت‌هایی مانند @username 5: آخرین ۵ عکس پروفایل یا کانال مشخص‌شده کپی می‌شود.


English:
To control the script, send messages to the created channel:

Sending a photo sets it as your Telegram profile picture.

Commands:

pause: temporarily pause the script

continue: resume the script

stop: fully stop the script


Example: @username 5 will copy the last 5 profile/channel photos from that username.

https://t.me/DamnAmo 
