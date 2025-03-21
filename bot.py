from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Replace with your bot token
TOKEN = "7877784866:AAHCiUM68--nVcTZXOWVz_9AzwqXo5BU69w"

# Define product catalog
PRODUCTS = [
    {"id": 1, "name": "Wise Business", "description": "Manage global finances.", "price": "$60"},
    {"id": 2, "name": "SumUp UK 🇬🇧", "description": "UK-based payment processor.", "price": "$120"},
    {"id": 3, "name": "SumUp Europe 🇪🇺", "description": "Europe-based payment processor.", "price": "$50"},
    {"id": 4, "name": "SSN with ID", "description": "Social security number with ID.", "price": "$10"},
    {"id": 5, "name": "SSN without ID", "description": "Social security number only.", "price": "$2"},
    {"id": 6, "name": "Shopify Payment", "description": "Shopify payment gateway setup.", "price": "$50"},
]

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🛍️ Browse Products", callback_data='browse_products')],
        [InlineKeyboardButton("📦 My Orders", callback_data='my_orders')],
        [InlineKeyboardButton("📞 Contact Support", callback_data='contact_support')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Welcome! Choose an option:", reply_markup=reply_markup)

# Browse products handler
async def browse_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton(f"{p['name']} - {p['price']}", callback_data=f"view_product_{p['id']}")] for p in PRODUCTS]
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data='back_to_home')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("🛍️ Available Products:", reply_markup=reply_markup)

# View product details handler
async def view_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    product_id = int(query.data.split('_')[-1])
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        text = f"**{product['name']}**\n\n{product['description']}\n\n💰 Price: {product['price']}"
        keyboard = [[InlineKeyboardButton("🛒 Order Now", callback_data=f"order_product_{product['id']}")]]
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data='browse_products')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)

# Order product handler
async def order_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    product_id = int(query.data.split('_')[-1])
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        order_text = f"✅ **Order Confirmed**\n\n**Product:** {product['name']}\n💰 **Price:** {product['price']}\n\nOur team will contact you soon!"
        await query.edit_message_text(order_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data='browse_products')]]))

# My Orders handler (Placeholder)
async def my_orders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📦 **Your Orders**\n\nYou have no orders yet.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data='back_to_home')]]))

# Contact Support handler
async def contact_support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    support_text = "📞 **Contact Support**\n\nFor assistance, contact us:\n📧 Email: support@example.com\n💬 Telegram: @SupportBot"
    await query.edit_message_text(support_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data='back_to_home')]]))

# Back to Home handler
async def back_to_home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await start(update, context)

# Main function
def main() -> None:
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(browse_products, pattern="browse_products"))
    app.add_handler(CallbackQueryHandler(view_product, pattern="view_product_.*"))
    app.add_handler(CallbackQueryHandler(order_product, pattern="order_product_.*"))
    app.add_handler(CallbackQueryHandler(my_orders, pattern="my_orders"))
    app.add_handler(CallbackQueryHandler(contact_support, pattern="contact_support"))
    app.add_handler(CallbackQueryHandler(back_to_home, pattern="back_to_home"))
    
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
