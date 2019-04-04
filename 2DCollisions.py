import numpy as np 
from matplotlib import pyplot as plt 
from vpython import *

# Size of the 'table' or allowed area too the pucks
size_x = 50 
size_y = 50

# Size of the timestep used to calculate changes in position
dt = 0.001 

radius_puck = 1
height_puck = .25

class puck:

    def __init__(self, Pos, Vel, Mass, Color):

        self.pos = Pos + vector(radius_puck, radius_puck, 0)
        self.vel = Vel
        self.mass = Mass
        self.stick = False

        self.positions_x = [] #self variable to hold all the x positions the puck was in
        self.positions_y = [] #ditto for y positions
        self.velocities = [] # unimplemented list too hold velocites

        self.object = cylinder(pos = self.pos, axis = vector(0,0,height_puck), radius = radius_puck, color = Color )  

    def UpdatePos(self, dt, other):

        self.pos = self.pos + dt*self.vel
        self.object.pos = self.pos + dt*self.vel

        self.positions_x.append(self.pos.x)
        self.positions_y.append(self.pos.y)


    def CheckWallCollision(self):

        if self.pos.x >= size_x - radius_puck:
            self.vel.x = -1 * self.vel.x

        if self.pos.x <= 0 + radius_puck:
            self.vel.x = -1 * self.vel.x

        if self.pos.y >= size_y - radius_puck:
            self.vel.y = -1 * self.vel.y

        if self.pos.y <= 0 + radius_puck:
            self.vel.y = -1 * self.vel.y
    
    def CheckCollision(self, other):

        if True == True:
            if mag(self.pos - other.pos) < 2 * radius_puck:
                self.vel = self.vel - (2*other.mass)/(self.mass + other.mass) * dot(self.vel - other.vel, self.pos - other.pos)/(mag2(self.pos - other.pos)) * (self.pos - other.pos)
                other.vel = other.vel - (2*self.mass)/(other.mass + self.mass) * dot(other.vel - self.vel, other.pos - self.pos)/(mag2(other.pos - self.pos)) * (other.pos - self.pos)
        else:
            if mag(self.pos - other.pos) < 2 * radius_puck:
                self.vel  = (other.vel*other.mass + self.vel*self.mass)/(other.mass + self.mass)
                other.vel = (other.vel*other.mass + self.vel*self.mass)/(other.mass + self.mass)

def SetupWalls():

    scene.title = '2D - Collisions Simulation'
    scene.width = 1200
    scene.heigth = 2000
    scene.autoscale = True

    #Center the camera on the center of the space available to the pucks
    scene.center = vector((1/2)*size_x, (1/2)*size_y, 0)

    #Horizontal Walls on top and bottom
    box(pos = vector((1/2) * size_x,0,0), size = vector(size_x, .25, .25) )
    box(pos = vector((1/2) * size_x,size_y,0), size = vector(size_x, .25, .25) )

    #Vertical Walls on left and right
    box(pos = vector(0,(1/2)*size_y,0), size = vector(.25, size_y, .25) )
    box(pos = vector(size_x,(1/2)*size_y,0), size = vector(.25, size_y, .25) )


def ExportData(name, object, time):
    
    f = open("data/" + name+ ".csv",'w')

    for n, each in enumerate(object.positions_x):
        f.write( str(time[n]) + "," + str(each) + "," + str(object.positions_y[n]) + '\n' ) 
        print(each)

    f.close()

def main():
    
    SetupWalls() #setup canvas and create enviroment

    puck_1 = puck( vector(25,0,0), vector(0,10,0), 100, color.blue) #Create puck1 , Usage is puck( POSITION, VELOCITY, MASS, COLOR)
    puck_2 = puck( vector(0,25/3,0), vector(30,0,0) , 1, color.green)

    time = [] #Empty list too hold all the time points where a position point was taken. 
    t = 0 

    while t < 3: # Run the time for 3 seconds

        rate(350) # display rate, higher number means it runs quicker, this is essentially a delay

        puck_1.UpdatePos(dt, puck_2) #increment the position of the puck by its velocity for given dt
        puck_1.CheckWallCollision() #Just turn the pucks around if they hit a wall, actually not important because the collisions are all we care about but hey, its here

        puck_2.UpdatePos(dt, puck_1)
        puck_2.CheckWallCollision()

        puck_1.CheckCollision(puck_2) #check if the pucks collided if they did change the velocities


        time.append(t) #add time to list
        t = t + dt

    plt.plot(time, puck_1.positions_x) # Create a plot of X pos(puck 1) vs. Time
    plt.xlabel(' Time(s) ')
    plt.ylabel(' Position (x) ')
    plt.show()

    ExportData("Behemoth", puck_1, time)
    ExportData("Normal", puck_2, time)

if __name__ == "__main__":
    main()
    exit(0)

