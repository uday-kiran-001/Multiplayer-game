import socket
import threading
import pygame
import time
import random
import pickle

IP = socket.gethostbyname(socket.gethostname())
PORT = 8080
ADDR = (IP, PORT)
FORMAT = 'utf-8'
SIZE = 1024
DISCONNECT_MSG = "!DISCONNECT"
MAX_PLAYERS = 3
BIKE_SPEED = 4
 
# Initialize pygame and set the colors
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

gamedisplays = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("car game")
clock = pygame.time.Clock()
bike_number = random.randrange(1,7)
backgroundpic = pygame.image.load("road2.png")
intro_background = pygame.image.load("background.jpg")
instruction_background = pygame.image.load("background.jpg")
car_width = 47
car_height = 107
pause = False

# Player details
player_name = "UK"
room_id = "abc" 
number_of_players = 0
x = 0
y = 0
 
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(mouse, click)
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
            elif action == "home":
                enter_details()
    else:
        pygame.draw.rect(gamedisplays,
                         ic,
                         (x, y, w, h))
    smalltext = pygame.font.Font("freesansbold.ttf", 20)
    textsurf, textrect = text_objects(msg, smalltext)
    textrect.center = ((x+(w/2)), (y+(h/2)))
    gamedisplays.blit(textsurf, textrect)

def enter_details():
    global player_name
    global room_id
    intro = True
    text_font = pygame.font.Font(None, 36)
    text_color = black
    name_input_box = pygame.Rect(300, 200, 200, 30)     # Define the input box position and size
    room_id_box = pygame.Rect(300, 250, 200, 30)
    active1 = False                                     # Flag to track if the input box is active1 (selected)
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
        text = font.render('Name ', True, black)
        textRect = text.get_rect()
        textRect.center = ((200, 215))
        gamedisplays.blit(text, textRect)

        # Render text('Room Id') 
        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render('Room Id ', True, black)
        textRect = text.get_rect()
        textRect.center = ((200, 265))
        gamedisplays.blit(text, textRect)

        button("ENTER", 300, 340, 200, 50, blue, bright_blue, "details")
        button("QUIT", 150, 520, 100,
               50,
               red,
               bright_red,
               "quit")
        button("INSTRUCTION", 500, 520, 200,
               50, blue, bright_blue,
               "intro")
        
        pygame.display.update()
        clock.tick(50)

def intro_loop():
    global number_of_players
    # print(f"At intro_loop start: {number_of_players}")
    while number_of_players!= MAX_PLAYERS:
        number_of_players = int(client.recv(SIZE).decode(FORMAT))
        print(f"Num of players in room: {number_of_players}")
        gamedisplays.blit(intro_background, (0, 0))
        largetext = pygame.font.Font('freesansbold.ttf', 40)
        TextSurf, TextRect = text_objects(f"Waiting for {MAX_PLAYERS - number_of_players}  more players..", largetext)
        TextRect.center = (400, 100)
        gamedisplays.blit(TextSurf, TextRect)
        
        pygame.display.update()
        clock.tick(50)
    countdown()

 
def get_validation_from_server():
    global player_name
    global room_id
    global number_of_players
    global x
    global y
    global bike_number
    # print("Validating..")
    data = {"name":player_name, "room_id":room_id, "bike_num":bike_number}
    data = pickle.dumps(data)
    client.send(data)
    # print("sent details")
    coordinates = client.recv(SIZE)
    coordinates = pickle.loads(coordinates)
    x = coordinates["x"]
    y = coordinates["y"]
    print(f"Starting Coordinates: {x}, {y}")
    intro_loop()

def game_loop():
    global pause
    global x
    global y
    global bike_number
    x_change = 0
    obstacle_speed = 9
    y_change = 0
    obs_startx = 0
    obs_starty = 0
    y2 = 7
 
    bumped = False
    while not bumped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -BIKE_SPEED
                if event.key == pygame.K_RIGHT:
                    x_change = BIKE_SPEED
                if event.key == pygame.K_UP:
                    y_change -= BIKE_SPEED
                if event.key == pygame.K_DOWN:
                    y_change += BIKE_SPEED
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
        data = pickle.dumps({"x":x, "y":y})
        client.send(data)
        data = client.recv(SIZE)
        data = pickle.loads(data)
        # print(data)
        obs_startx = data["obs"][0]
        obs_starty = data["obs"][1]
        obs = data["obs_img"]
        opponents_position = data["opponents"]
        players_left = data["players_left"]
        # print(f"Players Left: {players_left}")
        if players_left == 1:
            winner()

        if data["res"]== "-1":
            crash()
        elif data["res"]!= "1":
            x -= x_change
            y -= y_change

        gamedisplays.fill(gray)

        rel_y = y2 % background_height

        # Adjust the blitting positions for the background
        gamedisplays.blit(backgroundpic, (0, rel_y - background_height))
        gamedisplays.blit(backgroundpic, (0, rel_y))
 
        y2 += obstacle_speed
        obstacle(obs_startx, obs_starty, obs)
        bike(bike_number, x, y)
        for coords in opponents_position:
            bike(coords[0], coords[1], coords[2])
        

        pygame.display.update()
        clock.tick(60)

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
            "This is a Bike Game, where you will be eliminated if you hit an obstacle.", smalltext)
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
        atextSurf, atextRect = text_objects("ARROW UP : ACCELERATOR", smalltext)
        atextRect.center = ((150), (500))
        rtextSurf, rtextRect = text_objects("ARROW DOWN : BRAKE ", smalltext)
        rtextRect.center = ((150), (550))
        gamedisplays.blit(stextSurf, stextRect)
        gamedisplays.blit(hTextSurf, hTextRect)
        gamedisplays.blit(atextSurf, atextRect)
        gamedisplays.blit(rtextSurf, rtextRect)
        button("BACK", 600, 450, 100, 50, blue,
               bright_blue, "home")
        pygame.display.update()
        clock.tick(30)

def countdown_background():
    font = pygame.font.SysFont(None, 25)
    global x
    global y
    global bike_number
    gamedisplays.blit(backgroundpic, (0, 0))
    gamedisplays.blit(backgroundpic, (0, 200))
    gamedisplays.blit(backgroundpic, (0, 400))
    gamedisplays.blit(backgroundpic, (700, 0))
    gamedisplays.blit(backgroundpic, (700, 200))
    gamedisplays.blit(backgroundpic, (700, 400))

    bike(bike_number, x, y)
    # for coords in opponents_position:
    #         car(coords[0], coords[1])
 
 
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

def bike(bike_num, x, y):
    bike_img = pygame.image.load(f'bike{bike_num}.png')
    gamedisplays.blit(bike_img, (x, y))

def crash():
    global number_of_players
    number_of_players = 0
    print("YOU LOST")
    message_display("YOU LOST")
    enter_details()

def winner():
    global number_of_players
    number_of_players = 0
    print("YOU WON!!!")
    message_display("YOU WON!!!")
    enter_details()

def obstacle(obs_startx, obs_starty, obs):
    obs_pic = pygame.image.load(f"car{obs}.png")
    gamedisplays.blit(obs_pic, (obs_startx, obs_starty))


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# def recv_msgs():
#     pass

# def send_msgs():
#     pass



# recv_msgs_thread = threading.Thread(target=recv_msgs)
# recv_msgs_thread.start()

# send_msgs_thread = threading.Thread(target=send_msgs)
# send_msgs_thread.start()

enter_details()
# game_loop()
# pygame.quit()
# quit()