import uuid
import copy
from django.utils import timezone
import jdatetime
from PIL import ImageFont, Image, ImageDraw
from django.conf import settings
import re
from monogram.text import *

def generate_uid():
	return str(uuid.uuid4()).split("-")[0]

def get_time():
  now = jdatetime.datetime.utcnow()
  time_zone = jdatetime.timedelta(hours=3, minutes=30)
  now = now + time_zone
  # return now
  return now.isoformat()

def get_date2():
	now = jdatetime.datetime.utcnow()
	time_zone = jdatetime.timedelta(hours=3, minutes=30)
	now = now + time_zone

	return f"{now.year}/{now.month}/{now.day}"


def edit_keyboard(data, target_callback_data, new_text):
	array = data
	for inner_list in array:
		for item in inner_list:
			if item["callback_data"] == target_callback_data:
				item.update({"text": new_text})
	return array



def get_filename_with_date(base_filename, extension):
  """
  Combines a base filename with the current date in YYYY-MM-DD format.

  Args:
      base_filename (str): The base name of the file (without extension).
      extension (str): The file extension (e.g., ".txt", ".csv").

  Returns:
      str: The combined filename with date (e.g., "report_2024-07-18.txt").
  """

  # Get today's date in YYYY-MM-DD format
  today_str = timezone.now().timestamp()

  # Combine filename, date, and extension
  filename_with_date = f"{base_filename}_{today_str}{extension}"

  return filename_with_date



def generate_ticket(name, date, ticket):
	number = {'1': '۱', '2': '۲', '3': '۳', '4': '۴', '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹', '0': '۰'}
	shamsi_date = jdatetime.datetime.fromgregorian(datetime=date)
	date = shamsi_date.strftime('%Y/%m/%d %H:%M')
	for i in number:
		if i in date:
			date = date.replace(i, number[i])
	font_dir = settings.BASE_DIR / 'panel' / 'fonts'
	english_font = ImageFont.truetype(font_dir/"Fonarto.ttf", 80)
	english_font2 = ImageFont.truetype(font_dir/"Fonarto.ttf", 120)
	persian_font = ImageFont.truetype(font_dir/"Estedad.ttf", 80)
	image = Image.open(settings.BASE_DIR / 'panel' /"ticket.jpg")

	draw = ImageDraw.Draw(image)
	draw.text((1080, 660), name, (109, 129, 58), font=persian_font)
	draw.text((620, 400), ticket, (109, 129, 58), font=english_font2)

	draw.text((255, 645), date, (109, 129, 58), font=persian_font)

	draw = ImageDraw.Draw(image)
	path = get_filename_with_date(ticket, '.png')
	path = f"media/img/tickets/" + path
	image.save(path)

	return path


import jdatetime
from datetime import datetime

def convert_date(date):
    if date:
        # Convert to Shamsi date
        shamsi_date = jdatetime.datetime.fromgregorian(datetime=date)
        # Update the field in the dictionary
        return shamsi_date.strftime('%Y-%m-%d %H:%M')

def timeValidation(start_datetime, end_datetime, setting):
    try:
        current_time = jdatetime.datetime.now()
        # Convert to Jalali datetime objects
        shamsi_start_time = jdatetime.datetime.fromgregorian(datetime=start_datetime)
        shamsi_end_time = jdatetime.datetime.fromgregorian(datetime=end_datetime)
        if shamsi_start_time > shamsi_end_time:
            shamsi_start_time = shamsi_start_time - jdatetime.timedelta(days=7)
        # print('start time is: ', shamsi_start_time, 'day of week is:', shamsi_start_time.weekday())
        # print('end time is: ', shamsi_end_time, 'day of week is:', shamsi_end_time.weekday())
        # print('currnet time is: ', current_time, 'day of week is:', current_time.weekday())
        # # Check if the current date is within the registration period
        # print(start_time,current_time,end_time)
        # print(shamsi_start_time , current_time , shamsi_end_time)
        # print(shamsi_start_time <= current_time <= shamsi_end_time)
        # print(shamsi_start_time.weekday(), current_time.weekday(), shamsi_end_time.weekday(), shamsi_start_time.weekday() <= current_time.weekday() <= shamsi_end_time.weekday())
        st = jdatetime.datetime(year=current_time.year, month=current_time.month, day=shamsi_start_time.day, hour=shamsi_start_time.hour, minute=shamsi_start_time.minute)
        et = jdatetime.datetime(year=current_time.year, month=current_time.month, day=shamsi_end_time.day, hour=shamsi_end_time.hour, minute=shamsi_end_time.minute)
        # print(st, current_time, et, st<= current_time<= et)

        if shamsi_start_time.weekday() <= current_time.weekday() <= shamsi_end_time.weekday() and st<= current_time<= et:
            msg = "زمان ثبت نام در قرعه کشی فرا رسیده."
            return True, msg
        else:
            days_of_week = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه']

            def conver_to_shamsi(date):
                shamsi_date = jdatetime.datetime.fromgregorian(datetime=date)
                return shamsi_date

            shamsi_start_time = conver_to_shamsi(setting.start_time)
            start_time = {
                'day': days_of_week[shamsi_start_time.weekday()],
                'time': shamsi_start_time.strftime('%H:%M')
            }
            shamsi_end_time = conver_to_shamsi(setting.end_time)
            end_time = {
                'day': days_of_week[shamsi_end_time.weekday()],
                'time': shamsi_end_time.strftime('%H:%M')
            }
            shamsi_lottery_time = conver_to_shamsi(setting.lottery_time)
            lottery_time = {
                'day': days_of_week[shamsi_lottery_time.weekday()],
                'time': shamsi_lottery_time.strftime('%H:%M')
            }
            msg = f"{Bold('زمان ثبت نام در قرعه کشی هنوز شروع نشده.')} ثبت نام در قرعه کشی هر هفته از روز {Bold(start_time['day'])} ساعت {Bold(start_time['time'])} شروع میشه وروز {Bold(end_time['day'])} ساعت {Bold(end_time['time'])} تمام میشه و زمان قرعه کشیو اعالم برنده هاروز {Bold(lottery_time['day'])} ساعت {Bold(lottery_time['time'])} می باشد"
            return False, msg

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return False, "خطایی رخ داده است."


def keyboard_generator(my_list):
  """
  Creates a paired array from a given list.

  Args:
    my_list: The input list.

  Returns:
    A list of lists, where each inner list contains at most two elements.
  """

  paired_array = []
  i = 0
  while i < len(my_list):
    paired_array.append(my_list[i:i+3])
    i += 3
  return paired_array


def is_valid_username(username):
    """
    بررسی می‌کند که آیا یک نام کاربری فقط شامل حروف انگلیسی است و با عدد شروع نمی‌شود یا خیر.

    Args:
        username: نام کاربری مورد بررسی

    Returns:
        True اگر نام کاربری معتبر باشد، در غیر این صورت False.
    """

    # الگوی منظم برای بررسی نام کاربری معتبر:
    pattern = r"^[a-zA-Z]+[a-zA-Z0-9]*$"

    try:
        if isinstance(username, str):
            if re.match(pattern, username):
                return True, ''
            else:
                return False,  "نام کاربری باید با حرف انگلیسی شروع شود و شامل حروف انگلیسی و اعداد باشد."
        else:
            return False, "نام کاربری باید یک رشته باشد."
    except TypeError:
        return False, "نوع ورودی نامعتبر است."

def is_persian_name(text):
  pattern = r'^[\u0600-\u06FF\s]+$'
  match = re.match(pattern, text)

  return bool(match)
