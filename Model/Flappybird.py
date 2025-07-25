import pygame
import sys
from pygame.locals import *
import random
pygame.init()

#define game variables
clock=pygame.time.Clock()
fps=60
flying=False
game_over=False
pipe_gap=150
pipe_frequency=1500 #millionseconds
last_pipe=pygame.time.get_ticks() - pipe_frequency
score=0
pass_pipe=False
screen_width=864
screen_height=936
screen=pygame.display.set_mode((screen_width, screen_height))
#define font and color
font = pygame.font.SysFont('Bauhaus 93', 60) #60 là size
color=(255, 255, 255)# màu trắng
#define game loads
pygame.display.set_caption('Flappy Bird')
bg=pygame.image.load('Images/bg.png')
ground_img=pygame.image.load('Images/ground.png')
button_img=pygame.image.load('Images/restart.png')
ground_scroll=0
scroll_speed=4

def draw_text(text, font, text_color, x, y):
	img = font.render(text, True, text_color) #True: conver font -> ảnh, False là ngc lại 
	screen.blit(img, (x,y))

class Bird(pygame.sprite.Sprite): #pygame.sprite.Sprite là 1 class và class Bird sẽ kế thừa các thuộc tính, method trong class pygame.sprite.Sprite
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images=[]
		self.index=0
		self.counter=0
		for num in range(1,4):
			img=pygame.image.load(f'Images/bird{num}.png')
			self.images.append(img)
		self.image=self.images[self.index]
		self.rect=self.image.get_rect() #vẽ đường bo hình chữ nhật xung quanh vật thể(bird)
		self.rect.center=[x,y]#gắn cho vật thể(bird) vị trí tọa độ
		self.vel=0
		self.click=False


	def update(self): #tạo animation cho bird
	#tạo di chuyển lên xuống
		#tạo gravity(đi xuống)
		if flying == True:
			self.vel += 0.5	
			if self.vel>8: 
				self.vel=8
			if self.rect.bottom<768:
				self.rect.y+=int(self.vel)

		#tạo đi lên bằng click chuột
		if pygame.mouse.get_pressed()[0] == 1 and self.click == False:#0: là chuột trái, 1: là chuột giữa, 2: là chuột phải, còn = 1 là đã được click
			self.vel=-10 # để đưa vật thể(bird) về vị trí ở phía trên do y giảm
			self.click=True
		if pygame.mouse.get_pressed()[0]==0: #chuột trái không được click
			self.click=False


		if game_over==False: #khi game chưa kết thúc thì tạo animation cho bird
	       #tạo animation
			self.counter+=1
			flappy_cooldown=5
			if self.counter>flappy_cooldown: #cho bird {num} giữ nguyên vị trí 1 khoảng tg trước khi sang bird 2 khi self.index=1, và sang bird3...
				self.counter=0
				self.index+=1
				if self.index>=len(self.images):
					self.index=0
			self.image=self.images[self.index]   #sau đó do vòng lặp while ở dưới và chạy bird_group.update() nên cứ lặp lại như vậy => tạo animation


			#tạo rotation
			self.image=pygame.transform.rotate(self.images[self.index], self.vel*-2)
		else: 
			self.image=pygame.transform.rotate(self.images[self.index], -80)


class Pipe(pygame.sprite.Sprite):
	def __init__(self, x, y, position):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load('Images/pipe.png')
		self.rect=self.image.get_rect()
		if position==1: #1 là tạo ống ở trên
			self.image=pygame.transform.flip(self.image, False, True)
			self.rect.bottomleft=[x, y - int(pipe_gap/2)]
		if position==-1:#-1 là tạo ống ở dưới
			self.rect.topleft=[x, y + int(pipe_gap/2)]

	def update(self):
		self.rect.x-=scroll_speed
		if self.rect.right<0:# do khi chạy thì pipe_group sẽ chứa rất nhiều pipes bên trong và gây tốn dung lượng
			#nên nếu mà pipe nào đó thoát khỏi màn hình thì sẽ bị xóa => tiết kiệm dung lượng
			self.kill()

class Button:
	def __init__(self, x, y, image):
		self.image=image
		self.rect=self.image.get_rect()
		self.rect.topleft=(x,y)

	def draw(self):
		action=False
		#get mouse position
		pos=pygame.mouse.get_pos() #dùng phương thức này cho ra 1 list [x,y] là tọa độ của chuột get_pos()[0]: x, get_pos()[1]:y
		#check xem chuột có nằm trên image ko
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0]==1:
				action=True
		
		#draw button
		screen.blit(self.image,(self.rect.x, self.rect.y))
		return action


def reset_game():
	pipe_group.empty()
	flappy.rect.x=100
	flappy.rect.y=int(screen_height/2)
	score=0
	return score
	
bird_group=pygame.sprite.Group() #bird_group là nhóm các vật thể (birds),
# hiện đang trống, muốn thêm vào cần dùng phương thức add

pipe_group=pygame.sprite.Group()

flappy=Bird(100,int(screen_height/2)) #chạy class Bird, self=flappy, x=100, y=int(screen_height/2)
bird_group.add(flappy)

#create restart button instances
button=Button(screen_width//2 - 50, screen_height//2 - 50, button_img)

run=True
while run:
	clock.tick(fps)
	screen.blit(bg,(0,0)) #chèn background
	bird_group.draw(screen)
	bird_group.update()
	pipe_group.draw(screen)

	#check the score
	if len(pipe_group)>0:
		if bird_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.left\
		 and bird_group.sprites()[0].rect.right<pipe_group.sprites()[0].rect.right\
		 and pass_pipe==False:
		 	pass_pipe=True
	
		if pass_pipe == True:
			if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
				score+=1
				pass_pipe=False
	draw_text(str(score), font, color, int(screen_width/2), 110)


	#chèn background
	screen.blit(ground_img, (ground_scroll,768))

	#look for collison( xem có va chạm vào cột ko?)
	if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top<0: # nếu set False đầu tiên -> True thì bird_group khi va chạm với pipe_group sẽ biến mất, tương tự với False thứ 2 khi set về True
		game_over=True
    #check xem có chạm đáy ko?
	if flappy.rect.bottom >=768:
		game_over=True
		flying=False

	if game_over==False and flying == True: #khi game chưa kết thúc thì background sẽ ko chạy nữa, và phải ấn click chuột trái để flying=True thì mới bắt đầu các câu lệnh phía dưới

		#generate more pipes
		time_now=pygame.time.get_ticks() #lấy thời điểm hiện tại 
		#Giải thích sơ bộ để tạo more pipes: mỗi vòng lặp mà game chưa kết thúc (game_over=False) thì biến time_now = thời điểm lúc đó, 
		# khoảng thời gian từ lúc biến time_now đc làm mới đến thời điểm ban đầu last_pipe (ở trên) mà > pipe_frequency( là 1.5s) thì sẽ tạo thêm pipes
		#tuy nhiên, lúc ban đầu khi game mới bắt đầu chưa có pipe nào thì time_now = last_pipe=0s -> time_now -last_pipe=0 < pipe_frequency(chưa tạo thêm pipe)
		#tuy nhiên, sau đó khoảng 1,5 s thì time_now quanh quanh 1.5s, last_pipe=0, nên đáp ứng đc yêu cầu -> tạo pipe
		#Hơn nữa, lúc này cần gán lại cho last_pipe=time_now vừa xong để sau 1,5 s tiếp theo thì time_now mới=time_now cũ+1,5s và khi ấy time_now - last_pipe> pipe_frequency -> đáp ứng đk -> tạo cột
		#1 lưu ý là ta ko muốn phải sau 1,5s khi trò chơi bắt đầu pipe mới đc tạo -> đặt lại last_pipe=pygame.time.get_ticks()-pipe_frequency để khi lặp lần đầu thì đáp ứng đc đk luôn
		if time_now - last_pipe >= pipe_frequency: 
			pipe_height=random.randint(-100, 100)
			btm_pipe=Pipe(screen_width, int(screen_height/2) + pipe_height,-1) 
			top_pipe=Pipe(screen_width, int(screen_height/2) + pipe_height, 1)
			pipe_group.add(btm_pipe)
			pipe_group.add(top_pipe)
			last_pipe=time_now

		# ground & scroll
		ground_scroll-=scroll_speed  #để cho ground_img chạy về bên trái, tạo hiệu ứng
		if abs(ground_scroll)>35: # khi mà chạy hết ảnh của ground_img nghĩa là ground_scroll >35 pixels thì cần cho nó =0 để lặp lại hình ảnh ground_img
			ground_scroll=0
		pipe_group.update()
	if game_over==True:
		if button.draw()==True:
			game_over=False
			score = reset_game()

	for event in pygame.event.get(): #các sự kiện trong game
		if event.type==pygame.QUIT: #sự kiện người chơi ấn vào phím thoát ra ngoài
			run=False
		if event.type==pygame.MOUSEBUTTONDOWN and flying==False and game_over==False:
			flying=True  #khi đó khi vòng lặp đc lặp lại và bird_group.update() đc chạy thì sẽ chạy gravity ở trên
	pygame.display.update()
pygame.quit()

