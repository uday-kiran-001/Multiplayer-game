# code for developing car racing game in python
import pygame
import time
import random
 
# initialize pygame and set the colors
pygame.init()
gray = (119, 118, 110)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 200)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
bright_blue = (0, 0, 255)
display_width = 800
display_height = 600 
# Race track dimensions
background_width = 840
background_height = 650

# Player details
player_name = ""
room_id = "" 
 


gamedisplays = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("car game")
clock = pygame.time.Clock()
carimg = pygame.image.load('bike1.png')
backgroundpic = pygame.image.load("road2.png")
# yellow_strip = pygame.image.load("yellow-stripe.png")
# strip = pygame.image.load("white-stripe.png")
intro_background = pygame.image.load("background.jpg")
instruction_background = pygame.image.load("background.jpg")
car_width = 47
car_height = 107
pause = False
 
# Intro screen
 
 
def intro_loop():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
        gamedisplays.blit(intro_background, (0, 0))
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("CAR GAME", largetext)
        TextRect.center = (400, 100)
        gamedisplays.blit(TextSurf, TextRect)
        button("START", 150, 520, 100, 50, green,
               bright_green, "play")
        button("QUIT", 550, 520, 100,
               50,
               red,
               bright_red,
               "quit")
        button("INSTRUCTION", 300, 520, 200,
               50, blue, bright_blue,
               "intro")
        pygame.display.update()
        clock.tick(50)

def enter_details():
    global player_name
    global room_id
    intro = True
    text_font = pygame.font.Font(None, 36)
    text_color = black
    name_input_box = pygame.Rect(300, 300, 200, 30)  # Define the input box position and size
    room_id_box = pygame.Rect(300, 360, 200, 30)
    active1 = False  # Flag to track if the input box is active1 (selected)
    active2 = False
    
    while intro:
        gamedisplays.fill(gray)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is inside the input box
                if name_input_box.collidepoint(event.pos):
                    active1 = not active1  # Toggle the active1 state
                else:
                    active1 = False
                if room_id_box.collidepoint(event.pos):
                    active2 = not active2
                else:
                    active2 = False
            if event.type == pygame.KEYDOWN:
                if active1:
                    if event.key == pygame.K_RETURN:
                        print("Player Name: ", player_name)
                        player_name = ""  
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode
                if active2:
                    if event.key == pygame.K_RETURN:
                        print("Room Id: ", room_id)
                        room_id = ""  
                    elif event.key == pygame.K_BACKSPACE:
                        room_id = room_id[:-1]
                    else:
                        room_id += event.unicode

        # Render the name input box
        txt_surface = text_font.render(player_name, True, text_color)
        width = max(200, txt_surface.get_width()+10)
        name_input_box.w = width
        gamedisplays.blit(txt_surface, (name_input_box.x+5, name_input_box.y+5))
        pygame.draw.rect(gamedisplays, text_color, name_input_box, 2)

        # Render the room Id input box
        txt_surface = text_font.render(room_id, True, text_color)
        width = max(200, txt_surface.get_width()+10)
        room_id_box.w = width
        gamedisplays.blit(txt_surface, (room_id_box.x+5, room_id_box.y+5))
        pygame.draw.rect(gamedisplays, text_color, room_id_box, 2)

        # Render text('Name') 
        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render('Name ', True, green, blue)
        textRect = text.get_rect()
        textRect.center = ((200, 310))
        gamedisplays.blit(text, textRect)

        # Render text('Room Id') 
        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render('Room Id ', True, green, blue)
        textRect = text.get_rect()
        textRect.center = ((200, 380))
        gamedisplays.blit(text, textRect)

        button("ENTER", 300, 420, 200, 50, blue, bright_blue, "details")
        
        pygame.display.update()
        clock.tick(50)


# def intro_loop():
#     global player_name
#     global room_id
#     intro = True
#     text_font = pygame.font.Font(None, 36)
#     text_color = black
#     name_input_box = pygame.Rect(300, 300, 200, 30)  # Define the input box position and size
#     room_id_box = pygame.Rect(300, 360, 200, 30)
#     active1 = False  # Flag to track if the input box is active1 (selected)
#     active2 = False

#     while intro:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 quit()
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 # Check if the mouse click is inside the input box
#                 if name_input_box.collidepoint(event.pos):
#                     active1 = not active1  # Toggle the active1 state
#                 else:
#                     active1 = False
#                 if room_id_box.collidepoint(event.pos):
#                     active2 = not active2
#                 else:
#                     active2 = False
#             if event.type == pygame.KEYDOWN:
#                 if active1:
#                     if event.key == pygame.K_RETURN:
#                         print("Player Name: ", player_name)
#                         player_name = ""  
#                     elif event.key == pygame.K_BACKSPACE:
#                         player_name = player_name[:-1]
#                     else:
#                         player_name += event.unicode
#                 if active2:
#                     if event.key == pygame.K_RETURN:
#                         print("Room Id: ", room_id)
#                         room_id = ""  
#                     elif event.key == pygame.K_BACKSPACE:
#                         room_id = room_id[:-1]
#                     else:
#                         room_id += event.unicode

#         gamedisplays.blit(intro_background, (0, 0))
#         largetext = pygame.font.Font('freesansbold.ttf', 115)
#         TextSurf, TextRect = text_objects("CAR GAME", largetext)
#         TextRect.center = (400, 100)
#         gamedisplays.blit(TextSurf, TextRect)

#         # Render the name input box
#         txt_surface = text_font.render(player_name, True, text_color)
#         width = max(200, txt_surface.get_width()+10)
#         name_input_box.w = width
#         gamedisplays.blit(txt_surface, (name_input_box.x+5, name_input_box.y+5))
#         pygame.draw.rect(gamedisplays, text_color, name_input_box, 2)

#         # Render the room Id input box
#         txt_surface = text_font.render(room_id, True, text_color)
#         width = max(200, txt_surface.get_width()+10)
#         room_id_box.w = width
#         gamedisplays.blit(txt_surface, (room_id_box.x+5, room_id_box.y+5))
#         pygame.draw.rect(gamedisplays, text_color, room_id_box, 2)

#         button("START", 150, 520, 100, 50, green, bright_green, "play")
#         button("QUIT", 550, 520, 100, 50, red, bright_red, "quit")
#         button("INSTRUCTION", 300, 520, 200, 50, blue, bright_blue, "intro")
#         button("ENTER", 300, 420, 200, 50, blue, bright_blue, "details")

#         # Render text('Name') 
#         font = pygame.font.Font('freesansbold.ttf', 30)
#         text = font.render('Name ', True, green, blue)
#         textRect = text.get_rect()
#         textRect.center = ((200, 310))
#         gamedisplays.blit(text, textRect)

#         # Render text('Room Id') 
#         font = pygame.font.Font('freesansbold.ttf', 30)
#         text = font.render('Room Id ', True, green, blue)
#         textRect = text.get_rect()
#         textRect.center = ((200, 380))
#         gamedisplays.blit(text, textRect)

#         pygame.display.update()
#         clock.tick(50)

 
 
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gamedisplays,
                         ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "play":
                countdown()
            elif action == "quit":
                pygame.quit()
                quit()
                sys.exit()
            elif action == "intro":
                introduction()
            elif action == "details":
                get_validation_from_server()
            # elif action == "menu":
            #     intro_loop()
            # elif action == "pause":
            #     paused()
            # elif action == "unpause":
            #     unpaused()
 
    else:
        pygame.draw.rect(gamedisplays,
                         ic,
                         (x, y, w, h))
    smalltext = pygame.font.Font("freesansbold.ttf", 20)
    textsurf, textrect = text_objects(msg, smalltext)
    textrect.center = ((x+(w/2)), (y+(h/2)))
    gamedisplays.blit(textsurf, textrect)
 
def get_validation_from_server():
    print("Enter Clicked")
    intro_loop()

def introduction():
    introduction = True
    while introduction:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
        gamedisplays.blit(instruction_background, (0, 0))
        largetext = pygame.font.Font('freesansbold.ttf', 80)
        smalltext = pygame.font.Font('freesansbold.ttf', 20)
        mediumtext = pygame.font.Font('freesansbold.ttf', 40)
        textSurf, textRect = text_objects(
            "This is an car game in which you" +
            "need dodge the coming cars", smalltext)
        textRect.center = ((350), (200))
        TextSurf, TextRect = text_objects("INSTRUCTION", largetext)
        TextRect.center = ((400), (100))
        gamedisplays.blit(TextSurf, TextRect)
        gamedisplays.blit(textSurf, textRect)
        stextSurf, stextRect = text_objects(
            "ARROW LEFT : LEFT TURN", smalltext)
        stextRect.center = ((150), (400))
        hTextSurf, hTextRect = text_objects(
            "ARROW RIGHT : RIGHT TURN", smalltext)
        hTextRect.center = ((150), (450))
        atextSurf, atextRect = text_objects("A : ACCELERATOR", smalltext)
        atextRect.center = ((150), (500))
        rtextSurf, rtextRect = text_objects("B : BRAKE ", smalltext)
        rtextRect.center = ((150), (550))
        ptextSurf, ptextRect = text_objects("P : PAUSE  ", smalltext)
        ptextRect.center = ((150), (350))
        sTextSurf, sTextRect = text_objects("CONTROLS", mediumtext)
        sTextRect.center = ((350), (300))
        gamedisplays.blit(sTextSurf, sTextRect)
        gamedisplays.blit(stextSurf, stextRect)
        gamedisplays.blit(hTextSurf, hTextRect)
        gamedisplays.blit(atextSurf, atextRect)
        gamedisplays.blit(rtextSurf, rtextRect)
        gamedisplays.blit(ptextSurf, ptextRect)
        button("BACK", 600, 450, 100, 50, blue,
               bright_blue, "menu")
        pygame.display.update()
        clock.tick(30)
 
 
# def paused():
#     global pause
 
#     while pause:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 quit()
#                 sys.exit()
#         gamedisplays.blit(instruction_background, (0, 0))
#         largetext = pygame.font.Font('freesansbold.ttf', 115)
#         TextSurf, TextRect = text_objects("PAUSED", largetext)
#         TextRect.center = (
#             (display_width/2),
#             (display_height/2)
#         )
#         gamedisplays.blit(TextSurf, TextRect)
#         button("CONTINUE", 150, 450,
#                150, 50, green,
#                bright_green, "unpause")
#         button("RESTART", 350, 450, 150,
#                50, blue, bright_blue,
#                "play")
#         button("MAIN MENU", 550, 450,
#                200, 50, red, bright_red,
#                "menu")
#         pygame.display.update()
#         clock.tick(30)
 
 
# def unpaused():
#     global pause
#     pause = False
 
 
def countdown_background():
    font = pygame.font.SysFont(None, 25)
    x = (display_width*0.45)
    y = (display_height*0.8)
    gamedisplays.blit(backgroundpic, (0, 0))
    gamedisplays.blit(backgroundpic, (0, 200))
    gamedisplays.blit(backgroundpic, (0, 400))
    gamedisplays.blit(backgroundpic, (700, 0))
    gamedisplays.blit(backgroundpic, (700, 200))
    gamedisplays.blit(backgroundpic, (700, 400))

    gamedisplays.blit(carimg, (x, y))
    text = font.render("DODGED: 0", True, black)
    score = font.render("SCORE: 0", True, red)
    gamedisplays.blit(text, (0, 50))
    gamedisplays.blit(score, (0, 30))
    # button("PAUSE", 650, 0, 150, 50, blue, bright_blue, "pause")
 
 
def countdown():
    countdown = True
 
    while countdown:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
        gamedisplays.fill(gray)
        countdown_background()
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("3", largetext)
        TextRect.center = (
            (display_width/2),
            (display_height/2))
        gamedisplays.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)
        gamedisplays.fill(gray)
        countdown_background()
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("2", largetext)
        TextRect.center = (
            (display_width/2),
            (display_height/2))
        gamedisplays.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)
        gamedisplays.fill(gray)
        countdown_background()
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("1", largetext)
        TextRect.center = (
            (display_width/2),
            (display_height/2))
        gamedisplays.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)
        gamedisplays.fill(gray)
        countdown_background()
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("GO!!!", largetext)
        TextRect.center = (
            (display_width/2),
            (display_height/2))
        gamedisplays.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)
        game_loop()
 
 
def obstacle(obs_startx, obs_starty, obs):
    if obs == 0:
        obs_pic = pygame.image.load("bike6.png")
    elif obs == 1:
        obs_pic = pygame.image.load("bike6.png")
    elif obs == 2:
        obs_pic = pygame.image.load("bike6.png")
    elif obs == 3:
        obs_pic = pygame.image.load("bike6.png")
    elif obs == 4:
        obs_pic = pygame.image.load("bike6.png")
    elif obs == 5:
        obs_pic = pygame.image.load("bike6.png")
    elif obs == 6:
        obs_pic = pygame.image.load("bike6.png")
    gamedisplays.blit(obs_pic, (obs_startx, obs_starty))
 
 
def score_system(passed, score):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Passed"+str(passed), True, black)
    score = font.render("Score"+str(score), True, red)
    gamedisplays.blit(text, (0, 50))
    gamedisplays.blit(score, (0, 30))
 
 
def text_objects(text, font):
    textsurface = font.render(text, True, black)
    return textsurface, textsurface.get_rect()
 
 
def message_display(text):
    largetext = pygame.font.Font("freesansbold.ttf", 80)
    textsurf, textrect = text_objects(text, largetext)
    textrect.center = (
        (display_width/2),
        (display_height/2))
    gamedisplays.blit(textsurf, textrect)
    pygame.display.update()
    time.sleep(3)
    # game_loop()
 
 
def crash():
    message_display("YOU CRASHED")
    # pygame.display.update()
    # time.sleep(3)
    intro_loop()
 
 
def background():
    gamedisplays.blit(backgroundpic, (0, 0))
    gamedisplays.blit(backgroundpic, (0, 200))
    gamedisplays.blit(backgroundpic, (0, 400))
    gamedisplays.blit(backgroundpic, (700, 0))
    gamedisplays.blit(backgroundpic, (700, 200))
    gamedisplays.blit(backgroundpic, (700, 400))
    # gamedisplays.blit(yellow_strip, (400, 0))
    # gamedisplays.blit(yellow_strip, (400, 100))
    # gamedisplays.blit(yellow_strip, (400, 200))
    # gamedisplays.blit(yellow_strip, (400, 300))
    # gamedisplays.blit(yellow_strip, (400, 400))
    # gamedisplays.blit(yellow_strip, (400, 500))
    # gamedisplays.blit(strip, (120, 0))
    # gamedisplays.blit(strip, (120, 100))
    # gamedisplays.blit(strip, (120, 200))
    # gamedisplays.blit(strip, (680, 0))
    # gamedisplays.blit(strip, (680, 100))
    # gamedisplays.blit(strip, (680, 200))
 
 
def car(x, y):
    gamedisplays.blit(carimg, (x, y))
 
 
def game_loop():
    global pause
    x = (display_width*0.45)
    y = (display_height*0.8)
    x_change = 0
    obstacle_speed = 9
    obs = 0
    y_change = 0
    obs_startx = random.randrange(200, (display_width-200))
    obs_starty = -750
    obs_width = 47
    obs_height = 107
    passed = 0
    level = 0
    score = 0
    y2 = 7
    fps = 120
 
    bumped = False
    while not bumped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # print(event.type, pygame.KEYUP, pygame.KEYDOWN, pygame.K_LEFT, pygame.K_RIGHT )
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_UP:
                    y_change -= 5
                if event.key == pygame.K_DOWN:
                    y_change += 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    x_change = 0
                if event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP:
                    y_change = 0 
                if event.key == pygame.K_DOWN:
                    y_change = 0
 
        x += x_change
        y += y_change
        # pause = True
        gamedisplays.fill(gray)

        rel_y = y2 % background_height

        # Adjust the blitting positions for the background
        gamedisplays.blit(backgroundpic, (0, rel_y - background_height))
        gamedisplays.blit(backgroundpic, (0, rel_y))

        # For the right side of the screen, you need to adjust the x-coordinate
        # gamedisplays.blit(backgroundpic, (background_width, rel_y - background_height))
        # gamedisplays.blit(backgroundpic, (background_width, rel_y))

        # Update the condition for seamless scrolling
        # if rel_y < background_height:
        #     gamedisplays.blit(backgroundpic, (0, rel_y + background_height))
        #     gamedisplays.blit(backgroundpic, (background_width, rel_y + background_height))

        # This is Geeks for geeks
        # rel_y = y2 % backgroundpic.get_rect().width
        # gamedisplays.blit(
        #     backgroundpic, (0,
        #                     rel_y-backgroundpic.get_rect().width))
        # gamedisplays.blit(backgroundpic,
        #                   (550, rel_y -
        #                    backgroundpic.get_rect().width))
        # if rel_y < 750:
        #     gamedisplays.blit(backgroundpic, (0, rel_y))
        #     gamedisplays.blit(backgroundpic, (550, rel_y))
 
        y2 += obstacle_speed
 
        obs_starty -= (obstacle_speed/4)
        obstacle(obs_startx, obs_starty, obs)
        obs_starty += obstacle_speed
        car(x, y)
        score_system(passed, score)
        print(x, y, car_width, obs_startx, obs_starty, display_width, display_height, obs_width, obs_height)

        # Collision with Side tracks/walls
        if x > 690-car_width or x < 110:
            crash()
        if obs_starty > display_height:
            obs_starty = 0-obs_height
            obs_startx = random.randrange(170, (display_width-170))
            obs = random.randrange(0, 7)
            passed = passed+1
            score = passed*10
            # if int(passed) % 10 == 0:
            #     level = level+1
            #     obstacle_speed+2
            #     largetext = pygame.font.Font("freesansbold.ttf", 80)
            #     textsurf, textrect = text_objects(
            #         "LEVEL"+str(level), largetext)
            #     textrect.center = (
            #         (display_width/2), (display_height/2))
            #     gamedisplays.blit(textsurf, textrect)
                # pygame.display.update()
                # time.sleep(3)
 
        if y < obs_starty+obs_height and y + car_height > obs_starty:
            if (x > obs_startx and x < obs_startx + obs_width) or (x+car_width > obs_startx and x+car_width < obs_startx+obs_width):
                crash()
        pygame.display.update()
        clock.tick(60)


enter_details()
# intro_loop()
game_loop()
pygame.quit()
quit()