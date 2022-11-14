import pygame
import os
import button as b
def main_menu():
    background = pygame.image.load(os.path.join(image_path,"background.png"))
    
    while True:
        SCREEN.blit(background,(0,0))
        menu_mouse_pos = pygame.mouse.get_pos()
        menu_text = get_font(100).render('YENA',True,'#b68f40')
        menu_rect = menu_text.get_rect(center=(640,100))
        
        play_button = b(image)