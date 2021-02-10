import sys                    #to give file as grg in cmd
fileName = sys.argv[1]

# fileName=input()                       #to input file name from keyboard
f = open(fileName)  
list_ = f.read().split('\n')    #take text file as an input

# list_ = input().split('\n')   #to input from keyboard

line_1 = list(map(int,list_[0].split()))
n_videos = line_1[0]
n_endpoints = line_1[1]
req_description = line_1[2]
n_caches = line_1[3]
caches_size = line_1[4]
remsize_cache = [caches_size]*n_caches
videos_size = list(map(int, list_[1].split()))
i=2

print("collecting endpoints data")

#collecting endpoints latency to caches
endpoints_data = []
endpoint_l = []
while(n_endpoints > 0):
    latency, connected_caches = list(map(int, list_[i].split()))
    endpoint_l.append(latency)
    t_dict = {}
    i+=1
    while(connected_caches>0):
        c_index, c_latency = list(map(int, list_[i].split()))
        t_dict[c_index]=c_latency
        i+=1
        connected_caches-=1
    endpoints_data.append(t_dict)
    n_endpoints-=1

print("request discription...")
req_dict = {}
while(req_description > 0):
    i_video, i_endpoint, n_req = list(map(int, list_[i].split()))
    if (i_video, i_endpoint) in req_dict:
        req_dict[(i_video, i_endpoint)] = min(req_dict[(i_video, i_endpoint)],n_req)
    else:
        req_dict[(i_video, i_endpoint)] = n_req
    req_description-=1
    i+=1


temp_l=[]
for i in req_dict.items():
    temp_l.append([i[1],i[0]])
temp_l.sort() #returns list
print("creating score list")
score_list = []
for i in reversed(range(len(temp_l))):
    n_req, y = temp_l[i]
    i_video = y[0]
    i_endpoint = y[1]
    td = endpoints_data[i_endpoint]
    done = False
    while not done:
        if len(td)==0:   #check for empty dict condition
            break
        i_cache = min(td,key=td.get) 
        done = True
        if int(remsize_cache[i_cache]) < videos_size[i_video]:
            td.pop(i_cache)
            done = False
    if not done:
        score_list.append([0,None,None])
        continue
    remsize_cache[i_cache] -= videos_size[i_video]
    t_score = (endpoint_l[i_endpoint] - td[i_cache])*n_req
    score_list.append([t_score,i_video,i_cache])

score_list = list(reversed(score_list))
print("creating output list")
output_list = {i:[] for i in range(n_caches)}
remsize_cache = [caches_size]*n_caches
score=999
while(True):
    score, i_video, i_cache = max(score_list)
    if score==0:
        break
    if remsize_cache[i_cache] >= videos_size[i_video]:
        output_list[i_cache].append(i_video)
        remsize_cache[i_cache] -= videos_size[i_video]
    i_obj = score_list.index(max(score_list))
    del score_list[i_obj]
    del temp_l[i_obj]


output_str=''
caches_used = 0
for k,v in output_list.items():
    if len(v) > 0:
        caches_used+=1
        output_str += str(k)+ ' '
        for i in v:
            output_str += str(i) + ' '
        output_str += " \n"
output_str = str(caches_used) + " \n" + output_str

# print(output_str)
with open(fileName+'.out','w') as fp:
    fp.write(output_str)
