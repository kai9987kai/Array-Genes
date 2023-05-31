import turtle
import random

# Screen setup
screen = turtle.Screen()
screen.setup(800, 600)

# List of bots
bots = []

# List of plants
plants = []

# List of obstacles
obstacles = []

# Genetic attributes
GENETIC_ATTRIBUTES = {
    "speed": {
        "A": 1.0,
        "B": 0.8,
        "C": 0.5,
        "D": 0.3,
        "E": 0.1
    },
    "hostility": {
        "A": True,
        "B": False,
        "C": True,
        "D": False,
        "E": True
    }
}

# Bot class
class Bot(turtle.Turtle):
    def __init__(self, x, y, color, genetic_code, age=0):
        super().__init__()
        self.penup()
        self.goto(x, y)
        self.color(color)
        self.shape('circle')
        self.speed(1)
        self.moves = 0
        self.genetic_code = genetic_code
        self.speed_gene = GENETIC_ATTRIBUTES["speed"][self.genetic_code[0]]
        self.hostility = GENETIC_ATTRIBUTES["hostility"][self.genetic_code[1]]
        self.age = age

    def move(self):
        self.forward(10 * self.speed_gene)
        self.moves += 1
        self.age += 1
        if self.moves == 4 and not self.hostility:
            self.reproduce()
            self.moves = 0

    def reproduce(self):
        x = random.randint(-300, 300)
        y = random.randint(-200, 200)
        child_genetic_code = self.genetic_code + random.choice('ABCDE')
        child = Bot(x, y, self.color()[0], child_genetic_code)
        bots.append(child)

    def eat(self, plant):
        if self.distance(plant) < 20:
            plants.remove(plant)
            plant.hideturtle()
            del plant
            self.moves = 0

    def fight(self, other):
        if self.hostility and self.distance(other) < 20:
            if self.speed_gene > other.speed_gene:
                bots.remove(other)
                other.hideturtle()
                del other
                self.hostility = False

    def display_stats(self):
        print(f"Bot ID: {self}, Genetic Code: {self.genetic_code}, Speed: {self.speed_gene}, Hostility: {self.hostility}, Age: {self.age}")

# Plant class
class Plant(turtle.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.penup()
        self.goto(x, y)
        self.color('green')
        self.shape('circle')

# Obstacle class
class Obstacle(turtle.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.penup()
        self.goto(x, y)
        self.color('black')
        self.shape('square')

# Create initial bots
for _ in range(10):
    x = random.randint(-300, 300)
    y = random.randint(-200, 200)
    color = random.choice(['blue', 'pink'])
    genetic_code = random.choice('ABCDE') + random.choice('ABCDE')
    bot = Bot(x, y, color, genetic_code)
    bots.append(bot)

# Create initial plants
for _ in range(20):
    x = random.randint(-300, 300)

    y = random.randint(-200, 200)
    plant = Plant(x, y)
    plants.append(plant)

# Create initial obstacles
for _ in range(5):
    x = random.randint(-300, 300)
    y = random.randint(-200, 200)
    obstacle = Obstacle(x, y)
    obstacles.append(obstacle)

# Main loop
while True:
    for bot in bots:
        bot.right(random.randint(-90, 90))
        bot.move()
        for plant in plants:
            bot.eat(plant)
        for other in bots:
            if other != bot:
                bot.fight(other)
        if bot.xcor() > 390 or bot.xcor() < -390 or bot.ycor() > 290 or bot.ycor() < -290:
            bot.right(180)
        if bot.age > 100:  # If bot is too old, it dies
            bots.remove(bot)
            bot.hideturtle()
            del bot
        bot.display_stats()  # Display bot's stats

turtle.done()
