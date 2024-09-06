import pygame
import sys

# Pygame starten
pygame.init()

# Fenstergröße festlegen
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("First GUI mit background")

# Hintergrundbilder laden
menu_background_image = pygame.image.load("Pics/Background.png")
level_select_background_image = pygame.image.load("Pics/LevelSelectBackground.png")

# Schriftart festlegen
font = pygame.font.Font(None, 40)

# Farben definieren
white = (255, 255, 255)  # Weiß
black = (0, 0, 0)        # Schwarz
gray = (200, 200, 200)    # Grau
blue = (0, 0, 255)       # Blau
red = (255, 0, 0)        # Rot
light_gray = (150, 150, 150)  # Heller Grau für deaktivierte Levels

# Klasse für Buttons erstellen
class Button:
    def __init__(self, text, pos, width, height, color, hover_color, transparency=128):
        self.text = text  # Text auf dem Button
        self.pos = pos    # Position des Buttons
        self.width = width  # Breite des Buttons
        self.height = height  # Höhe des Buttons
        self.color = color  # Normale Farbe des Buttons
        self.hover_color = hover_color  # Farbe, wenn man mit der Maus drüberfährt
        self.transparency = transparency  # Transparenzstufe
        self.rect = pygame.Rect(pos, (width, height))  # Rechteck für den Button
        
        # Erstellen einer transparenten Oberfläche für den Button
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.update_button()

    def update_button(self):
        # Zeichnen des Buttons auf der Oberfläche
        self.surface.fill(self.color)
        pygame.draw.rect(self.surface, self.color, self.rect.inflate(-10, -10))  # Button-Hintergrund
        text_surface = font.render(self.text, True, black)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.surface.blit(text_surface, text_rect)
        self.surface.set_alpha(self.transparency)

    # Button zeichnen
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()  # Mausposition abfragen
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            screen.blit(self.surface, self.rect.topleft)
        
        # Text auf dem Button anzeigen
        screen.blit(self.surface, self.rect.topleft)

    # Prüfen, ob der Button geklickt wurde
    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()  # Mausposition abfragen
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:  # Linke Maustaste
                return True
        return False

# Funktion zum Einlesen der Level-Verfügbarkeit
def load_level_availability(filename):
    level_status = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):  # Ignoriere leere Zeilen und Kommentare
                    continue
                key, value = line.split('=')
                key = key.strip()
                value = value.strip().lower()
                if value in ['available', 'unavailable']:
                    level_status[key] = value == 'available'
    except FileNotFoundError:
        print(f"Configuration file {filename} not found.")
    return level_status

# Level-Verfügbarkeit einlesen
level_availability = load_level_availability('Levelcheck.cfg')

# Erstellen der Level-Buttons
level_buttons = {}
levels = [
    {"number": "1", "pos": (150, 200)},
    {"number": "2", "pos": (300, 200)},
    {"number": "3", "pos": (450, 200)},
    {"number": "4", "pos": (600, 200)}
]

for level in levels:
    available = level_availability.get(f"level_{level['number']}", False)
    color = blue if available else light_gray
    level_buttons[level["number"]] = Button(level["number"], level["pos"], 100, 100, color, white, transparency=128)

# Buttons erstellen für Menü
start_button = Button("Start", (300, 200), 200, 50, gray, white, transparency=128)  # Start-Button
quit_button = Button("Quit", (300, 300), 200, 50, gray, white, transparency=128)   # Quit-Button

# Spielzustände definieren
MENU = "menu"
LEVEL_SELECT = "level_select"
current_state = MENU  # Startet im Menü

# Hauptschleife des Spiels
while True:
    # Events (Ereignisse) behandeln
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Wenn das Fenster geschlossen wird
            pygame.quit()  # Pygame beenden
            sys.exit()     # Programm beenden

    # Bildschirm füllen, um alte Inhalte zu löschen
    screen.fill(black)  # Hier kannst du auch eine andere Farbe oder ein Hintergrundbild verwenden

    if current_state == MENU:  # Wenn wir im Menü sind
        # Hintergrundbild zeichnen
        screen.blit(menu_background_image, (0, 0))

        # Buttons zeichnen
        start_button.draw(screen)
        quit_button.draw(screen)

        # Prüfen, ob Buttons geklickt wurden
        if start_button.is_clicked():
            current_state = LEVEL_SELECT  # In den Level-Auswahlzustand wechseln
        if quit_button.is_clicked():
            pygame.quit()  # Pygame beenden
            sys.exit()     # Programm beenden

    elif current_state == LEVEL_SELECT:  # Wenn wir im Level-Auswahlzustand sind
        # Hintergrundbild zeichnen
        screen.blit(level_select_background_image, (0, 0))

        # Caption für die Level-Auswahl
        caption_text = font.render("Choose the level", True, white)
        caption_rect = caption_text.get_rect(center=(screen_width // 2, 50))  # Zentriert oben
        screen.blit(caption_text, caption_rect)

        # "Zurück"-Button erstellen
        back_button = Button("Zurück", (20, 20), 100, 50, gray, white, transparency=128)
        back_button.draw(screen)

        # Level-Buttons zeichnen
        for level_number, button in level_buttons.items():
            button.draw(screen)

        # Prüfen, ob "Zurück"-Button geklickt wurde
        if back_button.is_clicked():
            current_state = MENU  # Zurück zum Menü

        # Prüfen, ob ein Level ausgewählt wurde
        for level_number, button in level_buttons.items():
            if button.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:  # Linke Maustaste
                if level_availability.get(f"level_{level_number}", False):
                    print(f"Level {level_number} ausgewählt")
                else:
                    print(f"Level {level_number} ist derzeit nicht verfügbar")

    # Bildschirm aktualisieren
    pygame.display.update()
