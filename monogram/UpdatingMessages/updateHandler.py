from django.http import HttpResponse
from monogram.UpdatingMessages import Update
from monogram.types import CallbackQuery
import json
from pprint import pprint
from panel.models import Setting, Profile
from monogram.methods import getChatMember
from monogram.types import ChatMember, InlineKeyboardMarkup, InlineKeyboardButton
from monogram.extentions.conversation import Conversation

def check_regester(message):
    setting = Setting.objects.get(id=1)
    channel = setting.channel
    chat_member = getChatMember(chat_id=channel, user_id=message.chat.id)
    chat_member = ChatMember(**chat_member['result'])
    status = chat_member.status
    if status != 'member':
        channel = channel.replace('@', '')
        url = 'https://t.me/' + channel
        keyboard = [[InlineKeyboardButton("🔗 کانال", url)]]
        keyboard = InlineKeyboardMarkup(keyboard)
        message.answer("برای استفاده از ربات  ابتدا باید عضو کانال ما شوید.", keyboard=keyboard)
        return False
    else:
        text = 'شما هنوز ثبت نام نکردید, برای ثبت نام از دستور /start استفاده کنید.'
        conv = Conversation(message.chat.id)
        data = conv.data()
        regestering = data['callback_data'] == 'login' or data['callback_data'] == 'enter_name' or data['callback_data'] == 'enter_id' if data else None
        print(data, regestering)

        try:
            user = Profile.objects.get(user_id=message.chat.id)
            if user.status != 'Registered':
                print('state 1:UNRegistered', not regestering)
                if not regestering:
                    print('state 1:regestering')
                    message.answer(text)
                    return False
                else:
                    return True
            else:
                return True
        except Profile.DoesNotExist:
            print('state 2', not regestering)
            if regestering:
                message.answer(text)
                return False
            else:
                return True


def UpdateHandler(request, UPDATE_HANDLER):
    if request.method == 'POST' and UPDATE_HANDLER is not None:
        result = json.loads(request.body.decode('utf-8'))
        # pprint(result)
        # if 'callback_query' in result:
        #     # run callback query functions
        #     for cqf in UPDATE_HANDLER['callback_query']:
        #         # result['from_user'] = result['callback_query']
        #         # cqf(CallbackQuery(result['callback_query']))
        #         cqf(result['callback_query'])
        # else:
        update = Update(**result)
        if 'callback_query' in result:
            for cqf in UPDATE_HANDLER['callback_query']:
                cqf(update.callback_query)
        elif 'message' in result:
            if check_regester(update.message):
                for message in UPDATE_HANDLER['message']:
                    message(update.message)
        else:
            pass
        return HttpResponse("Hello, world!")
