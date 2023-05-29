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

            time.sleep(0.005)  # Update every 5 milliseconds

    def random_genes(self):
        return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(len(self.genetic_code))])

    def inherited_genes(self):
        return random.choice('abcdefghijklmnopqrstuvwxyz')

    def time_genes(self):
        current_time = datetime.datetime.now()
        return f"{current_time.minute % 100:02d}{current_time.second % 100:02d}"

    def check_genetic_code(self):
        for i in range(1, len(self.genetic_code)):
            if self.genetic_code[i] < self.genetic_code[i-1]:
                self.alive = False
                print(f"Bot {self.id} died. Genetic Code: {self.genetic_code}")
                break

    def reproduce(self, bots):
        if self.alive:
            if self.killed_count > 0 and all(bot.killed_count > 0 for bot in bots if bot.id != self.id):
                new_genetic_code = self.genetic_code[:len(self.genetic_code)//2]
                if self.id % 5 == 4:
                    num_reproduced_bots = int(self.weight) * 2
                else:
                    num_reproduced_bots = int(self.weight)
                for _ in range(num_reproduced_bots):
                    new_genetic_code = self.mutate_genes(new_genetic_code)
                    new_bot = Bot(len(bots), new_genetic_code, health=self.health)
                    new_bot.speed_gene = self.speed_gene
                    new_bot.gender = random.choice(["Male", "Female"])
                    new_bot.weight = self.weight * 1.1  # Increase weight by 10 percent
                    bots.append(new_bot)
                    print(f"Bot {self.id} reproduced. New bot {new_bot.id} created.")
                    self.weight -= 1

    def mutate_genes(self, genetic_code):
        mutated_code = ""
        for gene in genetic_code:
            if random.random() < MUTATION_RATE:
                mutated_code += random.choice('abcdefghijklmnopqrstuvwxyz')
            else:
                mutated_code += gene
        return mutated_code

    def crossover_genes(self, partner_code):
        crossed_code = ""
        for gene1, gene2 in zip(self.genetic_code, partner_code):
            if random.random() < CROSSOVER_RATE:
                crossed_code += gene1
            else:
                crossed_code += gene2
        return crossed_code

    def share_health(self, bots):
        if self.alive:
            for bot in bots:
                if bot.id > self.id and self.health > 0 and bot.health < MAX_HEALTH and self.health > 0 and random.choice(self.genetic_code) == bot.id:
                    self.health -= 1
                    bot.health += 1
                    print(f"Bot {self.id} shared health with Bot {bot.id}.")
                    break

    def deal_damage(self, bot):
        if self.health > 0 and random.choice(self.genetic_code) == bot.id:
            damage = self.genetic_code.count(self.damage_gene)
            bot.health -= damage
            print(f"Bot {self.id} dealt {damage} damage to Bot {bot.id}.")
            if bot.health <= 0:
                bot.alive = False
                print(f"Bot {bot.id} killed by Bot {self.id}.")
                self.hostility = False

    def move(self):
        speed = (self.genetic_code.count(self.speed_gene) + 1) * 5  # Increase the distance moved
        self.turtle.forward(speed)

    def rotate(self):
        angle = random.randint(-15, 15)
        self.turtle.right(angle)

    def get_duration(self):
        return round(time.time() - self.start_time, 2)

    def find_visible_bots(self, radius):
        visible_bots = []
        for bot in bots:
            if bot.id != self.id and bot.alive and self.turtle.distance(bot.turtle) <= radius:
                visible_bots.append(bot)
        return visible_bots

    def move_towards_bots(self, visible_bots):
        opposite_gender_bots = [bot for bot in visible_bots if bot.gender != self.gender]
        non_hostile_bots = [bot for bot in visible_bots if not bot.hostility]

        if opposite_gender_bots:
            self.move_towards_target(opposite_gender_bots[0].turtle.position())

        elif non_hostile_bots and random.random() < 0.12:
            self.move_towards_target(non_hostile_bots[0].turtle.position())

    def move_towards_target(self, target_position):
        angle = self.turtle.towards(target_position)
        self.turtle.setheading(angle)
        self.move()

    def avoid_hostile_bots(self, visible_bots):
        hostile_bots = [bot for bot in visible_bots if bot.hostility]
        if hostile_bots:
            self.turtle.right(180)

    def update_health(self):
        self.health -= 0.001 * self.genetic_code.count(self.damage_gene)

    def apply_environmental_factors(self):
        # Implement environmental factors such as limited resources, climate conditions, etc.
        pass

def create_box_colliders():
    colliders = []
    for _ in range(4):
        collider = turtle.Turtle()
        collider.shape("square")
        collider.color("red")
        collider.penup()
        collider.speed(0)
        collider.shapesize(stretch_wid=6, stretch_len=1)
        collider.goto(random.randint(-360, 360), random.randint(-260, 260))
        colliders.append(collider)
    return colliders

def main():
    # Initialize bots with random genetic codes
    bots = [Bot(i, ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10)])) for i in range(50)]  # Start with 50 bots

    colliders = create_box_colliders()

    for bot in bots:
        bot.start()

    while True:
        for collider in colliders:
            for bot in bots:
                if bot.turtle.distance(collider) < 30:
                    bot.turtle.right(180)

        for bot in bots:
            for other_bot in bots:
                if bot.id != other_bot.id and bot.alive and other_bot.alive:
                    if bot.hostility and other_bot.hostility:
                        bot.deal_damage(other_bot)
                    elif not bot.hostility and not other_bot.hostility and bot.gender != other_bot.gender:
                        if random.random() < CROSSOVER_RATE:
                            new_genetic_code = bot.crossover_genes(other_bot.genetic_code)
                            new_genetic_code = bot.mutate_genes(new_genetic_code)
                            new_bot = Bot(len(bots), new_genetic_code, health=bot.health)
                            new_bot.speed_gene = bot.speed_gene
                            new_bot.gender = random.choice(["Male", "Female"])
                            new_bot.weight = bot.weight * 1.1  # Increase weight by 10 percent
                            bots.append(new_bot)
                            print(f"Bot {bot.id} and Bot {other_bot.id} reproduced. New bot {new_bot.id} created.")
                            bot.weight -= 1

        for bot in bots:
            bot.share_health(bots)

        # Sort bots by duration (longest living first)
        bots.sort(key=lambda bot: bot.get_duration(), reverse=True)

        # Kill the lower bots
        for bot in bots[50:]:
            bot.alive = False
            print(f"Bot {bot.id} killed due to lower survival time.")

        print("\nCurrent Bot Status:")
        for bot in bots:
            print(f"Bot {bot.id}: Genetic Code: {bot.genetic_code}, Duration: {bot.get_duration()} seconds, Weight: {bot.weight}, Health: {bot.health}/{MAX_HEALTH}, Gender: {bot.gender}, Hostility: {bot.hostility}")

        time.sleep(1)

if __name__ == "__main__":
    main()
