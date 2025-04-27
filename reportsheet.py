from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from datetime import datetime
import re
import os
import json
from google.oauth2.service_account import Credentials

# Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
AUTHORIZED_USER_ID = os.getenv("AUTHORIZED_USER_ID")
SHEET_NAME = os.getenv("SHEET_NAME")

# Initialiser l'API Google Sheets
def get_sheets_service():
    creds_json = os.getenv("GOOGLE_CREDENTIALS")
    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=[
        "https://www.googleapis.com/auth/spreadsheets"
    ])
    service = build("sheets", "v4", credentials=creds)
    return service


# Formatter la date au format dd/mm/aaaa
def get_formatted_date():
    return datetime.now().strftime("%d/%m/%Y")

# Extraire une date au format dd/mm/yyyy du message
def extract_date_from_message(message):
    # Recherche une date au format dd/mm/yyyy (par exemple, 24/04/2025)
    date_pattern = r'\b(\d{2}/\d{2}/\d{4})\b'
    match = re.search(date_pattern, message)
    if match:
        return match.group(1)  # Retourne la date trouvée (par exemple, "24/04/2025")
    return get_formatted_date()  # Si aucune date n'est trouvée, retourne la date actuelle

# Reformuler le message en tâche
def format_task(message):
    # Supprime la date du message pour ne garder que la tâche
    date_pattern = r'\b\d{2}/\d{2}/\d{4}\b'
    task = re.sub(date_pattern, "", message).strip()  # Supprime la date
    task = re.sub(r"^j'ai\s+", "", task, flags=re.IGNORECASE).strip()  # Supprime "j'ai"
    task = task[0].upper() + task[1:] if task else task  # Met la première lettre en majuscule
    return task.rstrip(".")

# Ajouter une ligne dans Google Sheets (case à cocher, date, tâche)
def append_to_sheet(date, task):
    try:
        service = get_sheets_service()
        
        # 1. Trouver la prochaine ligne vide
        range_c = f"'{SHEET_NAME}'!C:C"  # On vérifie la colonne C (tâche)
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_c
        ).execute()
        values = result.get('values', [])
        
        # Calculer la ligne suivante (en ignorant l'en-tête)
        next_row = len(values) + 1 if values else 2
        
        # 2. Écrire dans la ligne exacte
        range_name = f"'{SHEET_NAME}'!A{next_row}:C{next_row}"
        values = [[True, date, task]]
        body = {"values": values}
        
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
        return True
    except Exception as e:
        print(f"Erreur lors de l'écriture : {e}")
        return False

# Handler pour les messages texte
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id != AUTHORIZED_USER_ID:
        await update.message.reply_text("Accès refusé.")
        return

    message = update.message.text
    date = extract_date_from_message(message)  # Extraire la date du message
    task = format_task(message)

    # Ajouter à Google Sheets
    if append_to_sheet(date, task):
        await update.message.reply_text(f"Tâche ajoutée : {task} ({date})")
    else:
        await update.message.reply_text("Erreur lors de l'ajout de la tâche.")

# Handler pour la commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot démarré ! Envoyez un message pour ajouter une tâche.")

def main():
    # Initialiser le bot
    app = Application.builder().token(BOT_TOKEN).build()

    # Ajouter les handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Démarrer le bot
    print("Bot démarré...")
    app.run_polling()

if __name__ == "__main__":
    main()