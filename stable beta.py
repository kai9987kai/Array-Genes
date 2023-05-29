import random
import turtle
import copy
import time
import datetime
import statistics
import threading

# Initialize turtle screen
screen = turtle.Screen()
screen.setup(800, 600)
screen.title("Bot Simulation")

# Define global constants
MAX_HEALTH = 10
MUTATION_RATE = 0.01
CROSSOVER_RATE = 0.8

class Bot(threading.Thread):
    def __init__(self, id, genetic_code, health=MAX_HEALTH):
        threading.Thread.__init__(self)
        self.id = id
        self.genetic_code = genetic_code
        self.alive = True
        self.weight = 1
        self.health = health
        self.start_time = time.time()
        self.damage_gene = random.choice('abcdefghijklmnopqrstuvwxyz')
        self.speed_gene = random.choice('abcdefghijklmnopqrstuvwxyz')
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

    def run(self):
        while self.alive:
            self.check_genetic_code()
            self.rotate()
            self.move()

            # Look for bots within a certain radius
            visible_bots = self.find_visible_bots(100)

            # Move towards bots of opposite gender or non-hostile bots
            self.move_towards_bots(visible_bots)

            # Avoid hostile bots
            self.avoid_hostile_bots(visible_bots)

            # Update health and apply environmental factors
            self.update_health()
            self.apply_environmental_factors()

            self.reproduce()

            time.sleep(0.005)  # Update every 5 milliseconds

    def random_genes(self):
        return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(len(self.genetic_code))])

    def inherited_genes(self):
        return random.choice('abcdefghijklmnopqrstuvwxyz')

    def time_genes(self):
        current_time = datetime.datetime.now()
        return f"{current_time.minute % 100:02d}{current_time.second % 100:02d}"

    def check_genetic_code(self):
        if self.damage_gene in self.genetic_code:
            self.health -= 1

        if self.speed_gene in self.genetic_code:
            self.turtle.speed(1)
        else:
            self.turtle.speed(6)

    def rotate(self):
        angle = random.randint(-10, 10)
        self.turtle.right(angle)

    def move(self):
        self.turtle.forward(2)

    def find_visible_bots(self, radius):
        visible_bots = []
        for bot in bots:
            if bot != self and self.turtle.distance(bot.turtle) <= radius:
                visible_bots.append(bot)
        return visible_bots

    def move_towards_bots(self, visible_bots):
        opposite_gender_bots = [bot for bot in visible_bots if bot.gender != self.gender and bot.alive]
        if opposite_gender_bots:
            closest_bot = min(opposite_gender_bots, key=lambda bot: self.turtle.distance(bot.turtle))
            self.turtle.setheading(self.turtle.towards(closest_bot.turtle))

        non_hostile_bots = [bot for bot in visible_bots if not bot.hostility and bot.alive]
        if non_hostile_bots and random.random() <= 0.12:
            closest_bot = min(non_hostile_bots, key=lambda bot: self.turtle.distance(bot.turtle))
            self.turtle.setheading(self.turtle.towards(closest_bot.turtle))

    def avoid_hostile_bots(self, visible_bots):
        hostile_bots = [bot for bot in visible_bots if bot.hostility and bot.alive]
        if hostile_bots:
            closest_bot = min(hostile_bots, key=lambda bot: self.turtle.distance(bot.turtle))
            self.turtle.setheading(self.turtle.towards(closest_bot.turtle) + 180)

    def update_health(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= 10:
            self.health -= 1
            self.start_time = time.time()

        if self.health <= 0:
            self.alive = False
            self.turtle.hideturtle()

    def apply_environmental_factors(self):
        # Randomly apply environmental factors
        if random.random() <= 0.05:
            self.health -= 1

    def reproduce(self):
        if self.health >= 7 and random.random() <= 0.12:
            child_genetic_code = ""
            for i in range(len(self.genetic_code)):
                if random.random() <= CROSSOVER_RATE:
                    child_genetic_code += self.genetic_code[i]
                else:
                    child_genetic_code += self.inherited_genes()
            child_genetic_code += self.random_genes()
            child = Bot(len(bots), child_genetic_code, health=self.health / 2)
            child.turtle.goto(self.turtle.position())
            child.turtle.setheading(self.turtle.heading())
            if self.gender == "Male":
                child.turtle.color("red")
            else:
                child.turtle.color("pink")
            child.turtle.shapesize(self.turtle.shapesize()[0] * 1.1)
            bots.append(child)

# Create initial population of bots
bots = []
for i in range(10):
    genetic_code = "abcdefghijklmnopqrstuvwxyz"
    bot = Bot(i, genetic_code)
    bots.append(bot)

# Start the simulation
for bot in bots:
    bot.start()

turtle.done()
