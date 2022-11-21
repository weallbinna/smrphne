import pygame
import os
import gun as g
import button
import random

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
duck_x_pos = (screen_width)-300
duck_y_pos = screen_height-stage_height-duck_height
duck_pop = False
duck_rage = False
duck_health = 100
duck_ragehealth = 1000

#캐릭터 이동 방향
character_x_left = 0
character_x_right = 0
lookingr = True

#캐릭터 이동 속도
character_speed = 15

#점프를 위한 중력
y_gravity = 1
jump_height = 20
y_velocity = jump_height
jumping = False

e_gravity = 2
e_jump_height = 40
e_velocity = e_jump_height
e_jumping = False

#font 정의
game_font = pygame.font.SysFont('arial',40,True,True)
total_time = 100
start_ticks = pygame.time.get_ticks()

game_result = "Game Over"

#rage mode duck fight
def jumpattack(health,inix,iniy):
	global e_velocity,e_jump_height,e_gravity,character_x_pos,e_jumping,jumpcooldown,buncnt
	in_x,in_y = inix,iniy
	
	cur_y = iniy
	cur_x = inix
	cur_x+=(character_x_pos-inix)/10
	cur_y -= e_velocity
	e_velocity -= e_gravity
	if e_velocity < -e_jump_height:    #landed
		e_velocity = e_jump_height
		e_jumping = True
		jumpcooldown = 0
		buncnt+=1
	return (cur_x,cur_y)
def firing():
    pass
lvl = 0
tick = 0
effct = False
jumpcooldown = 0
buncnt = 0
call = 0
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

	if lvl == 0:
		if duck_health>0:
			duck_pop = True
		elif duck_ragehealth<0:
			duck_rage = False
		else:
			duck_pop = False
			duck_rage = True   #rage part
        
		if not effct:
			character_x_pos -= 1000
			effct = True
    
	
	if duck_rage and duck_ragehealth>0:
		jumpcooldown+=clock.get_time()
		if call ==0:
			call = random.randrange(1,4)   #to make duck do different moves
		if call == 1:
			if not e_jumping and jumpcooldown >1000 and buncnt<3:
				duck_x_pos,duck_y_pos = jumpattack(duck_ragehealth,duck_x_pos,duck_y_pos)
				e_jumping = False
			elif buncnt==3:
				if duck_x_pos<(screen_width)-300: 
					duck_x_pos+=50
				else:
					buncnt=0
					call = 0
		elif call == 2:
			pass
		else:
			pass
    
    #총알 이동

	g.weapons = [[w[0]+g.weapon_speed if w[2] else w[0]-g.weapon_speed,w[1],w[2]] for w in g.weapons]

	#양끝에 닿은 총알 없애기
	g.weapons = [[w[0],w[1],w[2]] for w in g.weapons if w[0] > 0 and w[0]<screen_width]
	#스테이지 이동
	if character_x_pos < 100:
		character_x_pos = 100
		if lvl>=0:
			if not duck_pop and not duck_rage:
				if stage_x <= stage_x2: #뒤로가기
					if stage_x<0:
						stage_x+=50
						stage_x2+=50
					else:
						lvl -= 1
						stage_x2 = stage_x - stage_size2[0]
				else:
					if stage_x2<0:
						stage_x2+=50
						stage_x+=50	
					else:
						lvl-=1
						stage_x = stage_x2 - stage_size[0]
	
	elif character_x_pos > screen_width-character_width-600:
		character_x_pos = screen_width-character_width-600
		if not duck_pop and not duck_rage:
			if stage_x <= stage_x2:  #앞으로 가기
				if stage_x>-(stage_size[0]):
					stage_x-=50
					stage_x2-=50
				else:
					lvl+=1
					stage_x = stage_x2+stage_size2[0]
			else:
				if stage_x2>-(stage_size2[0]):
					stage_x2 -= 50
					stage_x-=50
				else:
					lvl+=1
					stage_x2 = stage_x+stage_size[0]
	# 4. 충돌 처리
	character_rect = character.get_rect()
	character_rect.left = character_x_pos
	character_rect.top = character_y_pos
	
	duck_rect = duck.get_rect()
	duck_rect.left = duck_x_pos
	duck_rect.top = duck_y_pos
	
	for weapon_idx, weapon_val in enumerate(g.weapons):
		weapon_pos_x = weapon_val[0]
		weapon_pos_y = weapon_val[1]

		#무기 rect 정보 업데이트
		weapon_rect = g.weapon.get_rect()
		weapon_rect.left = weapon_pos_x
		weapon_rect.top = weapon_pos_y
		
		if weapon_rect.colliderect(duck_rect):
			g.weapon_to_remove = weapon_idx # 해당무기 없애기 위한 값 설정
			duck_health-=g.weapon_dmg
			if duck_rage:
				duck_ragehealth-=g.weapon_dmg

	if g.weapon_to_remove>-1:
		del g.weapons[g.weapon_to_remove]
		g.weapon_to_remove = -1
    

	# 5. 화면에 그리기
	screen.blit(background,(0,0))

	for weapon_x_pos,weapon_y_pos,_ in g.weapons:
		screen.blit(g.weapon,(weapon_x_pos,weapon_y_pos))
	screen.blit(stage,(stage_x,stage_y))
	screen.blit(stage2,(stage_x2,stage_y2))
	screen.blit(character,(character_x_pos,character_y_pos))
	if duck_pop or duck_rage:
		screen.blit(duck,(duck_x_pos,duck_y_pos))

	#경과 시간
	elapsed_time = (pygame.time.get_ticks()-start_ticks)/1000

	pygame.display.update() #게임화면 다시 그리기


pygame.quit() #게임 나가기

 