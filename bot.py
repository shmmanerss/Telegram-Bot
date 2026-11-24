import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession

logging.basicConfig(level=logging.INFO)

# На хостинге токен и ID будут браться из настроек (Environment Variables)
BOT_TOKEN = os.getenv("BOT_TOKEN", "9092668406:AAELrQPP9QIGt5hAVyceZDNpdRwE99EbzNs")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "-4633763126")) 
PROXY_URL = os.getenv("PROXY_URL", "socks5://127.0.0.1:3067") 

CATALOG = {
    "adrenaline": {
        "name": "Adrenaline Rush",
        "drinks": [
            {"id": "adr_original", "name": "Adrenaline Rush Original, объем 0.5 л", "photo": "AgACAgIAAxkBAAMFawQIGvXyFJCkSDDSS2LEbP6XmV4AAhAcaxuD-SFIk_zZgOYSPGEBAAMCAAN4AAM9BA"},
            {"id": "adr_berry",     "name": "Adrenaline Rush Berry Energy, объем 0.5 л",     "photo": "AgACAgIAAxkBAAMIawQJ56V2yI2sxBM1a2d0BSiPgOIAAh8caxuD-SFIs04hB2UCieIBAAMCAAN4AAM9BA"},
            {"id": "adr_zero",     "name": "Adrenaline Rush Zero Sugar, объем 0.5 л",   "photo": "AgACAgIAAxkBAAMHawQJ2L9rP15VuPqiGSHnmDNNsRsAAh0caxuD-SFITeq9aPgwvocBAAMCAAN4AAM9BA"},
            {"id": "adr_str",     "name": "Adrenaline Rush Юдзу-Клубника, объем 0.5 л",   "photo": "AgACAgIAAxkBAAMJawQJ98q2oshtp1aLJwIBDbeY_4UAAiEcaxuD-SFI8Yk8JZvsOUYBAAMCAAN4AAM9BA"},
            {"id": "adr_myst",     "name": "Adrenaline Rush Mystic Energy, объем 0.5 л",   "photo": "AgACAgIAAxkBAAMKawQKDkTQdD2vxGMx9dvR87LTl5AAAiIcaxuD-SFIgqUcdyUKl7IBAAMCAAN4AAM9BA"},
            {"id": "adr_pom",     "name": "Adrenaline Rush Помело-ананас, объем 0.5 л",   "photo": "AgACAgIAAxkBAAMLawQKOgZZgxx4jg3oBsUFa19g0bsAAiQcaxuD-SFIu25IgMafscUBAAMCAAN4AAM9BA"},
            {"id": "adr_trop",     "name": "Adrenaline Rush Tropical Energy, объем 0.5 л",   "photo": "AgACAgIAAxkBAAMLawQKOgZZgxx4jg3oBsUFa19g0bsAAiQcaxuD-SFIu25IgMafscUBAAMCAAN4AAM9BA"}, 
        ]
    },
    "monster": {
        "name": "Monster Energy",
        "drinks": [
            {"id": "mon_apple", "name": "Monster Energy Киви-Яблоко(Китай), объём 0.33л ", "photo": "AgACAgIAAxkBAAMOawQKh-846CWLhNVzWYW2ArV0ecEAAigcaxuD-SFIjq3S_5YwoR0BAAMCAAN4AAM9BA"},
            {"id": "mon_zero", "name": "Monster Energy Ultra-White (Китай), объём 0.33л ", "photo": "AgACAgIAAxkBAAMPawQKlKRTP-jo9DYwLzEVSG_xPREAAikcaxuD-SFIbL-LHAUa7moBAAMCAAN4AAM9BA"},
            {"id": "mon_loco", "name": "Monster Energy Mango-Loco (Китай), объём 0.33л ", "photo": "AgACAgIAAxkBAAMQawQKqqB7u9vwuAezFcFQWFRLfBUAAiocaxuD-SFISJZnQprQHsUBAAMCAAN4AAM9BA"},
            {"id": "mon_green", "name": "Monster Energy Green (Китай), объём 0.33л ", "photo": "AgACAgIAAxkBAAMRawQKsgu2lHK0xCAat01rozzo_u0AAiscaxuD-SFInkM7qk-YGXkBAAMCAAN4AAM9BA"},
            {"id": "mon_zero2", "name": "Monster Energy Ultra-White (Польша), объём 0.5л ", "photo": "AgACAgIAAxkBAAMSawQK8cV_FYwPv7R0nYuxXUugF2MAAi8caxuD-SFI7tHlFEdCZ2wBAAMCAAN4AAM9BA"},
            {"id": "mon_loco2", "name": "Monster Energy Mango-Loco (Польша), объём 0.5л ", "photo": "AgACAgIAAxkBAAMTawQK-PJUhGdx8mBq-4C_jz1pqhQAAjAcaxuD-SFIO-czZ-4LE8gBAAMCAAN4AAM9BA"},
            {"id": "mon_green2", "name": "Monster Energy Green (Польша), объём 0.5л ", "photo": "AgACAgIAAxkBAAMUawQLAo2NgxEic_033f9PEk7wzIAAAjEcaxuD-SFIjw8hVU1LyZYBAAMCAAN4AAM9BA"},
            {"id": "mon_full", "name": "Monster Energy Full Throttle Zero Sugar (Польша), объём 0.5л ", "photo": "AgACAgIAAxkBAAMVawQLDPuf1C5qyuCgNaWJaBp0wTwAAjIcaxuD-SFIa9ZXZc4-7qABAAMCAAN4AAM9BA"},
            {"id": "mon_nitro", "name": "Monster Energy Nitro Dry (Польша), объём 0.5л ", "photo": "AgACAgIAAxkBAAMWawQLIulFy2KQl8wTQsjSwU8uyioAAjMcaxuD-SFI2tkP6Qvm5iYBAAMCAAN4AAM9BA"},
            {"id": "mon_lem", "name": "Monster Energy Aussie Lemonade (Польша), объём 0.5л ", "photo": "AgACAgIAAxkBAAOiawR9PvTIdnZhvrN5AAHokxTkcskKAAIzH2sbg_khSBErWAfwNjPfAQADAgADeQADPQQ"},
            {"id": "mon_peach", "name": "Monster Energy Ultra Peachy Keen (Польша), объём 0.5л ", "photo": "AgACAgIAAxkBAAOhawR85XCKiOrnE8aDwtn6XS5vMwUAAjEfaxuD-SFIlI0Od21BNaoBAAMCAAN4AAM9BA"},
            {"id": "mon_pink", "name": "Monster Energy Pipeline Punch (Польша), объём 0.5л ", "photo": "AgACAgIAAxkBAAOgawR80fr-fGCW3oRDCdvYou5YoagAAjAfaxuD-SFIzUAtkhlK1pYBAAMCAAN5AAM9BA"},
        ]
    },
    "redbull": {
        "name": "Red Bull",
        "drinks": [
            {"id": "rb_classic", "name": "Red Bull Classic (Австралия), объём 0.25л", "photo": "AgACAgIAAxkBAAMXawQLY4Cn6Uw-WHopfBwUDMr2_fgAAjgcaxuD-SFITiSCz9u8LyQBAAMCAAN4AAM9BA"},
            {"id": "rb_zero", "name": "Red Bull Zero Sugar (Австралия), объём 0.25л", "photo": "AgACAgIAAxkBAAMYawQLaJDv5SAGDK0zIhDV6VabasgAAjkcaxuD-SFIF8Ha1cc3XAQBAAMCAAN4AAM9BA"},
            {"id": "rb_trop", "name": "Red Bull Tropical Edition (Австралия), объём 0.25л", "photo": "AgACAgIAAxkBAAMZawQLb9PEGd6r46bhqCuv-wnUos0AAjocaxuD-SFIyXaS4df4obgBAAMCAAN4AAM9BA"},
            {"id": "rb_winter", "name": "Red Bull Winter Edition (Австрия), объём 0.25л", "photo": "AgACAgIAAxkBAAMcawQLyhmKDbncOw18H5WhelsngaEAAj0caxuD-SFIWnjFHZTlk1sBAAMCAAN4AAM9BA"},
            {"id": "rb_sea", "name": "Red Bull Sea Blue Edition (Австрия), объём 0.25л", "photo": "AgACAgIAAxkBAAMbawQLvzRxFaMMx6VZdpIU5JAgEoEAAjwcaxuD-SFIXtDbtiqvSXYBAAMCAAN4AAM9BA"},
            {"id": "rb_peach", "name": "Red Bull Peach Edition (Сербия), объём 0.25л", "photo": "AgACAgIAAxkBAAMaawQLkjiKiFnVZEQ4C8W3S9iuFG0AAjscaxuD-SFIwqXs1dfnNk0BAAMCAAN4AAM9BA"},
            
        ]
    },
    "burn": {
        "name": "Burn",
        "drinks": [
            {"id": "burn_original", "name": "Burn Original, объём 0.5л", "photo": "AgACAgIAAxkBAAMeawQMW0K5BDmkQt1XcV9hSgzQWvYAAkEcaxuD-SFIHtQ4QeIHYtcBAAMCAAN4AAM9BA"},
            {"id": "burn_zero", "name": "Burn Zero Sugar, объём 0.5л", "photo": "AgACAgIAAxkBAAMdawQMJiAauBOOzRFGVweWMy4LvzMAAj4caxuD-SFIMaeqCmVBcNUBAAMCAAN4AAM9BA"},
            {"id": "burn_apple", "name": "Burn Apple-Kiwi, объём 0.5л", "photo": "AgACAgIAAxkBAAMgawQMW6mwumdMNOA3jZxwLqvjC6AAAkMcaxuD-SFIxaibe73P2X4BAAMCAAN4AAM9BA"},
            {"id": "burn_mg", "name": "Burn Mango, объём 0.5л", "photo": "AgACAgIAAxkBAAMfawQMWyaHfSOssQAB9Qrvdmk07m5yAAJCHGsbg_khSPPKiTaI3oSdAQADAgADeAADPQQ"},
        ]
    },
    
}

router = Router()

# ========== ГЛАВНОЕ МЕНЮ ==========
async def show_main_menu(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Хочу энергетик", callback_data="want_energy")]
    ])
    await message.answer("Привет! Нажми кнопку, чтобы получить энергетик:", reply_markup=kb)

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await show_main_menu(message)

# ========== ШАГ 1 ==========
@router.callback_query(F.data == "want_energy")
async def want_energy(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    # Временный шаг для теста (потом уберем)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Я Ваня, хочу энергос", callback_data="role_vanya")],
        [InlineKeyboardButton(text="Я тестировщик",         callback_data="role_tester")],
    ])
    await callback.message.edit_text("Кто ты? (временный шаг)", reply_markup=kb)

# ========== ШАГ 2 ==========
@router.callback_query(F.data.startswith("role_"))
async def choose_role(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    role = callback.data.split("_")[1]
    await state.update_data(role=role)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Хочу сюрприз, удиви меня",       callback_data="mode_surprise")],
        [InlineKeyboardButton(text="Выбрать энергетик из каталога", callback_data="mode_catalog")],
    ])
    await callback.message.edit_text("Что выберешь?", reply_markup=kb)

# ========== СЮРПРИЗ ==========
@router.callback_query(F.data == "mode_surprise")
async def mode_surprise(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data_state = await state.get_data()
    role = data_state.get("role", "tester")

    await callback.bot.send_message(
        ADMIN_CHAT_ID,
        f"🎁 Сюрприз!\n"
        f"Пользователь: {callback.from_user.full_name} (@{callback.from_user.username})\n"
        f"Роль: {role}\n"
        f"Выбрал: «Хочу сюрприз, удиви меня»"
    )
    await callback.message.edit_text("Сюрприз принят! Ожидайте, ваш подарок уже готовится 🎉")
    await show_main_menu(callback.message)

# ========== КАТАЛОГ: ВЫБОР БРЕНДА ==========
@router.callback_query(F.data == "mode_catalog")
async def mode_catalog(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    buttons = []
    for key, brand in CATALOG.items():
        buttons.append([InlineKeyboardButton(text=brand["name"], callback_data=f"brand_{key}")])
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="want_energy")])
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text("Выбери бренд:", reply_markup=kb)

# ========== КАТАЛОГ: ПОКАЗ НАПИТКОВ ==========
@router.callback_query(F.data.startswith("brand_"))
async def choose_brand(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    brand_key = callback.data.split("_", 1)[1]
    brand = CATALOG.get(brand_key)
    if not brand:
        await callback.message.answer("Бренд не найден")
        return

    for drink in brand["drinks"]:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Хочу этот!", callback_data=f"order_{drink['id']}")]
        ])
        await callback.message.answer_photo(
            photo=drink["photo"],
            caption=drink["name"],
            reply_markup=kb
        )

    kb_back = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ К выбору бренда", callback_data="mode_catalog")]
    ])
    await callback.message.answer("Или вернись назад:", reply_markup=kb_back)

# ========== ОФОРМЛЕНИЕ ЗАКАЗА ==========
@router.callback_query(F.data.startswith("order_"))
async def order_drink(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    drink_id = callback.data.replace("order_", "", 1)
    data_state = await state.get_data()
    role = data_state.get("role", "tester")

    drink = None
    for brand in CATALOG.values():
        for d in brand["drinks"]:
            if d["id"] == drink_id:
                drink = d
                break
        if drink:
            break

    if not drink:
        await callback.message.answer("Ошибка: напиток не найден")
        return

    await callback.bot.send_message(
        ADMIN_CHAT_ID,
        f"🎁 Новый заказ!\n"
        f"Пользователь: {callback.from_user.full_name} (@{callback.from_user.username})\n"
        f"Роль: {role}\n"
        f"Напиток: {drink['name']}"
    )
    await callback.message.answer(
        "Заказ оформлен, ожидайте ваш энергетический напиток на парах ⚡️"
    )
    await show_main_menu(callback.message)

# ========== ЗАПУСК ==========
async def main():
    # Если задан прокси, используем его (для локального запуска)
    if PROXY_URL:
        session = AiohttpSession(proxy=PROXY_URL)
        bot = Bot(token=BOT_TOKEN, session=session)
    else:
        bot = Bot(token=BOT_TOKEN)
        
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    
    print("Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
