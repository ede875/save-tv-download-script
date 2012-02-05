VORAUSSETZUNGEN:

- Python
- das Pythonmodul "python-mechanize"
- wget
- ein Save.tv Account
- eine Internetverbindung

==========================================================================
DISCLAIMER:

Der Autor uebernimmt keinerlei Haftung fuer Schaeden, die durch 
den Gebrauch der Software entstehen.

==========================================================================
LIZENZ:

Die Software wird dem Nutzer unter den Bedingungen der GPL v3
(http://www.gpl.org) zur Verfuegung gestellt.

==========================================================================
CREDITS:

Dieses Skript basiert auf der Idee und dem Quelltext von Oscar Knapp 
(soly.org). Vielen Dank dafür!

Ich hatte das Skript im Einsatz und konnte nach umfangreichen Umbauten
an der save.tv-Seite nicht mehr automatisch downloaden. Darauhin habe
ich das Skript komplett überarbeitet und dabei auch auf wget zum Download
der Aufnahmen umgestellt.

Fehler und Erweiterungswünsche bitte hier einstellen:
http://code.google.com/p/save-tv-download-script/issues/list

==========================================================================
INSTALLATION:

Die Dateien in einem Verzeichnis auf der Festplatte ablegen.
Die Save.tv Nutzerdaten und das Zielverzeichnis für die Aufnahmen in 
der Datei savetv.cfg einstellen.

Die Software wird mit dem Befehl "python stvDld.py" ausgeführt.

Um den Download zu automatisieren kann die Software per cron periodisch
gestartet werden. 

==========================================================================
CHANGELOG:

v.0.1 initiale Veroeffentlichung
v.0.2 Anpassung an geänderte save.tv Seitenstruktur. 
      Verwendung von wget zum Download der Aufnahmen.
      Geänderte Verwaltung von Teildownloads
v.0.3 Aufnahmen können nach erfolgreichem Download aus 
      dem Videoarchiv gelöscht werden.