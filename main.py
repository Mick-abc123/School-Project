import pygame
import sys

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
weiss = (255, 255, 255)  # Weiß
schwarz = (0, 0, 0)      # Schwarz
grau = (200, 200, 200)  # Grau
blau = (0, 0, 255)      # Blau
rot = (255, 0, 0)       # Rot
hell_grau = (150, 150, 150)  # Heller Grau für deaktivierte Levels

# Klasse für Buttons erstellen
class Button:
    def __init__(self, text, position, breite, hoehe, farbe, hover_farbe, transparenz=128):
        self.text = text  # Text auf dem Button
        self.position = position  # Position des Buttons
        self.breite = breite  # Breite des Buttons
        self.hoehe = hoehe  # Höhe des Buttons
        self.farbe = farbe  # Normale Farbe des Buttons
        self.hover_farbe = hover_farbe  # Farbe, wenn man mit der Maus drüberfährt
        self.transparenz = transparenz  # Transparenzstufe
        self.rechteck = pygame.Rect(position, (breite, hoehe))  # Rechteck für den Button
        
        # Erstellen einer transparenten Oberfläche für den Button
        self.ooberflaeche = pygame.Surface((breite, hoehe), pygame.SRCALPHA)
        self.update_button()

    def update_button(self):
        # Zeichnen des Buttons auf der Oberfläche
        self.ooberflaeche.fill(self.farbe)
        pygame.draw.rect(self.ooberflaeche, self.farbe, self.rechteck.inflate(-10, -10))  # Button-Hintergrund
        text_ooberflaeche = schriftart.render(self.text, True, schwarz)
        text_rechteck = text_ooberflaeche.get_rect(center=(self.breite // 2, self.hoehe // 2))
        self.ooberflaeche.blit(text_ooberflaeche, text_rechteck)
        self.ooberflaeche.set_alpha(self.transparenz)

    # Button zeichnen
    def zeichnen(self, bildschirm):
        maus_position = pygame.mouse.get_pos()  # Mausposition abfragen
        if self.rechteck.collidepoint(maus_position):
            pygame.draw.rect(bildschirm, self.hover_farbe, self.rechteck)
        else:
            bildschirm.blit(self.ooberflaeche, self.rechteck.topleft)
        
        # Text auf dem Button anzeigen
        bildschirm.blit(self.ooberflaeche, self.rechteck.topleft)

    # Prüfen, ob der Button geklickt wurde
    def ist_geklickt(self):
        maus_position = pygame.mouse.get_pos()  # Mausposition abfragen
        if self.rechteck.collidepoint(maus_position):
            if pygame.mouse.get_pressed()[0]:  # Linke Maustaste
                return True
        return False

# Funktion zum Einlesen der Level-Verfügbarkeit
def lade_level_verfuegbarkeit(dateiname):
    level_status = {}
    try:
        with open(dateiname, 'r') as datei:
            for zeile in datei:
                zeile = zeile.strip()
                if not zeile or zeile.startswith("#"):  # Ignoriere leere Zeilen und Kommentare
                    continue
                schluessel, wert = zeile.split('=')
                schluessel = schluessel.strip()
                wert = wert.strip().lower()
                if wert in ['available', 'unavailable']:
                    level_status[schluessel] = wert == 'available'
    except FileNotFoundError:
        print(f"Konfigurationsdatei {dateiname} nicht gefunden.")
    return level_status

# Level-Verfügbarkeit einlesen
level_verfuegbarkeit = lade_level_verfuegbarkeit('Levelcheck.cfg')

# Erstellen der Level-Buttons
level_buttons = {}
level_liste = [
    {"nummer": "1", "position": (150, 200)},
    {"nummer": "2", "position": (300, 200)},
    {"nummer": "3", "position": (450, 200)},
    {"nummer": "4", "position": (600, 200)}
]

for level in level_liste:
    verfuegbar = level_verfuegbarkeit.get(f"level_{level['nummer']}", False)
    farbe = blau if verfuegbar else hell_grau
    level_buttons[level["nummer"]] = Button(level["nummer"], level["position"], 100, 100, farbe, weiss, transparenz=128)

# Buttons erstellen für Menü
start_button = Button("Start", (300, 200), 200, 50, grau, weiss, transparenz=128)  # Start-Button
quit_button = Button("Beenden", (300, 300), 200, 50, grau, weiss, transparenz=128)  # Beenden-Button

# Spielzustände definieren
MENUE = "menue"
LEVEL_AUSWAHL = "level_auswahl"
aktueller_zustand = MENUE  # Startet im Menü

# Hauptschleife des Spiels
while True:
    # Events (Ereignisse) behandeln
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:  # Wenn das Fenster geschlossen wird
            pygame.quit()  # Pygame beenden
            sys.exit()     # Programm beenden

    # Bildschirm füllen, um alte Inhalte zu löschen
    bildschirm.fill(schwarz)  # Hier kannst du auch eine andere Farbe oder ein Hintergrundbild verwenden

    if aktueller_zustand == MENUE:  # Wenn wir im Menü sind
        # Hintergrundbild zeichnen
        bildschirm.blit(menue_hintergrund_bild, (0, 0))

        # Buttons zeichnen
        start_button.zeichnen(bildschirm)
        quit_button.zeichnen(bildschirm)

        # Prüfen, ob Buttons geklickt wurden
        if start_button.ist_geklickt():
            aktueller_zustand = LEVEL_AUSWAHL  # In den Level-Auswahlzustand wechseln
        if quit_button.ist_geklickt():
            pygame.quit()  # Pygame beenden
            sys.exit()     # Programm beenden

    elif aktueller_zustand == LEVEL_AUSWAHL:  # Wenn wir im Level-Auswahlzustand sind
        # Hintergrundbild zeichnen
        bildschirm.blit(level_auswahl_hintergrund_bild, (0, 0))

        # Caption für die Level-Auswahl
        caption_text = schriftart.render("Wähle das Level", True, weiss)
        caption_rechteck = caption_text.get_rect(center=(bildschirm_breite // 2, 50))  # Zentriert oben
        bildschirm.blit(caption_text, caption_rechteck)

        # "Zurück"-Button erstellen
        zurueck_button = Button("Zurück", (20, 20), 100, 50, grau, weiss, transparenz=128)
        zurueck_button.zeichnen(bildschirm)

        # Level-Buttons zeichnen
        for level_nummer, button in level_buttons.items():
            button.zeichnen(bildschirm)

        # Prüfen, ob "Zurück"-Button geklickt wurde
        if zurueck_button.ist_geklickt():
            aktueller_zustand = MENUE  # Zurück zum Menü

        # Prüfen, ob ein Level ausgewählt wurde
        for level_nummer, button in level_buttons.items():
            if button.rechteck.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:  # Linke Maustaste
                if level_verfuegbarkeit.get(f"level_{level_nummer}", False):
                    print(f"Level {level_nummer} ausgewählt")
                else:
                    print(f"Level {level_nummer} ist derzeit nicht verfügbar")

    # Bildschirm aktualisieren
    pygame.display.update()