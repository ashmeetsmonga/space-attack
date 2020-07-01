import pygame
import os
import random

from Laser import collide
from Player import Player
from Enemy import Enemy
pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Attack")

#Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    player_vel = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 1
    laser_vel = 10
    enemy_laser_vel = 4
    lost = False
    lost_count = 0

    player = Player(300, 640)

    clock = pygame.time.Clock()

    def redraw():
        #Adds a background BG
        WIN.blit(BG, (0, 0))

        #Drawing font
        lives_label = main_font.render(f"Lives : {lives}", True, (255, 255, 255))
        level_label = main_font.render(f"Level : {level}", True, (255, 255, 255))

        #Rendering lives and levels
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        # Draws the enemies
        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost :(", True, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH // 2 - lost_label.get_width() // 2, 350))

        #Updates the window
        pygame.display.update()

    #Main loop
    while run:
        clock.tick(FPS)
        redraw()

        #Checks for losing conditions
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        #If lost, displays the lost sign for 3 secs and halts the game
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        #When clearing a level, it increases the level, ships number and add new ships
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red", "green", "blue"]))
                enemies.append(enemy)

        # Stops the window when clicked on quit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #Controlling the ship
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_UP] and player.y + player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 20 < HEIGHT:
            player.y += player_vel
        #Shooting lasers
        if keys[pygame.K_SPACE]:
            player.shoot()

        #Loops through a copy of enemies list to move enemies and check whether they reached the end
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(enemy_laser_vel, player)

            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

#Main Menu
def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press the mouse to begin...", True, (255, 255, 255))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()