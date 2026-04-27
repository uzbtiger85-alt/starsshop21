import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import json
import os
from datetime import datetime, timedelta

# --- CONFIG (from environment variables) ---
BOT_TOKEN = os.environ["8627903535:AAELrpmb31tXASbslYEPS7JhD1igKMck1s4"]
ADMIN_ID = int(os.environ["8058955962"])
CHAT_ID = int(os.environ["-1003801760994"])
CARD_NUMBER = os.environ.get("CARD_NUMBER", "5614 6803 7065 8706")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "@WarNexxxx")
SUPPORT_USERNAMES = os.environ.get("SUPPORT_USERNAMES", "WarNexxxx,Sytik11").split(",")
REVIEW_CHANNEL_ID = int(os.environ.get("REVIEW_CHANNEL_ID", "-1003760630548"))

GIFTS_CATALOG = {
    "heart": {"emoji": "💖", "name_uz": "Yurak", "name_ru": "Сердце", "price": 3150},
    "teddy": {"emoji": "🧸", "name_uz": "Oyunchoq", "name_ru": "Плюшевый медведь", "price": 3150},
    "flower": {"emoji": "🌹", "name_uz": "Gul", "name_ru": "Цветок", "price": 5250},
    "gift": {"emoji": "🎁", "name_uz": "Sovga", "name_ru": "Подарок", "price": 5250},
    "bunny": {"emoji": "🐰", "name_uz": "Quyon", "name_ru": "Кролик", "price": 10500},
    "cake": {"emoji": "🎂", "name_uz": "Tort", "name_ru": "Торт", "price": 10500},
    "daisy": {"emoji": "🌸", "name_uz": "Chamaman", "name_ru": "Маргаритка", "price": 10500},
    "rocket": {"emoji": "🚀", "name_uz": "Rakeeta", "name_ru": "Ракета", "price": 10500},
    "bottle": {"emoji": "🍾", "name_uz": "Shampanskoe", "name_ru": "Шампанское", "price": 10500},
    "moai": {"emoji": "🗿", "name_uz": "Moia", "name_ru": "Статуя Моаи", "price": 10500},
    "gem": {"emoji": "💎", "name_uz": "Tosh", "name_ru": "Драгоценный камень", "price": 21000},
    "trophy": {"emoji": "🏆", "name_uz": "Kubok", "name_ru": "Кубок", "price": 21000},
}
# --- NARXLAR ---
STAR_PRICES = {
    50: 10750,
    75: 16125,
    100: 21500,
    150: 32250,
    250: 53750,
    350: 75250,
    500: 107500,
    1000: 215000,
    2000: 430000,
    5000: 1075000,
}

PRICE_PER_STAR = 215

PREMIUM_PRICES = {
    3: 169990,
    6: 229990,
    12: 399990,
}

REFERRAL_REWARD_STARS = 10
WITHDRAW_AMOUNTS = [75, 100, 150, 200]

# Gift options with emoji
GIFTS = {
    "teddy": {"emoji": "🐻", "name_uz": "Mishka", "name_ru": "Мишка", "price": 5000},
    "flower": {"emoji": "🌹", "name_uz": "Gul", "name_ru": "Цветок", "price": 3000},
    "heart": {"emoji": "❤️", "name_uz": "Yurak", "name_ru": "Сердце", "price": 2000},
    "star": {"emoji": "⭐", "name_uz": "Yulduz", "name_ru": "Звезда", "price": 4000},
    "gift": {"emoji": "🎁", "name_uz": "Sovga", "name_ru": "Подарок", "price": 6000},
    "cake": {"emoji": "🎂", "name_uz": "Tort", "name_ru": "Торт", "price": 5500},
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# --- TRANSLATIONS ---
TEXTS = {
    "uz": {
        "welcome": "👋 <b>{name}</b>, Star Shop'ga xush kelibsiz!\n\n⭐ Stars va 💎 Premium eng arzon narxlarda!\n🚀 Qulay menyu orqali buyurtma bering:",
        "choose_lang": "🌐 Пожалуйста, выберите язык / Iltimos, tilni tanlang:",
        "lang_set": "✅ Til o'zbekchaga o'zgartirildi!",
        "main_menu": "🏠 Bosh menyu",
        "buy_stars": "⭐ Yulduz sotib olish",
        "gifts": "🎁 Sovg'alar",
        "buy_premium": "💎 Premium sotib olish",
        "my_orders": "📦 Buyurtmalarim",
        "referrals": "🔗 Referallar",
        "bonuses": "💰 Bonuslar",
        "instructions": "📖 Ko'rsatmalar",
        "contact": "📞 Bog'lanish",
        "settings": "⚙️ Sozlamalar",
        "stars_title": "⭐ <b>Telegram Stars sotib olish</b>\n\nObunani rasmiylashtirish uchun quyidagi variantlardan birini tanlang.",
        "premium_title": "💎 <b>Telegram Premium miqdorini tanlang</b>\n\n<i>Obunani rasmiylashtirish uchun quyidagi variantlardan birini tanlang.</i>",
        "back": "↩️ Orqaga",
        "back_main": "↩️ Bosh menyu",
        "custom_amount": "➕ Boshqa miqdor",
        "recipient_self": "👤 O'zimga",
        "no_orders": "📦 Sizda hali buyurtmalar yo'q.",
        "orders_title": "📦 <b>Sizning buyurtmalaringiz:</b>\n\n",
        "contact_text": "🛠️ <b>Star Shop qo'llab-quvvatlash xizmati</b>\n\n👨‍💼 Qo'llab-quvvatlash:\n@{s1}\n@{s2}\n\n⚡ Odatda juda tez javob beramiz.",
        "contact_btn": "📞 Qo'llab-quvvatlash bilan bog'lanish",
        "settings_text": "⚙️ <b>Sozlamalar</b>\n\n👤 Ism: {name}\n🆔 ID: <code>{uid}</code>\n📝 Username: @{uname}\n🌐 Til: O'zbekcha",
        "change_lang": "🌐 Tilni o'zgartirish",
        "bonus_text": "💰 <b>Bonus balansi</b>\n\n⭐ Stars bonuslari: <b>{stars} Stars</b>\n\nYechish miqdorini tanlang:",
        "bonus_low": "❌ Minimal yechish: 75 Stars. Sizda: {stars} Stars",
        "bonus_withdraw_req": "💰 <b>Bonus Stars yechish</b>\n\nSizda: <b>{stars} ⭐ Stars</b>\nYechish summasi: <b>{amount} ⭐</b>\n\nYechish uchun @{admin} ga murojaat qiling.",
        "ref_text": "🔗 <b>Referal tizimi</b>\n\n👥 Taklif qilingan: <b>{count}</b>\n⭐ Har bir referal uchun: <b>{reward} Stars</b>\n\n🔗 Sizning havolangiz:\n<a href='{link}'>{link}</a>\n\n📋 <b>Qanday ishlaydi:</b>\n1. Havolani do'stlaringizga yuboring\n2. Ular botga kiradi\n3. Birinchi marta Stars sotib olganda\n4. Siz avtomatik <b>{reward} ⭐</b> olasiz\n\n💎 Bonus Stars: <b>{stars} ⭐</b>",
        "share_ref": "📤 Referalni ulashish",
        "withdraw_bonus": "💰 Bonuslarni yechish",
        "no_data": "Hali ma'lumot yo'q.",
        "custom_min": "❌ Minimal miqdor: 50 ⭐",
        "custom_num": "❌ Iltimos, faqat raqam kiriting!",
        "custom_prompt": "✏️ Nechta yulduz sotib olmoqchisiz?\n\nMinimal: 50 ⭐\nRaqamni kiriting:",
        "enter_username_prompt": "⭐️ Yulduzlar: <b>{amount}</b>\n💴 Narx: <b>{price:,} UZS</b>\n\n❗️ Qabul qiluvchining @username kiriting, yoki o'zingiz uchun tugmani bosing",
        "order_confirmation": (
            "🛍 Buyurtmani tasdiqlash\n\n"
            "📦 Xizmat: {service}\n"
            "📥 Miqdor: {amount}\n"
            "👤 Qabul qiluvchi: {recipient}\n\n"
            "💰 To'lov summasi: {price:,} UZS\n"
            "🏦 To'lov rekvizitlari:\n"
            "{card}\n\n"
            "📌 To'lovni amalga oshirgandan so'ng, chekni shu yerga yuboring.\n\n"
            "⏱️ Tasdiqlangandan keyin xizmat 1–3 daqiqa ichida faolashadi."
        ),
        "gift_order_confirmation": (
            "🛍 Buyurtmani tasdiqlash\n\n"
            "🎁 Sovga: {gift_name}\n"
            "👤 Qabul qiluvchi: {recipient}\n\n"
            "💰 To'lov summasi: {price:,} UZS\n"
            "🏦 To'lov rekvizitlari:\n"
            "{card}\n\n"
            "📌 To'lovni amalga oshirgandan so'ng, chekni shu yerga yuboring.\n\n"
            "⏱️ Tasdiqlangandan keyin sovga 1–3 daqiqa ichida yetkaziladi."
        ),
        "receipt_accepted": (
            "✅ Chekingiz qabul qilindi!\n\n"
            "⏳ Hozir admin tomonidan tekshirilmoqda...\n"
            "Faollashtirish 1–3 daqiqa ichida tugallanadi."
        ),
        "prem_enter_username": "💎 Telegram Premium: <b>{months} oylik</b>\n💴 Narx: <b>{price:,} UZS</b>\n\n❗️ Qabul qiluvchining @username kiriting, yoki o'zingiz uchun tugmani bosing:",
        "approved_msg": "✅ <b>Buyurtma #{oid} tasdiqlandi!</b>\n\n{emoji} Xizmat yuborildi. Rahmat! 🙏",
        "rejected_msg": "❌ <b>Buyurtma #{oid} rad etildi.</b>\n\nIltimos, qayta urinib ko'ring yoki @{admin} bilan bog'laning.",
        "referral_joined": "🎉 Yangi referal! <b>{name}</b> sizning havolangiz orqali qo'shildi!\n\nUlar birinchi marta Stars sotib olganda siz <b>{reward} ⭐ Stars</b> olasiz!",
        "referral_reward": "🎉 <b>Referal mukofot!</b>\n\nSizning referal do'stingiz birinchi marta xarid qildi!\n✨ Hisobingizga <b>{reward} ⭐ Stars bonusi</b> qo'shildi!\n\nJami bonus Stars: <b>{total} ⭐</b>",
        "instructions_text": "📖 <b>Star Shop - Qo'llanma</b>\n\n<b>🌟 Stars sotib olish:</b>\n1. \"⭐ Yulduz sotib olish\" bosing\n2. Miqdorni tanlang\n3. Qabul qiluvchini kiriting\n4. To'lov chekini yuboring\n5. Tekshiruvdan o'tgach Stars yuboriladi\n\n<b>💎 Premium sotib olish:</b>\n1. \"💎 Premium sotib olish\" bosing\n2. Muddatni tanlang (3, 6 yoki 12 oy)\n3. Qabul qiluvchini kiriting\n4. To'lov chekini yuboring\n\n<b>🎁 Sovga sotib olish:</b>\n1. \"🎁 Sovg'alar\" bosing\n2. Sovga tanlang\n3. To'lov chekini yuboring\n\n<b>💰 Bonuslar:</b>\n- Do'stlaringizni taklif qiling\n- Ular birinchi xarid qilganda 10 Stars oling\n- Bonuslarni yechish uchun \"💰 Bonuslar\" bosing\n\n<b>💳 To'lov:</b>\n- Karta raqami chekda beriladi\n- Chekni to'lovdan keyin yuboring\n- Admin 1-3 daqiqada tasdiqlaydi\n\n<b>❓ Savollar?</b>\nQo'llab-quvvatlash: @WarNexxxx",
        "gifts_title": "🎁 <b>Sovg'alar katalogi</b>\n\nSotib olmoqchi bo'lgan sovg'ani tanlang:",
        "select_withdrawal": "💰 <b>Yechish miqdorini tanlang:</b>",
        "no_username_error": "❌ Sizning Telegram akkauntda username yo'q. Iltimos, Telegram sozlamalaridan username qo'shing.",
    },
    "ru": {
        "welcome": "👋 <b>{name}</b>, добро пожаловать в Star Shop!\n\n⭐ Stars и 💎 Premium по самым низким ценам!\n🚀 Сделайте заказ через удобное меню:",
        "choose_lang": "🌐 Пожалуйста, выберите язык / Iltimos, tilni tanlang:",
        "lang_set": "✅ Язык изменён на русский!",
        "main_menu": "🏠 Главное меню",
        "buy_stars": "⭐ Купить звёзды",
        "gifts": "🎁 Подарки",
        "buy_premium": "💎 Купить Premium",
        "my_orders": "📦 Мои заказы",
        "referrals": "🔗 Рефералы",
        "bonuses": "💰 Бонусы",
        "instructions": "📖 Инструкция",
        "contact": "📞 Связаться",
        "settings": "⚙️ Настройки",
        "stars_title": "⭐ <b>Купить Telegram Stars</b>\n\nВыберите один из вариантов для оформления подписки.",
        "premium_title": "💎 <b>Выберите срок Telegram Premium</b>\n\n<i>Выберите один из вариантов для оформления подписки.</i>",
        "back": "↩️ Назад",
        "back_main": "↩️ Главное меню",
        "custom_amount": "➕ Другое количество",
        "recipient_self": "👤 Себе",
        "no_orders": "📦 У вас ещё нет заказов.",
        "orders_title": "📦 <b>Ваши заказы:</b>\n\n",
        "contact_text": "🛠️ <b>Служба поддержки Star Shop</b>\n\n👨‍💼 Поддержка:\n@{s1}\n@{s2}\n\n⚡ Обычно отвечаем очень быстро.",
        "contact_btn": "📞 Связаться с поддержкой",
        "settings_text": "⚙️ <b>Настройки</b>\n\n👤 Имя: {name}\n🆔 ID: <code>{uid}</code>\n📝 Username: @{uname}\n🌐 Язык: Русский",
        "change_lang": "🌐 Сменить язык",
        "bonus_text": "💰 <b>Бонусный баланс</b>\n\n⭐ Stars бонусы: <b>{stars} Stars</b>\n\nВыберите сумму для вывода:",
        "bonus_low": "❌ Минимальный вывод: 75 Stars. У вас: {stars} Stars",
        "bonus_withdraw_req": "💰 <b>Вывод бонусных Stars</b>\n\nУ вас: <b>{stars} ⭐ Stars</b>\nСумма вывода: <b>{amount} ⭐</b>\n\nДля вывода обратитесь к @{admin}.",
        "ref_text": "🔗 <b>Реферальная система</b>\n\n👥 Приглашено: <b>{count}</b>\n⭐ За каждого реферала: <b>{reward} Stars</b>\n\n🔗 Ваша ссылка:\n<a href='{link}'>{link}</a>\n\n📋 <b>Как работает:</b>\n1. Отправьте ссылку друзьям\n2. Они заходят через вашу ссылку\n3. При первой покупке Stars\n4. Вы автоматически получаете <b>{reward} ⭐</b>\n\n💎 Бонусные Stars: <b>{stars} ⭐</b>",
        "share_ref": "📤 Поделиться рефералом",
        "withdraw_bonus": "💰 Вывести бонусы",
        "no_data": "Данных пока нет.",
        "custom_min": "❌ Минимальное количество: 50 ⭐",
        "custom_num": "❌ Пожалуйста, введите только цифры!",
        "custom_prompt": "✏️ Сколько звёзд хотите купить?\n\nМинимум: 50 ⭐\nВведите число:",
        "enter_username_prompt": "⭐️ Звезды: <b>{amount}</b>\n💴 Цена: <b>{price:,} UZS</b>\n\n❗️ Введите @username получателя, или нажмите кнопку ниже если для себя",
        "order_confirmation": (
            "🛍 Подтверждение заказа\n\n"
            "📦 Услуга: {service}\n"
            "📥 Количество: {amount}\n"
            "👤 Получатель: {recipient}\n\n"
            "💰 Сумма платежа: {price:,} UZS\n"
            "🏦 Реквизиты платежа:\n"
            "{card}\n\n"
            "📌 После завершения платежа отправьте скриншот чека здесь.\n\n"
            "⏱️ После подтверждения услуга будет активирована в течение 1–3 минут."
        ),
        "gift_order_confirmation": (
            "🛍 Подтверждение заказа\n\n"
            "🎁 Подарок: {gift_name}\n"
            "👤 Получатель: {recipient}\n\n"
            "💰 Сумма платежа: {price:,} UZS\n"
            "🏦 Реквизиты платежа:\n"
            "{card}\n\n"
            "📌 После завершения платежа отправьте скриншот чека здесь.\n\n"
            "⏱️ После подтверждения подарок будет доставлен в течение 1–3 минут."
        ),
        "receipt_accepted": (
            "✅ Ваш чек принят!\n\n"
            "⏳ Сейчас проверяется администратором...\n"
            "Активация будет завершена в течение 1–3 минут."
        ),
        "prem_enter_username": "💎 Telegram Premium: <b>{months} мес.</b>\n💴 Цена: <b>{price:,} UZS</b>\n\n❗️ Введите @username получателя, или нажмите кнопку ниже если для себя:",
        "approved_msg": "✅ <b>Заказ #{oid} подтверждён!</b>\n\n{emoji} Услуга отправлена. Спасибо! 🙏",
        "rejected_msg": "❌ <b>Заказ #{oid} отклонён.</b>\n\nПопробуйте снова или свяжитесь с @{admin}.",
        "referral_joined": "🎉 Новый реферал! <b>{name}</b> присоединился по вашей ссылке!\n\nКогда они купят Stars впервые — вы получите <b>{reward} ⭐ Stars</b>!",
        "referral_reward": "🎉 <b>Реферальный бонус!</b>\n\nВаш реферал впервые сделал покупку!\n✨ На ваш счёт начислено <b>{reward} ⭐ Stars</b>!\n\nВсего бонусных Stars: <b>{total} ⭐</b>",
        "instructions_text": "📖 <b>Star Shop - Инструкция</b>\n\n<b>🌟 Покупка Stars:</b>\n1. Нажмите \"⭐ Купить звёзды\"\n2. Выберите количество\n3. Введите @username получателя\n4. Отправьте скриншот чека\n5. После проверки Stars поступят\n\n<b>💎 Покупка Premium:</b>\n1. Нажмите \"💎 Купить Premium\"\n2. Выберите срок (3, 6 или 12 месяцев)\n3. Введите @username получателя\n4. Отправьте скриншот чека\n\n<b>🎁 Покупка подарка:</b>\n1. Нажмите \"🎁 Подарки\"\n2. Выберите подарок\n3. Отправьте скриншот чека\n\n<b>💰 Бонусы:</b>\n- Приглашайте друзей\n- Получайте 10 Stars за каждого\n- Выводите бонусы через \"💰 Бонусы\"\n\n<b>💳 Платёж:</b>\n- Реквизиты карты указаны в чеке\n- Отправьте скриншот после платежа\n- Администратор подтвердит в течение 1-3 минут\n\n<b>❓ Вопросы?</b>\nПоддержка: @WarNexxxx",
        "gifts_title": "🎁 <b>Каталог подарков</b>\n\nВыберите подарок для покупки:",
        "select_withdrawal": "💰 <b>Выберите сумму вывода:</b>",
        "no_username_error": "❌ Ваш аккаунт Telegram не имеет username. Пожалуйста, добавьте username в настройках Telegram.",
    }
}

def t(lang, key, **kwargs):
    text = TEXTS.get(lang, TEXTS["uz"]).get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except:
            return text
    return text

# --- ORDERS DB ---
ORDERS_FILE = "orders.json"

def load_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_orders(orders):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

def add_order(order: dict):
    orders = load_orders()
    orders.append(order)
    save_orders(orders)
    return len(orders)

def update_order_status(order_id: int, status: str):
    orders = load_orders()
    for o in orders:
        if o.get("id") == order_id:
            o["status"] = status
    save_orders(orders)

# --- USERS DB ---
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def get_or_create_user(user_id: int, username: str, full_name: str):
    users = load_users()
    uid = str(user_id)
    if uid not in users:
        users[uid] = {
            "id": user_id,
            "username": username,
            "full_name": full_name,
            "joined": datetime.now().isoformat(),
            "referrer": None,
            "balance_bonus": 0,
            "bonus_stars": 0,
            "orders_count": 0,
            "has_purchased": False,
            "lang": None,
        }
        save_users(users)
    return users[uid]

def get_user(user_id: int):
    users = load_users()
    return users.get(str(user_id))

def get_user_lang(user_id: int) -> str:
    user = get_user(user_id)
    if user and user.get("lang"):
        return user["lang"]
    return "uz"

def update_user(user_id: int, data: dict):
    users = load_users()
    uid = str(user_id)
    if uid in users:
        users[uid].update(data)
        save_users(users)

def get_referral_count(user_id: int, period: str = "all"):
    users = load_users()
    now = datetime.now()
    result = []
    for u in users.values():
        if str(u.get("referrer")) == str(user_id):
            if period == "all":
                result.append(u)
            else:
                joined = u.get("joined", "")
                try:
                    joined_dt = datetime.fromisoformat(joined)
                    if period == "today" and joined_dt.date() == now.date():
                        result.append(u)
                    elif period == "week" and joined_dt >= now - timedelta(days=7):
                        result.append(u)
                    elif period == "month" and joined_dt >= now - timedelta(days=30):
                        result.append(u)
                except:
                    pass
    return len(result)

# --- FSM STATES ---
class LangState(StatesGroup):
    choosing = State()

class OrderStates(StatesGroup):
    choosing_amount = State()
    entering_custom_amount = State()
    entering_username = State()
    waiting_payment = State()

class PremiumStates(StatesGroup):
    choosing_period = State()
    entering_username = State()
    waiting_payment = State()

class WithdrawState(StatesGroup):
    choosing_amount = State()

class GiftStates(StatesGroup):
    choosing_gift = State()
    choosing_recipient = State()
    waiting_payment = State()

# --- KEYBOARDS ---
def lang_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang_ru"),
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="set_lang_uz"),
        ]
    ])

def main_menu_keyboard(lang="uz"):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang, "buy_stars"))],
            [KeyboardButton(text=t(lang, "gifts")), KeyboardButton(text=t(lang, "buy_premium"))],
            [KeyboardButton(text=t(lang, "my_orders")), KeyboardButton(text=t(lang, "referrals")), KeyboardButton(text=t(lang, "bonuses"))],
            [KeyboardButton(text=t(lang, "instructions")), KeyboardButton(text=t(lang, "contact")), KeyboardButton(text=t(lang, "settings"))],
        ],
        resize_keyboard=True
    )

def star_amounts_keyboard(lang="uz"):
    buttons = []
    items = list(STAR_PRICES.items())
    for i in range(0, len(items), 2):
        row = []
        star1, price1 = items[i]
        row.append(InlineKeyboardButton(text=f"{star1} ⭐ - {price1:,} UZS", callback_data=f"stars_{star1}"))
        if i + 1 < len(items):
            star2, price2 = items[i + 1]
            row.append(InlineKeyboardButton(text=f"{star2} ⭐ - {price2:,} UZS", callback_data=f"stars_{star2}"))
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text=t(lang, "custom_amount"), callback_data="stars_custom")])
    buttons.append([InlineKeyboardButton(text=t(lang, "back_main"), callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def premium_keyboard(lang="uz"):
    buttons = []
    for months, price in PREMIUM_PRICES.items():
        label = f"{months} oy" if lang == "uz" else f"{months} мес."
        buttons.append([InlineKeyboardButton(text=f"{label} 💎 - {price:,} UZS", callback_data=f"premium_{months}")])
    buttons.append([InlineKeyboardButton(text=t(lang, "back_main"), callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def gifts_keyboard(lang="uz"):
    buttons = []
    gift_items = list(GIFTS.items())
    for i in range(0, len(gift_items), 2):
        row = []
        key1, gift1 = gift_items[i]
        emoji1 = gift1["emoji"]
        name1 = gift1.get("name_uz" if lang == "uz" else "name_ru", gift1.get("name_uz", "Gift"))
        price1 = gift1.get("price", 0)
        row.append(InlineKeyboardButton(text=f"{emoji1} {name1} - {price1:,}", callback_data=f"gift_{key1}"))
        if i + 1 < len(gift_items):
            key2, gift2 = gift_items[i + 1]
            emoji2 = gift2["emoji"]
            name2 = gift2.get("name_uz" if lang == "uz" else "name_ru", gift2.get("name_uz", "Gift"))
            price2 = gift2.get("price", 0)
            row.append(InlineKeyboardButton(text=f"{emoji2} {name2} - {price2:,}", callback_data=f"gift_{key2}"))
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text=t(lang, "back_main"), callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def recipient_keyboard(lang="uz"):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "recipient_self"), callback_data="recipient_self")],
        [InlineKeyboardButton(text=t(lang, "back_main"), callback_data="back_main")],
    ])

def premium_recipient_keyboard(lang="uz"):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "recipient_self"), callback_data="prem_recipient_self")],
        [InlineKeyboardButton(text=t(lang, "back_main"), callback_data="back_main")],
    ])

def gift_recipient_keyboard(lang="uz"):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "recipient_self"), callback_data="gift_recipient_self")],
        [InlineKeyboardButton(text=t(lang, "back_main"), callback_data="back_main")],
    ])

def admin_order_keyboard(order_id: int, user_id: int, order_type: str = "stars"):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Начать выполнение", callback_data=f"admin_start_{order_id}_{user_id}_{order_type}")],
        [
            InlineKeyboardButton(text="✅ Выполнить", callback_data=f"admin_confirm_{order_id}_{user_id}_{order_type}"),
            InlineKeyboardButton(text="❌ Отменить", callback_data=f"admin_cancel_{order_id}_{user_id}_{order_type}"),
        ]
    ])

def withdrawal_keyboard(lang="uz"):
    buttons = []
    for amount in WITHDRAW_AMOUNTS:
        buttons.append(InlineKeyboardButton(text=f"{amount} ⭐", callback_data=f"withdraw_{amount}"))
    rows = []
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            rows.append([buttons[i], buttons[i + 1]])
        else:
            rows.append([buttons[i]])
    rows.append([InlineKeyboardButton(text=t(lang, "back_main"), callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def referral_keyboard(ref_link: str, lang="uz"):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "share_ref"), url=f"https://t.me/share/url?url={ref_link}&text=Star%20Shop%20orqali%20arzon%20narxda%20Stars%20va%20Premium%20sotib%20oling!")],
        [InlineKeyboardButton(text=t(lang, "withdraw_bonus"), callback_data="withdraw_bonus")],
    ])

def contact_keyboard(lang="uz"):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "contact_btn"), url=f"https://t.me/{SUPPORT_USERNAMES[0]}")],
    ])

# --- HANDLERS ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    user = get_or_create_user(
        message.from_user.id,
        message.from_user.username or "",
        message.from_user.full_name
    )
    args = message.text.split()
    if len(args) > 1:
        ref_param = args[1]
        ref_id = ref_param.replace("ref_", "") if ref_param.startswith("ref_") else ref_param
        if ref_id.isdigit() and ref_id != str(message.from_user.id) and not user.get("referrer"):
            update_user(message.from_user.id, {"referrer": ref_id})
            ref_lang = get_user_lang(int(ref_id))
            try:
                await bot.send_message(int(ref_id), t(ref_lang, "referral_joined", name=message.from_user.full_name, reward=REFERRAL_REWARD_STARS), parse_mode="HTML")
            except:
                pass
    if not user.get("lang"):
        await state.update_data(pending_start=True)
        await message.answer(t("uz", "choose_lang"), reply_markup=lang_keyboard())
        return
    lang = user.get("lang", "uz")
    await message.answer(t(lang, "welcome", name=message.from_user.full_name), reply_markup=main_menu_keyboard(lang), parse_mode="HTML")

@dp.callback_query(F.data.startswith("set_lang_"))
async def set_language(callback: types.CallbackQuery, state: FSMContext):
    lang = callback.data.replace("set_lang_", "")
    update_user(callback.from_user.id, {"lang": lang})
    await callback.message.delete()
    await callback.answer(t(lang, "lang_set"))
    await callback.message.answer(t(lang, "welcome", name=callback.from_user.full_name), reply_markup=main_menu_keyboard(lang), parse_mode="HTML")

@dp.message(F.text.in_(["⭐ Yulduz sotib olish", "⭐ Купить звёзды"]))
async def buy_stars(message: types.Message, state: FSMContext):
    lang = get_user_lang(message.from_user.id)
    await state.set_state(OrderStates.choosing_amount)
    await message.answer(t(lang, "stars_title"), reply_markup=star_amounts_keyboard(lang), parse_mode="HTML")

@dp.callback_query(F.data.startswith("stars_"))
async def select_stars(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_lang(callback.from_user.id)
    data = callback.data.replace("stars_", "")
    if data == "custom":
        await state.set_state(OrderStates.entering_custom_amount)
        await callback.message.edit_text(t(lang, "custom_prompt"), reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=t(lang, "back_main"), callback_data="back_main")]]))
    else:
        amount = int(data)
        price = STAR_PRICES.get(amount, amount * PRICE_PER_STAR)
        await state.update_data(stars=amount, price=price)
        await state.set_state(OrderStates.entering_username)
        await callback.message.edit_text(t(lang, "enter_username_prompt", amount=amount, price=price), reply_markup=recipient_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@dp.message(OrderStates.entering_custom_amount)
async def enter_custom_amount(message: types.Message, state: FSMContext):
    lang = get_user_lang(message.from_user.id)
    try:
        amount = int(message.text.strip())
        if amount < 50:
            await message.answer(t(lang, "custom_min"))
            return
        price = amount * PRICE_PER_STAR
        await state.update_data(stars=amount, price=price)
        await state.set_state(OrderStates.entering_username)
        await message.answer(t(lang, "enter_username_prompt", amount=amount, price=price), reply_markup=recipient_keyboard(lang), parse_mode="HTML")
    except ValueError:
        await message.answer(t(lang, "custom_num"))

@dp.callback_query(F.data == "recipient_self", OrderStates.entering_username)
async def recipient_self(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_lang(callback.from_user.id)
    if not callback.from_user.username:
        await callback.answer(t(lang, "no_username_error"), show_alert=True)
        return
    data = await state.get_data()
    if not data.get("stars") or not data.get("price"):
        await callback.answer("❌ Xatolik: Iltimos qaytadan urinib ko'ring.", show_alert=True)
        await state.clear()
        return
    username = f"@{callback.from_user.username}"
    await state.update_data(recipient=username)
    data = await state.get_data()
    await process_stars_order(callback, data, lang, state, callback.from_user.id, callback.from_user)
    await callback.answer()

@dp.message(OrderStates.entering_username)
async def enter_username(message: types.Message, state: FSMContext):
    lang = get_user_lang(message.from_user.id)
    username = message.text.strip()
    if not username.startswith("@"):
        username = "@" + username
    await state.update_data(recipient=username)
    data = await state.get_data()
    await process_stars_order(message, data, lang, state, message.from_user.id, message.from_user)

async def process_stars_order(msg, data: dict, lang: str, state: FSMContext, user_id: int, from_user: types.User):
    amount = data.get("stars", "?")
    price = data.get("price", 0)
    recipient = data.get("recipient", "?")
    order = {
        "id": None, "type": "stars", "user_id": user_id,
        "username": from_user.username or from_user.full_name,
        "stars": data["stars"], "price": data["price"],
        "recipient": data["recipient"], "status": "pending",
        "created_at": datetime.now().isoformat(),
    }
    order_id = add_order(order)
    order["id"] = order_id
    _dt = datetime.fromisoformat(order['created_at'])
    order_text = (
        f"🆕 <b>Новый заказ</b>\n\n🆔 Order ID: <b>{order_id}</b>\n"
        f"👤 Пользователь: @{order['username']}\n🆔 User ID: <code>{order['user_id']}</code>\n\n"
        f"🎁 Услуга: <b>Telegram Stars</b>\n📦 Количество: <b>{order['stars']}</b>\n"
        f"💰 Сумма: <b>{order['price']:,} UZS</b>\n🎯 Получатель: <b>{order['recipient']}</b>\n\n"
        f"📅 Дата: <b>{_dt.strftime('%Y-%m-%d')}</b>\n⏰ Время: <b>{_dt.strftime('%H:%M:%S')}</b>"
    )
    try:
        await bot.send_message(CHAT_ID, order_text, reply_markup=admin_order_keyboard(order_id, user_id, "stars"), parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error sending to chat: {e}")
    confirmation_text = t(lang, "order_confirmation", service="Telegram Stars ⭐️", amount=f"{amount} ⭐️", recipient=recipient, price=price, card=CARD_NUMBER)
    await state.set_state(OrderStates.waiting_payment)
    await state.update_data(order_id=order_id)
    if isinstance(msg, types.CallbackQuery):
        try:
            await msg.message.edit_text(confirmation_text, parse_mode="HTML")
        except:
            await msg.message.answer(confirmation_text, parse_mode="HTML")
    else:
        await msg.answer(confirmation_text, parse_mode="HTML")

@dp.message(OrderStates.waiting_payment, F.photo | F.document)
async def receive_stars_payment_proof(message: types.Message, state: FSMContext):
    lang = get_user_lang(message.from_user.id)
    data = await state.get_data()
    order_id = data.get("order_id", "?")
    chek_caption = (f"📸 <b>Чек для заказа #{order_id}</b>\n👤 Пользователь: @{message.from_user.username or message.from_user.full_name}\n🆔 ID: <code>{message.from_user.id}</code>")
    try:
        await bot.forward_message(CHAT_ID, message.chat.id, message.message_id)
        await bot.send_message(CHAT_ID, chek_caption, reply_markup=admin_order_keyboard(order_id, message.from_user.id, "stars"), parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error sending to chat: {e}")
    await message.answer(t(lang, "receipt_accepted"))
    new_order_text = ("🆕 <b>Yangi zakaz!</b>\n\nSiz yangi buyurtma berdingiz.\nAdmin tekshirishi tugagach, xizmat yetkaziladi. ✅" if lang == "uz" else "🆕 <b>Новый заказ!</b>\n\nВы оформили новый заказ.\nПосле проверки администратором услуга будет доставлена. ✅")
    await message.answer(new_order_text, parse_mode="HTML", reply_markup=main_menu_keyboard(lang))
    await state.clear()

@dp.message(F.text.in_(["💎 Premium sotib olish", "💎 Купить Premium"]))
async def buy_premium(message: types.Message, state: FSMContext):
    lang = get_user_lang(message.from_user.id)
    await state.set_state(PremiumStates.choosing_period)
    await message.answer(t(lang, "premium_title"), reply_markup=premium_keyboard(lang), parse_mode="HTML")

@dp.callback_query(F.data.startswith("premium_"))
async def select_premium(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_lang(callback.from_user.id)
    months = int(callback.data.replace("premium_", ""))
    price = PREMIUM_PRICES.get(months)
    await state.update_data(months=months, price=price)
    await state.set_state(PremiumStates.entering_username)
    await callback.message.edit_text(t(lang, "prem_enter_username", months=months, price=price), reply_markup=premium_recipient_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "prem_recipient_self", PremiumStates.entering_username)
async def prem_recipient_self(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_lang(callback.from_user.id)
    if not callback.from_user.username:
        await callback.answer(t(lang, "no_username_error"), show_alert=True)
        return
    data = await state.get_data()
    if not data.get("months") or not data.get("price"):
        await callback.answer("❌ Xatolik: Iltimos qaytadan urinib ko'ring.", show_alert=True)
        await state.clear()
        return
    username = f"@{callback.from_user.username}"
    await state.update_data(recipient=username)
    data = await state.get_data()
    await process_premium_order(callback, data, lang, state, callback.from_user.id, callback.from_user)
    await callback.answer()

@dp.message(PremiumStates.entering_username)
async def enter_premium_username(message: types.Message, state: FSMContext):
    lang = get_user_lang(message.from_user.id)
    username = message.text.strip()
    if not username.startswith("@"):
        username = "@" + username
    await state.update_data(recipient=username)
    data = await state.get_data()
    await process_premium_order(message, data, lang, state, message.from_user.id, message.from_user)

async def process_premium_order(msg, data: dict, lang: str, state: FSMContext, user_id: int, from_user: types.User):
    months = data.get("months", "?")
    price = data.get("price", 0)
    recipient = data.get("recipient", "?")
    order = {
        "id": None, "type": "premium", "user_id": user_id,
        "username": from_user.username or from_user.full_name,
        "months": data["months"], "price": data["price"],
        "recipient": data["recipient"], "status": "pending",
        "created_at": datetime.now().isoformat(),
    }
    order_id = add_order(order)
    order["id"] = order_id
    _dt2 = datetime.fromisoformat(order['created_at'])
    order_text = (
        f"🆕 <b>Новый заказ</b>\n\n🆔 Order ID: <b>{order_id}</b>\n"
        f"👤 Пользователь: @{order['username']}\n🆔 User ID: <code>{order['user_id']}</code>\n\n"
        f"🎁 Услуга: <b>Telegram Premium</b>\n📦 Количество: <b>{order['months']} oy</b>\n"
        f"💰 Сумма: <b>{order['price']:,} UZS</b>\n🎯 Получатель: <b>{order['recipient']}</b>\n\n"
        f"📅 Дата: <b>{_dt2.strftime('%Y-%m-%d')}</b>\n⏰ Время: <b>{_dt2.strftime('%H:%M:%S')}</b>"
    )
    try:
        await bot.send_message(CHAT_ID, order_text, reply_markup=admin_order_keyboard(order_id, user_id, "premium"), parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error sending to chat: {e}")
    label = "oylik" if lang == "uz" else "мес."
    confirmation_text = t(lang, "order_confirmation", service="Telegram Premium 💎", amount=f"{months} {label}", recipient=recipient, price=price, card=CARD_NUMBER)
    await state.set_state(PremiumStates.waiting_payment)
    await state.update_data(order_id=order_id)
    if isinstance(msg, types.CallbackQuery):
        try:
            await msg.message.edit_text(confirmation_text, parse_mode="HTML")
        except:
            await msg.message.answer(confirmation_text, parse_mode="HTML")
    else:
        await msg.answer(confirmation_text, parse_mode="HTML")

@dp.message(PremiumStates.waiting_payment, F.photo | F.document)
async def receive_premium_payment_proof(message: types.Message, state: FSMContext):
    lang = get_user_lang(message.from_user.id)
    data = await state.get_data()
    order_id = data.get("order_id", "?")
    chek_caption = (f"📸 <b>Чек для заказа #{order_id}</b> (💎 Premium)\n👤 Пользователь: @{message.from_user.username or message.from_user.full_name}\n🆔 ID: <code>{message.from_user.id}</code>")
    try:
        await bot.forward_message(CHAT_ID, message.chat.id, message.message_id)
        await bot.send_message(CHAT_ID, chek_caption, reply_markup=admin_order_keyboard(order_id, message.from_user.id, "premium"), parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error sending to chat: {e}")
    await message.answer(t(lang, "receipt_accepted"))
    new_order_text = ("🆕 <b>Yangi zakaz!</b>\n\nSiz yangi buyurtma berdingiz.\nAdmin tekshirishi tugagach, xizmat yetkaziladi. ✅" if lang == "uz" else "🆕 <b>Новый заказ!</b>\n\nВы оформили новый заказ.\nПосле проверки администратором услуга будет доставлена. ✅")
    await message.answer(new_order_text, parse_mode="HTML", reply_markup=main_menu_keyboard(lang))
    await state.clear()

@dp.message(F.text.in_(["🎁 Sovg'alar", "🎁 Подарки"]))
async def buy_gifts(message: types.Message, state: FSMContext):
    lang = get_user_lang(message.from_user.id)
    await state.set_state(GiftStates.choosing_gift)
    await message.answer(t(lang, "gifts_title"), reply_markup=gifts_keyboard(lang), parse_mode="HTML")

@dp.callback_query(F.data.startswith("gift_"))
async def select_gift(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_lang(callback.from_user.id)
    gift_key = callback.data.replace("gift_", "")
    if gift_key not in GIFTS:
        await callback.answer("❌ Invalid gift")
        return
    gift = GIFTS[gift_key]
    price = gift["price"]
    gift_name = gift.get("name_uz" if lang == "uz" else "name_ru", gift.get("name_uz", "Gift"))
    await state.update_data(gift_key=gift_key, price=price, gift_name=gift_name, gift_emoji=gift["emoji"])
    await state.set_state(GiftStates.choosing_recipient)
    gift_display = f"{gift['emoji']} {gift_name}"
    price_text = (f"💝 <b>{gift_display}</b>\n💴 Narx: <b>{price:,} UZS</b>\n\n❗️ Qabul qiluvchining @username kiriting, yoki o'zingiz uchun tugmani bosing:" if lang == "uz" else f"💝 <b>{gift_display}</b>\n💴 Цена: <b>{price:,} UZS</b>\n\n❗️ Введите @username получателя, или нажмите кнопку ниже если для себя:")
    await callback.message.edit_text(price_text, reply_markup=gift_recipient_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "gift_recipient_self", GiftStates.choosing_recipient)
async def gift_recipient_self(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_lang(callback.from_user.id)
    if not callback.from_user.username:
        await callback.answer(t(lang, "no_username_error"), show_alert=True)
        return
    data = await state.get_data()
    if not data.get("gift_key") or not data.get("price"):
        await callback.answer("❌ Xatolik: Iltimos qaytadan urinib ko'ring.", show_alert=True)
        await state.clear()
        return
    username = f"@{callback.from_user.username}"
    await state.update_data(recipient=username)
    data = await state.get_data()
    await process_gift_order(callback, data, lang, state, callback.from_user.id, callback.from_user)
    await callback.answer()

@dp.message(GiftStates.choosing_recipient)
async def enter_gift_username(message: types.Message, state: FSMContext):
    lang = get_user_lang(message.from_user.id)
    username = message.text.strip()
    if not username.startswith("@"):
        username = "@" + username
    await state.update_data(recipient=username)
    data = await state.get_data()
    await process_gift_order(message, data, lang, state, message.from_user.id, message.from_user)

async def process_gift_order(msg, data: dict, lang: str, state: FSMContext, user_id: int, from_user: types.User):
    gift_emoji = data.get("gift_emoji", "🎁")
    gift_name = data.get("gift_name", "Gift")
    price = data.get("price", 0)
    recipient = data.get("recipient", "?")
    order = {
        "id": None, "type": "gift", "user_id": user_id,
        "username": from_user.username or from_user.full_name,
        "gift_name": gift_name, "gift_emoji": gift_emoji,
        "price": price, "recipient": recipient, "status": "pending",
        "created_at": datetime.now().isoformat(),
    }
    order_id = add_order(order)
    order["id"] = order_id
    _dt3 = datetime.fromisoformat(order['created_at'])
    order_text = (
        f"🆕 <b>Новый заказ</b>\n\n🆔 Order ID: <b>{order_id}</b>\n"
        f"👤 Пользователь: @{order['username']}\n🆔 User ID: <code>{order['user_id']}</code>\n\n"
        f"🎁 Услуга: <b>Sovga</b>\n📦 Количество: <b>{order['gift_emoji']} {order['gift_name']}</b>\n"
        f"💰 Сумма: <b>{order['price']:,} UZS</b>\n🎯 Получатель: <b>{order['recipient']}</b>\n\n"
        f"📅 Дата: <b>{_dt3.strftime('%Y-%m-%d')}</b>\n⏰ Время: <b>{_dt3.strftime('%H:%M:%S')}</b>"
    )
    try:
        await bot.send_message(CHAT_ID, order_text, reply_markup=admin_order_keyboard(order_id, user_id, "gift"), parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error sending to chat: {e}")
    confirmation_text = t(lang, "gift_order_confirmation", gift_name=gift_name, recipient=recipient, price=price, card=CARD_NUMBER)
    await state.set_state(GiftStates.waiting_payment)
    await state.update_data(order_id=order_id)
    if isinstance(msg, types.CallbackQuery):
        try:
            await msg.message.edit_text(confirmation_text, parse_mode="HTML")
        except:
            await msg.message.answer(confirmation_text, parse_mode="HTML")
    else:
        await msg.answer(confirmation_text, parse_mode="HTML")

@dp.message(GiftStates.waiting_payment, F.photo | F.document)
async def receive_gift_payment_proof(message: types.Message, state: FSMContext):
    lang = get_user_lang(message.from_user.id)
    data = await state.get_data()
    order_id = data.get("order_id", "?")
    chek_caption = (f"📸 <b>Чек для заказа #{order_id}</b> (🎁 Подарок)\n👤 Пользователь: @{message.from_user.username or message.from_user.full_name}\n🆔 ID: <code>{message.from_user.id}</code>")
    try:
        await bot.forward_message(CHAT_ID, message.chat.id, message.message_id)
        await bot.send_message(CHAT_ID, chek_caption, reply_markup=admin_order_keyboard(order_id, message.from_user.id, "gift"), parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error sending to chat: {e}")
    await message.answer(t(lang, "receipt_accepted"))
    new_order_text = ("🆕 <b>Yangi zakaz!</b>\n\nSiz yangi buyurtma berdingiz.\nAdmin tekshirishi tugagach, xizmat yetkaziladi. ✅" if lang == "uz" else "🆕 <b>Новый заказ!</b>\n\nВы оформили новый заказ.\nПосле проверки администратором услуга будет доставлена. ✅")
    await message.answer(new_order_text, parse_mode="HTML", reply_markup=main_menu_keyboard(lang))
    await state.clear()

@dp.callback_query(F.data.startswith("admin_confirm_"))
async def admin_confirm(callback: types.CallbackQuery):
    user_id_check = callback.from_user.id
    username_check = (callback.from_user.username or "").lower()
    is_support = username_check in [u.lower() for u in SUPPORT_USERNAMES]
    if user_id_check != ADMIN_ID and not is_support:
        await callback.answer("❌ Доступ запрещён!")
        return
    parts = callback.data.split("_")
    order_id = int(parts[2])
    user_id = int(parts[3])
    order_type = parts[4] if len(parts) > 4 else "stars"
    update_order_status(order_id, "approved")
    user = get_user(user_id)
    user_lang = get_user_lang(user_id)
    if user and not user.get("has_purchased") and user.get("referrer"):
        ref_id = user.get("referrer")
        ref_user = get_user(int(ref_id))
        if ref_user:
            new_stars = ref_user.get("bonus_stars", 0) + REFERRAL_REWARD_STARS
            update_user(int(ref_id), {"bonus_stars": new_stars})
            ref_lang = get_user_lang(int(ref_id))
            try:
                await bot.send_message(int(ref_id), t(ref_lang, "referral_reward", reward=REFERRAL_REWARD_STARS, total=new_stars), parse_mode="HTML")
            except:
                pass
        update_user(user_id, {"has_purchased": True})
    emoji = "⭐" if order_type == "stars" else ("💎" if order_type == "premium" else "🎁")
    await bot.send_message(user_id, t(user_lang, "approved_msg", oid=order_id, emoji=emoji), parse_mode="HTML")
    if REVIEW_CHANNEL_ID != 0:
        orders = load_orders()
        order = next((o for o in orders if o.get("id") == order_id), None)
        if order:
            if order_type == "stars":
                service_text = f"⭐ {order.get('stars', '?')} Stars"
            elif order_type == "premium":
                service_text = f"💎 Premium {order.get('months', '?')} oy"
            else:
                service_text = f"🎁 {order.get('gift_emoji', '🎁')} {order.get('gift_name', 'Sovga')}"
            review_text = (f"✅ <b>Yangi muvaffaqiyatli xarid!</b>\n\n📦 Xizmat: <b>{service_text}</b>\n👤 Mijoz: @{order.get('username', '?')}\n📥 Qabul qiluvchi: <b>{order.get('recipient', '?')}</b>\n💰 Summa: <b>{order.get('price', 0):,} UZS</b>\n\n⭐ <b>Star Shop</b> dan mamnun mijoz!\n👉 @starshopuzb_bot")
            try:
                await bot.send_message(REVIEW_CHANNEL_ID, review_text, parse_mode="HTML")
            except Exception as e:
                logger.error(f"Error sending to review channel: {e}")
    try:
        await callback.message.edit_text(callback.message.text + "\n\n✅ <b>ПОДТВЕРЖДЕНО</b>", parse_mode="HTML")
    except:
        pass
    await callback.answer("✅ Заказ подтверждён!")

@dp.callback_query(F.data.startswith("admin_cancel_"))
async def admin_cancel(callback: types.CallbackQuery):
    user_id_check = callback.from_user.id
    username_check = (callback.from_user.username or "").lower()
    is_support = username_check in [u.lower() for u in SUPPORT_USERNAMES]
    if user_id_check != ADMIN_ID and not is_support:
        await callback.answer("❌ Доступ запрещён!")
        return
    parts = callback.data.split("_")
    order_id = int(parts[2])
    user_id = int(parts[3])
    update_order_status(order_id, "cancelled")
    user_lang = get_user_lang(user_id)
    await bot.send_message(user_id, t(user_lang, "rejected_msg", oid=order_id, admin=ADMIN_USERNAME.lstrip("@")), parse_mode="HTML")
    try:
        await callback.message.edit_text(callback.message.text + "\n\n❌ <b>ОТМЕНЕНО</b>", parse_mode="HTML")
    except:
        pass
    await callback.answer("❌ Заказ отменён!")

@dp.message(F.text.in_(["📦 Buyurtmalarim", "📦 Мои заказы"]))
async def my_orders(message: types.Message):
    lang = get_user_lang(message.from_user.id)
    orders = load_orders()
    user_orders = [o for o in orders if o.get("user_id") == message.from_user.id]
    if not user_orders:
        await message.answer(t(lang, "no_orders"))
        return
    text = t(lang, "orders_title")
    for o in user_orders[-10:][::-1]:
        status_emoji = {"pending": "⏳", "approved": "✅", "cancelled": "❌", "rejected": "❌"}.get(o.get("status", ""), "❓")
        if o.get("type") == "premium":
            label = "oylik" if lang == "uz" else "мес."
            detail = f"{o.get('months')} {label} 💎 → {o.get('recipient')}"
        elif o.get("type") == "gift":
            detail = f"{o.get('gift_emoji', '🎁')} {o.get('gift_name', 'Gift')} → {o.get('recipient')}"
        else:
            detail = f"{o.get('stars', '?')} ⭐ → {o.get('recipient')}"
        text += f"#{o.get('id', '?')} {status_emoji} | {detail}\n💰 {o.get('price', 0):,} UZS | {o.get('created_at', '')[:10]}\n\n"
    await message.answer(text, parse_mode="HTML")

@dp.message(F.text.in_(["🔗 Referallar", "🔗 Рефералы"]))
async def referrals(message: types.Message):
    lang = get_user_lang(message.from_user.id)
    bot_info = await bot.get_me()
    ref_link = f"https://t.me/{bot_info.username}?start={message.from_user.id}"
    ref_count = get_referral_count(message.from_user.id)
    user = get_user(message.from_user.id)
    bonus_stars = user.get("bonus_stars", 0) if user else 0
    await message.answer(t(lang, "ref_text", count=ref_count, reward=REFERRAL_REWARD_STARS, link=ref_link, stars=bonus_stars), reply_markup=referral_keyboard(ref_link, lang), parse_mode="HTML", disable_web_page_preview=True)

@dp.callback_query(F.data == "withdraw_bonus")
async def withdraw_bonus(callback: types.CallbackQuery):
    lang = get_user_lang(callback.from_user.id)
    user = get_user(callback.from_user.id)
    bonus_stars = user.get("bonus_stars", 0) if user else 0
    if bonus_stars < 75:
        await callback.answer(t(lang, "bonus_low", stars=bonus_stars), show_alert=True)
        return
    await callback.message.answer(t(lang, "select_withdrawal"), reply_markup=withdrawal_keyboard(lang), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data.startswith("withdraw_"))
async def process_withdraw(callback: types.CallbackQuery):
    lang = get_user_lang(callback.from_user.id)
    amount_str = callback.data.replace("withdraw_", "")
    try:
        amount = int(amount_str)
    except:
        await callback.answer()
        return
    user = get_user(callback.from_user.id)
    bonus_stars = user.get("bonus_stars", 0) if user else 0
    await callback.message.edit_text(t(lang, "bonus_withdraw_req", stars=bonus_stars, amount=amount, admin=ADMIN_USERNAME.lstrip("@")), parse_mode="HTML")
    await callback.answer()

@dp.message(F.text.in_(["💰 Bonuslar", "💰 Бонусы"]))
async def bonuses(message: types.Message):
    lang = get_user_lang(message.from_user.id)
    user = get_user(message.from_user.id)
    bonus_stars = user.get("bonus_stars", 0) if user else 0
    await message.answer(t(lang, "bonus_text", stars=bonus_stars), reply_markup=withdrawal_keyboard(lang), parse_mode="HTML")

@dp.message(F.text.in_(["📖 Ko'rsatmalar", "📖 Инструкция"]))
async def instructions(message: types.Message):
    lang = get_user_lang(message.from_user.id)
    await message.answer(t(lang, "instructions_text"), reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=t(lang, "back_main"), callback_data="back_main")]]), parse_mode="HTML")

@dp.message(F.text.in_(["📞 Bog'lanish", "📞 Связаться"]))
async def contact(message: types.Message):
    lang = get_user_lang(message.from_user.id)
    s1 = SUPPORT_USERNAMES[0]
    s2 = SUPPORT_USERNAMES[1]
    await message.answer(t(lang, "contact_text", s1=s1, s2=s2), reply_markup=contact_keyboard(lang), parse_mode="HTML")

@dp.message(F.text.in_(["⚙️ Sozlamalar", "⚙️ Настройки"]))
async def settings(message: types.Message):
    lang = get_user_lang(message.from_user.id)
    uname = message.from_user.username or ("yo`q" if lang == "uz" else "нет")
    await message.answer(t(lang, "settings_text", name=message.from_user.full_name, uid=message.from_user.id, uname=uname), reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=t(lang, "change_lang"), callback_data="change_lang")]]), parse_mode="HTML")

@dp.callback_query(F.data == "change_lang")
async def change_lang(callback: types.CallbackQuery):
    await callback.message.answer(t("uz", "choose_lang"), reply_markup=lang_keyboard())
    await callback.answer()

@dp.callback_query(F.data == "back_main")
async def back_main(callback: types.CallbackQuery, state: FSMContext):
    lang = get_user_lang(callback.from_user.id)
    await state.clear()
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer(t(lang, "main_menu"), reply_markup=main_menu_keyboard(lang))
    await callback.answer()

@dp.callback_query(F.data.startswith("admin_start_"))
async def admin_start_order(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Ruxsat yo'q!", show_alert=True)
        return
    parts = callback.data.split("_")
    order_id = int(parts[2])
    await callback.answer(f"🚀 Zakaz #{order_id} bajarilmoqda...", show_alert=True)
    try:
        await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"⏳ Bajarilmoqda... #{order_id}", callback_data="noop")],
            [
                InlineKeyboardButton(text="✅ Выполнить", callback_data=f"admin_confirm_{'_'.join(parts[2:])}"),
                InlineKeyboardButton(text="❌ Отменить", callback_data=f"admin_cancel_{'_'.join(parts[2:])}"),
            ]
        ]))
    except:
        pass

@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    orders = load_orders()
    users = load_users()
    pending = [o for o in orders if o.get("status") == "pending"]
    approved = [o for o in orders if o.get("status") == "approved"]
    total_revenue = sum(o.get("price", 0) for o in approved)
    await message.answer(f"🔧 <b>Admin Panel</b>\n\n👥 Users: <b>{len(users)}</b>\n📦 Total Orders: <b>{len(orders)}</b>\n⏳ Pending: <b>{len(pending)}</b>\n✅ Approved: <b>{len(approved)}</b>\n💰 Total Revenue: <b>{total_revenue:,} UZS</b>", parse_mode="HTML")

@dp.message(Command("stats"))
async def stats(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    orders = load_orders()
    users = load_users()
    total_revenue = sum(o.get("price", 0) for o in orders if o.get("status") == "approved")
    stars_orders = [o for o in orders if o.get("type") == "stars"]
    premium_orders = [o for o in orders if o.get("type") == "premium"]
    gift_orders = [o for o in orders if o.get("type") == "gift"]
    await message.answer(
        f"📊 <b>Detailed Statistics</b>\n\n👥 Users: <b>{len(users)}</b>\n📦 Total Orders: <b>{len(orders)}</b>\n"
        f"  ⭐ Stars: <b>{len(stars_orders)}</b>\n  💎 Premium: <b>{len(premium_orders)}</b>\n  🎁 Gifts: <b>{len(gift_orders)}</b>\n\n"
        f"✅ Approved: <b>{len([o for o in orders if o.get('status') == 'approved'])}</b>\n"
        f"❌ Rejected: <b>{len([o for o in orders if o.get('status') in ['rejected', 'cancelled']])}</b>\n"
        f"⏳ Pending: <b>{len([o for o in orders if o.get('status') == 'pending'])}</b>\n\n"
        f"💰 Total Revenue: <b>{total_revenue:,} UZS</b>", parse_mode="HTML")

async def main():
    logger.info("Bot starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
