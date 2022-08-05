#Черненко Коля
#2019 год 30 сентября - начало проекта
# - конец проекта
#Игра в стиле Space Invaders, улучшеная версия первой
import pygame, sys, random, os

base_path = os.path.dirname(__file__)

#Инициализация игры
pygame.init()

#Устанавлеваем имя окна
pygame.display.set_caption('Space Invanders')

#Иконка приложения
icon_of_app_path = os.path.join(base_path, "icon.png")
icon_of_app = pygame.image.load(icon_of_app_path)

#Устанавлеваем иконку приложения 
pygame.display.set_icon(icon_of_app)

#Картинка босса- кота
picture_of_boss_path = os.path.join(base_path, "boss.png")
picture_of_boss = pygame.image.load(picture_of_boss_path)

#Звуки
shoot = pygame.mixer.Sound(os.path.join(base_path, "sound of bang.wav"))
dead_enemy = pygame.mixer.Sound(os.path.join(base_path, "sound of killing the enemy.wav"))
dead_player = pygame.mixer.Sound(os.path.join(base_path, "sound of fail.wav"))

#Технические константы
FPS = 60
display_width = 650
display_height = 600
BACKGROUND_COLOR = (16, 56, 94)

#Константа для показателя жизней
image_heart = pygame.image.load(os.path.join(base_path, "hp.png"))

#Картинка для фона игры
BG = pygame.image.load(os.path.join(base_path, "background.jpg"))

#Картинка галвного игрока, его х, его у, его скорость перемещения
image_puska = pygame.image.load(os.path.join(base_path, "ship.png"))
x_pushka = 300
y_pushka = 480
speed_pushka = 2

#Цвет пуль
RED = (255, 0, 0)

#Массив пуль
bullets = []

#Картинка противника
enemy_image = pygame.image.load(os.path.join(base_path, "enemy.png"))

#Скорость игрового цикла
display = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

#массивы для показателя жизней
hearts_arr = []
hearts_arr1 = []

#Класс для кнопок
class Button:
    '''Инициализация кнопки'''
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color =  (45, 61, 204)
        self.active_color =  (41, 179, 87)

    '''Отрисовка кнопки'''
    def draw_button(self, x, y, message, x_mess, y_mess, font_size=30, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if x <= mouse[0] <= x + self.width and y <= mouse[1] <= y + self.height:
            pygame.draw.rect(display, self.active_color, (x, y, self.width, self.height))

            if click[0] == 1:
                if action is not None:
                    action()
        else:
            pygame.draw.rect(display, self.inactive_color, (x, y, self.width, self.height))
        print_text(message, x_mess, y_mess, font_size, (0,0,0))

#Класс пуль для пушки и противников
class Bullet:
    '''Инициализация пули'''
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed

    '''Отрисовка пуль'''    
    def draw_bullets(self): 
        pygame.draw.circle(display, self.color, (self.x, self.y), self.radius)                        
#Класс врагов
class Enemy:
    '''Инициализация врага'''
    def __init__(self, x, y, image, height_rect, width_rect):
        self.x = x
        self.y = y
        self.image = image
        self.height_rect = height_rect
        self.width_rect = width_rect

    '''Отрисовка врагов'''
    def draw(self):
        display.blit(self.image, (self.x, self.y))    

#Переменные координаты для показателя жизней
x_heart = 530
y_heart = 15

#Добавляет жизни в массив для жизней
def append_hearts():
    global x_heart, y_heart
    for i in range(1, 4):
        hearts_arr.append([x_heart, y_heart, image_heart])
        x_heart += 37        

#Рисует жизни
def draw_hearts():
    for i in hearts_arr:
        display.blit(i[2], (i[0], i[1])) 
    if len(hearts_arr1) != 0:
        for heart in hearts_arr1:
            display.blit(heart[2], (heart[0], heart[1]))     

#Переменная для максимального количества врагов в спике врагов с уровнями эта переменная увеличивается  
Max_Num_Enemies = 15

#Пустой список для врагов
enemies = []

#Функция создает врагов через класс врагов
def enemy_append(listt):
    global x_enemy, y_enemy
    for number in range(1, Max_Num_Enemies):
        listt.append(Enemy(random.randint(0, display_width - 45), random.randint(-2000, -150), enemy_image, 45, 65))

enemy_append(enemies)

#Функция для отрисовки врагов из списка врагов
def enemies_draw():
    for enemy in enemies:
        enemy.draw()

#Функция по передвижению врагов
def move_enemy():
    for enemy in enemies:
        enemy.y += 2        

#Функция для удаления врага если его у перевалил за высоту экрана
def del_enemy_lower_height():
    for enemy in enemies:
        if enemy.y > 710:
            del enemies[enemies.index(enemy)]

#Функция по проверке: если количество врагов в видимой части меньше 6 
#то добавить парочку
def check_how_much_enemies_are_visible():
    if len(enemies) <= 3:
        enemy_append(enemies)  

#Массив для пуль противников
bullets_for_enemy = []

#Массив
number_ran_num_enem_bullets = 170 #1000000

#Функция для для определения который будут ли враги стрелять
def enemy_strike():
    global number_ran_num_enem_bullets
    for enemy in enemies:
        if enemy.y > 0:
            random_num_for_strike = random.randint(0, number_ran_num_enem_bullets)
            if random_num_for_strike == 0:
                bullets_for_enemy.append(Bullet(enemy.x + 65, enemy.y + 65, 5, RED, 7))
            else:
                pass
        else:
            pass    

#Проходит по массиву для пуль противника и отрисовывает их 
def draw_enemies_bullets():
    if len(bullets_for_enemy) != 0:
        for bullet in bullets_for_enemy:
            bullet.draw_bullets()   

#Функция заставляет пули противников двигаться и удаляться
#  после перехода рубежа высоты                 
def enemies_bullets_move():
    for bullet in bullets_for_enemy:
        if bullet.y < display_height + 100:
            bullet.y += bullet.speed
        else:
            bullets_for_enemy.pop(bullets_for_enemy.index(bullet)) 

rect1 = []
rect2 = []
#Функция по доабавлению ректов каждому противнику 
def append_rects_for_enemies():
    #Добавление ректа верхушки космолета
    for enemy in enemies:
        rect1.append(pygame.Rect((enemy.x + 48, enemy.y + 39, 80 - 48, 57 - 39)))
    del rect1[0:-(len(enemies))]
    
    #Добавление ректа низа космолета 
    for enemy in enemies:
        rect2.append(pygame.Rect((enemy.x + 34, enemy.y + 10, 94 - 34, 26 - 10)))
    del rect2[0:-(len(enemies))]  

#Функция проверяет х и у ректа противника и пули
def check_collisions_bull_enemy():
    global score
    if len(enemies) != 0 and len(bullets) != 0:
        for bullet in bullets:
            for rect in rect1:
                if rect.bottomleft[0] <= bullet.x <= rect.bottomright[0] or rect.bottomleft[0] <= bullet.x + 5 <= rect.bottomright[0]:
                    if rect.topleft[1] <= bullet.y <= rect.bottomleft[1]: 
                        index_of_dead = rect1.index(rect) 
                        del bullets[bullets.index(bullet)]  
                        del enemies[index_of_dead]
                        
                        dead_enemy.set_volume(0.5)
                        dead_enemy.play()

                        #Добавление 50 очков в очки
                        score += 50

                        return True

    if len(enemies) != 0 and len(bullets) != 0:
        for bullet2 in bullets:
            for rect3 in rect2:
                if rect3.bottomleft[0] <= bullet2.x <= rect3.bottomright[0] or rect3.bottomleft[0] <= bullet2.x + 5 <= rect3.bottomright[0]:
                    if rect3.topleft[1] <= bullet2.y <= rect3.bottomleft[1]: 
                        index_of_dead2 = rect2.index(rect3) 
                        del bullets[bullets.index(bullet2)]  
                        del enemies[index_of_dead2]

                        dead_enemy.set_volume(0.5)
                        dead_enemy.play()
                        #Добавление 50 очков на счет
                        score += 50
                        return True   

#Функция проверяет столкновение противнка и игрока
def check_collisions_char_enemy(): 
    for enemy in enemies:
        if x_pushka + 8 <= enemy.x + 75 <= x_pushka + 43:
            if y_pushka + 6 <= enemy.y + 59 <= y_pushka + 97:
                del enemies[enemies.index(enemy)]
                return True

        if x_pushka + 8 <= enemy.x + 51 <= x_pushka + 43:
            if y_pushka + 6 <= enemy.y + 59 <= y_pushka + 97:
                del enemies[enemies.index(enemy)]
                return True  
                
        if x_pushka + 8 <= enemy.x + 95 <= x_pushka + 43:
            if y_pushka + 6 <= enemy.y + 9 <= y_pushka + 97:
                del enemies[enemies.index(enemy)]
                return True  

        if x_pushka + 8 <= enemy.x + 30 <= x_pushka + 43:
            if y_pushka + 6 <= enemy.y + 9 <= y_pushka + 97:
                del enemies[enemies.index(enemy)]
                return True

#Функция проверяет столкновение летающего сердца и игрока
def check_collisions_char_heart(): 
    if len(hearts_arr1) != 3: 
        for heart in arr_for_fly_hearts:
            if x_pushka + 8 <= heart[0] + 19 <= x_pushka + 43:
                if y_pushka + 6 <= heart[1] + 25 <= y_pushka + 97:
                    if len(hearts_arr) < 3:
                        hearts_arr.append([hearts_arr[-1][0] + 37, 15, image_heart])
                    else:
                        if len(hearts_arr1) == 0:
                            hearts_arr1.append([530, 50, image_heart])  
                        else:
                            hearts_arr1.append([hearts_arr1[-1][0] + 37, 50, image_heart])      
              
                    del arr_for_fly_hearts[arr_for_fly_hearts.index(heart)]
                    return True

            if x_pushka + 8 <= heart[0] + 9 <= x_pushka + 43:
                if y_pushka + 6 <= heart[1] + 25 <= y_pushka + 97:
                    if len(hearts_arr) < 3:
                        hearts_arr.append([hearts_arr[-1][0] + 37, 15, image_heart])
                    del arr_for_fly_hearts[arr_for_fly_hearts.index(heart)]
                    return True  
                
            if x_pushka + 8 <= heart[0] + 25 <= x_pushka + 43:
                if y_pushka + 6 <= heart[1] + 4 <= y_pushka + 97:
                    if len(hearts_arr) < 3:
                        hearts_arr.append([hearts_arr[-1][0] + 37, 15, image_heart])
                    del arr_for_fly_hearts[arr_for_fly_hearts.index(heart)]
                    return True  

            if x_pushka + 8 <= heart[1] + 6 <= x_pushka + 43:
                if y_pushka + 6 <= heart[1] + 4 <= y_pushka + 97:
                    if len(hearts_arr) < 3:
                        hearts_arr.append([hearts_arr[-1][0] + 37, 15, image_heart])
                    del arr_for_fly_hearts[arr_for_fly_hearts.index(heart)] 
                    return True  

def check_wether_bullet_in_character():
    global rect6
    for bullet in bullets_for_enemy:
        if rect6.topright[0] >= bullet.x >= rect6.topleft[0]:
            if rect6.bottomleft[1] >= bullet.y >= rect6.topleft[1]:
                bullets_for_enemy.pop(bullets_for_enemy.index(bullet))
                #arr_for_bullets_in_character.append(1)
                return True  

#Координаты босса
x_boss = 285
y_boss = -100

#Функция вызывает вылет котейка босса
def cat_is_standing_on_spot():
    global x_boss, y_boss, width_rect
    if width_rect != 0:
        display.blit(picture_of_boss, (x_boss, y_boss))
        if y_boss <= 200:
            y_boss += 4   

#Скорость передвижения босса
speed_boss = 12
#Направление босса
direction = 'right'
#передвижение босса по достижению 200 пикселей слева направо
def boss_move():
    global y_boss, speed_boss, x_boss, direction
    if y_boss == 204:
        x_boss += speed_boss
        if x_boss >= display_width - 80:
            direction = 'left'
        elif x_boss <= 0:
            direction = 'right'

        if direction == 'right':
            if speed_boss < 0:
                speed_boss = 12
            else:
                speed_boss = +speed_boss    
        elif direction == 'left':
            speed_boss = -12 

#массив для пуль босса  
arr_for_bull_boss = []   

number_for_random_for_boss_bullets = 10

#Добавление пуль в массив для пуль босса
def append_boss_bullets():
    global number_for_random_for_boss_bullets
    if y_boss == 204:
        randomNum = random.randint(0, number_for_random_for_boss_bullets) 
        if randomNum == 0:
            arr_for_bull_boss.append(Bullet(x_boss + 40, y_boss + 39, 5, RED, 7))

#Функция по отрисовке пуль босса
def draw_bullets_boss():
    for bullet in arr_for_bull_boss:
        bullet.draw_bullets()        

#Функция по передвижению пуль босса
def move_bullets_boss():
    for bullet in arr_for_bull_boss:
        if bullet.y < 650:
            bullet.y += bullet.speed  

width_rect = 300
#Функция по отрисовке линии жизней босса
def draw_boss_xp():
    if y_boss == 204:
        pygame.draw.lines(display, (255, 255, 255), True, [[170 - 3, 120 - 3], [470 + 3, 120 - 3], [470 + 3, 140 + 3], [170 - 3, 140 + 3]], 3)
        pygame.draw.rect(display, RED, (170, 120, width_rect, 20))                                

minus_boss_xp = 20
#Функция проверки столкновения пули и босса
def check_wether_bull_in_boss():
    global x_boss, y_boss, width_rect, score, minus_boss_xp
    if width_rect != 0 and y_boss == 204:
        if len(bullets) != 0:
            for bullet in bullets:
                if x_boss <= bullet.x <= x_boss + 80 or x_boss <= bullet.x + 5 <= x_boss + 80:
                    if y_boss <= bullet.y <= y_boss + 79:  
                        del bullets[bullets.index(bullet)]  
                        width_rect -= minus_boss_xp

                        score += 10
                        
                        dead_enemy.set_volume(0.5)
                        dead_enemy.play()      

#переменная для запуска цикла сцены полета главного персонажа
fly = True  

#Функция запуска игры после победы босса
def after_boss():                         
    global x_pushka, y_pushka, shows_menu, shows_lose, running, fly, rect6, boss, level
    shows_lose = False
    level += 1
    shows_menu = False
    fly = False
    running = True
    display.blit(BG, (0,0))
    del bullets[0:]
    del arr_for_bull_boss[0:]
    del bullets_for_enemy[0:]
    draw_bullets()
    boss = False
    x_pushka = 300
    y_pushka = 480
    game()
    draw_bullets()    
    enemies_draw()
    move_enemy()
    check_wether_bullet_in_character() 
    del_enemy_lower_height()
    check_how_much_enemies_are_visible()
    enemy_strike()
    draw_enemies_bullets()
    enemies_bullets_move()
    append_rects_for_enemies()
    append_fly_heart()
    draw_hearts_fly()
    move_fly_hearts()
    check_collisions_bull_enemy()
    check_collisions_char_heart()
    draw_hearts() 
    append_bullet()
    levels()
    draw_score()
    game()

#Функция по улетанию персонажа после победы босса
def fly_pers():
    global y_pushka, x_pushka, image_puska, fly
    while fly:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()   
         
        display.blit(BG, (0, 0))
        if y_pushka >= -120:
            display.blit(image_puska, (x_pushka, y_pushka))  

        y_pushka -= 10

        if y_pushka <= -120:
            fly = False
            after_boss()

        pygame.display.update()  
        clock.tick(30)               

boss = True
#Функция для активации босса после 5000 очков
def boss_here():
    global running, x_pushka, y_pushka, image_puska, score, boss, shows_lose, fly, number_for_random_for_boss_bullets
    #Ставим на стоп главный цикл
    running = False
    #Запускаем цикл выхода босса   
    while boss:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                running = False    
                shows_menu = False
            #Добавление пули в массив пуль и их отрисовка    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused()        
                #Добавляем пули в список при нажатии пробела    
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(round(x_pushka + 27), round(y_pushka + 40), 5, RED, 7))
                    shoot.set_volume(0.5)
                    shoot.play()  
        #Заливка экрана             
        display.blit(BG, (0,0))
        
        #Убираемс экрана врагов
        del enemies[0:]
       
        #Устанавлеваем скорость пушке
        speed_pushka = 2

        #Рисуем наши жизни
        draw_hearts()
        
        #Рисует пушку
        if len(hearts_arr) != 0:
            display.blit(image_puska, (x_pushka, y_pushka))
        
        #Проверяет сьолкновение пули босса и игрока
        def check_wether_bullet_in_character2():
            for bullet in arr_for_bull_boss:
                if rect6.topright[0] >= bullet.x >= rect6.topleft[0]:
                    if rect6.bottomleft[1] >= bullet.y >= rect6.topleft[1]:
                        arr_for_bull_boss.pop(arr_for_bull_boss.index(bullet))
                        return True      

        rect6 = pygame.Rect((x_pushka + 8, y_pushka + 4, 35, 100))                  
        
        #Получение ключей для передвижения пушки
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and x_pushka > 0 + 4:
            x_pushka -=  4
        if keys[pygame.K_RIGHT] and x_pushka < 650 - 64:
            x_pushka += 4  

        if check_wether_bullet_in_character2() == True:
            if len(hearts_arr1) == 0:
                del hearts_arr[-1]
            else:
                del hearts_arr1[-1]
            dead_player.set_volume(0.5)
            dead_player.play()          

        #Движение пуль и удаление ненужных
        for bullet in bullets:
            if bullet.y > 0:
                bullet.y -= bullet.speed
            else:
                bullets.pop(bullets.index(bullet))   

        #Проверка на проигрыш    
        if len(hearts_arr) == 0: 
            shows_lose = True          
            boss = False    
            running = True                           
            lose()               
         
        #Отрисовка пуль 
        draw_bullets() 
         
        #Вызов функции подхода босса на место передвижения
        cat_is_standing_on_spot()  
        
        if width_rect != 0:
            #вызов функции по проверке не попала ли пуля босса в перса
            check_wether_bullet_in_character2()
        
            #Вызов функции по проверке попадания пули в босса
            check_wether_bull_in_boss()
        
            #вызов функции по отрисове жизней босса
            draw_boss_xp()

            #Вызов функции по передвижению босса
            boss_move() 
        
            #Вызов функции по добавлению пуль босса в массив для пуль босса
            append_boss_bullets()

            #Вызов функции по отресовке пуль босса
            draw_bullets_boss()

            #Вызов функции по передвижению пуль босса
            move_bullets_boss()
            
            #Отрисовка очков
            draw_score()
        else:
            del arr_for_bull_boss[0:]
            fly_pers()
            fly = True
            boss = False

        #Обновление экрана
        pygame.display.update()  
        
        #FPS
        clock.tick(30)    

kl = []

#Переменная для очков за убитых врагов
score = 0                        

#Выводит очки на экран
def draw_score():
    global score

    #Выводит очки на экран
    print_text('Score:' + str(score), 300, 10, 30, (62, 130, 38)) 

#Константа для номера уровня
level = 1
def levels():
    global level
    #Выводит номер уровня на экран
    print_text('Level:' + str(level), 15, 10, 30, (62, 130, 38))                             

#Добавление сердец в их массив 
append_hearts()

#Рисует пули
def draw_bullets():
    for bullet in bullets:
        bullet.draw_bullets() 

#Массив для летающих сердец
arr_for_fly_hearts = []

#Добавляет в список летающих сердец екземпляр сердца
def append_fly_heart():
    number_ran_flyHearts = random.randint(0, 300) 
    if number_ran_flyHearts == 0 and len(arr_for_fly_hearts) <= 1:
        arr_for_fly_hearts.append([random.randint(0, display_width - 45), random.randint(-2000, -150), image_heart])

#Рисует летающие сердца
def draw_hearts_fly():
    for heart in arr_for_fly_hearts:
        display.blit(heart[2], (heart[0], heart[1])) 

speed_fly_hearts = 2

#Перемещяет  летающие сердца
def move_fly_hearts():
    global speed_fly_hearts
    for heart in arr_for_fly_hearts:
        if heart[1] < display_height + 100:
            heart[1] += speed_fly_hearts
        else:
            arr_for_fly_hearts.pop(arr_for_fly_hearts.index(heart))

#Выводит текст при паузе
def print_text(text, x, y, size, color):
    text1 = pygame.font.SysFont('Arial', size)
    pri = text1.render(text, 1, color)
    display.blit(pri, (x, y))        

#Остонавливает игру на паузу            
def paused():
    pause = True   
    while pause:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()   

        print_text('Pause. Press ENTER to continue', 35 , 250, 48, (45, 61, 204)) 
         
        ke = pygame.key.get_pressed() 
        if ke[pygame.K_KP_ENTER]:
            pause = False 

        pygame.display.update()  
        clock.tick(30)

#Добавляем пули в массив после нажатия на пробел
def append_bullet():
    for event in pygame.event.get():    
        if event.type == pygame.KEYDOWN:        
            #Добавляем пули в список при нажатии пробела    
            if event.key == pygame.K_SPACE:
                bullets.append(Bullet(round(x_pushka + 27), round(y_pushka + 40), 5, RED, 7))     
                shoot.set_volume(0.5)
                shoot.play() 

#Массив для ректов пушки
arr_rects_puska = []

#Картинка для фона меню
menu_back = pygame.image.load(os.path.join(base_path, "background.jpg"))

#Кнопки из класса кнопок окна меню
btn_2 = Button(210, 80)
btn_4 = Button(210, 80)

#Кнопки из класса кнопок окна проигрыша
btn_3 = Button(210, 80)
btn_22 = Button(210, 80)

#переменная для цикла меню
shows_menu = True

#Функция для показа меню
def show_menu():
    global bt_2, bt_4, shows_menu

    while shows_menu:
        clock.tick(FPS)
        
        #Проверка на выход из цикла
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
         
        #Рисует фон меню
        display.blit(BG, (0, 0))

        print_text('Menu', 265, 45, 60, (45, 61, 204))
        btn_2.draw_button(display_width // 2 - 105.5, 150, 'Start', round(280.5), 160, 50, start_game)
        btn_4.draw_button(display_width // 2 - 105.5, 250, 'Quit', round(280.5), 260, 50, quits)

        pygame.display.update()
        
        clock.tick(FPS)
         
#Переменная для показа меню проигрыша         
shows_lose = True
#Функция для отображения экрана проигрыша
def lose():
    global bt_3, bt_4, shows_lose

    while shows_lose:
        clock.tick(FPS)
         
        #Заливка экрана
        display.blit(BG, (0, 0))

        #Проверка на выход из цикла
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
         
        #Кнопки и текст для меню проигрыша
        print_text('You lose!', 230, 45, 60, (45, 61, 204))
        btn_3.draw_button(display_width // 2 - 105.5, 150, 'Start again', round(225), 160, 50, start_game_again)
        btn_4.draw_button(display_width // 2 - 105.5, 250, 'Quit', round(280.5), 260, 50, quits)

        pygame.display.update()
        
        clock.tick(FPS)

#Начатие игры
def start_game():
    game()

#Выход из игры по нажанию игры
def quits():
    pygame.quit()
    sys.exit()      

#Переменная цикла
running = True                                               

game_over = True

y = 80
num = 120
#Начать игру по новой после проирыша
def start_game_again():

    #Глобальные координаты
    global  x_heart, y, num, score, level, width_rect, y_boss, x_boss
    
    #Аннулирование очков
    score = 0

    #Удаление пуль пущенных боссом раннее
    del arr_for_bull_boss[0:] 

    #Возврат координатов босса га их прежние значения
    y_boss = -100
    x_boss = 285

    #Обновление жизней босса
    width_rect = 300 

    #Аннулирование достигнутых уровней
    level = 1

    #Обновление координаты пушки
    x_pushka = 300 

    #Удаленнтие пуль пущенных в предыдущим уровне 
    del bullets[0:]

    #Удаление пуль пущенных противником в предыдущем уровне
    del bullets_for_enemy[0:]

    #Обновление z координат сердец 
    x_heart = 530
    y_heart = 15

    #Удаление противников с того уровня
    del enemies[0:]

    #Удаление летающих сердец с тогог уровня
    del arr_for_fly_hearts[0:]

    #Обновление массива сердец
    append_hearts()
    
    #Вызываем игру по новой
    game()    
        
#Кнопки из класса кнопок для меню и окна проигрыша
btn_7 = Button(110, 80)
btn_8 = Button(220, 80)        

arr_for_bullets_in_character = []

#Игровой цикл
def game():
    global running, x_pushka, minus_boss_xp, y_pushka, shows_menu, shows_lose, number_for_random_for_boss_bullets, game_over, x_heart, y_heart, rect6, boss, y_boss, x_boss, width_rect
    #shows_lose = False
    while running:
        clock.tick(FPS)
        #Проверка на выход из цикла
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                running = False    
                shows_menu = False
            #Добавление пули в массив пуль и их отрисовка    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused()        
                #Добавляем пули в список при нажатии пробела    
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(round(x_pushka + 27), round(y_pushka + 40), 5, RED, 7))
                    shoot.set_volume(0.5)
                    shoot.play()     

        #Движение пушки
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and x_pushka > 0 + 4:
            x_pushka -=  4
        if keys[pygame.K_RIGHT] and x_pushka < 650 - 64:
            x_pushka += 4                 

        #Второй рект для корпуса пушки
        rect6 = pygame.Rect((x_pushka + 8, y_pushka + 4, 35, 100))   
            
        #Проверка на проигрыш    
        if len(hearts_arr) == 0:  
            shows_lose = True                                                     
            lose()      

        if score == 100 or score == 10000 or score == 15000:
            #Удаленнтие пуль пущенных в предыдущим уровне 
            del bullets[0:]
            #Возврат координатов босса га их прежние значения
            y_boss = -100
            x_boss = 285

            minus_boss_xp -= 5  
            number_for_random_for_boss_bullets -= 1  
            #Обновление жизней босса
            width_rect = 300 
            shows_lose = False
            boss = True
            boss_here()             

        #Движение пуль и удаление ненужных
        for bullet in bullets:
            if bullet.y > 0:
                bullet.y -= bullet.speed
            else:
                bullets.pop(bullets.index(bullet))  

        #Если функция по проверке координат пули противника и ректа главногго 
        # героя возвращает правду то уменьшение жизней         
        if check_wether_bullet_in_character() == True or check_collisions_char_enemy() == True:
            if len(hearts_arr1) == 0:
                del hearts_arr[-1]
            else:
                del hearts_arr1[-1]
            dead_player.set_volume(0.5)
            dead_player.play()   

        #Заливаем экран картинкой
        display.blit(BG, (0, 0))   

        #Рисует пушку
        if len(hearts_arr) != 0:
            display.blit(image_puska, (x_pushka, y_pushka))                                                

        #Отрисовывает все пули
        draw_bullets()
        
        #Вызов функции по отрисовке врагов
        enemies_draw()
        
        #Вызов фунции по передвижению врагов
        move_enemy()

        #Вызов функции по проверке
        # координат пули врага и ректа персонажа
        check_wether_bullet_in_character() 

        #Вызов функции по удалению вргаов которые перевалили за низ экрана
        del_enemy_lower_height()
        
        #вызов функция проверяет если три врага скрылись тот добавляет 
        #еще врагов
        check_how_much_enemies_are_visible()

        #Вызов функции по отстрелке врагов
        enemy_strike()

        #Вызов функции по отрисовке пуль противника
        draw_enemies_bullets()
        
        #Вызов функции по передвижению пуль врагов
        enemies_bullets_move()

        #Вызов функции по добавлению ректов врагов в их массив
        append_rects_for_enemies()
        
        #Вызов функции по добавлению летающих сердец в их список
        append_fly_heart()

        #Вызов функции  по отресовке летающих сердец
        draw_hearts_fly()

        #Вызов функции по передвижению летающих сердец
        move_fly_hearts()
        
        #Вызов функции по проверке столкновения пули и противника
        check_collisions_bull_enemy()

        #Вызов функции по проверке столкновения игрока и летающего сердца
        check_collisions_char_heart()
        
        #Рисует сердечки
        draw_hearts() 
          
        #Добавляет пули пушки в их массив при нажатии пробела  
        append_bullet()

        #Вызов функции по отрисовке номера уровня
        levels()

        #вызов функции по выводу очков на экран
        draw_score()

        #Обновление экрана
        pygame.display.update()    

show_menu()
game()

  




















