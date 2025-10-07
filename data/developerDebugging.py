import pygame, sys, os.path

import pyperclip

pyperclip.set_clipboard("xclip")

pygame.init

key_constants = {getattr(pygame, name): name for name in dir(pygame) if name.startswith("K_")}

layout = "{:<12} | {:<15} | {:<10}"

for key_code in sorted(key_constants.keys()):
    name = pygame.key.name(key_code)
    const_name = key_constants[key_code]
    if name != "unknown key":
        print(layout.format(key_code, name, const_name))

print("\n",pyperclip.paste(),"\n")

screen = pygame.display.set_mode((100, 100), pygame.RESIZABLE)
pygame.display.set_caption('Debugging Tools')

winodowImage = pygame.image.load('data/pythonClickerIcon.png')
pygame.display.set_icon(winodowImage)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            keysDown = pygame.key.get_pressed()
            
            name = pygame.key.name(event.key)

            const_name = key_constants[event.key]

            print(layout.format(event.key, name, const_name))
    
    screen.fill((255,255,255))

    pygame.display.update()

pygame.quit()