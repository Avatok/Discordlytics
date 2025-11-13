import discord
from discord.ext import commands
import csv
import os
from datetime import datetime

# ---------- CONFIG ----------
TRACKED_CHANNELS = [
    1437414720045846629,  # Channel 1
    1437414836761006100,  # Channel 2
    1437414887667138630,  # Channel 3
]

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

CSV_FILE = "server_activity.csv"

# ---------- CSV HEADER ----------
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Datum", "User", "Channel", "Inhalt", "Status", "MessageID"])

# ---------- CSV HELPER ----------
def get_timestamp():
    return datetime.now().strftime("%d.%m.%Y %H:%M:%S")

def update_csv(message_id, new_content=None, new_status=None):
    if not os.path.exists(CSV_FILE):
        return

    rows = []
    found = False
    timestamp = get_timestamp()

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if row[5] == str(message_id):
                if new_content is not None:
                    row[3] = new_content
                if new_status is not None:
                    row[4] = new_status
                row[0] = timestamp  # Datum aktualisieren
                found = True
            rows.append(row)

    if found:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)

# ---------- EVENTS ----------
@bot.event
async def on_message(message):
    if message.author.bot or message.channel.id not in TRACKED_CHANNELS:
        return

    timestamp = get_timestamp()
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp,
            str(message.author),
            str(message.channel),
            message.content,
            "original",
            message.id
        ])
    await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):
    if after.author.bot or after.channel.id not in TRACKED_CHANNELS:
        return
    update_csv(after.id, new_content=after.content, new_status="bearbeitet")

@bot.event
async def on_message_delete(message):
    if message.author.bot or message.channel.id not in TRACKED_CHANNELS:
        return
    update_csv(message.id, new_status="gelöscht")

# Bot starten
bot.run("MTQzNDkzMzkwMDI4NjYyMzg3OA.GA9Sda.lNfuNGpm77R5nU5AqJQGRujmsWADiYvwfV6O_k")