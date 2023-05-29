import turtle
import random
import time

# Initialize turtle screen
screen = turtle.Screen()
screen.setup(800, 600)
screen.title("Bot Simulation")

# Define global constants
MAX_HEALTH = 10
MUTATION_RATE = 0.01
CROSSOVER_RATE = 0.8
FERTILITY_RATE_INCREASE = 0.05
BOT_SPAWN_INTERVAL = 10  # In seconds

# Create obstacle types, colors, sizes, and locations
OBSTACLE_TYPES = ['square', 'triangle', 'circle']
OBSTACLE_COLORS = ['blue', 'orange', 'purple']
OBSTACLE_SIZES = [30, 40, 50]
OBSTACLE_LOCATIONS = [(-100, 100), (200, -150), (-300, -50)]

# Create plant colors and locations
PLANT_COLORS = ['green', 'dark green', 'lime green']
PLANT_LOCATIONS = [(200, 200), (-250, -200), (100, -150), (-300, 200)]

# Create obstacles
obstacles = []
for obstacle_type, color, size, location in zip(OBSTACLE_TYPES, OBSTACLE_COLORS, OBSTACLE_SIZES, OBSTACLE_LOCATIONS):
    obstacle = turtle.Turtle()
    obstacle.shape(obstacle_type)
    obstacle.color(color)
    obstacle.shapesize(size / 20)
    obstacle.penup()
    obstacle.goto(location)
    obstacles.append(obstacle)

# Create plants
plants = []
for color, location in zip(PLANT_COLORS, PLANT_LOCATIONS):
    plant = turtle.Turtle()
    plant.shape('circle')
    plant.color(color)
    plant.shapesize(0.5)
    plant.penup()
    plant.goto(location)
    plants.append(plant)

class Bot:
    def __init__(self, genetic_code, health=MAX_HEALTH):
        self.genetic_code = genetic_code
        self.alive = True
        self.weight = 1
        self.health = health
        self.damage_gene = random.choice('abcdefghijklmnopqrstuvwxyz')
        self.speed_gene = random.choice('abcdefghijklmnopqrstuvwxyz')
        self.feed_gene = random.choice('abcdefghijklmnopqrstuvwxyz')
        self.gender = random.choice(["Male", "Female"])
        self.hostility = True

        # Create turtle for the bot
        self.turtle = turtle.Turtle()
        self.turtle.shape("circle")
        if self.gender == "Male":
            self.turtle.color("red")
        else:
            self.turtle.color("pink")
        self.turtle.penup()

        # Set initial position on the canvas
        x = random.randint(-380, 380)
        y = random.randint(-280, 280)
        self.turtle.goto(x, y)

        # Set initial heading
        self.turtle.setheading(random.randint(0, 359))

    def move(self):
        self.turtle.forward(2)

    def avoid_obstacles(self):
        for obstacle in obstacles:
            if self.distance_to_obstacle(obstacle) <= 20:
                self.turtle.right(180)
                self.turtle.forward(10)
                self.turtle.right(180)

    def distance_to_obstacle(self, obstacle):
        x1, y1 = self.turtle.position()
        x2, y2 = obstacle.position()
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def is_outside_window(self):
        x, y = self.turtle.position()
        return abs(x) > 400 or abs(y) > 300

# Create initial bots
bots = []
for _ in range(23):
    bot = Bot([])
    bots.append(bot)

last_bot_spawn_time = 0

def move_bots():
    global last_bot_spawn_time

    current_time = time.time()

    # Move and update health for existing bots
    for bot in bots:
        if bot.alive:
            bot.move()
            bot.avoid_obstacles()

    # Spawn a new bot every BOT_SPAWN_INTERVAL seconds
    if current_time - last_bot_spawn_time >= BOT_SPAWN_INTERVAL:
        new_bot = Bot([])
        bots.append(new_bot)
        last_bot_spawn_time = current_time

    screen.update()
    turtle.ontimer(move_bots)

# Start the simulation
move_bots()
turtle.done()
