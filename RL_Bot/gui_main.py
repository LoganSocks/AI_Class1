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
goal_position = (15, 15)
reward = 0

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
    # This adds text to the canvas, that eventually will be a picture of the drone
    canvas.create_text(x1 + cell_size//2, y2 + cell_size//2, text="DRONE", fill="white", font=("Arial",12, "bold"))

#Move drone randomly one space at a time
def move_drone():
    #Keep track of the dornes position or state
    global drone_row, drone_column
    #Give 4 directions to move
    #This is the list of the possible directons
    directions = ["up", "down", "left", "right"]
    #This will chose a radnom direction from the list
    direction = random.choice(directions)

    #This will figure out which direction the drone chose and move it accordingly
    if direction == "up":
        #Move drone by decreasing row number, stop at 0 because it is the wall
        drone_row = max(0, drone_row - 1)

    elif direction == "down":
        #move down a row by increasing row number, stop at 3 because it is the wall for a 4x4 grid
        drone_row = min(3, drone_row + 1)

    elif direction == "left":
        #Move a column left by decreasing the column number , stop at 0 which is the wall
        drone_column = max(0, drone_column - 1)
    
    elif direction == "right":
        #Move rught a column by increasing the column number, 3 is the wall again
        drone_column = min(3, drone_column + 1)    

    #draw the drone in it's new position
    draw_drone()
    #Update the user and print it to the console
    print(f"Patrol Drone moved {direction} to position: Row {drone_row}, Column {drone_column}")
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
        time.sleep(0.5)
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

draw_grid()
draw_drone()
draw_goal()
#Update the user on current state of drone
print("Drone Awake")
print(f"Drone starting pos Row: {drone_row}, Column: {drone_column}")
#THIS ALLOWS US TO SEE IF NOT HERE NOTHING WILL APPEAR
window.mainloop()

