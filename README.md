📊 Discordlytics

Discordlytics ist ein Discord-Tracking-Tool mit Web-Dashboard.
Der Bot sammelt Serveraktivitäten (z. B. Nachrichten, Useraktivität, Channels) und speichert sie in einer CSV-Datei.
Eine Flask-Webanwendung liest die Daten ein und visualisiert sie mit klaren Diagrammen.

⚙️ Installation & Einrichtung

ZIP herunterladen und entpacken.

install_packages.bat ausführen – alle benötigten Python-Bibliotheken werden automatisch installiert.

Währenddessen:

Erstelle im Discord Developer Portal
 eine neue Application und unter dem Reiter Bot einen Bot-User.

Kopiere den Bot Token (wird später in bot.py benötigt).

Lade den Bot über den OAuth2-Link auf deinen Server ein.

Aktiviere folgende Berechtigungen (Intents) im Developer Portal:

✅ MESSAGE CONTENT INTENT

✅ SERVER MEMBERS INTENT

✅ PRESENCE INTENT

Diese sind notwendig, damit der Bot Nachrichten lesen, Mitglieder tracken und Aktivität erfassen kann.

Öffne bot.py

Trage bei Tracked Channels die Channel-IDs ein, die getrackt werden sollen.

Füge ganz unten deinen Bot Token ein.

▶️ Nutzung

Bot starten:

python bot.py


Der Bot beginnt, Nachrichten und Aktivitäten zu tracken und speichert sie automatisch in einer .csv-Datei.

Web-Dashboard starten:

python app.py


Die Flask-Website zeigt alle wichtigen Diagramme und Statistiken – z. B. wer am meisten schreibt oder welche Channels am aktivsten sind.

💡 Features

Automatisches Tracking von Nachrichten, Usern & Channel-Aktivität

Speicherung aller Daten in einer CSV-Datei

Interaktive Diagramme & Statistiken via Flask

Übersichtliche Analyse, welcher User am aktivsten ist

Einfache Einrichtung mit nur zwei Python-Skripten
