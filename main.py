import pygame
import os
import json
import random
import time
import Cocoa

#Setup
pygame.init()

def getfilesindirectory(directory):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.iso'):
                files.append(os.path.join(root, filename))
    return files

def eatFile(file):
    global fullness 
    print("Eating file:", file)
    if os.path.exists(file):
        file_size = os.path.getsize(file) / (1024 * 1024) 
        print(f"File size: {file_size} MB")
        fullness += file_size
        print(f"Fullness increased to: {fullness} MB")
        os.remove(file)
    else:
        print("File not found!")

window_x = 500
window_y = 350
display_x = pygame.display.Info().current_w
display_y = pygame.display.Info().current_h

x = display_x - window_x
y = display_y - window_y

os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"

try:
    with open('petmem.json', 'r') as petmemory:
        petmemory_data = json.load(petmemory)
    fullness = petmemory_data.get('fullness', 100)
except FileNotFoundError:
    print("Pet memory file not found. Setting fullness to 100.")
    fullness = 100
except json.JSONDecodeError:
    print("Error in pet memory file. Setting fullness to 100.")
    fullness = 100
try:
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
    pet = config_data.get('pet', 'burger')
    hthreshold = config_data.get('hunger_threshold', 5)
    hrate = config_data.get('hunger_rate', 5)
    emergency_food_folder = config_data.get('food_folder', 5)
    tickspeed = config_data.get('tickspeed', 0.5)
    if config_data.get('custom_mode', False) == 'true':
        custom_mode = True
        pet = config_data.get('custom_pet', 'burger')
    else:
        custom_mode = False
        pet = config_data.get('pet', 'burger')
except FileNotFoundError:
    print("Config file not found. Using default pet.")
    pet = 'burger'
except json.JSONDecodeError:
    print("Error in config file. Using default pet.")
    pet = 'burger'


print("Deskpet Version 1.0, Pet:", pet)

if pet == "prophet orpheus":
    pet_sprites = ["./pets/orpheus/idle.png", "./pets/orpheus/idle2.png","./pets/orpheus/idle3.png", "./pets/orpheus/idle4.png", "./pets/orpheus/sleep.png", "./pets/orpheus/sleep2.png", "./pets/orpheus/sleep3.png"]
elif pet == "burger":
    pet_sprites = ["./pets/burger/idle.png", "./pets/burger/idle2.png", "./pets/burger/idle3.png", "./pets/burger/idle4.png", "./pets/burger/sleep.png", "./pets/burger/sleep2.png", "./pets/burger/sleep3.png"]
elif pet == "pizza":
    pet_sprites = ["./pets/pizza/idle.png", "./pets/pizza/idle2.png", "./pets/pizza/idle3.png", "./pets/pizza/idle4.png", "./pets/pizza/sleep.png", "./pets/pizza/sleep2.png", "./pets/pizza/sleep3.png"]

elif custom_mode == True:
    print("Loading custom pet...")
    pet_sprites = [f"./pets/{pet}/idle.png", f"./pets/{pet}/idle2.png", f"./pets/{pet}/idle3.png", f"./pets/{pet}/idle4.png", f"./pets/{pet}/sleep.png", f"./pets/{pet}/sleep2.png", f"./pets/{pet}/sleep3.png"]
else:
    print("Unable to load pet sprites. Defaulting to burger.")
    pet_sprites = ["./pets/burger/idle.png", "./pets/burger/idle2.png", "./pets/burger/idle3.png",  "./pets/burger/idle4.png", "./pets/burger/sleep.png", "./pets/burger/sleep2.png", "./pets/burger/sleep3.png"]

print("Sprites loaded for:", pet, pet_sprites)
windoww, windowh = 300, 300

screen = pygame.display.set_mode((windoww, windowh), pygame.NOFRAME)

pygame.display.set_caption("Deskpet")

def save_pet_memory():
    with open('petmem.json', 'w') as petmemory:
        json.dump({'fullness': fullness}, petmemory)


sprite = pygame.image.load(pet_sprites[random.randint(4,6)]).convert_alpha()
sleeping = False
running = True
while running:
    randvar = random.randint(0, 100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.DROPFILE & sleeping == False:
            filepath = event.file
            eatFile(filepath)
    #idle animation handling
    if sleeping == False:
        sprite = pygame.image.load(pet_sprites[random.randint(0,3)]).convert_alpha()
    screen.blit(sprite, (50, 50))
    time.sleep(tickspeed)
    pygame.display.flip()
    #hunger handling
    filepath = getfilesindirectory(emergency_food_folder)
    fullness -= hrate
    print("Fullness:", fullness)
    if fullness <= hthreshold & sleeping == False:
        filepath = getfilesindirectory(emergency_food_folder)
        print("Hunger threshold reached. Eating file...")
        if filepath:  # Check if filepath is not empty
            eatFile(filepath[0])
        else:
            print(f"No food files found in {emergency_food_folder} to eat.")
    save_pet_memory()
    #Sleeping handling
    if sleeping == False & 25 == random.randint(0, 50):
        if fullness <= 0:
            print("Your pet is hungry! it's going to sleep!")
            sleeping = True
            sprite = pygame.image.load(pet_sprites[random.randint(4,6)]).convert_alpha()
        elif fullness > 0:
            print("Your pet is tired! it's going to sleep!")
            sleeping = True
    if sleeping == True:
        sprite = pygame.image.load(pet_sprites[random.randint(4,6)]).convert_alpha()
    if randvar < random.randint(0, 100) & sleeping == True:
        print("Your pet is awake! it had a good nap!")
        sleeping = False
        sprite = pygame.image.load(pet_sprites[random.randint(0,3)]).convert_alpha()
pygame.quit()