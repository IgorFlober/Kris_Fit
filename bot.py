# -*- coding: utf-8 -*-
import sys
import logging
import time
import requests
from datetime import datetime
from telegram.error import NetworkError, TelegramError

# Настройка продвинутого логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_runtime.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

try:
    from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
    print("✅ Библиотека telegram установлена")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Установите библиотеку: pip3 install python-telegram-bot")
    sys.exit(1)

# Токен бота
BOT_TOKEN = "8025175693:AAH-z4bVN8ngE_Pv7i5-3890K_SZ8_nBB3g"

class ForeverBot:
    def __init__(self):
        self.start_time = datetime.now()
        self.restart_count = 0
        self.max_restarts = 10000
        self.user_data = {}
        
    def log_status(self):
        """Логирует статус бота"""
        uptime = datetime.now() - self.start_time
        logger.info(f"🟢 Бот работает: {uptime} | Перезапусков: {self.restart_count}")
        
    def health_check(self):
        """Проверяет здоровье бота"""
        try:
            response = requests.get(
                f"https://api.telegram.org/bot{BOT_TOKEN}/getMe", 
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Проверка здоровья не удалась: {e}")
            return False
    
    def run_forever(self):
        """Основной цикл работы бота"""
        while self.restart_count < self.max_restarts:
            try:
                print("=" * 60)
                logger.info(f"🚀 ЗАПУСК БОТА (попытка {self.restart_count + 1})")
                print("=" * 60)
                
                # Проверяем доступность Telegram API
                if not self.health_check():
                    logger.error("❌ Telegram API недоступен, ждем 60 секунд")
                    time.sleep(60)
                    continue
                
                # Создаем и настраиваем приложение
                application = Application.builder().token(BOT_TOKEN).build()
                
                # Регистрируем обработчики
                application.add_handler(CommandHandler("start", self.start))
                application.add_handler(MessageHandler(filters.TEXT, self.handle_all_messages))
                application.add_handler(CallbackQueryHandler(self.handle_callback))
                
                logger.info("✅ Бот успешно запущен и готов к работе")
                logger.info("📱 Отправьте /start вашему боту для тестирования")
                self.log_status()
                print("=" * 60)
                
                # Запускаем опрос
                application.run_polling(
                    poll_interval=1,
                    timeout=20,
                    drop_pending_updates=True
                )
                
            except (NetworkError, TelegramError) as e:
                self.restart_count += 1
                logger.warning(f"🌐 Сетевая ошибка: {e}")
                logger.info(f"🔄 Перезапуск через 30 секунд... ({self.restart_count}/{self.max_restarts})")
                time.sleep(30)
                
            except KeyboardInterrupt:
                logger.info("🛑 Бот остановлен пользователем")
                break
                
            except Exception as e:
                self.restart_count += 1
                logger.error(f"💥 Критическая ошибка: {e}")
                import traceback
                traceback.print_exc()
                logger.info(f"🔄 Перезапуск через 60 секунд... ({self.restart_count}/{self.max_restarts})")
                time.sleep(60)
        
        logger.critical("❌ Достигнут лимит перезапусков! Бот остановлен.")

    # ==================== ОСНОВНЫЕ ФУНКЦИИ БОТА ====================

    async def start(self, update, context):
        """Главное меню бота"""
        user_id = update.message.chat.id
        logger.info(f"👤 Пользователь {user_id} запустил бота")
        
        keyboard = [["🧘‍♀️ Спина + Таз", "💪 Подкачка"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            "Привет!👋\n\nВыбери направление тренировок:",
            reply_markup=reply_markup
        )

    async def handle_all_messages(self, update, context):
        """Обработчик всех текстовых сообщений"""
        user_text = update.message.text
        user_id = update.message.chat.id
        
        logger.info(f"📨 Сообщение от {user_id}: '{user_text}'")
        
        if user_text == "🧘‍♀️ Спина + Таз":
            await self.send_spine_hips_info(update)
            
        elif user_text == "💪 Подкачка":
            await self.send_pump_info(update)
            
        elif user_text == "📅 Запись на тренировку":
            await self.send_booking_info(update)
            
        elif user_text == "👤 Связь с тренером":
            await self.send_contact_info(update)
            
        elif user_text == "📊 Результаты":
            await self.send_results_info(update)
            
        elif user_text == "🔙 Назад к направлениям":
            await self.start(update, context)
            
        else:
            await update.message.reply_text("Пожалуйста, используйте кнопки для навигации 📱")
            await self.start(update, context)

    async def send_spine_hips_info(self, update):
        """Информация о направлении 'Спина + Таз'"""
        text = """🧘‍♀️ *Направление: «Спина + Таз»*

✨ *Фокус на:* расслабление, мобильность суставов, снятие напряжения и улучшение самочувствия.

🕒 *Как проходят:* 
Мягкие и спокойные тренировки, направленные на глубокую работу с суставами, снятие блоков и зажимов в области спины и таза.

🎯 *Для кого подходит?*
Идеально для всех, кто испытывает:
• 📍 Скованность в спине и пояснице
• 📍 Дискомфорт в области таза  
• 📍 Отеки и напряжение в ногах
• 📍 Желание проработать проблемные зоны

✅ *Результат:* Повышенная гибкость, уменьшение болей, ощущение легкости, уменьшение отечности и улучшение качества кожи."""
        
        # Клавиатура действий после выбора направления
        keyboard = [
            ["📅 Запись на тренировку", "👤 Связь с тренером"],
            ["📊 Результаты"],
            ["🔙 Назад к направлениям"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(text, parse_mode='Markdown')
        await update.message.reply_text("Выберите дальнейшее действие:", reply_markup=reply_markup)

    async def send_pump_info(self, update):
        """Информация о направлении 'Подкачка'"""
        text = """💪 *Направление: «Подкачка»*

✨ *Фокус на:* создание рельефа, повышение силы и выносливости.

🕒 *Как проходят:*
Динамичные и функциональные тренировки. Каждое занятие начинается с обязательной коррекционной части для подготовки суставов к нагрузке, что делает тренировку безопасной и эффективной. Далее следует силовой блок для проработки мышц всего тела.

🎯 *Для кого подходит?*
Для тех, кто хочет:
• 📍 Привести мышцы в тонус
• 📍 Создать красивый рельеф
• 📍 Укрепить мышечный корсет
• 📍 Повысить общий уровень энергии и выносливости

✅ *Результат:* Подтянутое, сильное тело, красивые очертания мышц и улучшение физической формы.

👥 *Мини-группы до 6 человек:* Я успеваю уделить внимание каждому, проконтролировать технику и дать персональные рекомендации."""
        
        # Клавиатура действий после выбора направления
        keyboard = [
            ["📅 Запись на тренировку", "👤 Связь с тренером"],
            ["📊 Результаты"],
            ["🔙 Назад к направлениям"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(text, parse_mode='Markdown')
        await update.message.reply_text("Выберите дальнейшее действие:", reply_markup=reply_markup)

    async def send_booking_info(self, update):
        """Запись на тренировку с inline-кнопкой"""
        text = """📅 *Запись на тренировку*

Нажмите на кнопку ниже чтобы записаться на тренировку ⬇️"""
        
        # Inline-кнопка для записи
        keyboard = [
            [InlineKeyboardButton("📅 Записаться на тренировку", url="http://t.me/ZavtraLive_bot?startapp=CoachKristina")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, parse_mode='Markdown', reply_markup=reply_markup)

    async def send_contact_info(self, update):
        """Контактная информация с inline-кнопками"""
        text = """👤 *Связь с тренером*

Вы можете написать мне напрямую:"""
        
        # Inline-кнопки для контактов
        keyboard = [
            [InlineKeyboardButton("💬 Написать в Telegram", url="https://t.me/kris_sultanova")],
            [InlineKeyboardButton("📷 Instagram", url="https://instagram.com/kris_syltanova")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, parse_mode='Markdown', reply_markup=reply_markup)

    async def send_results_info(self, update):
        """Результаты клиентов с inline-кнопкой"""
        text = """📊 *Результаты клиентов*

Посмотрите реальные результаты и отзывы моих клиентов:"""
        
        # Inline-кнопка для результатов
        keyboard = [
            [InlineKeyboardButton("📊 Посмотреть результаты", url="http://krisfit.ru.tilda.ws")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, parse_mode='Markdown', reply_markup=reply_markup)

    async def handle_callback(self, update, context):
        """Обработчик нажатий на inline-кнопки"""
        query = update.callback_query
        await query.answer()
        logger.info(f"🔘 Нажата inline-кнопка пользователем {query.from_user.id}")

if __name__ == "__main__":
    print("🎯 ЗАПУСК ФИТНЕС-БОТА КРИСТИНЫ")
    print("⏰ Бот будет работать 24/7 с автоперезагрузкой")
    bot = ForeverBot()
    bot.run_forever()