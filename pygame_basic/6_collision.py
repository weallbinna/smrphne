import pygame

pygame.init() #초기화(반드시필요)

screen_width = 1280 #화면 넓이
screen_height = 1080 #화면 높이
screen = pygame.display.set_mode((screen_width,screen_height))

#화면 타이틀 설정
pygame.display.set_caption("Nakevin game")

#FPs
clock = pygame.time.Clock()

#외부파일 가져와서 바탕에 칠하기
background = pygame.image.load("/workspace/project/background.png")

#캐릭터 불러오기
character = pygame.image.load("/workspace/project/character.png") 
character_size = character.get_rect().size #이미지의 크기를 불러오기
character_width = character_size[0] #캐릭터 가로 크기
character_height = character_size[1] #캐릭터 세로 크기
character_x_pos = screen_width / 2 - (character_width/2) #화면의 가로 절반 크기에 해당하는 곳 위치
character_y_pos = screen_height -  character_height   #화면의 세로 크기만큼 아래에 위치

#이동할 좌표
to_x = 0
to_y = 0

#이동 속도
character_speed = 0.6

#enemy
enemy = pygame.image.load("/workspace/project/enemy.png")
enemy_size = enemy.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = screen_width / 2 - (enemy_width/2)
enemy_y_pos = screen_height/2 - (enemy_height/2)


#이벤트 루프
running = True #게임이 진행중인가
while running :
    dt = clock.tick(60)  #FPS설정함
    print("fps :"+str(clock.get_fps()))
    
    for event in pygame.event.get(): #어떤 이벤트가 발생하는가?
        if event.type == pygame.QUIT: #창이 닫히는 이벤트가 발생하는가?
            running = False #게임이 진행중이 아님
            
        if event.type == pygame.KEYDOWN:   #키가 눌러졌는지 확인
            if event.key == pygame.K_LEFT: # 왼쪽으로
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT: #오른쪽으로
                to_x += character_speed
            elif event.key == pygame.K_UP:  #위로
                to_y -= character_speed
            elif event.key == pygame.K_DOWN: #아래로
                to_y += character_speed
        
        if event.type == pygame.KEYUP:     #방향키를 땠을때 안 움직임
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0
                
    character_x_pos += to_x *dt   #위치 재설정 & 델타타임을 곱해주면서 공정한 움직임 설정
    character_y_pos += to_y *dt
    
    # 화면밖으로 나가는거 막아주기 위함!
    if character_x_pos <0 :
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
    elif character_y_pos <0:
        character_y_pos = 0
    elif character_y_pos >screen_height -  character_height:
        character_y_pos = screen_height - character_height
        
    #충돌처리, 충돌영역을 가져오고, 그 영역을 잘 따라가게 만든것
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos
    
    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos
    #충돌했을때의 반응
    if character_rect.colliderect(enemy_rect):
        print("충돌했어요")
        running = False
    
    # screen.fill((0,255,0))   #외부파일 없이 그냥 바탕에 색 칠할때
    screen.blit(background,(0,0))   #외부파일 설정시 왼쪽 모서리를 어디에서 부터 시작하는지 설정
    screen.blit(character,(character_x_pos,character_y_pos))
    screen.blit(enemy,(enemy_x_pos,enemy_y_pos))
    pygame.display.update() #게임화면 다시 그리기
        
pygame.quit() #게임 쳐나가기