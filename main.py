import pygame
import os
import json
import random
import time
import logging
import datetime

logging.basicConfig(filename=f'./logs/deskpet{datetime.date.today()}.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
#Setup
pygame.init()
logging.info("Deskpet started, pygame initialized.")
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
sleep_conunter = 0
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"

logging.info("Reading json data from petmem.json and config.json")
try:
    with open('petmem.json', 'r') as petmemory:
        petmemory_data = json.load(petmemory)
    fullness = petmemory_data.get('fullness', 100)
    logging.info(f"Fullness loaded from petmem.json: {fullness}")
except FileNotFoundError:
    print("Pet memory file not found. Setting fullness to 100.")
    fullness = 100
    logging.warning("Pet memory file not found. Setting fullness to 100.")
except json.JSONDecodeError:
    print("Error in pet memory file. Setting fullness to 100.")
    fullness = 100
    logging.warning("Pet memory file not found. Setting fullness to 100.")
logging.info("Reading config.")
try:
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
    pet = config_data.get('pet', 'burger')
    hthreshold = config_data.get('hunger_threshold', 5)
    hrate = config_data.get('hunger_rate', 5)
    emergency_food_folder = config_data.get('food_folder', 5)
    tickspeed = config_data.get('tickspeed', 0.5)
    logging.info(f"Config loaded: {config_data}")
    if config_data.get('custom_mode', 'false') == 'true':
        custom_mode = True
        logging.info("Custom mode enabled. Loading custom pet.")
        pet = config_data.get('pet', 'burger')
        logging.info(f"Custom pet loaded: {pet}")
    else:
        custom_mode = False
        pet = config_data.get('pet', 'burger')
except FileNotFoundError:
    print("Config file not found. Using default pet.")
    pet = 'burger'
    logging.warning("Config file not found. Using default pet.")
except json.JSONDecodeError:
    print("Error in config file. Using default pet.")
    pet = 'burger'
    logging.warning("Error in config file. Using default pet.")


print("Deskpet Version 1.0, Pet:", pet)

if pet == "prophet orpheus":
    pet_sprites = ["./pets/orpheus/idle.png", "./pets/orpheus/idle2.png","./pets/orpheus/idle3.png", "./pets/orpheus/idle4.png", "./pets/orpheus/sleep.png", "./pets/orpheus/sleep2.png", "./pets/orpheus/sleep3.png"]
    logging.info("Sprites loaded for prophet orpheus!")
elif pet == "burger":
    pet_sprites = ["./pets/burger/idle.png", "./pets/burger/idle2.png", "./pets/burger/idle3.png", "./pets/burger/idle4.png", "./pets/burger/sleep.png", "./pets/burger/sleep2.png", "./pets/burger/sleep3.png"]
    logging.info("Sprites loaded for burger the dog!")
elif pet == "pizza":
    pet_sprites = ["./pets/pizza/idle.png", "./pets/pizza/idle2.png", "./pets/pizza/idle3.png", "./pets/pizza/idle4.png", "./pets/pizza/sleep.png", "./pets/pizza/sleep2.png", "./pets/pizza/sleep3.png"]
    logging.info("Sprites loaded for pizza the cat!")
elif custom_mode == True:
    print("Loading custom pet...")
    pet_sprites = [f"./pets/{pet}/idle.png", f"./pets/{pet}/idle2.png", f"./pets/{pet}/idle3.png", f"./pets/{pet}/idle4.png", f"./pets/{pet}/sleep.png", f"./pets/{pet}/sleep2.png", f"./pets/{pet}/sleep3.png"]
    logging.info(f"Custom pet sprites loaded for {pet}!")
else:
    print("Unable to load pet sprites. Defaulting to burger.")
    pet_sprites = ["./pets/burger/idle.png", "./pets/burger/idle2.png", "./pets/burger/idle3.png",  "./pets/burger/idle4.png", "./pets/burger/sleep.png", "./pets/burger/sleep2.png", "./pets/burger/sleep3.png"]
    logging.warning("Unable to load pet sprites. Defaulting to burger.")

print("Sprites loaded for:", pet, pet_sprites)
time.sleep(tickspeed)
windoww, windowh = 300, 300

screen = pygame.display.set_mode((windoww, windowh), pygame.NOFRAME)

pygame.display.set_caption("Deskpet")
logging.info("Window setup complete.")
def save_pet_memory():
    with open('petmem.json', 'w') as petmemory:
        json.dump({'fullness': fullness}, petmemory)


sprite = pygame.image.load(pet_sprites[random.randint(4,6)]).convert_alpha()
sleeping = False
running = True
logging.info("Beggining main loop.")
while running:
    f1 = int(fullness/100)
    f2 = int(fullness/10)
    randvar = random.randint(0, 100)
    logging.info("Script variables setup for this tick.")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            logging.info("User closed the window. Exiting.")
        elif event.type == pygame.DROPFILE & sleeping == False:
            filepath = event.file
            logging.info(f"Eating dropped file: {filepath}")
            eatFile(filepath)
    #idle animation handling
    if sleeping == False:
        sprite = pygame.image.load(pet_sprites[random.randint(0,3)]).convert_alpha()
        logging.info("idle animation loaded.")
    screen.blit(sprite, (50, 50))
    pygame.display.flip()
    #hunger handling
    filepath = getfilesindirectory(emergency_food_folder)
    fullness -= hrate
    logging.info(f"Fullness decreased to: {fullness}")
    print("Fullness:", fullness)
    if fullness <= hthreshold & sleeping == False:
        logging.info("Hunger threshold reached. Looking for food.")
        filepath = getfilesindirectory(emergency_food_folder)
        print("Hunger threshold reached. Eating file...")
        if filepath:  # Check if filepath is not empty
            logging.info(f"Emergency food folder contents: {filepath}")
            eatFile(filepath[0])
            logging.info(f"Eating file from emergency food folder: {filepath[0]}")
        else:
            print(f"No food files found in {emergency_food_folder} to eat.")
            logging.warning(f"No food files found in {emergency_food_folder} to eat.")
    save_pet_memory()
    #Sleeping handling
    if sleeping == False & 25 == random.randint(0, 100):
        if fullness <= 0:
            print("Your pet is hungry! it's going to sleep!")
            logging.info("Pet is hungry and going to sleep.")
            sleeping = True
            sprite = pygame.image.load(pet_sprites[random.randint(4,6)]).convert_alpha()
        elif fullness > 0:
            print("Your pet is tired! it's going to sleep!")
            logging.info("Pet is tired and going to sleep.")
            sleeping = True
    if sleeping == True:
        logging.info("Pet is sleeping.")
        sprite = pygame.image.load(pet_sprites[random.randint(4,6)]).convert_alpha()
        sleep_conunter += 1
        fullness += hrate
        logging.info(f"Sleep counter: {sleep_conunter}, Fullness: {fullness}")
    if randvar < random.randint(0, 100) & sleeping == True or sleep_conunter >= random.randint(f1, f2):
        print("Your pet is awake! it had a good nap!")
        logging.info("Pet sleep cycle ended.")
        sleeping = False
        sprite = pygame.image.load(pet_sprites[random.randint(0,3)]).convert_alpha()
        sleep_conunter = 0
    time.sleep(tickspeed)
    logging.info("Tick complete.")
pygame.quit()