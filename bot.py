import os
import logging
import asyncio
from threading import Thread
from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# --- 1. CONFIGURATION & LOGGING ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Render မှ PORT နှင့် Token ကို ယူပါ
TOKEN = os.getenv("TELEGRAM_TOKEN")
PORT = int(os.environ.get("PORT", 5000))

# --- 2. DUMMY WEB SERVER FOR RENDER ---
# Render သည် Port တစ်ခုတွင် Run နေမှသာ Service ကို အသက်ရှင်လျက်ထားမည်
app = Flask(__name__)

@app.route("/")
def index():
    return "Sun Legend Bot is Running!", 200

def run_flask():
    app.run(host="0.0.0.0", port=PORT)

# --- 3. GAME STATES ---
(
    CHAPTER_1,
    CHAPTER_4,
    CHAPTER_LEGACY,
    CHAPTER_FINAL,
) = range(4)

# --- 4. STORY LOGIC ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ဂိမ်းစတင်ခြင်း"""
    user = update.effective_user
    # Initialize User Stats
    context.user_data["stats"] = {"wisdom": 0, "affection": 0, "legacy": None}
    
    await update.message.reply_text(
        f"🌌 *နေမင်း၏ ဒဏ္ဍာရီ: စကြဝဠာ၏ နောက်ဆုံးခံတပ်* 🌌\n\n"
        f"မင်္ဂလာပါ {user.first_name}...\n"
        "သင်ဟာ အလင်းနဲ့ အမှောင်ကို ထိန်းချုပ်နိုင်တဲ့ တစ်ဦးတည်းသော နတ်ဘုရား 'နေမင်းနိုင်' ပါ။\n"
        "ရန်သူတွေက 'ဧရာဝဏ်' ဂြိုဟ်စုကို ဝိုင်းထားပြီး၊ သင့်ဘေးမှာ ချစ်သူ 'နေခြည်ထွေး' ရှိနေပါတယ်။\n\n"
        "နေခြည်ထွေး: 'ကိုကို... ရန်သူတွေ အရမ်းများတယ်။ ကမ္ဘာမြေကို ဆုတ်ခွာကြမလား?'",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(
            [["တိုက်ခိုက်မည်", "ဆုတ်ခွာမည်"]], one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return CHAPTER_1

async def chapter_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    stats = context.user_data["stats"]

    if choice == "တိုက်ခိုက်မည်":
        stats["wisdom"] -= 1
        await update.message.reply_text(
            "💥 သင်က အမှောင်စွမ်းအားကို သုံးပြီး တိုက်ခိုက်လိုက်တယ်။\n"
            "ရန်သူတချို့ သေပေမဲ့ ဂြိုဟ်စုကြီး တုန်ခါသွားပြီး နေခြည်ထွေး ဒဏ်ရာရသွားတယ်။\n"
            "(Chaos Path ရွေးချယ်မှု)"
        )
    else:
        stats["wisdom"] += 1
        await update.message.reply_text(
            "🛡️ သင်က နေခြည်ထွေးရဲ့ စကားကို နားထောင်ပြီး ကမ္ဘာမြေကို ဉာဏ်ရှိစွာ ဆုတ်ခွာခဲ့တယ်။\n"
            "(Wisdom Path ရွေးချယ်မှု)"
        )

    await asyncio.sleep(1)
    await update.message.reply_text(
        "⏳ *အခန်း (၄) - မေတ္တာ၏ နောက်ဆုံးစတေးခြင်း*\n\n"
        "ကမ္ဘာမြေပေါ်မှာ တိုက်ပွဲပြင်းထန်နေပြီ။ သင် အဆိပ်သင့်ဒဏ်ရာရနေချိန်မှာ "
        "နေခြည်ထွေးက သူမရဲ့ နှလုံးသားကို သင့်ကိုပေးဖို့ ပြင်ဆင်လိုက်ပြီ!\n\n"
        "နေခြည်ထွေး: 'ကျွန်မအသက်က ကိုကို့အတွက်ပါ... လက်ခံပေးပါနော်...'",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(
            [["တားဆီးမည်", "လက်ခံမည်"]], one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return CHAPTER_4

async def chapter_4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    stats = context.user_data["stats"]

    if choice == "တားဆီးမည်":
        stats["affection"] += 5
        await update.message.reply_text(
            "💔 သင်တားဆီးဖို့ ကြိုးစားပေမဲ့ သူမက အပြုံးနဲ့ပဲ စတေးမှုကို ဆက်လုပ်သွားတယ်။\n"
            "သင့်နှလုံးသားထဲမှာ နာကျင်မှုတွေ ကျန်ရစ်ခဲ့တယ်။"
        )
    else:
        stats["affection"] += 20
        await update.message.reply_text(
            "✨ သင်က မျက်ရည်ကျရင်း လက်ခံလိုက်တယ်။\n"
            "နေခြည်ထွေးရဲ့ နှလုံးသားက သင့်ရင်ဘတ်ထဲမှာ ပြန်ခုန်လာပြီး သင်ဟာ 'Hybrid God' ဖြစ်လာခဲ့ပြီ။"
        )

    await asyncio.sleep(1)
    await update.message.reply_text(
        "⚔️ *အခန်း (၅) - မျိုးဆက်သစ်၏ လမ်းပြ*\n\n"
        "၁၀ နှစ် ကြာပြီးနောက်... သင့်ရှေ့မှာ တပည့်နှစ်ယောက် ရောက်လာတယ်။ ဘယ်သူ့ကို ဦးစားပေးမလဲ?\n\n"
        "၁. သူရနိုင် (နတ္ထိပြုခြင်း - ခံစစ်)\n"
        "၂. သီရိနွေ (အနာဂတ်မြင်ခြင်း - ဗျူဟာ)",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(
            [["သူရနိုင်", "သီရိနွေ"]], one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return CHAPTER_LEGACY

async def chapter_legacy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    stats = context.user_data["stats"]

    if choice == "သူရနိုင်":
        stats["legacy"] = "defender"
        await update.message.reply_text(
            "🛡️ သင်က သူရနိုင်ကို 'နတ္ထိဝဇ္ဇရ' လှံတံ ပေးအပ်လိုက်တယ်။ သူက ကာကွယ်ရေးမှာ ဆရာကျသွားပြီ။"
        )
    else:
        stats["legacy"] = "oracle"
        await update.message.reply_text(
            "👁️ သင်က သီရိနွေကို 'စကြဝဠာမျက်လုံး' ဖွင့်ပေးလိုက်တယ်။ သူမက ရန်သူ့အားနည်းချက်ကို မြင်နိုင်ပြီ။"
        )

    await asyncio.sleep(1)
    await update.message.reply_text(
        "🔥 *အခန်း (၁၀) - နောက်ဆုံးတိုက်ပွဲ*\n\n"
        "ရန်သူ့ 'အမှောင်ကြယ်' အမြောက်ကြီး ကမ္ဘာကို ပစ်လွှတ်လိုက်ပြီ!\n"
        "ဒါဟာ နောက်ဆုံး ဆုံးဖြတ်ချက်ပါပဲ။",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(
            [["အသေခံတိုက်မည်", "တပည့်များကိုယုံကြည်မည်"]], one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return CHAPTER_FINAL

async def chapter_final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    stats = context.user_data["stats"]
    
    # ENDING LOGIC
    if choice == "အသေခံတိုက်မည်":
        await update.message.reply_text(
            "🌌 *BAD ENDING: THE LONELY STAR*\n\n"
            "သင်က နေခြည်ထွေးရဲ့ နှလုံးသားစွမ်းအင်ကို ဖောက်ခွဲပြီး ရန်သူကို သုတ်သင်လိုက်တယ်။\n"
            "ဒါပေမဲ့ သင့်ဝိညာဉ် ပျောက်ကွယ်သွားပြီး နေခြည်ထွေးရဲ့ ဝိညာဉ်က တစ်ယောက်တည်း ကျန်ရစ်ခဲ့တယ်။",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardRemove()
        )
    elif choice == "တပည့်များကိုယုံကြည်မည်":
        if stats["affection"] >= 20 and stats["wisdom"] >= 0:
            await update.message.reply_text(
                "🌅 *TRUE ENDING: THE ETERNAL DAWN*\n\n"
                "သူရနိုင်က အမြောက်ချက်ကို တားဆီးလိုက်ချိန်မှာ သင်နဲ့ သီရိနွေက ရန်သူ့ဗဟိုချက်ကို ဖျက်ဆီးလိုက်တယ်။\n"
                "နေခြည်ထွေးရဲ့ ဝိညာဉ် ပေါ်လာပြီး 'ကိုကို... ကျွန်မတို့ အတူတူ နားကြစို့' လို့ ပြောတယ်။\n"
                "သင်တို့နှစ်ယောက်ဟာ နေနဲ့ နေရောင်ခြည်အဖြစ် ကမ္ဘာမြေကို ထာဝရ စောင့်ရှောက်သွားကြလေရဲ့။",
                parse_mode="Markdown",
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            await update.message.reply_text(
                "🛡️ *NORMAL ENDING: THE GUARDIAN*\n\n"
                "ရန်သူကို နိုင်လိုက်ပေမဲ့ တပည့်တွေ ဒဏ်ရာအပြင်းအထန် ရသွားတယ်။\n"
                "သင်ဟာ ကမ္ဘာမြေရဲ့ အစောင့်အရှောက်အဖြစ် တစ်ကိုယ်တည်း ဆက်လက် ရပ်တည်ရတော့တယ်။",
                parse_mode="Markdown",
                reply_markup=ReplyKeyboardRemove()
            )

    await update.message.reply_text("ကစားပေးတဲ့အတွက် ကျေးဇူးတင်ပါတယ်။ /start ကို နှိပ်ပြီး ပြန်ကစားနိုင်ပါတယ်။")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ဂိမ်းကို ရပ်လိုက်ပါပြီ။ /start နှိပ်ပြီး ပြန်စနိုင်ပါတယ်။", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# --- 5. MAIN EXECUTION ---
if __name__ == "__main__":
    # Flask ကို Thread တစ်ခုအနေနဲ့ Run ပါ (Render အတွက်)
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Telegram Bot ကို Run ပါ
    if not TOKEN:
        print("Error: TELEGRAM_TOKEN မရှိပါ။ Environment Variable ထည့်ပေးပါ။")
    else:
        application = ApplicationBuilder().token(TOKEN).build()

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                CHAPTER_1: [MessageHandler(filters.TEXT & ~filters.COMMAND, chapter_1)],
                CHAPTER_4: [MessageHandler(filters.TEXT & ~filters.COMMAND, chapter_4)],
                CHAPTER_LEGACY: [MessageHandler(filters.TEXT & ~filters.COMMAND, chapter_legacy)],
                CHAPTER_FINAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, chapter_final)],
            },
            fallbacks=[CommandHandler("cancel", cancel)],
        )

        application.add_handler(conv_handler)
        
        print("Bot is polling...")
        application.run_polling()
