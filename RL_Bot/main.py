# Import random library for movements
import random

print("*********Bird Drone Security Training*********")
print("\n Our Bird Drones are state of the art technology that use reinforcement learning to patrol patches of our skies.")
print("\n Each drone has the ability to report back to us for directions moved and potential threats and debris")
print("\n Each Drone has the ability to move in the following directions")
print("\n **** 1 = Forward, 2 = Backward, 3 = Right, 4 = Left ****")

def auto_fly():

    distance_to_fly = input("How many tiles would you like me to fly on my own?")

    print(f"\n I am about to fly {distance_to_fly} tiles on my own.\n")
    for i in range(int(distance_to_fly)):
        direction_to_fly = random.randint(1,4)

        print(f"\n I have flown {i} of {distance_to_fly} tiles.")

        print("\n I just flew ", direction_to_fly)

        with open("flight_records.txt", "a") as f:
            f.write(str(direction_to_fly) + ",")
        
        print("I just wrote my flight path to a text file.")




def manually_fly_the_drone():

    flying = "yes"

    while flying.lower() == "yes" or "y":
        direction_to_fly = random.randint(1,4)

        print("\n I just flew ", direction_to_fly)

        with open("flight_records.txt", "a") as f:
            f.write(str(direction_to_fly) + ",")
        
        print("I just wrote my flight path to a text file.")

        flying = input("Should we continue patrol?")

#manually_fly_the_drone()
auto_fly()