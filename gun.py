import pygame
import os

current_path = os.path.dirname(__file__)	#현재 파일 위치 설정, 자동으로 현재 폴더로 편리하게 설정
image_path = os.path.join(current_path,"pygame_project/images") #이미지 폴더 위치 설정

#총알 만들기
weapon = pygame.image.load(os.path.join(image_path,"bullet.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
weapon_height = weapon_size[1]

# 총알 이동 속도
weapon_speed = 10

# 총알은 한 번에 여러 발 발사 가능
weapons = []

#사라질 무기
weapon_to_remove = -1

#공격력
weapon_dmg = 8