import pygame
import os
#무조건 해야하는 부분
#################################################################################
pygame.init() #초기화(반드시필요)

screen_width = 640 #화면 넓이
screen_height = 480 #화면 높이
screen = pygame.display.set_mode((screen_width,screen_height))

#화면 타이틀 설정
pygame.display.set_caption("Pang")

#FPS
clock = pygame.time.Clock()
############################################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__) #현재파일위치 반환
image_path = os.path.join(current_path,"pygame_project/images") #거기에 이미지 폴더 추가

#배경 만들기
background = pygame.image.load(os.path.join(image_path,"background.png"))

#스테이지 만들기
stage = pygame.image.load(os.path.join(image_path,"stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

#캐릭터 만들기
character = pygame.image.load(os.path.join(image_path,"character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2)-(character_width/2)
character_y_pos = screen_height - character_height - stage_height

#캐릭터 이동 방향
character_to_x_LEFT = 0
character_to_x_RIGHT = 0

#캐릭터 이동 속도
character_speed =5

#무기 만들기
weapon = pygame.image.load(os.path.join(image_path,"weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한 번에 여러 발 발사 가능
weapons = []

# 무기 이동 속도
weapon_speed = 10

# 공 만들기 (4개 크게에 대해 따로 처리)
ball_images = [
    pygame.image.load(os.path.join(image_path,"ballon1.png")),
    pygame.image.load(os.path.join(image_path,"ballon2.png")),
    pygame.image.load(os.path.join(image_path,"ballon3.png")),
    pygame.image.load(os.path.join(image_path,"ballon4.png"))
]

# 공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9] # index 0, 1, 2, 3에 해당하는 값

# 공들, dictionary로 관리
balls = []

# 최초 발생하는 큰 공 추가
balls.append({
    "pos_x" : 50,  #공의 x좌표
    "pos_y" : 50, #공의 y좌표
    "img_idx" : 0, #공의 크기 인덱스 값
    "to_x" : 3, # x축 이동방향, -3 이면 왼쪽으로, 3이면 오른쪽으로
    "to_y" : -6, #y축 이동 방향, 살짝 올라갔다 떨어지게 할려고
    "init_spe_y" : ball_speed_y[0]}) # 땅에 튕기고 튕긴 높이 설정

#사라질 무기, 공 정보 저장

weapon_to_remove = -1
ball_to_remove = -1

#Font 정의
game_font = pygame.font.Font(None,40)
total_time = 100
start_ticks = pygame.time.get_ticks() #시작 시간 정의

game_result = "Game Over"



pygame.time.delay(2000)
#이벤트 루프
running = True #게임이 진행중인가
while running :
    dt = clock.tick(60)  #FPS설정함
    
    # 2. 이벤트 처리(키보드, 마우스 등)
    for event in pygame.event.get(): #어떤 이벤트가 발생하는가?
        if event.type == pygame.QUIT: #창이 닫히는 이벤트가 발생하는가?
            running = False #게임이 진행중이 아님

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x_LEFT -= character_speed
            elif event.key==pygame.K_RIGHT:
                character_to_x_RIGHT += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (character_width/2)-(weapon_width/2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])
                
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                character_to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT = 0
    # 3. 게임 캐릭터 위치 정의            
    character_x_pos += character_to_x_LEFT + character_to_x_RIGHT
    
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
        
    #무기 위치 조정
    #100,200 -> 100, 190 -> 100, 180
    weapons = [[w[0],w[1]-weapon_speed] for w in weapons] #무기 위치 위로
    
    #천장에 닿은 무기 없애기
    weapons = [[w[0],w[1]] for w in weapons if w[1] > 0]
    
    #공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        
        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]
        
        # 가로벽에 닿았을 때 공 이동 위치 변경(튕겨 나온 효과)
        if ball_pos_x <= 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"]*-1
        v
        # 스테이지에 닿았을 때 다시 튕기기
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spe_y"]
        #걍 포물선으로 속도 양수로 바꿔주기
        else:
            ball_val["to_y"] += 0.4
        
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]
            
    
    # 4. 충돌 처리
    
    # 캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos
    
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        
        #공 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y
        
        if character_rect.colliderect(ball_rect):
            running = False
            break
            
        #공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]
            
            #무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y
            
            #충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx # 해당무기 없애기 위한 값 설정
                ball_to_remove = ball_idx # 해당 공 없애기 위한 값 설정
                
                #가장 작은 크기의 공이 아니라면 다음 단계의 공으로 나눠주기
                if ball_img_idx < 3:
                    #현재 공 크기 정보를 가지고 오기
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]
                    
                    #나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]
                    
                    #왼쪽으로 튕겨나가는 작은공
                    balls.append({
                        "pos_x" : ball_pos_x+(ball_width/2)-(small_ball_width/2),  #공의 x좌표
                        "pos_y" : ball_pos_y+(ball_height/2) - (small_ball_height/2), #공의 y좌표
                        "img_idx" : ball_img_idx +1, #공의 크기 인덱스 값
                        "to_x" : -3, # x축 이동방향, -3 이면 왼쪽으로, 3이면 오른쪽으로
                        "to_y" : -6, #y축 이동 방향, 살짝 올라갔다 떨어지게 할려고
                        "init_spe_y" : ball_speed_y[ball_img_idx+1]}) # 땅에 튕기고 튕긴 높이 설정
                    
                    #오른쪽으로 튕겨나가는 작은공
                    balls.append({
                        "pos_x" : ball_pos_x+(ball_width/2)-(small_ball_width/2),  #공의 x좌표
                        "pos_y" : ball_pos_y+(ball_height/2) - (small_ball_height/2), #공의 y좌표
                        "img_idx" : ball_img_idx +1, #공의 크기 인덱스 값
                        "to_x" : 3, # x축 이동방향, -3 이면 왼쪽으로, 3이면 오른쪽으로
                        "to_y" : -6, #y축 이동 방향, 살짝 올라갔다 떨어지게 할려고
                        "init_spe_y" : ball_speed_y[ball_img_idx+1]}) # 땅에 튕기고 튕긴 높이 설정

                break
        else: #계속 게임을 진행
            continue #안쪽 for문 조건이 맞지 않으면 continue, 바깥 for 문 계속 수행
        break #안쪽 for 문에서 break를 만나면 여기로 진입, 중첩문 탈출 노력은 배신하지 않는다
    #충돌된 공 or 무기 없애기
    if ball_to_remove>-1:
        del balls[ball_to_remove]
        ball_to_remove = -1
    
    if weapon_to_remove>-1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1
    
    #모든 공을 없앨 경우 게임 종료(성공)
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False
    
    # 5. 화면에 그리기
    screen.blit(background,(0,0))
    for weapon_x_pos,weapon_y_pos in weapons:
        screen.blit(weapon,(weapon_x_pos,weapon_y_pos))
    
    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx],(ball_pos_x,ball_pos_y))
    
    screen.blit(stage,(0,screen_height - stage_height))
    screen.blit(character,(character_x_pos,character_y_pos))
    
    
    #경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)),True,(255,255,253))
    screen.blit(timer,(10,10))
    
    #시간 초과했다면
    if total_time - elapsed_time <=0:
        game_result = "time over"
        running = False
            
    
    
    
    pygame.display.update() #게임화면 다시 그리기

#게임 오버 메시지
msg = game_font.render(game_result, True,(255,255,0))
msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
screen.blit(msg,msg_rect)
pygame.display.update()

#2초대기
pygame.time.delay(2000)
    
pygame.quit() #게임 쳐나가기