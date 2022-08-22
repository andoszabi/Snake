import time
import random
import tkinter as tk
from pynput import keyboard
import json

top = tk.Tk()
top.title("Snake")
top.geometry('300x400')
top.update()

def my_quit():
    top.destroy()
    exit()

class Block:

    def __init__(self, x, y, canvas):
        self.x = x
        self.y = y
        self.canvas = canvas

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def invalid(self):
        return self.x < 0 or self.x > 300 or self.y < 0 or self.y > 300

    def right(self):
        return Block(self.x + 20, self.y, self.canvas)

    def left(self):
        return Block(self.x - 20, self.y, self.canvas)

    def up(self):
        return Block(self.x, self.y - 20, self.canvas)

    def down(self):
        return Block(self.x, self.y + 20, self.canvas)

    def move(self, direction):
        switcher = {
            "right": self.right,
            "left": self.left,
            "up": self.up,
            "down": self.down,
        }
        return switcher.get(direction, "Invalid direction")()

    def where_is_it(self, other_block):
        if self.x == other_block.x:
            if self.y - other_block.y == 20:
                return "up"
            elif self.y - other_block.y == - 20:
                return "down"
        elif self.y == other_block.y:
            if self.x - other_block.x == 20:
                return "left"
            elif self.x - other_block.x == - 20:
                return "right"

    def line_creation_right(self, other_block):
        return self.canvas.create_line(self.x - 9, self.y, other_block.x + 9, other_block.y, width = 18, fill = "green")

    def line_creation_left(self, other_block):
        return self.canvas.create_line(self.x + 9, self.y, other_block.x - 9, other_block.y, width = 18, fill = "green")

    def line_creation_up(self, other_block):
        return self.canvas.create_line(self.x, self.y + 9, other_block.x, other_block.y - 9, width = 18, fill = "green")

    def line_creation_down(self, other_block):
        return self.canvas.create_line(self.x, self.y - 9, other_block.x, other_block.y + 9, width = 18, fill = "green")

    def line_creation_right_head(self, other_block):
        points = [self.x - 9, self.y + 9, self.x - 9, self.y - 9, other_block.x - 9, other_block.y - 9, other_block.x + 9, other_block.y - 4, other_block.x + 9, other_block.y + 4, other_block.x - 9, other_block.y + 9]
        points_eye1 = [other_block.x - 4.5, other_block.y + 2.5, other_block.x - 2.5, other_block.y + 4.5]
        points_eye2 = [other_block.x - 4.5, other_block.y - 2.5, other_block.x - 2.5, other_block.y - 4.5]
        return (self.canvas.create_polygon(points, fill = "green"), self.canvas.create_oval(*points_eye1, fill = "white", outline = "black"), self.canvas.create_oval(*points_eye2, fill = "white", outline = "black"))

    def line_creation_left_head(self, other_block):
        points = [self.x + 9, self.y + 9, self.x + 9, self.y - 9, other_block.x + 9, other_block.y - 9, other_block.x - 9, other_block.y - 4, other_block.x - 9, other_block.y + 4, other_block.x + 9, other_block.y + 9]
        points_eye1 = [other_block.x + 4.5, other_block.y + 2.5, other_block.x + 2.5, other_block.y + 4.5]
        points_eye2 = [other_block.x + 4.5, other_block.y - 2.5, other_block.x + 2.5, other_block.y - 4.5]
        return (self.canvas.create_polygon(points, fill = "green"), self.canvas.create_oval(*points_eye1, fill = "white", outline = "black"), self.canvas.create_oval(*points_eye2, fill = "white", outline = "black"))

    def line_creation_up_head(self, other_block):
        points = [self.x - 9, self.y + 9, self.x + 9, self.y + 9, other_block.x + 9, other_block.y + 9, other_block.x + 4, other_block.y - 9, other_block.x - 4, other_block.y - 9, other_block.x - 9, other_block.y + 9]
        points_eye1 = [other_block.x - 2.5, other_block.y + 4.5, other_block.x - 4.5, other_block.y + 2.5]
        points_eye2 = [other_block.x + 2.5, other_block.y + 4.5, other_block.x + 4.5, other_block.y + 2.5]
        return (self.canvas.create_polygon(points, fill = "green"), self.canvas.create_oval(*points_eye1, fill = "white", outline = "black"), self.canvas.create_oval(*points_eye2, fill = "white", outline = "black"))

    def line_creation_down_head(self, other_block):
        points = [self.x - 9, self.y - 9, self.x + 9, self.y - 9, other_block.x + 9, other_block.y - 9, other_block.x + 4, other_block.y + 9, other_block.x - 4, other_block.y + 9, other_block.x - 9, other_block.y - 9]
        points_eye1 = [other_block.x - 2.5, other_block.y - 4.5, other_block.x - 4.5, other_block.y - 2.5]
        points_eye2 = [other_block.x + 2.5, other_block.y - 4.5, other_block.x + 4.5, other_block.y - 2.5]
        return (self.canvas.create_polygon(points, fill = "green"), self.canvas.create_oval(*points_eye1, fill = "white", outline = "black"), self.canvas.create_oval(*points_eye2, fill = "white", outline = "black"))

    def line_creation_right_tail(self, other_block):
        points = [self.x - 9, self.y, self.x + 9, self.y + 9, other_block.x, other_block.y + 9, other_block.x, other_block.y - 9, self.x + 9, self.y - 9]
        return self.canvas.create_polygon(points, fill = "green")

    def line_creation_left_tail(self, other_block):
        points = [self.x + 9, self.y, self.x - 9, self.y + 9, other_block.x, other_block.y + 9, other_block.x, other_block.y - 9, self.x - 9, self.y - 9]
        return self.canvas.create_polygon(points, fill = "green")

    def line_creation_up_tail(self, other_block):
        points = [self.x, self.y + 9, self.x + 9, self.y - 9, other_block.x + 9, other_block.y, other_block.x - 9, other_block.y, self.x - 9, self.y - 9]
        return self.canvas.create_polygon(points, fill = "green")

    def line_creation_down_tail(self, other_block):
        points = [self.x, self.y - 9, self.x + 9, self.y + 9, other_block.x + 9, other_block.y, other_block.x - 9, other_block.y, self.x - 9, self.y + 9]
        return self.canvas.create_polygon(points, fill = "green")

    def line_creation(self, other_block, direction, head = False, tail = False):
        switcher = {
            ("right", False, False): self.line_creation_right,
            ("left", False, False): self.line_creation_left,
            ("up", False, False): self.line_creation_up,
            ("down", False, False):self.line_creation_down,
            ("right", True, False): self.line_creation_right_head,
            ("left", True, False): self.line_creation_left_head,
            ("up", True, False): self.line_creation_up_head,
            ("down", True, False):self.line_creation_down_head,
            ("right", False, True): self.line_creation_right_tail,
            ("left", False, True): self.line_creation_left_tail,
            ("up", False, True): self.line_creation_up_tail,
            ("down", False, True):self.line_creation_down_tail,
        }
        return switcher.get((direction, head, tail), "Invalid direction")(other_block)

class Treat(Block):

    def print_treat(self):

        x = self.x
        y = self.y

        points = [x - 5, y + 10, x + 5, y + 10, x + 9, y, x - 9, y]
        self.first = self.canvas.create_polygon(points, fill="goldenrod")
        
        points = [x - 5, y, x + 5, y, x + 5, y - 5, x - 5, y - 5]
        self.second = self.canvas.create_polygon(points, fill="tomato")

        self.third = self.canvas.create_oval(x, y - 5, x + 7, y, fill = "tomato", outline = "tomato")
        self.fourth = self.canvas.create_oval(x, y - 5, x - 7, y, fill = "tomato", outline = "tomato")
        self.fifth = self.canvas.create_oval(x - 3, y - 8, x + 3, y - 3, fill = "tomato", outline = "tomato")

        top.update()

    def destroy(self):

        self.canvas.delete(self.first)
        self.canvas.delete(self.second)
        self.canvas.delete(self.third)
        self.canvas.delete(self.fourth)
        self.canvas.delete(self.fifth)

        top.update()

class Snake:

    def __init__(self, canvas, stopbutton, pausebutton, initializer, score_label):

        self.initializer = initializer
        self.stopbutton = stopbutton
        self.pausebutton = pausebutton
        self.canvas = canvas
        self.score_label = score_label

        self.create_borders(canvas)
        self.set_up_snake()

        if self.initializer.last_save == None:
            self.score = 0
            self.generate_new_treat()
        else:
            self.score = self.initializer.last_save['Score']
            self.treat = Treat(self.initializer.last_save['Treat'][0], self.initializer.last_save['Treat'][1], self.canvas)
            self.treat.print_treat()

        top.update()

    def create_borders(self, canvas):

        canvas.create_line(1, 1, 299, 1)
        canvas.create_line(299, 1, 299, 299)
        canvas.create_line(299, 299, 1, 299)
        canvas.create_line(1, 299, 1, 1)

    def set_up_snake(self):

        if self.initializer.last_save == None:
            self.set_up_snake_normal()
        else:
            self.set_up_snake_from_last_save()

    def set_up_snake_normal(self):

        self.direction = "right"
        self.initializer.direction = self.direction

        self.blocks = [Block(110, 110, self.canvas), Block(130, 110, self.canvas), Block(150, 110, self.canvas)]
        self.lines = []
        self.tail_line = self.blocks[0].line_creation(self.blocks[1], direction = "right", tail = True)
        self.head_line = self.blocks[1].line_creation(self.blocks[2], direction = "right", head = True)

    def set_up_snake_from_last_save(self):

        self.blocks = []
        for i in self.initializer.last_save['Blocks']:
            self.blocks.append(Block(i[0], i[1], self.canvas))

        self.direction = self.blocks[-2].where_is_it(self.blocks[-1])
        tail_direction = self.blocks[0].where_is_it(self.blocks[1])

        self.lines = []
        for i in range(1, len(self.blocks) - 2):
            self.lines.append(self.blocks[i].line_creation(self.blocks[i + 1], direction = self.blocks[i].where_is_it(self.blocks[i + 1])))

        self.tail_line = self.blocks[0].line_creation(self.blocks[1], direction = tail_direction, tail = True)
        self.head_line = self.blocks[-2].line_creation(self.blocks[-1], direction = self.direction, head = True)

    def move_head_to_body(self):

        for i in self.head_line:
            self.canvas.delete(i)
        self.lines.append(self.blocks[-2].line_creation(self.blocks[-1], direction = self.blocks[-2].where_is_it(self.blocks[-1])))

    def move_block_to_tail(self):

        self.canvas.delete(self.lines[0])
        self.tail_line = self.blocks[1].line_creation(self.blocks[2], direction = self.blocks[1].where_is_it(self.blocks[2]), tail = True)
        self.lines = self.lines[1:]
        self.blocks = self.blocks[1:]

    def create_new_head(self, direction):

        old_block = self.blocks[-1]
        new_block = old_block.move(direction)
        self.head_line = old_block.line_creation(new_block, direction, head = True)
        self.blocks.append(new_block)

        return new_block

    def generate_new_treat(self):

        while True:
            a = random.randint(1, 15) * 20 - 10
            b = random.randint(1, 15) * 20 - 10
            if Block(a, b, self.canvas) not in self.blocks:
                self.treat = Treat(a, b, self.canvas)
                self.treat.print_treat()
                break

    def move_snake(self, direction, game):

        self.move_head_to_body()
        new_block = self.create_new_head(direction)
        new_score = False
        
        if new_block == self.treat:
            self.score += 1
            self.treat.destroy()
            self.generate_new_treat()
        else:
            self.canvas.delete(self.tail_line)
            self.move_block_to_tail()

        if new_block in self.blocks[:-1] or new_block.invalid():
            self.initializer.stopfunc()

        self.direction = direction
        top.update()

class Initialized:

    def __init__(self):
        self.isin = False
        self.stop = False
        self.pause = False
        self.quit = False
        self.retry = False
        self.direction = None
        self.user = None
        self.last_save = None

    def clicked(self):
        self.isin = True
    
    def stopfunc(self):
        self.stop = True

    def pausefunc(self):
        self.pause = True

    def playfunc(self):
        self.pause = False

    def quitfunc(self):
        self.quit = True

    def retryfunc(self):
        self.retry = True

    def userfunc(self, user, high_score):
        self.user = user
        self.high_score = high_score

    def lastsavefunc(self, last_save):
        self.last_save = last_save

class User_choice_menu:

    def __init__(self):

        self.read_json_high_scores()
        self.initializer = Initialized()

        if self.are_there_users:
            self.high_score_label = tk.Label(top, text = "The current high score is: {} by {}.".format(max(self.users.values()), max(self.users.keys(), key = lambda x: self.users[x])))
            self.high_score_label.pack()
            self.create_option_menu()
            self.label = tk.Label(top, text = "You failed to choose a user!")
            self.create_submit()

        self.new_player_button()
        self.wait()

    def read_json_high_scores(self):

        with open('users_high_scores.json', 'r') as users_json:
            self.users = json.load(users_json)

        self.are_there_users = (self.users != dict())

    def create_option_menu(self):

        options = []
        for i in self.users.keys():
            options.append(i)

        self.value_inside = tk.StringVar(top)
        self.value_inside.set("Choose a user")

        self.my_menu = tk.OptionMenu(top, self.value_inside, *options)
        self.my_menu.pack()

    def which_user(self):
        
        user = self.value_inside.get()
        if user != "Choose a user":
            self.initializer.userfunc(user, self.users[user])
        else:
            self.label.pack()

    def create_submit(self):

        self.submit_button = tk.Button(top, text = "Chosen", command = self.which_user)
        self.submit_button.pack()

    def new_player_button(self):

        def newplayerfunc():
            self.initializer.userfunc("Choose a user", 0)

        self.new_player = tk.Button(top, text = "I'm a new player", command = newplayerfunc)
        self.new_player.pack()

    def wait(self):

        while self.initializer.user == None:
            top.update()

        if self.are_there_users:
            self.submit_button.destroy()
            self.my_menu.destroy()
            self.label.destroy()
            self.high_score_label.destroy()

        self.new_player.destroy()

        if self.initializer.user == "Choose a user":
            self.create_a_new_user()

    def create_a_new_user(self):

        self.set_up_buttons_new_user()

        while self.initializer.user == "Choose a user":
            top.update()

        self.create_new_user_json()
        self.destroy_buttons_new_user()

    def newplayernamefunc(self):

        if self.username_entry.get() == "Choose a user" or self.username_entry.get() == "" or self.username_entry.get() in self.users.keys():
            self.fail_message.pack()
        else:
            self.initializer.userfunc(self.username_entry.get(), 0)

    def set_up_buttons_new_user(self):

        self.choose_a_username = tk.Label(top, text = "Choose a username:")
        self.choose_a_username.pack()

        self.username_entry = tk.Entry(top)
        self.username_entry.pack()

        self.fail_message = tk.Label(top, text = "Please choose a different username")

        self.username_button = tk.Button(top, text = "Chosen", command = self.newplayernamefunc)
        self.username_button.pack()

    def destroy_buttons_new_user(self):

        self.fail_message.destroy()
        self.choose_a_username.destroy()
        self.username_entry.destroy()
        self.username_button.destroy()

    def create_new_user_json(self):
        
        with open('users_high_scores.json', 'r') as json_file:
            high_scores = json.load(json_file)

        with open('users_last_save.json', 'r') as json_file:
            last_save = json.load(json_file)

        high_scores[self.initializer.user] = 0
        last_save[self.initializer.user] = {}

        with open('users_high_scores.json', 'w') as json_file:
            json.dump(high_scores, json_file)

        with open('users_last_save.json', 'w') as json_file:
            json.dump(last_save, json_file)

class Play_menu:

    def __init__(self, initializer):
        
        self.initializer = initializer
        self.read_json_last_save()

        btninit = tk.Button(top, text = "Play", command = initializer.clicked)
        btninit.pack()

        score_label = tk.Label(top, text = "High score: {}".format(initializer.high_score))
        score_label.pack()

        self.last_save_button()

        while not initializer.isin:
            top.update()

        btninit.destroy()
        score_label.destroy()
        if self.last_save != {}:
            self.btnlastsave.destroy()
        top.update()

    def read_json_last_save(self):

        with open('users_last_save.json', 'r') as json_file:
            self.last_save = json.load(json_file)[self.initializer.user]

    def last_save_button(self): 

        if self.last_save == {}:
            return 0

        def last_save_button_func():

            self.initializer.lastsavefunc(self.last_save)
            self.destroy_last_save()
            self.initializer.clicked()

        self.btnlastsave = tk.Button(top, text = "Continue from last save", command = last_save_button_func)
        self.btnlastsave.pack()

    def destroy_last_save(self):

        with open('users_last_save.json', 'r') as json_file:
            json_content = json.load(json_file)

        json_content[self.initializer.user] = {}

        with open('users_last_save.json', 'w') as json_file:
            json.dump(json_content, json_file)

class Game:

    def __init__(self, initializer):

        self.btnstop = tk.Button(top, text = "Stop")
        self.btnpause = tk.Button(top, text = "Pause")
        self.canvas = tk.Canvas(top, width = 300, height = 300)
        self.score_label = tk.Label(top, text = "Score: 0")
        self.btnsave = tk.Button(top, text = "Save game and quit")
        self.initializer = initializer
 
        self.game_setup()
        self.my_snake = Snake(self.canvas, self.btnstop, self.btnpause, self.initializer, self.score_label)

        self.start_listener()
        self.game()
        self.game_over()

    def game_setup(self):

        self.canvas.pack()
        self.score_label.pack()

        self.btnpause['command'] = self.initializer.pausefunc
        self.btnpause.pack()

        self.btnstop['command'] = self.initializer.stopfunc
        self.btnstop.pack()

        self.btnsave['command'] = self.savefunc
        self.btnsave.pack()

        top.update()

    def savefunc(self):

        with open('users_last_save.json', 'r') as json_file:
            json_content = json.load(json_file)

        blocks_list = [[i.x, i.y] for i in self.my_snake.blocks]
        treat = [self.my_snake.treat.x, self.my_snake.treat.y]

        json_content[self.initializer.user] = {"Treat": treat, "Blocks": blocks_list, "Score": self.my_snake.score}

        with open('users_last_save.json', 'w') as json_file:
            json.dump(json_content, json_file)

        self.initializer.stopfunc()

    def delete_last_save(self):

        with open('users_last_save.json', 'r') as json_file:
            json_content = json.load(json_file)

        json_content[self.initializer.user] = []

        with open('users_last_save.json', 'w') as json_file:
            json.dump(json_content, json_file)

    def start_listener(self):

        def on_press(key):
            switcher = {
                keyboard.Key.up: "up",
                keyboard.Key.down: "down",
                keyboard.Key.right: "right",
                keyboard.Key.left: "left",
            }
            self.initializer.direction = switcher.get(key, self.initializer.direction)

        self.listener = keyboard.Listener(on_press = on_press)
        self.listener.start()

    def game(self):

        while True:
            if self.initializer.stop:
                return 0
            self.update_score()
            self.wait_for_direction()
            if self.initializer.pause:
                self.pause()

    def update_score(self):

        self.score_label['text'] = "Score: " + str(self.my_snake.score)
        top.update()

    def wait_for_direction(self):
 
        opposite = {
            "right": "left",
            "left": "right",
            "up": "down",
            "down": "up",
        }

        current_direction = self.my_snake.direction
        self.initializer.direction = self.my_snake.direction
        time_end = time.time() + 0.8
        top.update()

        while time.time() < time_end:
            if self.initializer.pause or self.initializer.stop:
                return 0
            if self.initializer.direction != opposite.get(self.my_snake.direction):
                current_direction = self.initializer.direction
            top.update()

        self.my_snake.move_snake(current_direction, self)

    def pause(self):

        self.my_snake.pausebutton['text'] = 'Play'
        self.my_snake.pausebutton['command'] = self.initializer.playfunc
        top.update()

        while self.initializer.pause:
            if self.initializer.stop:
                return 0
            top.update()

        self.my_snake.pausebutton['text'] = 'Pause'
        self.my_snake.pausebutton['command'] = self.initializer.pausefunc
        top.update()

    def write_score_to_json(self):

        with open('users_high_scores.json', 'r') as users_json:
            users = json.load(users_json)
            the_score = max(self.my_snake.score, users[self.initializer.user])
            users[self.initializer.user] = the_score

        with open('users_high_scores.json', 'w') as users_json:
            json.dump(users, users_json)

    def game_over(self):

        self.write_score_to_json()

        self.canvas.destroy()
        self.btnstop.destroy()
        self.btnpause.destroy()
        self.score_label.destroy()
        self.btnsave.destroy()
        
        label = tk.Label(
        text="GAME OVER",
        fg="white",
        bg="black",
        width=40,
        height=10)
        label.pack()

        new_score_label = tk.Label(top, text = "Score: {}".format(self.my_snake.score))
        new_score_label.pack()

        btnretry = tk.Button(top, text = "Main menu", command = self.initializer.retryfunc)
        btnretry.pack()

        btnquit = tk.Button(top, text = "Quit", command = self.initializer.quitfunc)
        btnquit.pack()

        while not self.initializer.quit:
            top.update()
            if self.initializer.retry:
                btnquit.destroy()
                btnretry.destroy()
                label.destroy()
                new_score_label.destroy()
                top.update()
                return 0

        my_quit()

try:

    while True:

        the_menu1 = User_choice_menu()
        my_in = the_menu1.initializer
        the_menu2 = Play_menu(my_in)
        my_in = the_menu2.initializer
        Game(my_in)

except tk.TclError:

    exit()
