import sys

class Book:
    
    def __init__(self,index,reward):
        self.index = index
        self.reward = reward

class Library:
    
    def __init__(self,index,num_books,signup_time,ship_cap,lib_books):
        self.index = index
        self.num_books = num_books
        self.signup_time = signup_time
        self.ship_cap = ship_cap
        self.books = sorted(lib_books,key=(lambda indx : books[indx].reward))
        self.score = score(lib_books, signup_time)
        self.is_signedup = False
        self.is_completed = False
        self.scaned_books = []
        
def score(lib_books,signup_time):
    sum = 0
    for indx in lib_books:
        sum+=books[indx].reward
    sum-=signup_time
    return sum

fileName= sys.argv[1]
# fileName=input()                       #to input file name from keyboard
with open(fileName) as f:
    t_list = f.read().split('\n')    #saperating data in list 

while len(t_list[len(t_list)-1]) == 0:     #to remove last element if it is empty
    t_list.pop()
  
total_books, total_lib, total_days = map(int,t_list.pop(0).split())
#storing books data
books = []
i=0
for rwd in map(int,t_list.pop(0).split()):
    books.append(Book(i, rwd))
    i+=1

#storing library data
i=0
libraries = []
while len(t_list)>1:
    num_books, signup_time, ship_cap = map(int,t_list.pop(0).split())
    lib_books = list(map(int,t_list.pop(0).split()))
    libraries.append(Library(i,num_books,signup_time,ship_cap,lib_books))
    i+=1

old_lib = libraries    
libraries = sorted(libraries,key=(lambda l:l.score),reverse=True)
out_libraries = []
crnt_day=0
while crnt_day < total_days:
    for lib in range(len(libraries)):
        index = libraries[lib].index
        if not libraries[lib].is_signedup:                  #signup library
            libraries[lib].signup_time-=1                   #reduce days as it passed
            if libraries[lib].signup_time==0:                
                libraries[lib].is_signedup = True           
                out_libraries.append(libraries[lib].index)  
            break                                           #break for-loop so that no other library can signup
        else:
            if len(libraries[lib].books)==0:
                libraries[lib].is_completed = True
            else:
                for s in range(len(libraries[lib].books) if libraries[lib].ship_cap > len(libraries[lib].books) else libraries[lib].ship_cap): 
                    old_lib[index].scaned_books.append(libraries[lib].books.pop())
    for lib in reversed(range(lib+1)):          #from crnt library in reverse remove all library which has done task
        if libraries[lib].is_completed:
            libraries.pop(lib)
    crnt_day+=1

out_string = str(len(out_libraries))

for index in out_libraries:
    out_string+='\n'+str(index)+' '+str(len(old_lib[index].scaned_books))
    out_string+='\n'+' '.join(map(str,old_lib[index].scaned_books))

with open( fileName +'.out', 'w') as fp:
    fp.write(out_string)