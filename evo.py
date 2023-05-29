import random
import copy
import time
import datetime
import statistics

class Bot:
    def __init__(self, id, array, health=10):
        self.id = id
        self.array = array
        self.alive = True
        self.genes = []
        self.random_genes()
        self.inherited_genes()
        self.time_genes()
        self.start_time = time.time()
        self.weight = 1
        self.health = health

    def random_genes(self):
        num_random_genes = int(len(self.array) * 0.2)
        self.genes.extend([random.randint(1, 100) for _ in range(num_random_genes)])

    def inherited_genes(self):
        num_inherited_genes = int(len(self.array) * 0.5)
        parent_genes = random.choice(self.array)
        self.genes.extend([random.choice(self.array) for _ in range(num_inherited_genes)])

    def time_genes(self):
        current_time = datetime.datetime.now()
        self.genes.extend([current_time.minute % 100, current_time.second % 100])

    def check_numbers(self):
        prev_number = self.genes[0]
        for i in range(1, len(self.genes)):
            if self.genes[i] < prev_number:
                self.alive = False
                print(f"Bot {self.id} died. Array: {self.array}")
                break
            else:
                prev_number = self.genes[i]

    def reproduce(self, bots):
        if self.alive:
            new_array = self.genes[:len(self.genes)//2]
            if self.id % 5 == 4:
                num_reproduced_bots = int(self.weight) * 2
            else:
                num_reproduced_bots = int(self.weight)
            for _ in range(num_reproduced_bots):
                new_bot = Bot(len(bots), new_array, health=self.health)
                bots.append(new_bot)
                print(f"Bot {self.id} reproduced. New bot {new_bot.id} created.")
                self.weight -= 1

    def share_health(self, bots):
        if self.alive:
            for bot in bots:
                if bot.id > self.id and self.health > 0 and bot.health < 10 and self.health > 0 and random.choice(self.array) == bot.id:
                    self.health -= 1
                    bot.health += 1
                    print(f"Bot {self.id} shared health with Bot {bot.id}.")
                    break

    def get_duration(self):
        return round(time.time() - self.start_time, 2)

def main():
    # Initialize 10 bots with random arrays
    bots = [Bot(i, sorted([random.randint(1, 100) for _ in range(10)])) for i in range(10)]

    while any(bot.alive for bot in bots):
        for bot in bots:
            bot.check_numbers()

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
            print(f"Bot {bot.id}: Array: {bot.array}, Duration: {bot.get_duration()} seconds, Weight: {bot.weight}, Health: {bot.health}/10")

        time.sleep(1)

if __name__ == "__main__":
    main()
