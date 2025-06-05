import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

class Person:
    def __init__(self):
        self.x = random.randint(1, 100)
        self.y = random.randint(1, 100)
        self.speed = random.randint(1, 3)
        self.direction = random.choice(['S', 'SW', 'W', 'NW', 'N', 'NE', 'E', 'SE'])
        # self.state = random.choice(['healthy', 'infected', 'sick', 'recovering'])
        self.state = 'healthy'
        self.current_state_counter = 0
        self.age = np.random.randint(0, 60)
        self.set_immunities(initialize=True)
        self.current_turn_birth = False
        self.current_turn_contact = False

    def set_immunities(self, initialize=False):
        if self.age < 15 or self.age >= 70:
            self.immunity = 'low'
            if initialize:
                self.immunity_number = random.randint(0, 3)
        elif 40 <= self.age < 70:
            self.immunity = 'medium'
            if initialize:
                self.immunity_number = random.randint(4, 6)
        else:
            self.immunity = 'high'
            if initialize:
                self.immunity_number = random.randint(7, 10)

    def update_immunity(self):
        # def get_immunity(age):
        #     if age < 15 or age >= 70:
        #         return 'low'
        #     elif 40 <= age < 70:
        #         return 'medium'
        #     else:
        #         return 'high'

        if get_immunity_number(self.age, 'low') < self.immunity_number < get_immunity_number(self.age, 'high'):
            pass
        else:
            if self.immunity_number < get_immunity_number(self.age, 'low'):
                if self.immunity == 'medium':
                    self.immunity = 'low'
                elif self.immunity == 'high':
                    self.immunity = 'medium'

            elif self.immunity_number >= get_immunity_number(self.age, 'high'):
                if self.immunity == 'low':
                    self.immunity = 'medium'
                elif self.immunity == 'medium':
                    self.immunity = 'high'

    def move(self):
        # x cordinate
        if self.direction in ['E', 'NE', 'SE']:
            self.x += self.speed
        if self.direction in ['W', 'NW', 'SW']:
            self.x -= self.speed

        # y cordinate
        if self.direction in ['S', 'SW', 'SE']:
            self.y -= self.speed
        if self.direction in ['N', 'NW', 'NE']:
            self.y += self.speed

        self.x = max(0, min(self.x, 100))
        self.y = max(0, min(self.y, 100))

        if self.x in [0, 100] or self.y in [0, 100]:
            set_random_direction(self)

def get_color(state):
    return {
        'healthy': 'green',
        'infected': 'yellow',
        'sick': 'red',
        'recovering': 'orange'
    }.get(state)

def get_immunity_number(age, low_high):
        if age < 15 or age >= 70:
            return 0 if low_high == 'low' else 3
        elif 40 <= age < 70:
            return 4 if low_high == 'low' else 6
        else:
            return 7 if low_high == 'low' else 10

def set_random_direction(person):
    person.direction = random.choice([d for d in ['S', 'SW', 'W', 'NW', 'N', 'NE', 'E', 'SE'] if d != person.direction])

def next_turn(xs, ys, colors):
    def is_contact(person1, person2):
        return max(abs(person1.x - person2.x), abs(person1.y - person2.y)) <= 2

    def get_distance_2_people(person1, person2):
        return max(abs(person1.x - person2.x), abs(person1.y - person2.y))

    def can_be_parents(person1, person2):
        return (20 <= person1.age <= 40 and 20 <= person2.age <= 40
                and get_distance_2_people(person1, person2) <= 2
                and not person1.current_turn_birth and not person2.current_turn_birth)

    for person in population:
        person.move()

        person.age += 1
        # p o zmianie przedziaªu wiekowego o dp orno±¢ p owinna zosta¢ dostosowana do
        # aktualnej grupy wiekowej o ile jest wy»sza ni» maksymalna dla aktualnego
        # wieku => czyli w sumie tylko jak ma wiek 15???
        if person.age == 15:
            person.immunity = 'high'
            person.immunity_number = 7

        if person.age > 100 or person.immunity_number <= 0:
            population.remove(person)

        nearest_people = sorted(population, key=lambda other: np.hypot(person.x - other.x,
                                                                       person.y - other.y) if other != person else float('inf'))

        if person.state == 'infected':
            person.immunity_number -= 0.1
        if person.state == 'sick':
            person.immunity_number -= 0.5
        if person.state == 'recovering':
            person.immunity_number += 0.1
        if person.state == 'healthy':
            person.immunity_number += 0.05

        person.set_immunities()

        person.current_state_counter += 1
        if person.current_state_counter in [2,5,7]:
            if person.current_state_counter == 2 and person.state == 'infected':
                person.state = 'sick'
                person.current_state_counter = 0
            if person.current_state_counter == 7 and person.state == 'sick':
                person.state = 'recovering'
                person.current_state_counter = 0
            if person.current_state_counter == 5 and person.state == 'recovering':
                person.state = 'healthy'
                person.current_state_counter = 0


        if is_contact(person, nearest_people[0]):
            set_random_direction(person)
            set_random_direction(nearest_people[0])

            if can_be_parents(person, nearest_people[0]):
                person.current_turn_birth = True
                nearest_people[0].current_turn_birth = True

                for _ in range(random.randint(1,2)):
                    new_person = Person()
                    new_person.x = person.x
                    new_person.y = person.y
                    new_person.age = 0
                    new_person.immunity_number = 3
                    population.append(new_person)

            if not person.current_turn_contact and not nearest_people[0].current_turn_contact:
                if person.state == 'healthy':
                    if nearest_people[0].state == 'infected':
                        if person.immunity == 'low':
                            person.state = 'infected'
                    elif nearest_people[0].state == 'sick':
                        if person.immunity in ['low', 'medium']:
                            person.state = 'infected'
                        else:
                            person.immunity_number -= 3
                    elif nearest_people[0].state == 'recovering':
                        nearest_people[0].immunity_number += 1
                    elif nearest_people[0].state == 'healthy':
                        person.immunity_number = max(person.immunity_number, nearest_people[0].immunity_number)
                        if person.immunity_number > get_immunity_number(person.age, 'high'):
                            person.immunity_number = get_immunity_number(person.age, 'high')

                        nearest_people[0].immunity_number = max(nearest_people[0].immunity_number, person.immunity_number)
                        if nearest_people[0].immunity_number > get_immunity_number(nearest_people[0].age, 'high'):
                            nearest_people[0].immunity_number = get_immunity_number(nearest_people[0].age, 'high')

                elif person.state == 'sick':
                    if nearest_people[0].state == 'healthy':
                        if nearest_people[0].immunity in ['low', 'medium']:
                            nearest_people[0].state = 'infected'
                        person.current_state_counter = 0
                    elif nearest_people[0].state == 'recovering':
                        if nearest_people[0].immunity in ['low', 'medium']:
                            nearest_people[0].state = 'healthy'
                    elif nearest_people[0].state == 'sick':
                        person.current_state_counter = 0
                        nearest_people[0].current_state_counter = 0

                        person.immunity_number = min(person.immunity_number, nearest_people[0].immunity_number)
                        nearest_people[0].immunity_number = min(nearest_people[0].immunity_number, person.immunity_number)

                elif person.state == 'infected':
                    if nearest_people[0].state == 'recovering':
                        nearest_people[0].immunity_number -= 1
                    elif nearest_people[0].state == 'infected':
                        person.immunity_number -= 1
                        nearest_people[0].immunity_number -= 1

                person.update_immunity()
                nearest_people[0].update_immunity()

        xs.append(person.x)
        ys.append(person.y)
        colors.append(get_color(person.state))

    return xs, ys, colors

def update(frame):
    xs = []
    ys = []
    colors = []

    xs, ys, colors = next_turn(xs, ys, colors)

    scat.set_offsets(np.c_[xs, ys])
    scat.set_color(colors)
    print('healthy: ' ,sum(1 for person in population if person.state == 'healthy'))
    print('infected: ',sum(1 for person in population if person.state == 'infected'))
    print('sick: ',sum(1 for person in population if person.state == 'sick'))
    print('recovering: ', sum(1 for person in population if person.state == 'recovering'), end='\n\n')
    # for p in population:
    #     print(p.current_state_counter, p.state if p.state != 'healthy' else '', end=' ')
    ax.set_title(f"Turn: {frame + 1}")
    return scat, ax.title


population_size = 200
infected_people = 10
population = [Person() for _ in range(population_size)]
for person in population[:infected_people]:
    person.state = 'infected'


fig, ax = plt.subplots()
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

scat = ax.scatter([], [], s=50)

turn_count = 100
ani = FuncAnimation(fig, update, frames=turn_count, interval=100, blit=False, repeat=False)
plt.show()
