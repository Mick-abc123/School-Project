import pygame
import sys

# Pygame initialisieren
pygame.init()

# Fenstergröße festlegen
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Level 1")

# Farben definieren
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Schriftart für den Timer
font = pygame.font.Font(None, 36)  # Standard-Schriftart mit Größe 36

# Spieler-Model laden
player_image = pygame.image.load("C:/Users/Laptop/Documents/Schul-Projekt/Levels/Player.png")
player_image = pygame.transform.scale(player_image, (50, 50))  # Größe des Bildes anpassen
player_rect = player_image.get_rect()  # Rechteck des Spielers
player_rect.topleft = [100, screen_height - 100]  # Startposition des Spielers (nah am Boden)

# Zielposition und -größe
target_pos = [700, screen_height - 100]  # Ziel in der Nähe des Bodens platzieren
target_size = 50

# Sprungvariablen
jumping = False
jump_speed = 15  # Angepasste Sprunggeschwindigkeit
gravity = 0.25  # Leichtere Schwerkraft
player_y_velocity = 0

# Bewegungsgeschwindigkeit des Spielers
player_speed = 5

# Bodenhöhe
ground_height = screen_height - 50  # Höhe des Bodens (50 Pixel vom unteren Rand entfernt)

# Startzeit des Spiels
start_ticks = pygame.time.get_ticks()  # Zeit in Millisekunden seit Spielstart

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
                    level_status[schluessel] = wert
    except FileNotFoundError:
        print(f"Konfigurationsdatei {dateiname} nicht gefunden.")
    return level_status

# Funktion zum Aktualisieren der Level-Verfügbarkeit
def aktualisiere_level_verfuegbarkeit(dateiname, level_id, neuer_status):
    level_status = lade_level_verfuegbarkeit(dateiname)
    level_status[level_id] = neuer_status
    with open(dateiname, 'w') as datei:
        for schluessel, wert in level_status.items():
            datei.write(f"{schluessel} = {wert}\n")

# Hauptschleife des Spiels
while True:
    # Ereignisse abfragen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not jumping:  # Sprung auslösen
                jumping = True
                player_y_velocity = -jump_speed  # Sprunggeschwindigkeit nach oben

    # Tasten abfragen
    keys = pygame.key.get_pressed()

    # Bewegung links/rechts ermöglichen, egal ob in der Luft oder auf dem Boden
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < screen_width:
        player_rect.x += player_speed

    # Sprungmechanik
    if jumping:
        player_rect.y += player_y_velocity
        player_y_velocity += gravity  # Schwerkraft anwenden

        # Überprüfen, ob der Spieler den Boden berührt (d.h. wieder landet)
        if player_rect.bottom >= ground_height:  # Bodenhöhe
            player_rect.bottom = ground_height
            jumping = False  # Sprung beenden
            player_y_velocity = 0

    # Überprüfung, ob der Spieler das Ziel erreicht hat
    if player_rect.colliderect(pygame.Rect(target_pos[0], target_pos[1], target_size, target_size)):
        print("Level 1 abgeschlossen!")
        aktualisiere_level_verfuegbarkeit('Levelcheck.cfg', 'level_2', 'available')
        pygame.quit()
        sys.exit()

    # Verstrichene Zeit berechnen
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # Zeit in Sekunden umwandeln
    timer_text = font.render(f"Zeit: {elapsed_time:.2f} Sekunden", True, black)  # Text für den Timer erstellen

    # Bildschirm mit Weiß füllen
    screen.fill(white)

    # Timer zeichnen (oben im Bildschirm)
    screen.blit(timer_text, (10, 10))

    # Spieler und Ziel zeichnen
    screen.blit(player_image, player_rect)
    pygame.draw.rect(screen, red, (target_pos[0], target_pos[1], target_size, target_size))

    # Bildschirm aktualisieren
    pygame.display.update()
    pygame.time.Clock().tick(120)
