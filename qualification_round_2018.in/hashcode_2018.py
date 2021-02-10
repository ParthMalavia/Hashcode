import sys                    #to give file as grg in cmd

def distance(x,y):
    return (abs(x[0] - y[0]) + abs(x[1] - y[1]))

class Ride:
    
    def __init__(self, start, end, earliest_s, latest_f, dist, index):
        self.index = index
        self.start = start
        self.end = end
        self.earliest_s = earliest_s
        self.latest_f = latest_f 
        self.dist = dist 
        self.rejectedby = []
    
    
class Car:
    def __init__(self, index):
        self.index = index
        self.crnt_position = (0,0)
        self.dest_position = (0,0)
        self.rem_steps = 0
        self.is_free = True
        self.taken_rides = []
    
    def assign(self, ride):
        self.dest_position = ride.end 
        if is_pickedOnTime:
            self.rem_steps = ride.earliest_s + ride.dist - crnt_step
        else:
            self.rem_steps = distance(self.crnt_position, ride.start) + ride.dist
        self.taken_rides.append(str(ride.index))
        self.is_free = False


def total_dist(car,ride):
    if is_pickedOnTime:
        return rides[i].latest_f
    else:
        return distance(cars[c].crnt_position, rides[i].start) + rides[i].dist + crnt_step

fileName = sys.argv[1]
# fileName=input()                       #to input file name from keyboard
with open(fileName) as f:
    t_list = f.read().split('\n')    #saperating data in list 

raws, columns, n_vihicals, n_rides, bonus, sim_steps = list(map(int,t_list.pop(0).split()))
if len(t_list) > n_rides:
    t_list.pop()

#creating ride list
rides = []                          
index = 0
for l in t_list:
    r1, c1, r2, c2, earliest_s, latest_f = list(map(int,l.split()))
    dist = abs(r1 - r2) + abs(c1 - c2)
    rides.append(Ride((r1,c1), (r2,c2), earliest_s, latest_f, dist, index))
    index+=1

#creating cars(vehicles) 
cars = []
for c in range(n_vihicals):
    cars.append(Car(c))


rides = sorted(rides, key= lambda r:r.dist , reverse=True)  #sort rides in decreasing order according to distance
rejected_rides=[]
#starting simulation
crnt_step=0
while crnt_step<sim_steps:
    if len(rides)==0:               #once rejected ride could fit another time
        if len(rejected_rides)==0:
            break
        rides=rejected_rides
        for r in rides:
            r.rejectedby=[]
        rejected_rides=[]
        
    for c in range(n_vihicals):
        if cars[c].is_free:
            i=0
            done = False
            while (not done) and i < len(rides) :
                is_pickedOnTime = crnt_step+ distance(cars[c].crnt_position, rides[i].start) <=  rides[i].earliest_s
                if (cars[c].index not in rides[i].rejectedby) and  total_dist(cars[c], rides[i])<= rides[i].latest_f :
                    cars[c].assign(rides[i])
                    rides.pop(i)
                    i=0
                    done = True
                else:
                    rides[i].rejectedby.append(cars[c].index)
                    if len(rides[i].rejectedby) == n_vihicals:
                        rides.pop(i)
                    i+=1   
        else:
            cars[c].rem_steps-=1
            if cars[c].rem_steps==0:
                cars[c].is_free = True
                cars[c].crnt_position = cars[c].dest_position
    crnt_step+=1


#creating output file
out_string = ''
for car in cars:
    out_string+=str(len(car.taken_rides))+' '+' '.join(car.taken_rides)+'\n'
    
with open(fileName +'.out','w') as fp:
    fp.write(out_string)