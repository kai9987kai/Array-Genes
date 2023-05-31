import turtle
import random

# Screen setup
screen = turtle.Screen()
screen.setup(800, 600)

# List of bots
bots = []

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
    },
    "max_age": {
        "A": 60,
        "B": 70,
        "C": 80,
        "D": 90,
        "E": 100
    },
    "shape": {
        "A": "circle",
        "B": "square",
        "C": "triangle",
        "D": "turtle",
        "E": "classic"
    },
    "size": {
        "A": 1.0,
        "B": 0.8,
        "C": 0.6,
        "D": 0.4,
        "E": 0.2
    }
}

# Bot class
class Bot(turtle.Turtle):
    def __init__(self, x, y, color, genetic_code, age=0):
        super().__init__()
        self.penup()
        self.goto(x, y)
        self.color(color)
        self.shape(GENETIC_ATTRIBUTES["shape"][genetic_code[3]])
        self.shapesize(GENETIC_ATTRIBUTES["size"][genetic_code[4]])
        self.speed(1)
        self.moves = 0
        self.genetic_code = genetic_code
        self.speed_gene = GENETIC_ATTRIBUTES["speed"][self.genetic_code[0]]
        self.hostility = GENETIC_ATTRIBUTES["hostility"][self.genetic_code[1]]
        self.max_age = GENETIC_ATTRIBUTES["max_age"][self.genetic_code[2]]
        self.age = age

    def move(self):
        self.forward(10 * self.speed_gene)
        self.setheading(random.randint(0, 360))  # Update the heading
        self.moves += 1
        self.age += 1
        if self.moves == 4 and not self.hostility:
            self.reproduce()
            self.moves = 0
        if self.age > self.max_age:  # If bot is too old, it dies
            bots.remove(self)
            self.hideturtle()
            del self

    def reproduce(self):
        x = random.randint(-300, 300)
        y = random.randint(-200, 200)
        child_genetic_code = self.genetic_code + random.choice('ABCDE')
        if random.random() < 0.1:  # 10% chance of mutation
            mutation_index = random.randint(0, len(child_genetic_code) - 1)
            child_genetic_code = child_genetic_code[:mutation_index] + random.choice('ABCDE') + child_genetic_code[mutation_index + 1:]
        child = Bot(x, y, self.color()[0], child_genetic_code)
        bots.append(child)

    def display_stats(self):
        print(f"Bot ID: {self}, Genetic Code: {self.genetic_code}, Speed: {self.speed_gene}, Hostility: {self.hostility}, Age: {self.age}")

# Create initial bots
for _ in range(10):
    x = random.randint(-300, 300)
    y = random.randint(-200, 200)
    color = random.choice(['blue', 'pink'])
    genetic_code = random.choice('ABCDE') + random.choice('ABCDE') + random.choice('ABCDE') + random.choice('ABCDE') + random.choice('ABCDE')
    bot = Bot(x, y, color, genetic_code)
    bots.append(bot)

# Create plants
plants = []
for _ in range(5):
    x = random.randint(-300, 300)
    y = random.randint(-200, 200)
    plant = turtle.Turtle()
    plant.penup()
    plant.goto(x, y)
    plant.shape("circle")
    plant.color("green")
    plants.append(plant)

# Main loop
while True:
    for bot in bots:
        bot.move()
        for plant in plants:
            if bot.distance(plant) < 20:
                bot.moves = 0  # Reset moves after eating plant
                plant.hideturtle()
                plants.remove(plant)
                del plant
                break
    if len(bots) < 10:  # Repopulate if bots die out
        x = random.randint(-300, 300)
        y = random.randint(-200, 200)
        color = random.choice(['blue', 'pink'])
        genetic_code = random.choice('ABCDE') + random.choice('ABCDE') + random.choice('ABCDE') + random.choice('ABCDE') + random.choice('ABCDE')
        bot = Bot(x, y, color, genetic_code)
        bots.append(bot)
