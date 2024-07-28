from monogram.methods import *
from monogram import *
from monogram.text import *
from monogram.types import *
from monogram.UpdatingMessages import *
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import quote
from panel.models import *
from monogram.extentions.conversation import Conversation
import re
from panel.assist import *
from panel.views import convert_date as cnv_date
from django.utils import timezone

conf = configs(appname='panel')
bot = Monogram(**conf)



back_markup = ReplyKeyboardMarkup([[KeyboardButton('🔙 بازگشت')]], resize_keyboard=True)


@bot.newMessage(pattern=r'^/start')
def start(message):
    p = getUserProfile(user_id=message.chat.id)
    # print(p)
    p = UserProfilePhotos(**p['result'])
    # print(p.photos[0][0]['file_id'])
    # print(len(p.photos) !=0)
    filename = None
    if len(p.photos) !=0:
        f = getFile(p.photos[0][0]['file_id'])
        file_path = f['result']['file_path']
        filename = f'{message.chat.id}.jpg'
        pic = bot.download_file(filename=filename, dir_path='media/img/profile_pictures', file_path=file_path)
        # print(filename)
    try:
        user_info = Profile.objects.get(user_id=message.chat.id)
        message.answer('سلام دوباره! خیلی خوشحالیم که به جمع ما برگشتی.')
    except Profile.DoesNotExist:

        first_name = message.chat.first_name
        last_name = message.chat.last_name
        first_name = first_name if first_name else ''
        last_name = last_name if last_name else ''
        full_name = first_name + last_name
        filename = f"img/profile_pictures/{filename}" if filename else None
        login_code = message.text.split()[1].strip() if len(message.text.split()) > 1 else None
        username = message.chat.username
        user_id = message.chat.id
        user_info = Profile.objects.create(full_name=full_name, username=username, user_id=user_id, picture=filename, login_code=login_code)

        welcome_message = f"""سلام رفیق گل! ‍♀️‍♂️به {Bold('ربات مهمونشو')} خوش اومدی! اینجا یه جای باحالِ پر از آدمای باحالِ خوش‌گذرانِ دوست‌داشتنیه! هر هفته یه {Bold('قرعه‌کشی خفن')} داریم که برنده‌ها باید با جایزه‌شون دوستاشون رو مهمون کنن! فقط کافیه یه {Bold('کد معرفی')} از یکی از اعضای ربات بگیری و عضو شی تا تو هم تو این جمع باحال باشی! {Bold('منتظرتیم!')}"""
        message.answer(welcome_message)
    # print(user_info.login_code)
    if user_info.login_code == None:
        text = "🔹 کد معرف رو وارد کنید:"
        message.answer(text)
        c = Conversation(user_id=message.chat.id)
        c.create(callback_data='login')

    if user_info.login_code != None and user_info.enter_name == None:
        c = Conversation(user_id=message.chat.id)
        c.create(callback_data='enter_name')
        text = '👤 نام و نام خانوادگی خود را به حروف فارسی وارد کنید, توجه داشته باشید که این نام باید مطابق با نام و نام خانوادگی درج شده روی کارت بانکی شما باشد:'
        message.answer(text)

@bot.newMessage(pattern='📢 مشاهده کانال')
def visit_channel(message):
    # impelement is joined
    keyboard = [[InlineKeyboardButton("🔗 کانال", f"https://t.me/c/2000514189/999999999")]]
    keyboard = InlineKeyboardMarkup(keyboard)
    message.answer("🔹 برای دیدن کانال ما از دکمه زیر استفاده کن.", keyboard=keyboard)

@bot.newMessage(pattern='📤 ارسال کد معرف')
def share_invite_code(message):
    try:
        profile = Profile.objects.get(user_id=message.chat.id)
        full_name = profile.enter_name
        referral_code = profile.referral_code
        # print(referral_code)
        me = getMe()
        u = User(**me['result'])
        bot_id = u.id
        bot_username = u.username
        url = "http://t.me/share/url?url="
        text = f"سلام رفیق! من {full_name} هستم.\nدوست دارم باهات تو ربات مهمون شو بازی کنم!\nاگه موافق هستی که از این هفته بازی کنیم، روی لینک زیر بزن و با کد معرف من عضو ربات شو.\nhttp://t.me/{bot_username}?start={referral_code}"
        encoded_url = quote(text)
        url = url + encoded_url
        keyboard = [[InlineKeyboardButton("⤴ اشتراک گذاری", url)]]
        keyboard = InlineKeyboardMarkup(keyboard)
        message.answer(text, keyboard=keyboard)
    except Profile.DoesNotExist:
        message.answer("متاسفانه، کاربری با مشخصاتی که شما وارد کرده اید در سیستم ما یافت نشد.")

def friends_management_home():
    text = """🔹 میتونی با ارسال کد معرف به دوستات اونا رو عضو ربات کنی تا بعد بتونی به لیست دوستات اضافه‌شون کنی.
    🔸 برای اضافه کردن دوستات میتونی از دکمه <b>افزودن دوست</b> استفاده کنی.
    🔺 برای دیدن دوستات و حذف از لیست میتونی از دکمه <b>مشاهده لیست</b> استفاده کنی."""
    keyboard = [
        [
            InlineKeyboardButton("➕ افزودن دوست", callback_data="addfriend"),
            InlineKeyboardButton("👥 مشاهده لیست", callback_data="listfriend"),
        ],
    ]
    keyboard = InlineKeyboardMarkup(keyboard)
    return text, keyboard

@bot.newMessage(pattern='👤 ویرایش اطلاعات')
def edit_profile(message):
    try:
        profile = Profile.objects.get(user_id=message.chat.id)
        fullname = profile.enter_name
        username = profile.enter_id
        callback_data_fullname = 'editProfileFullname'
        callback_data_username = 'editProfileUsername'


        keyboard = [
            [
                InlineKeyboardButton(fullname, callback_data='null'),
                InlineKeyboardButton("نام و نام خانوادگی:", callback_data=callback_data_fullname),
            ],
            [
                InlineKeyboardButton(username, callback_data='null'),
                InlineKeyboardButton("نام کاربری:", callback_data=callback_data_username),
            ],
        ]
        keyboard = InlineKeyboardMarkup(keyboard)
        text = "در اینجا می توانید به راحتی اطلاعات پروفایل خود را ویرایش و به روز رسانی کنید. برای ویرایش هر بخش، کافی است بر روی دکمه مربوط به آن کلیک کنید."
        message.answer(text,keyboard=keyboard)
    except Profile.DoesNotExist:
        print('user not found')

@bot.newMessage(pattern='👥 لیست دوستان')
def friends_management(message):
    text, keyboard = friends_management_home()
    message.answer(text,keyboard=keyboard)

@bot.newMessage(pattern='🤖 آموزش ربات')
def bot_tutorial(message):
    try:
        setting = Setting.objects.get(id=1)
        video_link = setting.link
        sendVideo(chat_id=message.chat.id, video=video_link)
    except Setting.DoesNotExist:
        message.answer("آموزش بزودی قرار میگیرد.")

@bot.newMessage(pattern='☎ پشتیبانی')
def bot_support(message):
    try:
        profile = Profile.objects.get(user_id=message.chat.id)
        msg = Messages.objects.filter(sender=profile).last()
        if msg and msg.status == 'OPEN':
            text = 'پیام قبلی شما هنوز تویسط ادمین برسی نشده است. پس از برسی پیام قبلی دسترسی این بخش برای شما فعال میشود.'
            message.answer(text)
        else:
            text = 'بیام خود را بنویس تا برای ادمین ارسال کنم:'
            message.answer(text)
            conv = Conversation(message.chat.id)
            conv.create('support')
    except Messages.DoesNotExist:
        text = 'بیام خود را بنویس تا برای ادمین ارسال کنم:'
        message.answer(text)
        conv = Conversation(message.chat.id)
        conv.create('support')


@bot.newMessage(pattern='🎟 قرعه‌کشی')
def lottery(message):
    setting = Setting.objects.get(id=1)
    start_time = setting.start_time
    end_time = setting.end_time
    lottery_time = setting.lottery_time

    status, msg = timeValidation(start_time, end_time)
    if status:
        try:
            # Get the profile by ID
            profile = Profile.objects.get(user_id=message.chat.id)
            friends = profile.friends.all()
            friends = list(friends.values())

            lottery = Lottery.objects.filter(profile=profile)
            if lottery.exists():
                lottery = lottery.last()
                if lottery.status == "Unregistered":
                    lottery = Lottery(profile=profile, register_date=timezone.now(), status='Registering')
                    lottery.save()
                    keyboard = []
                    friends = lottery.friends.all()
                    try:
                        friendList = INIsection(Bold('دوستان انتخاب شده'), [])
                        game_name = INIsection(Bold('فعالیت انتخاب شده'), ' ')
                        msg = 'لطفا یکی از بازیهای زیر رو انتخاب کنید تا در صورت برنده شدن با دوستانتون انجام بدید:'
                        text = friendList + '\n' + game_name + '\n' + msg
                        games = Games.objects.all()
                        keyboard = []
                        for game in games:
                            inline_keyboard = InlineKeyboardButton(game.name,
                                                                   callback_data=f'selectedGame-{lottery.id}-{game.id}-{game.name}')
                            keyboard.append(inline_keyboard)
                        keyboard = keyboard_generator(keyboard)
                        keyboard = InlineKeyboardMarkup(keyboard)
                        # query.message.answer(text, keyboard=keyboard)
                        # editMessageText(text=text, reply_markup=keyboard, chat_id=chat_id, message_id=message_id)
                        message.answer(text, keyboard=keyboard)
                    except Games.DoesNotExist:
                        text = 'هیچ فعالیت یافت نشد!احتمالا ادمین هیچ فعالیت اضافه نکرده برای اطلاعات بیشتر با پشتیبانی تماس بگیرین.'
                        message.answer(text)

                elif lottery.status == "Registered":
                    path_file = lottery.ticket_picture.url[1:]
                    lottery_time = cnv_date(lottery_time)
                    text = 'شما قبلا ثبت نام کرده اید'
                    text = text + '\n' + f'زمان قرعه کشی:{lottery_time}'
                    sendPhoto(chat_id=message.chat.id, photo=InputFile(path_file), caption=text)
                else:
                    message.answer('شما هنوز ثبت نام خود را تکمیل نکرده اید.')
            else:

                lottery = Lottery(profile=profile, register_date=timezone.now(), status='Registering')
                lottery.save()

                try:
                    friendList = INIsection(Bold('دوستان انتخاب شده'), [])
                    game_name = INIsection(Bold('فعالیت انتخاب شده'), ' ')
                    msg = 'برای شرکت در قرعه کشی ابتدا از لیست فعالیت های موجود یک فعالیت را انتخاب کنید:'
                    text = friendList + '\n' + game_name + '\n' + msg
                    games = Games.objects.all()
                    keyboard = []
                    for game in games:
                        inline_keyboard = InlineKeyboardButton(game.name,
                                                               callback_data=f'selectedGame-{lottery.id}-{game.id}-{game.name}')
                        keyboard.append(inline_keyboard)
                    keyboard = keyboard_generator(keyboard)
                    keyboard = InlineKeyboardMarkup(keyboard)
                    # query.message.answer(text, keyboard=keyboard)
                    # editMessageText(text=text, reply_markup=keyboard, chat_id=chat_id, message_id=message_id)
                    message.answer(text, keyboard=keyboard)
                except Games.DoesNotExist:
                    text = 'هیچ فعالیت یافت نشد!احتمالا ادمین هیچ فعالیت اضافه نکرده برای اطلاعات بیشتر با پشتیبانی تماس بگیرین.'
                    message.answer(text)

        except Profile.DoesNotExist:
            pass

    else:
        message.answer(msg)

@bot.newMessage(pattern='📚 اطلاعات قرعه کشی')
def lottery_info(message):
    setting = Setting.objects.get(id=1)
    start_time = cnv_date(setting.start_time)
    end_time = cnv_date(setting.end_time)
    lottery_time = cnv_date(setting.lottery_time)
    # text = "ثبت نام در قرعه کشیهر هفتهاز روز ( روزی که تعیین کردم در پنل )ساعت ( ساعتی که تعیین کردم در پنل) شروع میشه وروز (روزی که تعیین کردم در پنل)ساعت (ساعتی که تعیین کردم در پنل) تمام میشه و زمان قرعه کشیو اعالم برنده ها( روز و ساعتی که در پنل برایقرعه کشی )می باشد"
    text = f"ثبت نام در قرعه کشی هر هفته از روز {start_time} شروع میشه وروز {end_time} تمام میشه و زمان قرعه کشی اعلام برنده ها{lottery_time}می باشد"
    message.answer(text)


from django.db.models import Count
@bot.newMessage(pattern='📊 آمار و ارقام')
def info(message):
    text = ''
    for action in ['profile', 'friends']:
        try:
            winning_lotteries = Lottery.objects.filter(winning=True)
            medals = "🥇🥈🥉🎖🎖"
            profiles = winning_lotteries.values(action).annotate(count=Count(action)).order_by('-count')
            lottery_data = []
            for index, profile in enumerate(profiles):
                # print(index, profile)
                profile_id = profile['profile'] if action == 'profile' else profile['friends']
                count = profile['count']
                # Get lottery entries for the current profile
                if profile_id:
                    profile = Profile.objects.get(id=profile_id)
                    lottery_data.append(f"{medals[index] if index <= 4 else ''} {profile.enter_name}")
            if action == 'profile':
                winners_text = INIsection(Bold('🏆 نفراتی که بیشترین بار برنده شدند'), lottery_data)
                text += '\n'+winners_text
            elif action == 'friends':
                friends_text = INIsection(Bold('👥 نفراتی که بیشترین بار به عنوان دوست برنده شدند'), lottery_data)
                text += '\n'+friends_text
        except Lottery.DoesNotExist:
            text += '\n'+ '🎖 فعلا برنده ای نداشتیم!'

    total_profiles = Profile.objects.count()
    text += '\n' + Bold('🤖 تعداد اعضای ربات') +': '+ str(total_profiles)
    message.answer(text)


def callback_query(query):
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    print(chat_id, message_id, query.data, query.data == 'listfriend')
    if query.data == 'listfriend':
        try:
            # Get the profile by ID
            profile = Profile.objects.get(user_id=chat_id)
            friends = profile.friends.all()
            friends = list(friends.values())
            keyboard = []
            for friend in friends[:20]:
                friend_username = friend['enter_id']
                friend_id = friend['id']
                keyboard.append([
                    InlineKeyboardButton(f"{friend_username}", callback_data="bck-friend"),
                    InlineKeyboardButton("❌ حذف", callback_data=f"rmfriend-{friend_id}-{chat_id}"),
                ])

            if len(friends) > 20:
                keyboard.append([InlineKeyboardButton(">>", callback_data="page-1-20")])
            if friends:
                text = f"{Bold('لیست دوستات اینجاست!')}\nمیتونی توی این صفحه دوستات رو ببینی و اگه دیگه نمیخوای باهاشون دوست باشی، میتونی راحت اونا رو حذف کنی."
            else:
                text = "فقط کافیه کد معرفت رو براشون بفرستی! بعدش میتونی لیست دوستات رو توی ربات ببینی و باهاشون بازی کنی."

            keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="bck-friend")])
            keyboard = InlineKeyboardMarkup(keyboard)

            editMessageText(text=text, reply_markup=keyboard, chat_id=chat_id, message_id=message_id)
        except Profile.DoesNotExist:
            # Handle case where profile with ID is not found
            pass

    if query.data == 'bck-friend':
        text, keyboard = friends_management_home()
        editMessageText(text=text, reply_markup=keyboard, chat_id=chat_id, message_id=message_id)
        conv = Conversation(chat_id)
        conv.cancel()

    if 'rmfriend' in query.data:
        data = query.data.split('-')
        friend_id = data[1]
        user_id = data[2]
        try:
            profile = Profile.objects.get(user_id=user_id)
            friend = profile.friends.get(id=friend_id)
            profile.friends.remove(friend)
            keyboard=[[InlineKeyboardButton("🔙 بازگشت", callback_data="listfriend")]]
            keyboard = InlineKeyboardMarkup(keyboard)
            text = 'یوزر مورد نظر با موفقیت از لیست دوستات حذف شد.'
            editMessageText(text=text, reply_markup=keyboard, chat_id=chat_id, message_id=message_id)
        except Profile.DoesNotExist:
            pass

    if query.data == 'addfriend':
        text = "فقط کافیه نام کاربرای که دوستت رو ازش بگیری و برام بفرستی تا به لیست دوستات اضافش کنم."
        keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data="bck-friend")]]
        keyboard = InlineKeyboardMarkup(keyboard)
        editMessageText(text=text, reply_markup=keyboard, chat_id=chat_id, message_id=message_id)
        conv = Conversation(chat_id)
        conv.create(callback_data='addfriend')

    if 'acceptFriend' in query.data:
        data = query.data.split('-')
        friend_id = data[1]
        username = data[2]
        try:
            profile = Profile.objects.get(user_id=friend_id)
            try:
                # Find friend profile by enter_id
                friend_profile = Profile.objects.get(user_id=chat_id)
                # Add friend to user's friend list
                profile.friends.add(friend_profile)
                profile.save()  # Save changes explicitly (optional for Django < 2.0)
                # Add user to friend's friend list for symmetry
                friend_profile.friends.add(profile)
                friend_profile.save()  # Optional for symmetry

                text = 'درخواست کاربر موردنظر باموفقیت تایید شد.'
                # sendMessage(chat_id=chat_id, text=text)
                editMessageText(text=text, message_id=query.message.message_id, chat_id=chat_id)
                text = f'کاربری با نام {Bold(friend_profile.enter_name)} یورنیم {Bold(friend_profile.enter_id)} درخواست دوستی شمارا قبول کرد'
                sendMessage(chat_id=friend_id, text=text)
                conv = Conversation(friend_id)
                conv.cancel()
            except Profile.DoesNotExist:
                pass
        except Profile.DoesNotExist:
            pass

    if 'cancelFriend' in query.data:
        data = query.data.split('-')
        friend_id = data[1]
        username = data[2]
        try:
            friend_profile = Profile.objects.get(user_id=chat_id)
            text = 'درخواست کاربر موردنظر باموفقیت رد شد.'
            # sendMessage(chat_id=chat_id, text=text)
            editMessageText(text=text, message_id=query.message.message_id, chat_id=chat_id)
            text = f'کاربری با نام {Bold(friend_profile.enter_name)} یورنیم {Bold(friend_profile.enter_id)} درخواست دوستی شمارا رد کرد'
            sendMessage(chat_id=friend_id, text=text)
            conv = Conversation(friend_id)
            conv.cancel()
        except Profile.DoesNotExist:
            pass

    if 'editProfileFullname' in query.data:
        conv = Conversation(chat_id)
        conv.create('editProfileFullname')
        text = '👤 نام و نام خانوادگی خود را به حروف فارسی وارد کنید:'
        sendMessage(chat_id=chat_id, text=text)

    if 'editProfileUsername' in query.data:
        conv = Conversation(chat_id)
        conv.create('editProfileUsername')
        text = '🔹 لطفا یک یوزرنیم به حروف انگلیسی برای خودتان انتخاب و ارسال کنید:'
        sendMessage(chat_id=chat_id, text=text)

    if 'selectFriend' in query.data:
        data = query.data.split('-')
        lottery_id = data[1]

        lottery = Lottery.objects.get(id=lottery_id)
        friends = lottery.profile.friends.all()
        keyboard = []
        if len(friends) != 0:
            for friend in friends:
                friend_name = friend.enter_name
                friend_id = friend.id
                keyboard.append([
                    InlineKeyboardButton(f"❌ {friend_name}",
                                         callback_data=f"selectedFriend-{friend_id}-{lottery.id}-{friend_name}"),
                ])
            game_name = lottery.game.name
            friendList = INIsection(Bold('دوستان انتخاب شده'), [])
            game_name = INIsection(Bold('فعالیت انتخاب شده'), game_name)
            msg = 'برای شرکت در قرعه کشی ابتدا باید از لیست زیر دوستان خودرا انتخاب کنید:'
            text = friendList + '\n' + game_name + '\n' + msg
            keyboard = InlineKeyboardMarkup(keyboard)
            # query.message.answer(text, keyboard=keyboard)
            editMessageText(text=text, reply_markup=keyboard, chat_id=chat_id, message_id=message_id)
        else:
            text = 'شماه هیچ دوستی ندارید.\nلطفا از قسمت "➕ افزودن دوست" اقدام به اضافه کردن دوستان خود کنید.'
            keyboard = [
                [
                    InlineKeyboardButton("➕ افزودن دوست", callback_data="addfriend"),
                ],
            ]
            keyboard = InlineKeyboardMarkup(keyboard)
            # query.message.answer(text, keyboard=keyboard)
            editMessageText(text=text, reply_markup=keyboard, chat_id=chat_id, message_id=message_id)

    if 'selectedFriend' in query.data:
        data = query.data.split('-')
        friend_id = data[1]
        lottery_id = data[2]
        friend_name = data[3]
        print(friend_id, lottery_id, friend_name)
        try:
            lottery = Lottery.objects.get(id=lottery_id)
            profile = Profile.objects.get(id=friend_id)
            keyboard = query.message.reply_markup['inline_keyboard']
            for inner_list in keyboard:
                for item in inner_list:
                    if item['text'] == '💳 رفتن به مرحله پرداخت':
                        print('selectGame:')
                        keyboard.remove(inner_list)
                        print(inner_list)
                        print(item)
                    if item["callback_data"] == query.data:
                        if "✅" not in item["text"]:
                            # text = f"✅ {item['text']}"
                            text = item["text"].replace("❌ ", "✅ ")
                            lottery.friends.add(profile)
                        else:
                            text = item["text"].replace("✅ ", "❌ ")
                            lottery.friends.remove(profile)
                        item.update({"text": text})

            friendList = []
            for friend in lottery.friends.all():
                name = friend.enter_name
                friendList.append(name)
            if len(friendList):
                payment = InlineKeyboardButton('💳 رفتن به مرحله پرداخت', callback_data=f"payment")
                if [payment] not in keyboard:
                    keyboard.append([payment])
            keyboard = InlineKeyboardMarkup(keyboard)
            friendList = INIsection(Bold('دوستان انتخاب شده'), friendList)
            game_name = lottery.game.name
            game_name = INIsection(Bold('فعالیت انتخاب شده'), game_name)
            msg = 'برای شرکت در قرعه کشی ابتدا باید از لیست زیر دوستان خودرا انتخاب کنید:'
            text = friendList + '\n' + game_name + '\n' + msg
            editMessageText(text=text, reply_markup=keyboard, chat_id=chat_id, message_id=message_id)

        except Lottery.DoesNotExist:
            print('lottery does not exist.')

    if 'selectedGame' in query.data:
        data = query.data.split('-')
        lottery_id = data[1]
        game_id = data[2]
        game_name = data[3]

        try:
            games = Games.objects.all()
            keyboard = []
            for game in games:
                gameName = "✅ "+game.name if game.name == game_name else game.name
                # print(game_name, gameName, game.name)
                inline_keyboard = InlineKeyboardButton(gameName, callback_data=f'selectedGame-{lottery_id}-{game.id}-{gameName}')
                keyboard.append(inline_keyboard)

            keyboard = keyboard_generator(keyboard)
            if '✅' not in game_name:
                keyboard.append([
                        InlineKeyboardButton('رفتن به انتخاب دوستان', callback_data=f"selectFriend-{lottery_id}")
                ])

            keyboard = InlineKeyboardMarkup(keyboard)

            # friendList = []
            lottery = Lottery.objects.filter(id=lottery_id).last()
            # profile = Profile.objects.get(id=friend_id)
            # lottery.friends.add(profile)
            # friends = lottery.friends.all()
            lottery.game = Games.objects.get(id=game_id)
            lottery.save()
            # for friend in friends:
            #     friendList.append(friend.enter_name)
            friendList = INIsection(Bold('دوستان انتخاب شده'), [])
            game_name = '' if '✅' in game_name else game_name
            game_name = INIsection(Bold('فعالیت انتخاب شده'), game_name)
            msg = 'برای شرکت در قرعه کشی ابتدا باید از لیست زیر دوستان خودرا انتخاب کنید:'
            text = friendList + '\n' + game_name + '\n' + msg
            editMessageText(text=text, reply_markup=keyboard, chat_id=chat_id, message_id=message_id)

        except Games.DoesNotExist:
            text = 'هیچ فعالیت یافت نشد!احتمالا ادمین هیچ فعالیت اضافه نکرده برای اطلاعات بیشتر با پشتیبانی تماس بگیرین.'
            message.answer(text)

    if 'payment' in query.data:
        setting = Setting.objects.get(id=1)
        card_number = Bold(setting.card_number)
        card_name = Bold(setting.card_name)
        payment_price = Bold(setting.price)
        # text = "برای واریز مبلغ مورد نظر، لطفا به شماره کارت {card_number} به نام {card_name} وجه {payment_price} تومان را انتقال دهید.\nسپس با فشردن دکمه زیر عکس فیش واریزی خود را ارسال کنید."
        text = f"لطفا مبلغ {payment_price} نومان را به شماره کارت زیر واریز نمایید و با فشردن دکمه زیر عکس فیش واریزی خود را ارسال کنید."
        text += "\n" + f"{card_number}" + "\n" + f"{card_name}"
        keyboard = [
            [
                InlineKeyboardButton("📑 ارسال فیش پرداخت", callback_data="paid"),
            ],
        ]
        keyboard = InlineKeyboardMarkup(keyboard)
        editMessageText(text=text, reply_markup=keyboard, chat_id=chat_id, message_id=message_id)
        
    if 'paid' in query.data:
        conv = Conversation(chat_id)
        conv.create('paid')
        text = 'لطفا عکس فیش واریزی خود را ارسال کنید:'
        query.message.answer(text)

def filter_message2(message):

  try:
    # Check if text or caption attribute exists
    text = message.text or message.caption
    if text:
        filter_patterns = ['^/start', '📢 مشاهده کانال', '📤 ارسال کد معرف', '👤 ویرایش اطلاعات', '👥 لیست دوستان','🤖 آموزش ربات', '☎ پشتیبانی', '🎟 قرعه‌کشی', '📊 آمار و ارقام']
        for pattern in filter_patterns:
            pattern_match = re.match(pattern, text)
            print(pattern_match, bool(pattern_match))
            if pattern_match:
                return True
                break
    else:
      # Handle case where both text and caption are missing
      return False
  except AttributeError as e:
    # Handle case where message object lacks required attributes
    print(f"Error accessing message attributes: {e}")
    return

def filter_message(message):
  try:
      text = message.text or message.caption
      if text:
          patterns = ['^/start', '📢 مشاهده کانال', '📤 ارسال کد معرف', '👤 ویرایش اطلاعات', '👥 لیست دوستان', '🤖 آموزش ربات', '☎ پشتیبانی', '🎟 قرعه‌کشی', '📊 آمار و ارقام']
          compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
          for pattern in compiled_patterns:
              match = pattern.search(text)
              if match:
                  return True
          return False
      else:
          return False
  except AttributeError as e:
    print(f"Error accessing message attributes: {e}")
    return False

from django.db.models import Exists

def any(message):
    # sendPhoto(message.chat.id, photo=InputFile('Screenshot (7).png'), caption='this is a test to sending photo.')
    # print(message)
    # print(message.photo != None)
    # Perform conversation tasks
    conv = Conversation(message.chat.id)
    data = conv.data()
    print('conversations:', data)
    print(filter_message(message))
    if data and not filter_message(message):

        if data['callback_data'] == 'login':
            # check validation of code:
            exists = Profile.objects.filter(login_code=message.text).exists()
            admin_login_code = Admins.objects.filter(login_code=message.text).exists()
            if exists or admin_login_code:
                profile = Profile.objects.get(user_id=message.chat.id)
                profile.login_code = message.text
                profile.save()
                # conv.cancel()
                conv.change_callback_data(callback_data='enter_name')
                text = '👤 نام و نام خانوادگی خود را به حروف فارسی وارد کنید, توجه داشته باشید که این نام با نام و نام خانوادگی روی کارت بانکی شما یکسان یاشد:'
                message.answer(text)
            else:
                text = 'لطفا کد معرف را از دوستان خود بگیرید یا از طریق لینک معرف آنها اقدام کنید, کد وارد شده صحیح نیست دوباره وارد کنید:'
                message.answer(text)
        if data['callback_data'] == 'enter_name':
            if is_persian_name(message.text):
                profile = Profile.objects.get(user_id=message.chat.id)
                profile.enter_name = message.text.lower()
                profile.save()
                conv.change_callback_data(callback_data='enter_id')
                text = '🔹 لطفا یک یوزرنیم به حروف انگلیسی برای خودتان انتخاب و ارسال کنید:'
                message.answer(text)
            else:
                message.answer(f"خطا! لطفا نام و نام خانوادگی خود را با {Bold('حروف فارسی')} وارد کنید")

        if data['callback_data'] == 'enter_id':
            text_status, msg = is_valid_username(message.text)
            if text_status:
                profile = Profile.objects.get(user_id=message.chat.id)
                profile.enter_id = message.text.lower()
                profile.save()
                conv.cancel()
                text = '✅ اطلاعاتت با موفقیت تکمیل شد!'
                keyboard = [
                    [KeyboardButton('🎟 قرعه‌کشی')],
                    [KeyboardButton('📚 اطلاعات قرعه کشی'),KeyboardButton('📤 ارسال کد معرف'),KeyboardButton('📢 مشاهده کانال'),],
                    [KeyboardButton('👤 ویرایش اطلاعات'),KeyboardButton('👥 لیست دوستان'),],
                    [
                        KeyboardButton('☎ پشتیبانی'),
                        KeyboardButton('📊 آمار و ارقام'),
                        KeyboardButton('🤖 آموزش ربات'),
                    ],
                ]
                keyboard = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

                message.answer(text, keyboard=keyboard)
            else:
                message.answer(msg)
        if data['callback_data'] == 'addfriend':
            try:
                profile = Profile.objects.get(user_id=message.chat.id)
                try:
                    # Find friend profile by enter_id
                    friend_profile = Profile.objects.get(enter_id=message.text)

                    # Check if friend is already in user's friend list
                    if friend_profile not in profile.friends.all():
                        text = f"کاربری با نام {profile.enter_name} و نام کاربری {profile.enter_id} برای شما درخواست دوستی فرستاده.از دکمه زیر برای تایید درخواست استفاده کنید.{Bold('توجه داشته باشد بعد از تایید به لیست دوستان یکدیگر اضافه میشوید.')}"
                        keyboard = [
                            [
                                InlineKeyboardButton("✅ تایید", callback_data=f"acceptFriend-{message.chat.id}-{message.text}"),
                                InlineKeyboardButton("❌ رد", callback_data=f"cancelFriend-{message.chat.id}-{message.text}"),
                            ]
                        ]
                        keyboard = InlineKeyboardMarkup(keyboard)
                        sendMessage(chat_id=friend_profile.user_id, text=text, reply_markup=keyboard)
                        text = 'درخواست دوستی شما برای کاربر مورد نظر ارسال شد پس از تایید, به لیست دوستات اضافه میشه.\nبرای اضافه کردن دوستان بیشتر از دکمه بازگشت استاده کنید.'
                        keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data="bck-friend")]]
                        keyboard = InlineKeyboardMarkup(keyboard)
                        message.reply(text=text, keyboard=keyboard)
                        # message.answer(chat_id=message.chat.id, text=text, keyboard=keyboard)

                    else:
                        text = 'در حال حاظر این کاربر در لیست دوستان شما قرار دارد\nیک نام کاربری دیگر را وارد کنید یا دکمه بازگشت را برای لفو عملیات بزنید.'
                        keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data="bck-friend")]]
                        keyboard = InlineKeyboardMarkup(keyboard)
                        message.reply(text=text, keyboard=keyboard)
                        # message.answer(chat_id=message.chat.id, text=text, keyboard=keyboard)
                except Profile.DoesNotExist:
                    text = 'هیچ کاربری با این نام کاربری در سیستم وجود ندارد\nیک نام کاربری دیگر را وارد کنید یا دکمه بازگشت را برای لفو عملیات بزنید.'
                    keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data="bck-friend")]]
                    keyboard = InlineKeyboardMarkup(keyboard)
                    message.reply(text=text, keyboard=keyboard)
                    # message.answer(chat_id=message.chat.id, text=text, keyboard=keyboard)
            except Profile.DoesNotExist:
                pass
        if data['callback_data'] == 'editProfileFullname':
            try:
                profile = Profile.objects.get(user_id=message.chat.id)
                profile.enter_name = message.text.lower()
                profile.save()
                conv.cancel()
                text = 'نام و نام خانوادگی شما با موفقیت ویرایش شد.'
                message.answer(text)

            except Profile.DoesNotExist:
                pass
        if data['callback_data'] == 'editProfileUsername':
            try:
                profile = Profile.objects.get(user_id=message.chat.id)
                profile.enter_id = message.text.lower()
                profile.save()
                conv.cancel()
                text = 'نام کاربری شما با موفقیت ویرایش شد.'
                message.answer(text)

            except Profile.DoesNotExist:
                pass
        if data['callback_data'] == 'support':
            try:
                profile = Profile.objects.get(user_id=message.chat.id)
                if message.photo == None:
                    Messages.objects.create(sender=profile, message=message.text)
                else:
                    file_id = message.photo[-1].file_id
                    f = getFile(file_id)
                    file_path = f['result']['file_path']
                    filename = get_filename_with_date(message.chat.id, '.jpg')
                    pic = bot.download_file(filename=filename, dir_path='media/img/uploads/', file_path=file_path)
                    filename = 'img/uploads/' + filename
                    Messages.objects.create(sender=profile, message=message.caption, sender_picture=filename)


                text = 'پیام شما با موفقیت ارسال شد.'
                message.answer(text)
                conv.cancel()
            except Profile.DoesNotExist:
                pass
        if data['callback_data'] == 'paid':
            try:
                profile = Profile.objects.get(user_id=message.chat.id)
                if message.photo != None:
                    lottery = Lottery.objects.filter(profile=profile).last()
                    file_id = message.photo[-1].file_id
                    f = getFile(file_id)
                    file_path = f['result']['file_path']
                    filename = get_filename_with_date(message.chat.id, '.jpg')
                    pic = bot.download_file(filename=filename, dir_path='media/img/uploads', file_path=file_path)
                    filename = 'img/uploads/' + filename
                    lottery.payment_picture = filename
                    lottery.save()
                    text = 'فیش شما با موفقیت ارسال شد منتظر تایید ادمین باشید.'
                    message.answer(text)
                    conv.cancel()
            except Profile.DoesNotExist:
                pass


UPDATE_HANDLER = {
    'message': [start, any, visit_channel, share_invite_code, friends_management, edit_profile, bot_tutorial, bot_support, lottery, lottery_info, info],
    'callback_query': [callback_query, ]
}
@csrf_exempt
def uph(request):
    return UpdateHandler(request, UPDATE_HANDLER)