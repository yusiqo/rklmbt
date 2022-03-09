import time
import json
import telebot

##TOKEN DETAILS
TOKEN = "Reklam"

BOT_TOKEN = "5267618322:AAGjCoO6Nwvwk8NsMhVgKjEa-9S5q_ilyz4"
PAYMENT_CHANNEL = "@ZetTekno" #add payment channel here including the '@' sign
OWNER_ID = 1342133634 #write owner's user id here.. get it from @MissRose_Bot by /id
CHANNELS = ["@ZetTekno"] #add channels to be checked here in the format - ["Channel 1", "Channel 2"] 
              #you can add as many channels here and also add the '@' sign before channel username
Daily_bonus = 0.1 #Put daily bonus amount here!
Mini_Withdraw = 1  #remove 0 and add the minimum withdraw u want to set
Per_Refer = 0.1 #add per refer bonus here

bot = telebot.TeleBot(BOT_TOKEN)

def check(id):
    for i in CHANNELS:
        check = bot.get_chat_member(i, id)
        if check.status != 'left':
            pass
        else:
            return False
    return True
bonus = {}

def menu(id):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🆔 Hesap')
    keyboard.row('🙌🏻 Referans', '🎁 Bonus')
    keyboard.row('〽️ Reklam Ver','📊Statistics')
    bot.send_message(id, "*🏡 Ana Menü*", parse_mode="Markdown",
                     reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start(message):
   try:
    user = message.chat.id
    msg = message.text
    if msg == '/start':
        user = str(user)
        data = json.load(open('users.json', 'r'))
        if user not in data['referred']:
            data['referred'][user] = 0
            data['total'] = data['total'] + 1
        if user not in data['referby']:
            data['referby'][user] = user
        if user not in data['checkin']:
            data['checkin'][user] = 0
        if user not in data['DailyQuiz']:
            data['DailyQuiz'][user] = "0"
        if user not in data['balance']:
            data['balance'][user] = 0
        if user not in data['wallet']:
            data['wallet'][user] = ""
        if user not in data['withd']:
            data['withd'][user] = 0
        if user not in data['id']:
            data['id'][user] = data['total']+1
        json.dump(data, open('users.json', 'w'))
        print(data)
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(
           text='✅ Katıldım', callback_data='check'))
        msg_start = "*🔆 Botu Kullana Bilmek İçin Kanala Katılmak Gerek - "
        for i in CHANNELS:
            msg_start += f"\n➡️ {i}\n"
        msg_start += "*"
        bot.send_message(user, msg_start,
                         parse_mode="Markdown", reply_markup=markup)
    else:

        data = json.load(open('users.json', 'r'))
        user = message.chat.id
        user = str(user)
        refid = message.text.split()[1]
        if user not in data['referred']:
            data['referred'][user] = 0
            data['total'] = data['total'] + 1
        if user not in data['referby']:
            data['referby'][user] = refid
        if user not in data['checkin']:
            data['checkin'][user] = 0
        if user not in data['DailyQuiz']:
            data['DailyQuiz'][user] = 0
        if user not in data['balance']:
            data['balance'][user] = 0
        if user not in data['wallet']:
            data['wallet'][user] = ""
        if user not in data['withd']:
            data['withd'][user] = 0
        if user not in data['id']:
            data['id'][user] = data['total']+1
        json.dump(data, open('users.json', 'w'))
        print(data)
        markups = telebot.types.InlineKeyboardMarkup()
        markups.add(telebot.types.InlineKeyboardButton(
            text='✅ Katıldım', callback_data='check'))
        msg_start = "*🔆 Botu Kullana Bilmek İçin Kanala Katılmak Gerek - \n➡️ @portakalmedya*"
        bot.send_message(user, msg_start,
                         parse_mode="Markdown", reply_markup=markups)
   except:
        bot.send_message(message.chat.id, "Bu Komutda Hata Algılandı Adminin Çözmesini Bekle")
        bot.send_message(OWNER_ID, "Your bot got an error fix it fast!\n Error on command: "+message.text)
        return

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
   try:
    ch = check(call.message.chat.id)
    if call.data == 'check':
        if ch == True:
            data = json.load(open('users.json', 'r'))
            user_id = call.message.chat.id
            user = str(user_id)
            bot.answer_callback_query(
                callback_query_id=call.id, text='✅ You joined Now you can earn')
            bot.delete_message(call.message.chat.id, call.message.message_id)
            if user not in data['refer']:
                data['refer'][user] = True

                if user not in data['referby']:
                    data['referby'][user] = user
                    json.dump(data, open('users.json', 'w'))
                if int(data['referby'][user]) != user_id:
                    ref_id = data['referby'][user]
                    ref = str(ref_id)
                    if ref not in data['balance']:
                        data['balance'][ref] = 0
                    if ref not in data['referred']:
                        data['referred'][ref] = 0
                    json.dump(data, open('users.json', 'w'))
                    data['balance'][ref] += Per_Refer
                    data['referred'][ref] += 1
                    bot.send_message(
                        ref_id, f"*🏧 Yeni Referans Level 1, Kazanç : +{Per_Refer} {TOKEN}*", parse_mode="Markdown")
                    json.dump(data, open('users.json', 'w'))
                    return menu(call.message.chat.id)

                else:
                    json.dump(data, open('users.json', 'w'))
                    return menu(call.message.chat.id)

            else:
                json.dump(data, open('users.json', 'w'))
                menu(call.message.chat.id)

        else:
            bot.answer_callback_query(
                callback_query_id=call.id, text='❌ Kanala Katılmadınız')
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(
                text='✅ Katıldım', callback_data='check'))
            msg_start = "*🔆 Botu Kullana Bilmek İçin Kanala Katılmak Gerek - \n➡️ @portakalmedya*"
            bot.send_message(call.message.chat.id, msg_start,
                             parse_mode="Markdown", reply_markup=markup)
   except:
        bot.send_message(call.message.chat.id, "Bu Komutda Hata Algılandı Adminin Çözmesini Bekle")
        bot.send_message(OWNER_ID, "Your bot got an error fix it fast!\n Error on command: "+call.data)
        return

@bot.message_handler(content_types=['text'])
def send_text(message):
   try:
    if message.text == '🆔 Hesap':
        data = json.load(open('users.json', 'r'))
        accmsg = '*👮 Kullanıcı : {}\n\n💸 Bakiye : *`{}`* {}*'
        user_id = message.chat.id
        user = str(user_id)

        if user not in data['balance']:
            data['balance'][user] = 0
        if user not in data['wallet']:
            data['wallet'][user] = ""

        json.dump(data, open('users.json', 'w'))

        balance = data['balance'][user]
        wallet = data['wallet'][user]
        msg = accmsg.format(message.from_user.first_name,
                            wallet, balance, TOKEN)
        bot.send_message(message.chat.id, msg, parse_mode="Markdown")
    if message.text == '🙌🏻 Referans':
        data = json.load(open('users.json', 'r'))
        ref_msg = "*⏯️ Toplam Ref : {} Users\n\n👥 Refferans Sistemi\n\n1 Level:\n🥇 Level°1 - {} {}\n\n🔗 Referans Link ⬇️\n{}*"

        bot_name = bot.get_me().username
        user_id = message.chat.id
        user = str(user_id)

        if user not in data['referred']:
            data['referred'][user] = 0
        json.dump(data, open('users.json', 'w'))

        ref_count = data['referred'][user]
        ref_link = 'https://telegram.me/{}?start={}'.format(
            bot_name, message.chat.id)
        msg = ref_msg.format(ref_count, Per_Refer, TOKEN, ref_link)
        bot.send_message(message.chat.id, msg, parse_mode="Markdown")
    if message.text == "⚙️ Set Wallet":
        user_id = message.chat.id
        user = str(user_id)

        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('🚫 Cancel')
        send = bot.send_message(message.chat.id, "_⚠️Send your TRX Wallet Address._",
                                parse_mode="Markdown", reply_markup=keyboard)
        # Next message will call the name_handler function
        bot.register_next_step_handler(message, trx_address)
    if message.text == "🎁 Bonus":
        user_id = message.chat.id
        user = str(user_id)
        cur_time = int((time.time()))
        data = json.load(open('users.json', 'r'))
        #bot.send_message(user_id, "*🎁 Bonus Button is Under Maintainance*", parse_mode="Markdown")
        if (user_id not in bonus.keys()) or (cur_time - bonus[user_id] > 60*60*24):
            data['balance'][(user)] += Daily_bonus
            bot.send_message(
                user_id, f"Başarıyla Kazandınız {Daily_bonus} {TOKEN}")
            bonus[user_id] = cur_time
            json.dump(data, open('users.json', 'w'))
        else:
            bot.send_message(
                message.chat.id, "❌*24 Saat Sonra Tekrar Ala bilirsiniz!*",parse_mode="markdown")
        return

    if message.text == "📊Statistics":
        user_id = message.chat.id
        user = str(user_id)
        data = json.load(open('users.json', 'r'))
        msg = "*📊 Toplam Kullanıcı : {}\n\n🥊 Toplam Yapılan Reklam: {} {}*"
        msg = msg.format(data['total'], data['totalwith'], TOKEN)
        bot.send_message(user_id, msg, parse_mode="Markdown")
        return

    if message.text == "〽️ Reklam Ver":
        user_id = message.chat.id
        user = str(user_id)

        data = json.load(open('users.json', 'r'))
        if user not in data['balance']:
            data['balance'][user] = 0
        if user not in data['wallet']:
            data['wallet'][user] = "none"
        json.dump(data, open('users.json', 'w'))

        bal = data['balance'][user]
        wall = data['wallet'][user]
        if bal == 0:
        	bot.send_message(
                user_id, f"_❌Çekim İçin Minumum 1 Puan Gerekir_", parse_mode="Markdown")
        if bal >= Mini_Withdraw:
            bot.send_message(user_id, "_Reklam Mesajı Giriniz_",
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, amo_with)
        else:
            bot.send_message(
                user_id, f"_❌Çekim İçin Minumum 1 Puan Gerekir_", parse_mode="Markdown")
            return
   except:
        bot.send_message(message.chat.id, "Bu Komutda Hata Algılandı Adminin Çözmesini Bekle")
        bot.send_message(OWNER_ID, "Your bot got an error fix it fast!\n Error on command: "+message.text)
        return

def trx_address(message):
   try:
    if message.text == "🚫 Cancel":
        return menu(message.chat.id)
    if len(message.text) == 34:
        user_id = message.chat.id
        user = str(user_id)
        data = json.load(open('users.json', 'r'))
        data['wallet'][user] = message.text

        bot.send_message(message.chat.id, "*💹Your Trx wallet set to " +
                         data['wallet'][user]+"*", parse_mode="Markdown")
        json.dump(data, open('users.json', 'w'))
        return menu(message.chat.id)
    else:
        bot.send_message(
            message.chat.id, "*⚠️ It's Not a Valid Trx Address!*", parse_mode="Markdown")
        return menu(message.chat.id)
   except:
        bot.send_message(message.chat.id, "Bu Komutda Hata Algılandı Adminin Çözmesini Bekle")
        bot.send_message(OWNER_ID, "Your bot got an error fix it fast!\n Error on command: "+message.text)
        return

def amo_with(message):
   try:
    user_id = message.chat.id
    amo = message.text
    user = str(user_id)
    data = json.load(open('users.json', 'r'))
    if user not in data['balance']:
        data['balance'][user] = 0
    if user not in data['wallet']:
        data['wallet'][user] = "none"
    json.dump(data, open('users.json', 'w'))
    bal = data['balance'][user]
    wall = data['wallet'][user]
    msg = message.text
    data['balance'][user] -= 1
    data['totalwith'] += 1
    bot_name = bot.get_me().username
    json.dump(data, open('users.json', 'w'))
    bot.send_message(user_id, "✅* Reklam Otomatik Olarak Kanala İletildi\n\n💹 Reklam Kanalı :- "+PAYMENT_CHANNEL+"*", parse_mode="Markdown")
    bot.send_message(PAYMENT_CHANNEL,  "✅* Yeni Reklam\n\n "+str(amo)+f" *", parse_mode="Markdown", disable_web_page_preview=True)
   except:
        bot.send_message(message.chat.id, "Bu Komutda Hata Algılandı Adminin Çözmesini Bekle")
        bot.send_message(OWNER_ID, "Your bot got an error fix it fast!\n Error on command: "+message.text)
        return

if __name__ == '__main__':
    bot.polling(none_stop=True)
