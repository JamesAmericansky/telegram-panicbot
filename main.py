from user_interaction import UserInteraction

from decouple import config
from telebot import TeleBot

API_KEY = config("API_KEY")

bot = TeleBot(API_KEY)

def is_admin(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    member = bot.get_chat_member(chat_id, user_id)

    # member.status может быть: "creator", "administrator", "member", "restricted", "left", "kicked"
    if member.status in ["creator", "administrator"]:
        return True
    return False


@bot.message_handler(commands=['alertme'])
def link_user(message):
    user_id = message.from_user.id
    result_msg = UserInteraction.add_user(user_id)
    
    bot.reply_to(message, f"@{message.from_user.username} {result_msg}")


@bot.message_handler(commands=['panic'])
def alert_users(message):
    chat_id = message.chat.id
    print(message.from_user.username + "активировал /panic")
    
    if is_admin(message):
        args = message.text.split(maxsplit=1)
        panic_reason = args[1] if len(args) > 1 else ''
        
        panic = UserInteraction.get_alert(panic_reason) if panic_reason else UserInteraction.get_alert()
        
        bot.send_message(chat_id, panic, parse_mode="Markdown")
    else:
        bot.send_message(chat_id, "У вас недостаточно прав")


@bot.message_handler(commands=['unalert', 'unalertme'])
def unlink_user(message):
    user_id = message.from_user.id
    result_str = UserInteraction.remove_user(user_id)
    
    bot.send_message(message.chat.id, result_str)
    
bot.polling(none_stop=True)