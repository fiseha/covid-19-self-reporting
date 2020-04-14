from __future__ import print_function
import logging
import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

# configuration reading and parsing
import configparser

# easier translations
import gettext

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from save_data import save_response



# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

USER_INFO = []

logger = logging.getLogger(__name__)

(
    INDICATORS,
    START,
    LOCATION,
    TEL,
    SYMPTOMS,
    CONDITIONS,
    TRAVEL_HISTORY,
    EXPOSURE,
    CARE_FACILITY,
    RESULT,
) = range(10)

ER_NUMBER = "8335"

# change to your prefered language here
# can be also programmatically switched, I haven't tried it yet
# try changing to am
el = gettext.translation("base", localedir="locales", languages=["en"])
el.install()
_ = el.gettext


def start(update, context):
    reply_keyboard = [
        [_("I'm experiencing at least one of these"), _("I do not have any of these")]
    ]

    update.message.reply_text(
        _(
            "Is this an emergency?\n \n Are you expreincing any of the following?\n \n 1️⃣ Severe, constant chest pain or pressure\n 2️⃣ Extreme difficulty breathing\n 3️⃣ Severe, constant lightheadedness\n 4️⃣ Serious disorientation or unresponsiveness"
        ),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    user_contact = update.message.contact

    USER_INFO.append(user_contact.phone_number)

    return INDICATORS


def emergency(update, context):
    user = update.message.from_user
    USER_INFO.append(update.message.text)
    logger.info("Emergency case of %s: %s", user.first_name, update.message.text)

    # accept location and phone number

    update.message.reply_text(
        _(
            "Dear {} You should call {}.\n \n Based on your reported symptoms, you should seek care immediately\n How to get a care...\n Thank you for participating in this self reporting"
        ).format(user.first_name, ER_NUMBER)
    )

    print(USER_INFO)

    save_response(
        [USER_INFO,]
    )

    USER_INFO.clear()

    return ConversationHandler.END


def age(update, context):
    user = update.message.from_user
    USER_INFO.append(update.message.text)

    reply_keyboard = [[_("Between 18 and 64"), _("64 or older")]]

    update.message.reply_text(
        _("How old are you?\n \n "),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return SYMPTOMS


def symptoms(update, context):
    user = update.message.from_user
    USER_INFO.append(update.message.text)

    reply_keyboard = [[_("None of the above"), _("One or more of the above")]]

    update.message.reply_text(
        _(
            "Are you experiencing any of these symptoms?\n \n 1️⃣ Fever, chills, or sweating\n 2️⃣ Difficulty breathing (not severe)\n 3️⃣ New or worsening cough\n 5️⃣ Sore throat\n 6️⃣ Aching throughout the body\n 7️⃣ Vomiting or diarrhea\n "
        ),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return CONDITIONS


def conditions(update, context):
    user = update.message.from_user
    USER_INFO.append(update.message.text)

    reply_keyboard = [[_("None of the above"), _("One or more of the above")]]

    update.message.reply_text(
        _(
            "Do you have any of these conditions??\n \n 1️⃣ Asthma or chronic lung disease\n 2️⃣ Pregnancy\n 3️⃣ Diabetes with complications\n 4️⃣ Diseases or conditions that make it harder to cough\n 5️⃣ Kidney failure that needs dialysis\n 6️⃣ Cirrhosis or the liver\n 7️⃣ Weakened immune system\n 8️⃣ Congestive heart failure\n 9️⃣ Extreme obesity"
        ),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return TRAVEL_HISTORY


def travel_history(update, context):
    user = update.message.from_user
    USER_INFO.append(update.message.text)

    reply_keyboard = [["1", "2"]]

    update.message.reply_text(
        _(
            "In the last 14 days, have you traveled internationally?\n \n 1️⃣ I have traveled Internationally\n 2️⃣ I have not traveled internationally"
        ),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return EXPOSURE


def exposure(update, context):
    user = update.message.from_user
    USER_INFO.append(update.message.text)

    reply_keyboard = [["1", "2", "3", "4"]]

    update.message.reply_text(
        _(
            "Do you live or work in a care facility??\n \n 1️⃣ I live with someone who has COVID-19\n 2️⃣ I have had close contact with someon who has COVID-19\n 3️⃣ I have been near someone who has COVID-19\n 4️⃣ I have had no exposure"
        ),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return CARE_FACILITY


def care_facility(update, context):
    user = update.message.from_user
    USER_INFO.append(update.message.text)

    reply_keyboard = [["1", "2", "3", "4"]]

    update.message.reply_text(
        _(
            "In the last 14 days, what is your exposure to others who are known to have COVID-19?\n <i>This includes a hospital, emergency room, other medical setting, or long-term facility.</i>\n \n 1️⃣ I live in a long-term care facility\n <i>This includes nursing homes or assisted living.</i>\n 2️⃣ I have worked in a hospital or other care facility in the past 14 days\n <i>This includes volunteering</i>\n 3️⃣ I plan to work in a hospital or other care facility in the next 14 days\n <i>This includes volunteering</i>\n 4️⃣ No, I do not live or work in a care facility"
        ),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return RESULT


def thank_you(update, context):
    user = update.message.from_user
    USER_INFO.append(update.message.text)

    reply_keyboard = [["1", "2", "3", "4"]]

    update.message.reply_text("Thank you ... based on your assessment ...\n ")

    print(USER_INFO)

    save_response(
        [USER_INFO,]
    )

    USER_INFO.clear()

    return ConversationHandler.END


def location(update, context):
    user = update.message.from_user

    location_keyboard = telegram.KeyboardButton(
        text=_("Please Share My Current Location"), request_location=True
    )

    custom_keyboard = [[location_keyboard]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)

    update.message.reply_text(
        _("Welcome\n \n  Intro text"),
        reply_markup=reply_markup,
        parse_mode=telegram.ParseMode.HTML,
    )

    return TEL


def tel(update, context):
    user = update.message.from_user
    user_location = update.message.location

    logger.info(
        "Location of %s: %f / %f",
        user.first_name,
        user_location.latitude,
        user_location.longitude,
    )
    lat_long = str(user_location.latitude) + ", " + str(user_location.longitude)
    # USER_INFO.append(str(user_location.latitude))
    # USER_INFO.append(str(user_location.longitude))
    USER_INFO.append(lat_long)
    USER_INFO.append(user.first_name)
    USER_INFO.append(user.last_name)

    contact_keyboard = telegram.KeyboardButton(
        text=_("Please Share My Contact"), request_contact=True
    )
    custom_keyboard = [[contact_keyboard]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)

    # logger.info("TEL of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        _("We got your location, Thank you. Please provided us with your contact."),
        reply_markup=reply_markup,
        parse_mode=telegram.ParseMode.HTML,
    )

    return START


def skip_location(update, context):
    user = update.message.from_user
    logger.info(_("User %s did not send a location."), user.first_name)
    update.message.reply_text(
        _("You seem a bit paranoid! " "At last, tell me something about yourself.")
    )

    return START


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        _("Bye! I hope you are safe."), reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # read config for telegram TOKEN
    config = configparser.ConfigParser()
    config.read("config.ini")
    updater = Updater(config["TELEGRAM"]["TOKEN"], use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", location)],
        states={
            START: [MessageHandler(Filters.contact, start)],
            INDICATORS: [
                MessageHandler(
                    Filters.regex(_("^(I'm experiencing at least one of these)")),
                    emergency,
                ),
                MessageHandler(Filters.regex(_("^(I do not have any of these)")), age),
            ],
            SYMPTOMS: [
                MessageHandler(
                    Filters.regex(_("^(Between 18 and 64|64 or older)")), symptoms
                )
            ],
            CONDITIONS: [
                MessageHandler(
                    Filters.regex(_("^(None of the above|One or more of the above)")),
                    conditions,
                )
            ],
            TRAVEL_HISTORY: [
                MessageHandler(
                    Filters.regex(_("^(None of the above|One or more of the above)")),
                    travel_history,
                )
            ],
            EXPOSURE: [MessageHandler(Filters.regex("^(1|2)"), exposure)],
            CARE_FACILITY: [MessageHandler(Filters.regex("^(1|2|3|4)"), care_facility)],
            RESULT: [MessageHandler(Filters.regex("^(1|2|3|4)"), thank_you)],
            TEL: [MessageHandler(Filters.location, tel)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
