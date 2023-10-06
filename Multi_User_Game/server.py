import socket
import threading
import pickle
import random

IP = socket.gethostbyname(socket.gethostname())
PORT = 8080
ADDR = (IP, PORT)
FORMAT = 'utf-8'
SIZE = 1024
DISCONNECT_MSG = "!DISCONNECT"
MAX_PLAYERS = 3

# clients = []
rooms = {}
starting_positions = [(200, 480), (400, 480), (600, 480)]
display_width = 800
display_height = 600
car_width = 47
car_height = 107
obs = random.randrange(1,7)
obs_startx = random.randrange(200, (display_width-200))
obs_starty = -750

def new_connections():
    # global clients
    while True:
        new_conn, addr = server.accept()
        print(f"NEW CONNECTION : {addr}.")
        # clients.append((new_conn, addr))
        # new_conn.send("SERVER: SUCCESFULLY CONNECTED TO THE SERVER.".encode(FORMAT))
        print(f"ACTIVE CONNECTIONS : {threading.active_count() - 1}")
        recv_msgs_thread = threading.Thread(target=recv_msgs, args=(new_conn, addr))
        recv_msgs_thread.start()


def recv_msgs(new_conn, addr):
    # global clients
    global rooms
    connection = True
    details = False
    game_on = False
    global obs
    global obs_startx
    global obs_starty
    obstacle_speed = 8
    obs_width = 70
    obs_height = 130
    in_room = ""
    position = 0
    while connection:
        try: 
            if details == False:
                arr = []
                game_status = False

                # Getting Name and Room Id from player
                print("Collecting details..")
                data = new_conn.recv(SIZE)
                data = pickle.loads(data)
                name = data["name"]
                room_id = data["room_id"]
                bike_number = data["bike_num"]
                in_room = room_id
                print(f"Name: {name}, Room Id: {room_id} Bike Num: {bike_number}")
                arr.extend([(new_conn, addr), name, game_status])

                # If room already exists, then append to the room or else create a new room
                if room_id in rooms.keys():
                    arr.extend([ starting_positions[len(rooms[room_id])][0], starting_positions[len(rooms[room_id])][1], bike_number])
                    rooms[room_id].append(arr)
                else:
                    arr.extend([ starting_positions[0][0], starting_positions[0][1] , bike_number])
                    rooms[room_id] = [arr]
                
                # Sending starting coordinates for each player
                data = pickle.dumps({"x":arr[3], "y":arr[4]})
                new_conn.send(data)

                # Sending number of players in the current room to all players
                players = rooms[room_id]
                num_of_players = len(players)
                position = num_of_players  - 1
                # print(rooms)
                if num_of_players<MAX_PLAYERS:
                    for player in players:
                        player[0][0].send(f"{num_of_players}".encode(FORMAT))
                else:
                    for player in players:
                        player[2] = True
                        player[0][0].send(f"{num_of_players}".encode(FORMAT))
                details = True
            elif game_on == True:
                player = rooms[in_room][position]
                x = player[3]
                y = player[4]
                obs_startx = random.randrange(200, (display_width-200))
                obs_starty = -750
                passed = 0
                level = 0
                score = 0
                y2 = 7
                opponents_index = []
                for i in range(MAX_PLAYERS):
                    opponents_index.append((position+i+1)%MAX_PLAYERS)

                while game_on:
                    if obs_starty > display_height:
                        obs_starty = 0-obs_height
                        obs_startx = random.randrange(170, (display_width-170))
                        obs = random.randrange(1, 7)
                    data = new_conn.recv(SIZE)
                    coordinates = pickle.loads(data)
                    x = coordinates["x"]
                    y = coordinates["y"]
                    
                    res = "1"
                    opponents_position = []
                    for i in range(MAX_PLAYERS):
                        try:
                            (x1, y1, bike_num) = (rooms[in_room][opponents_index[i]][3], rooms[in_room][opponents_index[i]][4], rooms[in_room][opponents_index[i]][5])
                        except:
                            (x1, y1, bike_num) = (150*(i+1), 800, 1)
                        opponents_position.append((bike_num, x1, y1))
                        # Check if there are any collisions with other players
                        if y < opponents_position[i][1] + car_height and y + car_height > opponents_position[i][1]:
                            if (x > opponents_position[i][0] and x < opponents_position[i][0] + car_width) or (x+car_width > opponents_position[i][0] and x + car_width < opponents_position[i][0] + car_width):
                                res = "0"
                    

                    # Collisions with walls
                    if x > 710-car_width or x < 130:
                        res = "-1"
                        game_on = False
                        details = False
                        
                    # Collisions with obstacles
                    if y < obs_starty+obs_height and y + car_height > obs_starty:
                        if (x > obs_startx and x < obs_startx + obs_width) or (x+car_width > obs_startx and x+car_width < obs_startx+obs_width):
                            res = "-1"
                            game_on = False
                            details = False

                    obs_starty -= (obstacle_speed/4)
                    obs_starty += obstacle_speed

                    data = {"res":res, "obs":(obs_startx, obs_starty), "obs_img":obs, "opponents":opponents_position, "players_left":len(rooms[in_room])}
                    data = pickle.dumps(data)
                    new_conn.send(data)
                    player[3] = coordinates["x"]
                    player[4] = coordinates["y"]

                    if len(rooms[in_room])==1:
                        game_on = False
                        details = False
                        
                    if game_on == False:
                        while True:
                            try:
                                print("About to delete..")
                                for i in range(len(rooms[in_room])):
                                    if rooms[room_id][i][0][1] == addr:
                                        rooms[room_id].pop(i)
                                print(f"After Popped: {rooms[in_room]}")
                                in_room = ""
                                position = 0
                                break
                            except Exception as e:
                                print(f"{addr[1]} Error: {e}")
            else:
                players = rooms[in_room]
                for player in players:
                    if player[0][0] == new_conn and player[2]==True:
                        game_on = True
        except Exception as e:
            print(f"{addr[1]} Error: {e}")
            print(f"[ DISCONNECTED {addr} ]")
            connection = False
    new_conn.close()



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
server.bind(ADDR)
server.listen(3)
print(f"[ SERVER STARTED ON : {ADDR} ]")


conn_thread = threading.Thread(target=new_connections)
conn_thread.start()
