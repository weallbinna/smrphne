import pygame
import os
import gun as g

#무조건 해야하는 부분
#################################################################################
pygame.init() #초기화(반드시필요)

screen_width = 1920 #화면 넓이
screen_height = 1080 #화면 높이
screen = pygame.display.set_mode((screen_width,screen_height))

#화면 타이틀 설정
pygame.display.set_caption("Smartphone")

#FPS
clock = pygame.time.Clock()
############################################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__)	#현재 파일 위치 설정, 자동으로 현재 폴더로 편리하게 설정
image_path = os.path.join(current_path,"pygame_project/images") #이미지 폴더 위치 설정

#배경 설정
background = pygame.image.load(os.path.join(image_path,"background.png"))

#스테이지 설정
stage = pygame.image.load(os.path.join(image_path,"stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]
stage_x = 0
stage_y = screen_height-stage_height

stage2 = pygame.image.load(os.path.join(image_path,"stage2.png"))
stage_size2 = stage2.get_rect().size
stage_height2 = stage_size2[1]
stage_x2 = stage_x+stage_size[0]
stage_y2 = screen_height-stage_height

#캐릭터 만들기

character = pygame.image.load(os.path.join(image_path,'character.png'))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width/2)-(character_width/2)
character_y_pos = screen_height-stage_height-character_height

duck = pygame.image.load(os.path.join(image_path,'duck.png'))
duck_size = duck.get_rect().size
duck_width = duck_size[0]
duck_height = duck_size[1]
duck_x_pos = (screen_width)
duck_y_pos = screen_height-stage_height-duck_height
duck_pop = False

#캐릭터 이동 방향
character_x_left = 0
character_x_right = 0
lookingr = True

#캐릭터 이동 속도
character_speed = 5

#점프를 위한 중력
y_gravity = 1
jump_height = 20
y_velocity = jump_height
jumping = False

#font 정의
game_font = pygame.font.SysFont('arial',40,True,True)
total_time = 100
start_ticks = pygame.time.get_ticks()

game_result = "Game Over"
print('hi')

lvl = 0
tick = 0
#이벤트 루프
running = True #게임이 진행중인가
while running :
	dt = clock.tick(60)  #FPS설정함
	tick = pygame.time.get_ticks()/1000

# 2. 이벤트 처리(키보드, 마우스 등)
	for event in pygame.event.get(): #어떤 이벤트가 발생하는가?
		if event.type == pygame.QUIT: #창이 닫히는 이벤트가 발생하는가?
			running = False #게임이 진행중이 아님
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				character_x_left -= character_speed
				lookingr = False
			elif event.key == pygame.K_RIGHT:
				character_x_right += character_speed
				lookingr = True
			elif event.key == pygame.K_z:
				weapon_x_pos = character_x_pos + character_width
				weapon_y_pos = character_y_pos + (character_height/2)-(g.weapon_height/2)
				g.weapons.append([weapon_x_pos, weapon_y_pos,lookingr])
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				character_x_left = 0
			elif event.key == pygame.K_RIGHT:
				character_x_right = 0

	#점프
	keys_pressed = pygame.key.get_pressed()

	if keys_pressed[pygame.K_SPACE]:
		jumping = True
	if jumping:
		character_y_pos -= y_velocity
		y_velocity -= y_gravity
		if y_velocity < -jump_height:
			jumping = False
			y_velocity = jump_height


	# 3. 게임 캐릭터 위치 정의  
	character_x_pos += character_x_left + character_x_right

	if lvl == 3:
		duck_pop = True
	else:
		duck_pop = False
	#총알 이동

	g.weapons = [[w[0]+g.weapon_speed if w[2] else w[0]-g.weapon_speed,w[1],w[2]] for w in g.weapons]

	#양끝에 닿은 총알 없애기
	g.weapons = [[w[0],w[1],w[2]] for w in g.weapons if w[0] > 0 and w[0]<screen_width]
	#스테이지 이동
	if not duck_pop:
		if character_x_pos < 100:
			character_x_pos = 100
			if lvl>=0:
				if stage_x <= stage_x2: #뒤로가기
					if stage_x<0:
						stage_x+=100
						stage_x2+=100
					else:
						lvl -= 1
						stage_x2 = stage_x - stage_size2[0]
				else:
					if stage_x2<0:
						stage_x2+=100
						stage_x+=100	
					else:
						lvl-=1
						stage_x = stage_x2 - stage_size[0]
					if duck_pop:
						duck_x_pos+=100

		elif character_x_pos > screen_width-character_width-100:
			character_x_pos = screen_width-character_width-100
			if stage_x <= stage_x2:  #앞으로 가기
				if stage_x>-(stage_size[0]):
					stage_x-=100
					stage_x2-=100
				else:
					lvl+=1
					stage_x = stage_x2+stage_size2[0]
			else:
				if stage_x2>-(stage_size2[0]):
					stage_x2 -= 100
					stage_x-=100
				else:
					lvl+=1
					stage_x2 = stage_x+stage_size[0]
			if duck_pop:
				duck_x_pos -= 100
	# 4. 충돌 처리


	# 5. 화면에 그리기
	screen.blit(background,(0,0))

	for weapon_x_pos,weapon_y_pos,_ in g.weapons:
		screen.blit(g.weapon,(weapon_x_pos,weapon_y_pos))
	screen.blit(stage,(stage_x,stage_y))
	screen.blit(stage2,(stage_x2,stage_y2))
	screen.blit(character,(character_x_pos,character_y_pos))
	if duck_pop:
		screen.blit(duck,(duck_x_pos,duck_y_pos))

	#경과 시간
	elapsed_time = (pygame.time.get_ticks()-start_ticks)/1000

	pygame.display.update() #게임화면 다시 그리기


pygame.quit() #게임 나가기