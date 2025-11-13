# 📊 Discordlytics

> Tracke und visualisiere deine Discord-Serveraktivität in Echtzeit — mit nur zwei Python-Skripten.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Dashboard-black?logo=flask)
![Discord](https://img.shields.io/badge/Discord-Bot-5865F2?logo=discord)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🧠 Übersicht

**Discordlytics** ist ein leichtgewichtiges Discord-Analytics-Tool, das:
- Serveraktivität wie Nachrichten, Channels und User trackt,
- alle Daten in einer `.csv`-Datei speichert,
- und sie über eine **Flask-Weboberfläche** als interaktive Diagramme darstellt.

Ideal für Server-Owner, die verstehen möchten, **wer am aktivsten ist**, **wann am meisten geschrieben wird** und **wie sich ihr Server entwickelt**.

---

## ⚙️ Installation & Einrichtung

### 1️⃣ Projekt herunterladen
Lade die ZIP-Datei von GitHub herunter und entpacke sie in einen beliebigen Ordner.

### 2️⃣ Pakete installieren
Starte die Datei:
```
install_packages.bat
```
Dadurch werden alle benötigten Python-Bibliotheken (Flask, pandas, matplotlib usw.) automatisch installiert.

### 3️⃣ Discord Bot erstellen
1. Öffne das [Discord Developer Portal](https://discord.com/developers/applications).  
2. Erstelle eine **neue Application** und füge unter dem Reiter **Bot** einen **Bot-User** hinzu.  
3. Kopiere den **Bot Token** – du benötigst ihn später in der Datei `bot.py`.  
4. Lade den Bot über den OAuth2-Link auf deinen Server ein.

### 4️⃣ Berechtigungen aktivieren
Unter **Privileged Gateway Intents** müssen folgende Optionen aktiviert werden:
- ✅ **MESSAGE CONTENT INTENT**  
- ✅ **SERVER MEMBERS INTENT**  
- ✅ **PRESENCE INTENT**

Diese sind notwendig, damit der Bot Nachrichten lesen und User-Aktivität auswerten kann.

### 5️⃣ Konfiguration
Öffne die Datei **`bot.py`**:
- Trage bei `Tracked Channels` die **Channel-IDs** ein, die getrackt werden sollen.  
- Füge ganz unten deinen **Bot Token** ein.  

---

## ▶️ Nutzung

### 🧩 Bot starten
```bash
python bot.py
```
Der Bot beginnt, Nachrichten, User und Channel-Aktivität zu tracken und speichert sie in einer `.csv`-Datei.

### 🌐 Flask-Dashboard starten
```bash
python app.py
```
Die Website öffnet ein Dashboard, das dir zeigt:
- Welche User am aktivsten sind  
- Welche Channels am meisten genutzt werden  
- Wie sich die Aktivität im Zeitverlauf verändert  

---

## 📈 Features

- 💬 **Nachrichten-Tracking** – analysiere, wer wie viel schreibt  
- 🗂️ **Channel-Statistiken** – sieh, welche Kanäle am aktivsten sind  
- 📁 **CSV-Datenspeicherung** – alle Daten lokal verfügbar  
- 🌐 **Web-Dashboard** – übersichtliche Diagramme dank Flask  
- ⚡ **Einfache Einrichtung** – kein kompliziertes Setup notwendig  

---

## 🧩 Verwendete Technologien

| Technologie | Beschreibung |
|--------------|--------------|
| [Python](https://www.python.org/) | Hauptprogrammiersprache |
| [Discord.py](https://discordpy.readthedocs.io/en/stable/) | Kommunikation mit der Discord API |
| [Flask](https://flask.palletsprojects.com/) | Webserver & Dashboard |
| [Pandas](https://pandas.pydata.org/) | Datenanalyse & CSV-Verarbeitung |
| [Matplotlib](https://matplotlib.org/) | Diagramme & Visualisierung |

---

## 🛠️ Wichtige CMD Befehle

```bash
# Bot starten
python bot.py

# Flask-Webseite starten
python app.py
```

---

## 🧾 Lizenz

Dieses Projekt steht unter der **MIT-Lizenz**.  
Du kannst den Code frei nutzen, verändern und teilen — Credits sind immer willkommen 🙌  
