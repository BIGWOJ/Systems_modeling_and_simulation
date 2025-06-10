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
        self.state = 'healthy'
        self.current_state_counter = 0
        self.age = np.random.randint(0, 60)
        self.set_immunities(initialize=True)
        self.current_turn_birth = False
        self.current_turn_contact = False

    def set_immunities(self, initialize=False, based_on_number=False):
        if based_on_number:
            if self.immunity in ['medium', 'high']:
                if self.immunity == 'medium' and self.immunity_number < get_immunity_number(self.age, 'low'):
                    self.immunity = 'low'
                elif self.immunity == 'high' and self.immunity_number < get_immunity_number(self.age, 'low'):
                    self.immunity = 'medium'
            return

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
        self.x = max(0, min(self.x, 100))

        # y cordinate
        if self.direction in ['S', 'SW', 'SE']:
            self.y -= self.speed
        if self.direction in ['N', 'NW', 'NE']:
            self.y += self.speed
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

    def count_states():
        healthy = sum(1 for person in population if person.state == 'healthy')
        infected = sum(1 for person in population if person.state == 'infected')
        sick = sum(1 for person in population if person.state == 'sick')
        recovering = sum(1 for person in population if person.state == 'recovering')
        return {'healthy': healthy,
                'infected': infected,
                'sick': sick,
                'recovering': recovering }

    for person in population:
        person.move()

        person.age += 1

        if person.age > 100 or person.immunity_number <= 0:
            population.remove(person)

        nearest_person = min((other for other in population if other != person),
                             key=lambda other: np.hypot(person.x - other.x, person.y - other.y))

        if person.state == 'infected':
            person.immunity_number -= 0.1
        if person.state == 'sick':
            person.immunity_number -= 0.5
        if person.state in ['recovering', 'healthy']:
            if person.immunity_number < get_immunity_number(person.age, 'high'):
                person.immunity_number += 0.1 if person.state == 'recovering' else 0.05

        person.set_immunities(based_on_number=True)

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

        if is_contact(person, nearest_person):
            set_random_direction(person)
            set_random_direction(nearest_person)

            if can_be_parents(person, nearest_person) and random.random() < birth_probability_after_contact:
                person.current_turn_birth = True
                nearest_person.current_turn_birth = True

                for _ in range(random.randint(1,2)):
                    new_person = Person()
                    new_person.x = person.x
                    new_person.y = person.y
                    new_person.age = 0
                    new_person.immunity_number = 3
                    population.append(new_person)

            if not person.current_turn_contact and not nearest_person.current_turn_contact:
                if person.state == 'healthy':
                    if nearest_person.state == 'infected':
                        if person.immunity == 'low':
                            person.state = 'infected'
                    elif nearest_person.state == 'sick':
                        if person.immunity in ['low', 'medium']:
                            person.state = 'infected'
                        else:
                            person.immunity_number -= 3
                    elif nearest_person.state == 'recovering':
                        nearest_person.immunity_number += 1
                    elif nearest_person.state == 'healthy':
                        person.immunity_number = max(person.immunity_number, nearest_person.immunity_number)
                        if person.immunity_number > get_immunity_number(person.age, 'high'):
                            person.immunity_number = get_immunity_number(person.age, 'high')

                        nearest_person.immunity_number = max(nearest_person.immunity_number, person.immunity_number)
                        if nearest_person.immunity_number > get_immunity_number(nearest_person.age, 'high'):
                            nearest_person.immunity_number = get_immunity_number(nearest_person.age, 'high')

                elif person.state == 'sick':
                    if nearest_person.state == 'infected':
                        if nearest_person.immunity in ['low', 'medium']:
                            nearest_person.state = 'sick'
                        person.current_state_counter = 0
                    elif nearest_person.state == 'recovering':
                        if nearest_person.immunity in ['low', 'medium']:
                            nearest_person.state = 'healthy'
                    elif nearest_person.state == 'sick':
                        person.current_state_counter = 0
                        nearest_person.current_state_counter = 0

                        person.immunity_number = min(person.immunity_number, nearest_person.immunity_number)
                        nearest_person.immunity_number = min(nearest_person.immunity_number, person.immunity_number)

                elif person.state == 'infected':
                    if nearest_person.state == 'recovering':
                        nearest_person.immunity_number -= 1
                    elif nearest_person.state == 'infected':
                        person.immunity_number -= 1
                        nearest_person.immunity_number -= 1

                person.update_immunity()
                nearest_person.update_immunity()

        xs.append(person.x)
        ys.append(person.y)
        colors.append(get_color(person.state))

    return xs, ys, colors, count_states()


def update(frame):
    xs = []
    ys = []
    colors = []

    xs, ys, colors, states_count_dict = next_turn(xs, ys, colors)
    if frame < animation_turn_count:
        state_changes_over_time.append(states_count_dict)

    scat.set_offsets(np.c_[xs, ys])
    scat.set_color(colors)
    ax.set_title(f"Turn: {frame + 1}")
    return scat, ax.title

def plot_state_changes(state_changes_over_time, turn_count):
    turns = range(0, turn_count + 1)
    healthy_counts = [state['healthy'] for state in state_changes_over_time]
    infected_counts = [state['infected'] for state in state_changes_over_time]
    sick_counts = [state['sick'] for state in state_changes_over_time]
    recovering_counts = [state['recovering'] for state in state_changes_over_time]

    plt.figure()
    plt.plot(turns, healthy_counts, label='Healthy', color='green')
    plt.plot(turns, infected_counts, label='Infected', color='yellow')
    plt.plot(turns, sick_counts, label='Sick', color='red')
    plt.plot(turns, recovering_counts, label='Recovering', color='orange')
    plt.xlabel('Turn')
    plt.ylabel('Population count')
    plt.title('State changes over time')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    ##### Simulation parameters
    population_size = 100
    starting_infected_people_count = 10
    animation_turn_count = 50
    birth_probability_after_contact = 0.9
    #####

    state_changes_over_time = []
    population = [Person() for _ in range(population_size)]
    for person in population[:starting_infected_people_count]:
        person.state = 'infected'

    fig, ax = plt.subplots()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    scat = ax.scatter([], [], s=50)

    ani = FuncAnimation(fig, update, frames=animation_turn_count, interval=100, blit=False, repeat=False)
    plt.show()

    plot_state_changes(state_changes_over_time, animation_turn_count)