import random
import turtle
import copy
import time
import datetime
import statistics

# Initialize turtle screen
screen = turtle.Screen()
screen.setup(800, 600)
screen.title("Bot Simulation")

class Bot:
    def __init__(self, id, genetic_code, health=10):
        self.id = id
        self.genetic_code = genetic_code
        self.alive = True
        self.weight = 1
        self.health = health
        self.start_time = time.time()
        self.damage_gene = random.choice('abcdefghijklmnopqrstuvwxyz')

        # Create turtle for the bot
        self.turtle = turtle.Turtle()
        self.turtle.shape("circle")
        self.turtle.color("blue")
        self.turtle.penup()

        # Set initial position on the canvas
        x = random.randint(-380, 380)
        y = random.randint(-280, 280)
        self.turtle.goto(x, y)

        # Set initial heading
        self.turtle.setheading(random.randint(0, 359))

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
                    new_bot = Bot(len(bots), new_genetic_code, health=self.health)
                    bots.append(new_bot)
                    print(f"Bot {self.id} reproduced. New bot {new_bot.id} created.")
                    self.weight -= 1

    def share_health(self, bots):
        if self.alive:
            for bot in bots:
                if bot.id > self.id and self.health > 0 and bot.health < 10 and self.health > 0 and random.choice(self.genetic_code) == bot.id:
                    self.health -= 1
                    bot.health += 1
                    print(f"Bot {self.id} shared health with Bot {bot.id}.")
                    break

    def deal_damage(self, bot):
        if self.health > 0 and random.choice(self.genetic_code) == bot.id:
            damage = self.genetic_code.count(self.damage_gene)
            bot.health -= damage
            print(f"Bot {self.id} dealt {damage} damage to Bot {bot.id}.")

    def move(self):
        self.turtle.forward(2)

    def rotate(self):
        angle = random.randint(-15, 15)
        self.turtle.right(angle)

    def get_duration(self):
        return round(time.time() - self.start_time, 2)

def main():
    # Initialize bots with random genetic codes
    bots = [Bot(i, ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10)])) for i in range(10)]

    while True:
        for bot in bots:
            bot.check_genetic_code()
            bot.rotate()
            bot.move()

        for bot in bots:
            for other_bot in bots:
                if bot.id != other_bot.id and bot.alive and other_bot.alive:
                    bot.deal_damage(other_bot)
                    if other_bot.health <= 0:
                        bot.killed_count += 1
                        other_bot.alive = False
                        print(f"Bot {bot.id} killed Bot {other_bot.id}.")

        for bot in bots:
            bot.reproduce(bots)
            bot.share_health(bots)

        # Sort bots by duration (longest living first)
        bots.sort(key=lambda bot: bot.get_duration(), reverse=True)

        # Kill the lower bots
        for bot in bots[10:]:
            bot.alive = False
            print(f"Bot {bot.id} killed due to lower survival time.")

        print("\nCurrent Bot Status:")
        for bot in bots:
            print(f"Bot {bot.id}: Genetic Code: {bot.genetic_code}, Duration: {bot.get_duration()} seconds, Weight: {bot.weight}, Health: {bot.health}/10")

        time.sleep(1)

if __name__ == "__main__":
    main()
