Anleitung: Noten verteilen
Mit dem Skript "Noten verteilen.py" kannst du Noten einer bestimmten Komposition schnell und einfach in einen Ordner kopieren, der für eine bevorstehende Probe verwendet wird. Hier ist eine Anleitung, wie du das Skript benutzen kannst:

Öffne das Skript "Noten verteilen.py".
Wähle in dem sich öffnenden Fenster die gewünschte Komposition aus dem Dropdown-Menü aus.
Gib das gewünschte Probedatum im dafür vorgesehenen Eingabefeld ein. Das Datum muss im Format JJJJ.MM.TT eingegeben werden (z.B. 2022.03.03).
Klicke auf den Button "Noten kopieren".
Das Skript wird nun automatisch alle Noten der gewählten Komposition suchen und kopieren, für die es Noten gibt.
Die Noten werden nun in einen Ordner im Verzeichnis "Probenmaterial" kopiert, dessen Name sich aus dem Probedatum und dem Wort "Vortrag" zusammensetzt (z.B. "Vortrag 2022.03.03").
Wichtig: Noten, die bereits im Zielordner vorhanden sind, aber ein älteres Datum aufweisen, bleiben unverändert.

Setup
Um das Skript "Noten verteilen.py" auszuführen, benötigst du eine installierte Python-Umgebung. Solltest du noch keine haben, kannst du sie unter https://www.python.org/downloads/ herunterladen und installieren.

Ordnerstruktur
Das Skript erwartet, dass die Noten in einer bestimmten Ordnerstruktur abgelegt werden. Hier ist eine Übersicht über die erwartete Ordnerstruktur:

python
Copy code
- Projektordner
  |- Noten verteilen.py
  |- Kompositionen
  |  |- Komposition 1
  |  |  |- Einzelstimmen
  |  |  |  |- Noten für Instrument 1 (z.B. "klarinette_2022.03.03.pdf").
  |  |  |  |- Noten für Instrument 2 (z.B. "flöte_2022.03.03.pdf").
  |  |- Komposition 2
  |  |  |- Einzelstimmen
  |  |  |  |- Noten für Instrument 1 (z.B. "klarinette_2022.03.03.pdf").
  |  |  |  |- Noten für Instrument 2 (z.B. "flöte_2022.03.03.pdf").
  |- Proben
