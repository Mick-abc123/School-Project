import pygame
import sys
import os
import time

# Pygame starten
pygame.init()

# Fenstergröße festlegen
bildschirm_breite = 800
bildschirm_hoehe = 800
bildschirm = pygame.display.set_mode((bildschirm_breite, bildschirm_hoehe))
pygame.display.set_caption("Erstes GUI mit Hintergrund")

# Hintergrundbilder laden
menue_hintergrund_bild = pygame.image.load("Pics/Background.png")
level_auswahl_hintergrund_bild = pygame.image.load("Pics/LevelSelectBackground.png")

# Schriftart festlegen
schriftart = pygame.font.Font(None, 40)

# Farben definieren
weiss = (255, 255, 255)
schwarz = (0, 0, 0)
grau = (200, 200, 200)
blau = (0, 0, 255)
hell_grau = (150, 150, 150)

# Klasse für Buttons erstellen
class Button:
    def __init__(self, text, position, breite, hoehe, farbe, hover_farbe, transparenz=128):
        self.text = text
        self.position = position
        self.breite = breite
        self.hoehe = hoehe
        self.farbe = farbe
        self.hover_farbe = hover_farbe
        self.transparenz = transparenz
        self.rechteck = pygame.Rect(position, (breite, hoehe))

    def zeichnen(self, bildschirm):
        maus_position = pygame.mouse.get_pos()
        button_farbe = self.hover_farbe if self.rechteck.collidepoint(maus_position) else self.farbe
        pygame.draw.rect(bildschirm, button_farbe, self.rechteck)

        text_ooberflaeche = schriftart.render(self.text, True, schwarz)
        text_rechteck = text_ooberflaeche.get_rect(center=self.rechteck.center)
        bildschirm.blit(text_ooberflaeche, text_rechteck)

    def ist_geklickt(self):
        maus_position = pygame.mouse.get_pos()
        return self.rechteck.collidepoint(maus_position) and pygame.mouse.get_pressed()[0]

# Funktion zum Einlesen der Level-Verfügbarkeit
def lade_level_verfuegbarkeit(dateiname):
    level_status = {}
    try:
        with open(dateiname, 'r') as datei:
            for zeile in datei:
                zeile = zeile.strip()
                if not zeile or zeile.startswith("#"):
                    continue
                schluessel, wert = zeile.split('=')
                schluessel = schluessel.strip()
                wert = wert.strip().lower()
                if wert in ['available', 'unavailable']:
                    level_status[schluessel] = wert == 'available'
    except FileNotFoundError:
        print(f"Konfigurationsdatei {dateiname} nicht gefunden.")
    return level_status

# Funktion zum Aktualisieren der Level-Verfügbarkeit
def aktualisiere_level_verfuegbarkeit(dateiname, level_id, neuer_status):
    level_status = lade_level_verfuegbarkeit(dateiname)
    level_status[level_id] = neuer_status
    with open(dateiname, 'w') as datei:
        for key, value in level_status.items():
            datei.write(f"{key} = {value}\n")

# Funktion zum Erstellen der Level-Buttons
def erstelle_level_buttons(level_liste, level_availability):
    level_buttons = {}
    for level in level_liste:
        verfuegbar = level_availability.get(f"level_{level['nummer']}", False)
        farbe = blau if verfuegbar else hell_grau
        level_buttons[level["nummer"]] = Button(level["nummer"], level["position"], 100, 100, farbe, weiss, transparenz=128)
    return level_buttons

# Level-Verfügbarkeit einlesen
level_verfuegbarkeit = lade_level_verfuegbarkeit('Levelcheck.cfg')

# Erstellen der Level-Buttons
level_liste = [
    {"nummer": "1", "position": (150, 200)},
    {"nummer": "2", "position": (300, 200)},
    {"nummer": "3", "position": (450, 200)},
    {"nummer": "4", "position": (600, 200)}
]
level_buttons = erstelle_level_buttons(level_liste, level_verfuegbarkeit)

# Buttons erstellen für Menü
start_button = Button("Start", (300, 200), 200, 50, grau, weiss, transparenz=128)
quit_button = Button("Beenden", (300, 300), 200, 50, grau, weiss, transparenz=128)

# Spielzustände definieren
MENUE = "menue"
LEVEL_AUSWAHL = "level_auswahl"
aktueller_zustand = MENUE

# Zeit des letzten Klicks initialisieren
letzter_klick_zeitpunkt = time.time()

# Hauptschleife des Spiels
while True:
    # Events (Ereignisse) behandeln
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Bildschirm füllen
    bildschirm.fill(schwarz)

    if aktueller_zustand == MENUE:
        bildschirm.blit(menue_hintergrund_bild, (0, 0))
        start_button.zeichnen(bildschirm)
        quit_button.zeichnen(bildschirm)

        if start_button.ist_geklickt():
            aktueller_zustand = LEVEL_AUSWAHL
        if quit_button.ist_geklickt():
            pygame.quit()
            sys.exit()

    elif aktueller_zustand == LEVEL_AUSWAHL:
        bildschirm.blit(level_auswahl_hintergrund_bild, (0, 0))

        caption_text = schriftart.render("Wähle das Level", True, weiss)
        caption_rechteck = caption_text.get_rect(center=(bildschirm_breite // 2, 50))
        bildschirm.blit(caption_text, caption_rechteck)

        zurueck_button = Button("Zurück", (20, 20), 100, 50, grau, weiss, transparenz=128)
        zurueck_button.zeichnen(bildschirm)

        # Level-Buttons zeichnen
        for level_nummer, button in level_buttons.items():
            button.zeichnen(bildschirm)

        if zurueck_button.ist_geklickt():
            aktueller_zustand = MENUE

        for level_nummer, button in level_buttons.items():
            if button.ist_geklickt():
                aktuelle_zeit = time.time()
                if aktuelle_zeit - letzter_klick_zeitpunkt > 0.5:
                    letzter_klick_zeitpunkt = aktuelle_zeit
                    if level_verfuegbarkeit.get(f"level_{level_nummer}", False):
                        print(f"Level {level_nummer} ausgewählt")
                        if level_nummer == "1":  # Beispiel für Level 1
                            os.system("python C:\\Users\\Laptop\\Documents\\Schul-Projekt\\Levels\\Level-1.py")
                            # Update level availability after completing the level
                            aktualisiere_level_verfuegbarkeit('Levelcheck.cfg', 'level_2', 'available')
                            # Refresh level buttons
                            level_verfuegbarkeit = lade_level_verfuegbarkeit('Levelcheck.cfg')
                            level_buttons = erstelle_level_buttons(level_liste, level_verfuegbarkeit)
                    else:
                        print(f"Level {level_nummer} ist derzeit nicht verfügbar")

    pygame.display.update()
