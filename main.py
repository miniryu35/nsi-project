import pygame
from sys import exit
import random

pygame.init()
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption('Jeu Tik Tok de con')
clock = pygame.time.Clock()

# Chargement des images
cube1_surf = pygame.image.load('images/cube1.png')
cube2_surf = pygame.image.load('images/cube2.png')

# Initialisation des listes pour stocker les cubes
cubes1 = []
cubes2 = []

# Couleurs
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

# Font pour les boutons et PV
font = pygame.font.Font(None, 36)

# Boutons
button_cube1_rect = pygame.Rect(50, 600, 200, 50)
button_cube2_rect = pygame.Rect(450, 600, 200, 50)

# Fonction pour générer un cube avec une vitesse aléatoire et 10 PV
def create_cube(image, x, y):
    rect = image.get_rect(midbottom=(x, y))
    
    # Ajuste la position pour éviter les coins ou les bords
    rect.x = max(10, min(700 - rect.width - 10, rect.x))  # Conserve les cubes à l'intérieur des bords horizontaux
    rect.y = max(10, min(700 - rect.height - 10, rect.y))  # Conserve les cubes à l'intérieur des bords verticaux
    
    velocity = [random.randint(-5, 5), random.randint(-5, 5)]
    if velocity == [0, 0]:  # Assure que les vitesses ne sont jamais nulles
        velocity = [1, 1]
    hp = 10
    return {'surface': image, 'rect': rect, 'velocity': velocity, 'hp': hp, 'original_size': rect.size}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_cube1_rect.collidepoint(event.pos):
                cubes1.append(create_cube(cube1_surf, random.randint(50, 650), random.randint(100, 500)))
            if button_cube2_rect.collidepoint(event.pos):
                cubes2.append(create_cube(cube2_surf, random.randint(50, 650), random.randint(100, 500)))

    # Mise à jour des positions des cubes
    for cube in cubes1:
        cube['rect'].x += cube['velocity'][0]
        cube['rect'].y += cube['velocity'][1]

        # Gestion des collisions avec les bords
        if cube['rect'].left < 0 or cube['rect'].right > 700:
            cube['velocity'][0] *= -1
        if cube['rect'].top < 0 or cube['rect'].bottom > 700:
            cube['velocity'][1] *= -1

    for cube in cubes2:
        cube['rect'].x += cube['velocity'][0]
        cube['rect'].y += cube['velocity'][1]

        # Gestion des collisions avec les bords
        if cube['rect'].left < 0 or cube['rect'].right > 700:
            cube['velocity'][0] *= -1
        if cube['rect'].top < 0 or cube['rect'].bottom > 700:
            cube['velocity'][1] *= -1

    # Gestion des collisions entre cubes similaires (Cube1)
    for i, cube1 in enumerate(cubes1):
        for j, cube2 in enumerate(cubes1):
            if i != j and cube1['rect'].colliderect(cube2['rect']):
                # Résolution des collisions
                if abs(cube1['rect'].right - cube2['rect'].left) < 10 or abs(cube1['rect'].left - cube2['rect'].right) < 10:
                    cube1['velocity'][0] *= -1
                    cube2['velocity'][0] *= -1
                if abs(cube1['rect'].bottom - cube2['rect'].top) < 10 or abs(cube1['rect'].top - cube2['rect'].bottom) < 10:
                    cube1['velocity'][1] *= -1
                    cube2['velocity'][1] *= -1
             

    # Gestion des collisions entre cubes similaires 
    for i, cube1 in enumerate(cubes2):
        for j, cube2 in enumerate(cubes2):
            if i != j and cube1['rect'].colliderect(cube2['rect']):
                # Résolution des collisions
                if abs(cube1['rect'].right - cube2['rect'].left) < 10 or abs(cube1['rect'].left - cube2['rect'].right) < 10:
                    cube1['velocity'][0] *= -1
                    cube2['velocity'][0] *= -1
                if abs(cube1['rect'].bottom - cube2['rect'].top) < 10 or abs(cube1['rect'].top - cube2['rect'].bottom) < 10:
                    cube1['velocity'][1] *= -1
                    cube2['velocity'][1] *= -1
               

    # Gestion des collisions entre cubes1 et cubes2
    for cube1 in cubes1:
        for cube2 in cubes2:
            if cube1['rect'].colliderect(cube2['rect']):
                # Dégâts sur les côtés pour Cube1
                if abs(cube1['rect'].right - cube2['rect'].left) < 10 or abs(cube1['rect'].left - cube2['rect'].right) < 10:
                    cube2['hp'] -= 1
                    cube1['velocity'][0] *= -1
                    cube2['velocity'][0] *= -1
                    # Rétrécissement du cube2
                    cube2['rect'].inflate_ip(-5, -5)
                    cube2['surface'] = pygame.transform.scale(cube2['surface'], cube2['rect'].size)

                # Dégâts sur le haut et le bas pour Cube2
                if abs(cube2['rect'].top - cube1['rect'].bottom) < 10 or abs(cube2['rect'].bottom - cube1['rect'].top) < 10:
                    cube1['hp'] -= 1
                    cube1['velocity'][1] *= -1
                    cube2['velocity'][1] *= -1
                    # Rétrécissement du cube1
                    cube1['rect'].inflate_ip(-5, -5)
                    cube1['surface'] = pygame.transform.scale(cube1['surface'], cube1['rect'].size)

    # Suppression des cubes avec 0 PV
    cubes1 = [cube for cube in cubes1 if cube['hp'] > 0]
    cubes2 = [cube for cube in cubes2 if cube['hp'] > 0]

    # Dessin à l'écran
    screen.fill((0, 0, 0))

    # Dessin des boutons
    pygame.draw.rect(screen, GRAY, button_cube1_rect)
    pygame.draw.rect(screen, GRAY, button_cube2_rect)
    screen.blit(font.render('Ajouter Cube1', True, WHITE), (button_cube1_rect.x + 20, button_cube1_rect.y + 10))
    screen.blit(font.render('Ajouter Cube2', True, WHITE), (button_cube2_rect.x + 20, button_cube2_rect.y + 10))

    # Dessin des cubes et affichage des PV
    for cube in cubes1:
        screen.blit(cube['surface'], cube['rect'])
        hp_text = font.render(str(cube['hp']), True, WHITE)
        screen.blit(hp_text, (cube['rect'].centerx - hp_text.get_width() // 2, cube['rect'].top - 20))

    for cube in cubes2:
        screen.blit(cube['surface'], cube['rect'])
        hp_text = font.render(str(cube['hp']), True, WHITE)
        screen.blit(hp_text, (cube['rect'].centerx - hp_text.get_width() // 2, cube['rect'].top - 20))

    pygame.display.update()
    clock.tick(60)

