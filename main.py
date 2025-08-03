import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile
)
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from datetime import datetime
import os

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("user_activity.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Токен бота (берётся из переменной окружения)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Инициализация бота
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# 🔐 Укажите ваш Telegram ID, чтобы получать уведомления
OWNER_ID = 1290042252  # ← Ваш ID (из @userinfobot)

# Функция для логирования и отправки уведомления владельцу
async def log_and_notify(user: types.User, action: str):
    try:
        user_info = f"ID: {user.id}, Username: @{user.username if user.username else 'нет'}, Name: {user.full_name}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {user_info} - {action}"
        
        # Логируем в файл
        with open("user_activity.log", "a", encoding="utf-8") as f:
            f.write(log_message + "\n")
        logger.info(log_message)

        # Отправляем уведомление владельцу
        notify_text = f"👤 <b>Пользователь:</b> {user.full_name}\n"
        notify_text += f"🆔 <b>ID:</b> {user.id}\n"
        if user.username:
            notify_text += f"👤 <b>Username:</b> @{user.username}\n"
        notify_text += f"🕒 <b>Время:</b> {timestamp}\n"
        notify_text += f"📌 <b>Действие:</b> {action}"

        try:
            await bot.send_message(OWNER_ID, notify_text, parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.error(f"Не удалось отправить уведомление владельцу: {e}")

    except Exception as e:
        logger.error(f"Ошибка при логировании: {e}")

# Данные бота
class BotData:
    def __init__(self):
        self.texts = {
            "greeting": """
Привет!👋

Я — Карина, дизайнер. 

Я работаю онлайн и готова помочь с вашим проектом в любой точке мира!

Выберите интересующий раздел:""",
            "portfolio": """ <b>Мое портфолио</b>
            
Мои работы в различных направлениях:

• <b>Веб-дизайн</b> - сайты, лендинги

• <b>Графический дизайн</b> - логотипы, брендбуки, инфографика для маркетплейсов, презентации, баннеры

• <b>UI/UX дизайн</b> - мобильные приложения, интерфейсы 

• <b>Программирование и другое</b> - телеграмм-боты, backend сайтов, добавление платежей, подключение домена и т.п. на Tilda

• <b>Работа с нейросетями</b> - генерация картинок и другое""",
            "resume": """📄 <b>Мое резюме</b>
            
<u>Опыт работы:</u>
• <b>2023-н.в.</b>: Freelance Designer (удаленная работа)

<u>Курсы:</u>
• Курс Freedom "Веб-разработка на Tilda"
• Курс Yudaev School по Figma
• Практический опыт +3 года
• Участник кейс-чемпионата от Альфа банка (роль капитана и дизайнера) (презентация и прототип приложения)  

<u>Ключевые навыки:</u>
• Веб-дизайн (дизайн сайтов, seo-оптимизация, сайты на Tilda)
• Графический дизайн (логотипы, айдентика)  
• Брендинг (разработка айдентики, гайдлайнов) 
• Создание продающей инфографики для маркетплейсов 
• Разработка чат-ботов в Telegram
• Программирование на Python
• Верстка на HTML, CSS
• Инструменты: Figma, Photoshop, нейросети  
• Опыт удалённой работы и фриланса (биржи, клиентские проекты)  
• Умение работать в срок и оперативно вносить правки  
• Администрирование сайта на постоянной основе  

<u>Дополнительные языки:</u>
• Английский - Upper Intermediate (работаю с иностранными клиентами)""",
            "services": """💼 <b>Мои услуги</b>
            
1. <b>Графический дизайн</b>
- Инфографика для маркетплейсов - от 500 ₽ слайд
- Разработка логотипов и фирменного стиля - от 2 000 ₽
- Дизайн полиграфии (визитки, буклеты) - от 2 000 ₽

2. <b>Веб-дизайн</b>
- Создание сайтов (лендинги, корпоративные) - от 10 000 ₽
- Редизайн интерфейсов - от 20 000 ₽
- UI/UX дизайн приложений - от 30 000 ₽

3. <b>Дизайн презентаций</b>
- Корпоративные презентации - от 3 000 ₽ 

4. <b>Работа с нейросетями</b>
- Обсуждается индивидуально 

5. <b>Программирование - работа с кодом</b>
- Обсуждается индивидуально

6. <b>Создание Telegram ботов</b>
- Обсуждается индивидуально

🔹 <b>Скидка 10%</b> на первый заказ через бота!
🔹 Работаю онлайн
🔹 Точная цена обсуждается индивидуально""",
            "contacts": """📱 <b>Мои контакты</b>
            
Я работаю удаленно и доступна для проектов из любой точки мира!

<u>Свяжитесь со мной:</u>
• Telegram: @karinadesignspb

<u>Часы работы:</u>
Пн-Пт: 10:00-18:00 (МСК)
Сб-Вс: по договоренности""",
            "reviews": """⭐ <b>Отзывы клиентов</b>
            
1. <b>Юлия Сергеевна, сайт косметологии:</b>
"Спасибо огромное Карине за разработку сайта моей студии, спасибо за терпение и учет моих пожеланий, переделок, редактирований и т.д. Действительно мастер своего дела, а так же чуткий и понимающий человек, который всегда был на связи и с пониманием относился к моим просьбам.👍👏💐"

2. <b>Андрей, баннер для сайта:</b>
"Отличное качество и соблюдение сроков."

3. <b>Михаил, инвестор:</b>
"Карина, благодарю за профессиональный подход, приятно с Вами сотрудничать, нас приняли в Сколково" """,
            "order": """✏️ <b>Оформить заказ</b>
            
Вы можете оформить заказ через бота или написать мне в личные сообщения @karinadesignspb

Опишите ваш проект:
1. Тип работы (логотип, сайт и т.д.)
2. Ваши пожелания
3. Бюджет (если есть)
4. Сроки
5. Ваш id для связи
Напиши в смс здесь - если хотите заказать услугу через бота

Я свяжусь с вами в течение 24 часов!

• Срочный заказ +30% к стоимости — пишите @karinadesignspb
• Пакетное предложение (скидка до 20%)""",
            "order_thanks": """✅ <b>Спасибо за заказ!</b>
Ваша заявка принята. Я свяжусь с вами в ближайшее время для обсуждения деталей.
До связи! 👋""",
            "referral": """🎁 <b>Акция "Приведи друга"</b>
Приведи клиента и получи <b>10%</b> от суммы его первого заказа на свой счет!

Как это работает:
1. Расскажи другу про мой бот
2. Друг делает заказ и называет твой @username
3. После оплаты его заказа ты получаешь вознаграждение
Можно использовать для своих будущих заказов!""",
            "faq": """❓ <b>Часто задаваемые вопросы</b>
            
<b>🔹 Каковы сроки выполнения работ?</b>
Сроки зависят от сложности проекта:
• Логотип: 1-3 дня
• Сайт: 5-30 дней
• Инфографика: 1-3 дня
Точные сроки оговариваются индивидуально после обсуждения всех деталей.

<b>🔹 Как происходит процесс работы?</b>
1. Вы оставляете заявку через бота или пишете мне напрямую
2. Мы обсуждаем детали проекта, цели, бюджет и сроки
3. Я предоставляю бриф для заполнения (если необходимо)
4. Создаю концепции/макеты
5. Вы вносите правки (до 2-х раундов бесплатно)
6. Я дорабатываю и передаю финальные файлы

<b>🔹 Можно ли внести правки после завершения проекта?</b>
В рамках проекта включены 2 раунда правок бесплатно. Дополнительные правки оплачиваются отдельно (500₽ за раунд).

<b>🔹 Работаете ли вы с иностранными клиентами?</b>
Да, работаю онлайн с клиентами из разных стран. Общение может вестись на русском или английском языках (Upper Intermediate).

<b>🔹 Что нужно для начала работы?</b>
Для начала работы мне нужно:
1. Краткое описание вашего проекта
2. Целевая аудитория
3. Примеры дизайнов, которые вам нравятся (если есть)
4. Логотип и фирменные цвета (если уже есть)
5. Бюджет и сроки (если определены)""",
            "share_bot": """📢 <b>Поделиться ботом</b>
<b>Ссылка для приглашения:</b>
https://t.me/KARINA_DESIGN_SPB_bot
<b>Что можно рассказать друзьям:</b>
• Профессиональный дизайн сайтов и логотипов
• Работа с Tilda и другими платформами
• Создание Telegram ботов
• Работа с нейросетями
• Удаленная работа из любой точки мира
🎁 <b>Бонус:</b> За каждого приведенного клиента вы получаете 10% от суммы его первого заказа!""",
            "tilda_sites": """🌐 <b>Мои сайты на Tilda</b>
            
<b>Последние проекты:</b>

🏗 <b>Element Klinker — поставки стройматериалов</b>
• Продающий лендинг с адаптивным дизайном
• SEO-оптимизация и быстрая загрузка
• Ссылка: <a href="https://elementklinker.ru">Перейти на сайт</a>

🚚 <b>Ecofeed Logistics — грузоперевозки</b>
• Минималистичный дизайн с акцентом на услуги
• Интеграция контактов и форм обратной связи
• Ссылка: <a href="https://ecofeed-logistics.ru/">Перейти на сайт</a>

🌾 <b>Ecofeed Group — кормовые добавки для животных</b>
• Многостраничный сайт с разделами продукции и партнеров
• Адаптивная верстка и современный UI
• Ссылка: <a href="https://ecofeedgroup.ru">Перейти на сайт</a>""",
            "ai_work": """ <b>Работа с нейросетями</b>
Я создаю уникальные изображения и видео с помощью ИИ для:
• Рекламы и соцсетей
• Артов и персонажей
• Фоновые изображения
• Визуализации идей и другое

✅ Быстро, качественно, в высоком разрешении
✅ Уникальные стили под ваш запрос

👉 Перейти к просмотру работу: <a href="https://www.avito.ru/sankt-peterburg/igry_pristavki_i_programmy/generatsiya_izobrazheniy_i_video_cherez_ii_7495771777">Заказать на Avito</a>""",
            "programming": """💻 <b>Программирование</b>
            
Опыт в разработке — более 5 лет.

Языки и технологии:
• Python (включая библиотеки: aiogram, Django, Flask)
• HTML, CSS, JavaScript
• Работа с CSV, JSON, XML
• Базы данных: SQLite, PostgreSQL (через Python)
• API интеграции (Telegram, Avito, Yandex и др.)

Что могу сделать:
• Парсинг данных с сайтов
• Автоматизация задач
• Интеграция платежей и CRM
• Настройка веб-сайтов на Tilda + кастомный код
• Верстка и адаптация под мобильные устройства 
• И другое

Пишите — обсудим ваш проект!""",
            "telegram_bots": """🤖 <b>Telegram-боты</b>
Разрабатываю ботов на Python с использованием библиотеки aiogram.

Что умею:
• Создавать многофункциональных ботов (заказы, опросы, рассылки)
• Подключать базы данных (SQLite, PostgreSQL)
• Интегрировать платежи (через ЮKassa, СБП, крипту)
• Добавлять inline-кнопки, меню, файлы
• Подключать к веб-сайтам и CRM

Примеры: боты для заказа услуг, личные помощники, боты-визитки, боты с админ-панелью.

Готова реализовать вашу идею! Пишите @karinadesignspb""",
        }
        self.resume_pdf_path = "Резюме Карина.pdf"
        self.resume_file_id = None
        self.order_button = "🛍️ Заказать"
        self.reviews_button = "⭐ Отзывы"
        self.orders_file = "orders.txt"
        self.subscribers_file = "subscribers.txt"

# Создание экземпляра данных бота
bot_data = BotData()

# Состояния пользователей
user_order_state = {}
user_question_state = {}

# Функция для сохранения заказа
def save_order(user_id: int, username: str, order_text: str):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(bot_data.orders_file, "a", encoding="utf-8") as f:
            f.write(f"\n=== Новый заказ ===\n")
            f.write(f"Дата: {timestamp}\n")
            f.write(f"ID пользователя: {user_id}\n")
            f.write(f"Username: @{username}\n")
            f.write(f"Текст заказа:\n{order_text}\n")
            f.write("=" * 20 + "\n")
        logger.info(f"Заказ от пользователя {username} сохранен")
    except Exception as e:
        logger.error(f"Ошибка при сохранении заказа: {e}")

# Функция для сохранения вопроса
def save_question(user_id: int, username: str, question_text: str):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("questions.txt", "a", encoding="utf-8") as f:
            f.write(f"\n=== Новый вопрос ===\n")
            f.write(f"Дата: {timestamp}\n")
            f.write(f"ID пользователя: {user_id}\n")
            f.write(f"Username: @{username}\n")
            f.write(f"Вопрос:\n{question_text}\n")
            f.write("=" * 20 + "\n")
        logger.info(f"Вопрос от пользователя {username} сохранен")
    except Exception as e:
        logger.error(f"Ошибка при сохранении вопроса: {e}")

# Управление подписчиками
def add_subscriber(user_id: int, username: str):
    try:
        with open(bot_data.subscribers_file, "a", encoding="utf-8") as f:
            f.write(f"{user_id}:{username}\n")
        logger.info(f"Добавлен подписчик: {username}")
        return True
    except Exception as e:
        logger.error(f"Ошибка при добавлении: {e}")
        return False

def remove_subscriber(user_id: int):
    try:
        subscribers = []
        with open(bot_data.subscribers_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    sub_id, username = line.strip().split(":", 1)
                    if int(sub_id) != user_id:
                        subscribers.append(line)
        with open(bot_data.subscribers_file, "w", encoding="utf-8") as f:
            f.writelines(subscribers)
        logger.info(f"Удалён подписчик: {user_id}")
        return True
    except Exception as e:
        logger.error(f"Ошибка при удалении: {e}")
        return False

def get_subscribers():
    try:
        subscribers = []
        with open(bot_data.subscribers_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    sub_id, username = line.strip().split(":", 1)
                    subscribers.append(int(sub_id))
        return subscribers
    except FileNotFoundError:
        return []
    except Exception as e:
        logger.error(f"Ошибка при получении подписчиков: {e}")
        return []

# Рассылка уведомлений
async def send_notification_to_subscribers(message_text: str):
    subscribers = get_subscribers()
    success_count = 0
    for user_id in subscribers:
        try:
            await bot.send_message(user_id, message_text, parse_mode=ParseMode.HTML)
            success_count += 1
            await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления пользователю {user_id}: {e}")
    logger.info(f"Уведомление отправлено {success_count} из {len(subscribers)}")

# Основная клавиатура
def get_main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2,
        keyboard=[
            [KeyboardButton(text="Портфолио 🎨"), KeyboardButton(text="Резюме 📄")],
            [KeyboardButton(text="Услуги 💼"), KeyboardButton(text=bot_data.reviews_button)],
            [KeyboardButton(text="Контакты 📱"), KeyboardButton(text=bot_data.order_button)],
            [KeyboardButton(text="❓ FAQ"), KeyboardButton(text="📢 Поделиться ботом")]
        ]
    )

# Обработчики команд
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    log_and_notify(message.from_user, "Запустил бота")
    user_order_state[message.from_user.id] = None
    user_question_state[message.from_user.id] = None
    await message.answer(bot_data.texts["greeting"], reply_markup=get_main_keyboard())

@dp.message(F.text == "Портфолио 🎨")
async def portfolio_handler(message: types.Message):
    log_and_notify(message.from_user, "Открыл портфолио")
    await message.answer(bot_data.texts["portfolio"])
    # Кнопки: сначала Tilda, потом три новых — нейросети, программирование, боты
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Figma", url="https://www.figma.com/design/TetYyMheMnoAnRSQiAvhu9/Work-Portfolio?node-id=0-1&t=VfbIusbOFb1gJMm5-1")],
        [InlineKeyboardButton(text="Behance", url="https://www.behance.net/...")],
        [InlineKeyboardButton(text="Сайты на Tilda", callback_data="tilda_sites")],
        [InlineKeyboardButton(text="Работа с нейросетями", callback_data="ai_work")],
        [InlineKeyboardButton(text="Программирование", callback_data="programming")],
        [InlineKeyboardButton(text="Telegram-боты", callback_data="telegram_bots")],
    ])
    await message.answer("🔗 Ссылки на мои работы:", reply_markup=markup)

@dp.callback_query(F.data == "tilda_sites")
async def tilda_sites_callback(callback: types.CallbackQuery):
    log_and_notify(callback.from_user, "Просмотрел сайты на Tilda")
    await callback.message.answer(bot_data.texts["tilda_sites"])
    await callback.answer()

@dp.callback_query(F.data == "ai_work")
async def ai_work_callback(callback: types.CallbackQuery):
    log_and_notify(callback.from_user, "Просмотрел работу с нейросетями")
    await callback.message.answer(bot_data.texts["ai_work"], parse_mode=ParseMode.HTML)
    await callback.answer()

@dp.callback_query(F.data == "programming")
async def programming_callback(callback: types.CallbackQuery):
    log_and_notify(callback.from_user, "Просмотрел раздел программирования")
    await callback.message.answer(bot_data.texts["programming"], parse_mode=ParseMode.HTML)
    await callback.answer()

@dp.callback_query(F.data == "telegram_bots")
async def telegram_bots_callback(callback: types.CallbackQuery):
    log_and_notify(callback.from_user, "Просмотрел раздел Telegram-ботов")
    await callback.message.answer(bot_data.texts["telegram_bots"], parse_mode=ParseMode.HTML)
    await callback.answer()

@dp.message(F.text == "Резюме 📄")
async def resume_handler(message: types.Message):
    log_and_notify(message.from_user, "Запросил резюме")
    try:
        await message.answer(bot_data.texts["resume"])
        if bot_data.resume_file_id:
            await message.answer_document(bot_data.resume_file_id, caption="📄 Мое резюме в PDF")
        elif os.path.exists(bot_data.resume_pdf_path):
            pdf = FSInputFile(bot_data.resume_pdf_path)
            sent_message = await message.answer_document(pdf, caption="📄 Мое резюме в PDF")
            bot_data.resume_file_id = sent_message.document.file_id
        else:
            await message.answer("⚠️ Файл резюме не найден.")
    except Exception as e:
        logger.error(f"Error sending resume: {e}")
        await message.answer("⚠️ Ошибка при отправке резюме.")

@dp.message(F.text == "Услуги 💼")
async def services_handler(message: types.Message):
    log_and_notify(message.from_user, "Просмотрел услуги")
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Заказать", callback_data="order_service")]
    ])
    await message.answer(bot_data.texts["services"], reply_markup=markup)

@dp.message(F.text == bot_data.reviews_button)
async def reviews_handler(message: types.Message):
    log_and_notify(message.from_user, "Просмотрел отзывы")
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оставить отзыв", url="https://t.me/...")],
        [InlineKeyboardButton(text="Все отзывы", url="https://vk.com/...")]
    ])
    await message.answer(bot_data.texts["reviews"], reply_markup=markup)

@dp.message(F.text == "Контакты 📱")
async def contacts_handler(message: types.Message):
    log_and_notify(message.from_user, "Просмотрел контакты")
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Написать", url="https://t.me/karinadesignspb")]
    ])
    await message.answer(bot_data.texts["contacts"], reply_markup=markup)

@dp.message(F.text == bot_data.order_button)
async def order_handler(message: types.Message):
    log_and_notify(message.from_user, "Начал оформление заказа")
    user_order_state[message.from_user.id] = True
    text = bot_data.texts["order"] + """
📎 <b>Вы можете прикрепить файл с ТЗ или дополнительными материалами к заказу!</b>
🎁 <b>Бонус:</b> назовите @username друга для скидки 10% на первый заказ!"""
    await message.answer(text)

@dp.message(F.text == "❓ FAQ")
async def faq_handler(message: types.Message):
    log_and_notify(message.from_user, "Просмотрел FAQ")
    await message.answer(bot_data.texts["faq"], parse_mode=ParseMode.HTML)

@dp.message(Command("logs"))
async def send_logs(message: types.Message):
    if message.from_user.id == OWNER_ID:
        try:
            if os.path.exists("user_activity.log"):
                await message.answer_document(
                    FSInputFile("user_activity.log"),
                    caption="📄 Последние действия пользователей"
                )
            else:
                await message.answer("⚠️ Файл логов не найден.")
        except Exception as e:
            await message.answer(f"❌ Ошибка: {e}")
    else:
        await message.answer("🔐 У вас нет доступа к этой команде.")

@dp.message(F.text == "📢 Поделиться ботом")
async def share_bot_handler(message: types.Message):
    log_and_notify(message.from_user, "Поделился ботом")
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Поделиться ссылкой", switch_inline_query="checkout")]
    ])
    await message.answer(bot_data.texts["share_bot"], reply_markup=markup)

@dp.message(F.text & ~F.text.startswith('/'))
async def process_order_details(message: types.Message):
    state = user_order_state.get(message.from_user.id)
    question_state = user_question_state.get(message.from_user.id)
    if state is True:
        log_and_notify(message.from_user, f"Отправил заказ: {message.text}")
        save_order(message.from_user.id, message.from_user.username or "нет", message.text)
        await message.answer("Прикрепите файлы или нажмите /done.")
        user_order_state[message.from_user.id] = "file"
    elif question_state is True:
        log_and_notify(message.from_user, f"Задал вопрос: {message.text}")
        save_question(message.from_user.id, message.from_user.username or "нет", message.text)
        await message.answer("✅ Вопрос отправлен!", reply_markup=get_main_keyboard())
        user_question_state[message.from_user.id] = None
    else:
        await message.answer("Выберите действие из меню.")

@dp.message(F.document | F.photo)
async def process_order_file(message: types.Message):
    state = user_order_state.get(message.from_user.id)
    if state in [True, "file"]:
        file_name = message.document.file_name if message.document else "photo.jpg"
        log_and_notify(message.from_user, f"Прикрепил файл: {file_name}")
        with open(bot_data.orders_file, "a", encoding="utf-8") as f:
            f.write(f"Файл: {file_name}\n")
        await message.answer("✅ Файл прикреплён. Можете отправить ещё или /done.")
        user_order_state[message.from_user.id] = "file"

@dp.message(Command("done"))
async def finish_order_files(message: types.Message):
    state = user_order_state.get(message.from_user.id)
    if state in [True, "file"]:
        log_and_notify(message.from_user, "Завершил заказ")
        await message.answer(bot_data.texts["order_thanks"], reply_markup=get_main_keyboard())
        user_order_state[message.from_user.id] = None

@dp.callback_query(F.data == "order_service")
async def order_service_callback(callback: types.CallbackQuery):
    log_and_notify(callback.from_user, "Нажал 'Заказать'")
    user_order_state[callback.from_user.id] = True
    await callback.message.answer(bot_data.texts["order"] + "\n🎁 Скидка 10% при упоминании друга!")
    await callback.answer()

# Запуск бота
async def main():
    try:
        logger.info("Starting bot...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.critical(f"Bot crashed: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
