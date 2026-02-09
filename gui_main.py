#Use tkinter for the GUI
import tkinter as tk
#Import the random library for movements
import random
#Import time to let us pause so we can see every move the drone makes
import time


window = tk.Tk()
#This is the title
window.title("Bird Drone Security Training")
#This makes squares a certain size
cell_size = 25
#We are making the dron start at (0,0) which is usually the upper leftmost squarer of a grid
drone_row = 0
drone_column = 0
#Create an area for us to draw everything
canvas = tk.Canvas(window, width=400, height=400, bg="white")
#Pack adds the element to the window
canvas.pack()
#Create a variable for the goal positions location
goal_position = (13, 13)
q_table = {}
total_points = 0
learning_rate = .1
discount_factor = .95
global epsilon
epsilon = 1
epsilon_decay = 0.995

def get_q_Values(row, col):

    state = (row, col)
    if state not in q_table:
        q_table[state] = {"up": 0, "down": 0, "left": 0, "right": 0}
    return q_table[state]
    
def choose_where_to_move():
    if random.random() < epsilon:
        return random.choice(["up", "down", "left", "right"])
    
    current_q_values = get_q_Values(drone_row, drone_column)
    return max(current_q_values, key=current_q_values.get)
#This function will draw a grid on the window
def draw_grid():
    #To make the grid loop through 5 times so 5 lines are drawn
    for i in range(16):
        #Draw horizontal lines for the grid
        canvas.create_line(0, i * cell_size, 400, i * cell_size, fill="black")
        #Draw the vertical lines for the grid
        canvas.create_line(i * cell_size, 0, i * cell_size, 400, fill="black")
#This function draws the goal or charging station
def draw_goal():
    #draws the goal in the bottom rightmost square
    canvas.create_rectangle(goal_position[1]*cell_size, goal_position[0]*cell_size,(goal_position[1]+1)* cell_size, (goal_position[0]+1)* cell_size, fill="green")
       
             


#This function will draw the robot
def draw_drone():
    #Everyimte this function is called it is deleted so everything can be redrawn in the new position
    canvas.delete('all')
    #Redraw the grid after it gets deleted
    draw_grid()
    #Redraw the goal after it gets deleted
    draw_goal()
    #Get the state
    #Get x position for left side
    x1 = drone_column * cell_size
    #Get y position aka forward or top
    y1 = drone_row * cell_size
    #Get X position for rigth side
    x2 = x1 + cell_size
    #Get the bootom position for the square
    y2 = y1 + cell_size
    #For now drone will be a orange box
    canvas.create_rectangle(x1,y1,x2,y2, fill="orange")
    
#This function will createb a window to view the q table
def view_q_table():
    q_table_window = tk.Toplevel(window)
    q_table_window.title("Drone's Brain Table")

    title = tk.Label(q_table_window, text="Q-Table: Square (Row, Col) and Direction Scores", font=("Arial", 10, "bold"))
    title.pack(pady=5)

    text_area = tk.Text(q_table_window, width=60, height=20)
    text_area.pack(padx=10, pady=10)

    text_area.insert(tk.END, f"{'Location':<15} | {'Scores (U, D, L, R)':<30}\n")
    text_area.insert(tk.END, "-"*50 + "\n")

    for state in sorted(q_table.keys()):
        scores = q_table[state]
        score_str = f"U:{scores['up']}, D:{scores['down']}, L:{scores['left']}, R:{scores['right']}"
        text_area.insert(tk.END, f"{str(state):<15} | {score_str:<30}\n")
#Move drone randomly one space at a time
def move_drone():
    #Keep track of the dornes position or state
    global drone_row, drone_column, total_points, epsilon
    #Get the current spot so it is avaialbe to be pulled for the old row and column
    current_memory = get_q_Values(drone_row, drone_column)
    #Give 4 directions to move
    #Call the choose where to go function and set it to the direction
    directions = choose_where_to_move()
    #Create variables for the old positions for the q table
    old_row = drone_row
    old_col = drone_column

    if directions == "up": drone_row = max(0, drone_row - 1)
    elif directions == "down": drone_row = min(15, drone_row + 1)
    elif directions == "left": drone_column = max(0, drone_column - 1)
    elif directions == "right": drone_column = min(15, drone_column + 1)

    if (drone_row, drone_column) == goal_position:
        reward = 100
        total_points += reward
        epsilon *= epsilon_decay
        drone_row = 0
        drone_column = 0
        print(f"SuccesfullPatrol! Total Points: {total_points}")
    elif (drone_row, drone_column) == (old_row, old_col):
        reward = -5
        total_points += reward
    else:
        reward = -1
        total_points += reward
    old_q_value = q_table[(old_row, old_col)][directions]
    next_max = max(get_q_Values(drone_row, drone_column).values())
    q_table[(old_row, old_col)][directions] += learning_rate * (reward + discount_factor * next_max - old_q_value)

    draw_drone()
        
    

     

    
    #Update the user and print it to the console
    print(f"Patrol Drone moved {directions} to position: Row {drone_row}, Column {drone_column}")
#Create a funciton to move multiple times in one go
def fly_multiple_times():
    #Use the user input to determine how many moves
    num_tiles_flown = int(entry.get())
    #This will loop the number of moves
    for i in range(num_tiles_flown):
        #Move the drone for each move
        move_drone()
        # Update the window
        window.update()
        #Delay so we have time to see what is happening
        #window.after(500)
        #I figured out that the above function was only scheduling a bg task for later
        #Gemini helped me figure out that the time.sleep function pauses execution for however long you say, so we are able to see every move
        time.sleep(0.1)
#This label informs user of what is happening 
label = tk.Label(window, text="Tiles to fly:", font=("Arial",12))
#Packing adds the element to the window
label.pack()

#extbox for number of moves we want
entry = tk.Entry(window, font=("Arial", 12))
entry.pack()

#Button to make drone move
button = tk.Button(window, text="Move Drone", command= fly_multiple_times, font=("Arial", 12), bg="lightgreen")
button.pack()
#Button to view the drones q-table
brain_button = tk.Button(window, text="View Drone Brain", command=view_q_table, font=("Arial", 12), bg="lightblue")
brain_button.pack(pady=5)

draw_grid()
draw_drone()
draw_goal()
#Update the user on current state of drone
print("Drone Awake")
print(f"Drone starting pos Row: {drone_row}, Column: {drone_column}")
#THIS ALLOWS US TO SEE IF NOT HERE NOTHING WILL APPEAR
window.mainloop()

