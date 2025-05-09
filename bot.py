
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = "7577193986:AAEpL6NKWGh4d4tqnoRDo5y1tzz765_1JRc"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Quest(StatesGroup):
    task1 = State()
    task2 = State()
    task3 = State()
    task4 = State()
    final = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "Привет! Я бот прошлого и будущего. Детства и взрослой жизни. Я есть и меня нет. И я всегда прихожу(как Санта и пасхальный кролик) к тем, кто достигает 24 лет и кто теряет юность в сердце. На тебя поступила жалоба от друзей, что взрослая жизнь поглощает тебя с каждым годом. Они переживают за тебя\n\n"
        "Готова ли ты доказать, что маленькая Настя всё ещё живёт в тебе?",
        reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("ДА!")
    )
    await Quest.task1.set()

@dp.message_handler(lambda m: m.text == "ДА!", state=Quest.task1)
async def task1_start(message: types.Message):
    await message.answer("Запиши видео, как будто ты в 10 лет записываешь ролик на YouTube (вроде у тебя уже был опыт?)")

@dp.message_handler(content_types=types.ContentType.VIDEO, state=Quest.task1)
async def task1_video(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True).add("Естественно", "Не хочу")
    await message.answer("Пересмотрел все видео… Ты ничуть не изменилась! Переходим ко второму заданию ?", reply_markup=kb)
    await Quest.task2.set()

@dp.message_handler(lambda m: m.text == "Не хочу", state=Quest.task2)
async def task2_skip(message: types.Message):
    await message.answer("Так отвечают только взрослые скуфы, а не дети! Жми другую кнопку!")

@dp.message_handler(lambda m: m.text == "Естественно", state=Quest.task2)
async def task2_riddle(message: types.Message):
    await message.answer(
        "Теперь перейдём к делу. Я знаю как ты любишь загадки, но это также знает и Андрей. Он предложил задание для тебя, с чем я спорить не стал. Я спрятал кодовое слово. Чтобы найти его ты должна понять это стихотворение:\n\n"
        "Тогда на ДНД аромат манил,\n"
        "Но что-то явно пошло не так.\n"
        "Ты — с улыбкой, я — с промахом,\n"
        "И вместо сладости — “моряк”.\n"
        "Один неверный жест руки —\n"
        "И напиток стал для храбрецов.\n"
        "Найди то место, где ошибка\n"
        "Оставила свой привкус слов.\n\n"
        "Ты должна написать слово, которое найдешь, чтобы пройти дальше! У тебя будет возможность взять подсказку, но она будет стоить 1 поцелуй (так как задание от Андрея). Чтобы взять подсказку, напиши /подсказка"
    )

@dp.message_handler(commands='подсказка', state=Quest.task2)
async def task2_hint1(message: types.Message):
    await message.answer("моряк = соль\nНапиток стал для храбрецов = испорченное кофе")

@dp.message_handler(lambda m: m.text.lower() == "детство", state=Quest.task2)
async def task2_answer(message: types.Message):
    await message.answer("Верно! Получаешь часть фразы: «Тозесн»")
    await message.answer(
        "Мне нравится как ты включилась в игру! чувствую как юность в сердце возвращается. Но мы не будем на этом останавливаться. Вот тебе еще одна загадка:\n\n"
        "Бодрящий по утрам,\n"
        "Такой опасный и манящий.\n"
        "Возвращаясь к знакомым продавцам\n"
        "Берешь океан своей рукой изящной.\n"
        "Лишь дно скрывает тайну,\n"
        "Которая важна для тебя крайне\n\n"
        "Введи ответ или /подсказка"
    )
    await Quest.task3.set()

@dp.message_handler(commands='подсказка', state=Quest.task3)
async def task3_hint(message: types.Message):
    await message.answer("Ищи в Анфисе")

@dp.message_handler(lambda m: m.text.lower() == "счастье", state=Quest.task3)
async def task3_answer(message: types.Message):
    await message.answer("Получаешь слово: «е»")
    await message.answer("Вижу твою улыбку на лице! И сразу сердце мое радуется. Теперь будет задание на внимательность. Собери X бумажных кусочка, которые разбросаны по кухне. Они складываются в слово. Когда найдёшь — впиши его сюда!")
    await Quest.task4.set()

@dp.message_handler(lambda m: m.text.lower() == "халупа", state=Quest.task4)
async def task4_answer(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True).add("перейти к последнему заданию")
    await message.answer("Что ж, осталось совсем немного до твоей трансформации. Финальная часть шифра у твоего брата. Остальное дело за тобой. Удачи!", reply_markup=kb)
    await Quest.final.set()

@dp.message_handler(lambda m: m.text.lower() == "перейти к последнему заданию", state=Quest.final)
async def final_intro(message: types.Message):
    await message.answer("Цезарь. Введите кодовую фразу:")

@dp.message_handler(lambda m: m.text.lower() == "плевок в вечность", state=Quest.final)
async def final_answer(message: types.Message, state: FSMContext):
    await message.answer("Умница! Осталось тебе открыться этому миру! Бегу туда, где дети любят проводить время")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
