from braidalgo import *
from khtfilegenerator import knotinfo_string_to_integer_array
from outputcomparer import integer_array_to_knotscape_string
import csv


#Quick and dirty way of verifying that the Khovanov complex when given the greedy matching, does not have cycles.
#If the program terminates given a braid, then the complex of that braid does not contain cycles.

#If a loop was found in the graph, this program does not alert the user, but instead goes into an infinite recursion loop.
#In my machine, this quickly results in the following error:
#
#RecursionError: maximum recursion depth exceeded in comparison 
#
#which of course could be evoked by a number of things in python.
#
#A cycle was found in "ADBcbDccbbADcb" and similar cycle in the smaller braid "ADcbccbbAD".

def updown_next_steps(braid,cell,history):
    fake_previous_u=-1

    """
    #Testing:
    if cell=="0yxx":
        return ["0xxy"]
    """


    for i in range(1,len(braid)+1):    
        if not cell[:i] in history[i]:
            fake_previous_u=i-1         
            break

    if fake_previous_u==-1:
        return []    

    steps_up=next_steps_up(braid, cell, fake_previous_u)
    
    steps_down=[]
    qdeg=qdeg_of_word(braid,cell)

    for step_pair in steps_up:
        if qdeg_of_word(braid,step_pair[0])!=qdeg:
            continue
        elif step_pair[0] in history[-1]:
            continue
        down=next_step_down(braid,step_pair[0],step_pair[1],history)
        if down!=-1 and down!=-2 and down[0]!=cell:
            steps_down.append(down[0])        

    return steps_down

def singlebraid(braid):

    all_words=generate_all_enhanced_words(braid)
    print(len(all_words))
    
    history=generate_unmatched_cell_history(braid)

    def verify(to_be_verified, cell):
        
        #print(cell)
        N=updown_next_steps(braid,cell,history)

        for v in N:
            #print(v)
            #if v=="111010101Y":
            #    continue

            to_be_verified=verify(to_be_verified,v)
        to_be_verified.discard(cell)

        return to_be_verified

    verified=all_words
    #verify(verified,"110011100y1110")


    while(len(verified)!=0):
        cell=verified.pop()
        #print(cell)

        verified.add(cell)
        verified=verify(verified,cell)


def finding_cycles_up_to_10_edges(braid):
    all_words=generate_all_enhanced_words(braid)
    print(len(all_words))
    
    history=generate_unmatched_cell_history(braid)

    def cyc_10_from(braid,word,history,path):
        if len(path)==7:
            #for 6 this gives no cycles
            #for 7 this gives a cycle
            return
        
        next_steps=updown_next_steps(braid,word,history)
        
        for n in next_steps:
            if n in path:
                print("CYCLEEE")
                print(path)
                #print(n)
        
        for n in next_steps:
            newpath=path.copy()
            newpath.append(n)
            cyc_10_from(braid,n,history,newpath)       
        

    for word in all_words:
        cyc_10_from(braid,word,history,[word])



    return None


"""
#testing
braid="aaaa"

singlebraid(braid)
history=generate_unmatched_cell_history(braid)
print("")
print("")

a=updown_next_steps(braid,"0yxx",history)   
print(a)
"""
def explicit_cycle_from(braid,cell):

    def continue_path(braid,path,history):

        #print("assda")
        vertex=path[-1]

        fake_previous_u=len(braid)
        for i in range(1,len(braid)+1):    
            if not vertex[:i] in history[i]:
                fake_previous_u=i-1         
                break
         
        
        steps_up=next_steps_up(braid, vertex, fake_previous_u)
        #print(steps_up)


        up_down_steps=[]
        qdeg=qdeg_of_word(braid,vertex)

        for step_pair in steps_up:
            if step_pair[0] in history[-1]:
                continue
            down=next_step_down(braid,step_pair[0],step_pair[1],history)
            if down!=-1 and down!=-2 and down[0]!=vertex:
                
                up_down_steps.append((step_pair[0],down[0]))
        
        for pair in up_down_steps:
            path_copy=path.copy()
            print(path_copy)
            print(pair[1])
            print("")

            if pair[1] in path_copy:
                path_copy.append(pair[0])
                path_copy.append(pair[1])
                print("Found a cycle!")
                print(path_copy)
                return (path_copy)
            else:
                path_copy.append(pair[0])
                path_copy.append(pair[1])
                continue_path(braid,path_copy,history)

    history=generate_unmatched_cell_history(braid)



    path=[cell]

    cycle=continue_path(braid,path,history)
    return cycle


#finding_cycles_up_to_10_edges("ADBcbDccbbADcb")

singlebraid("ADcbccbbAD")

"""

#singlebraid("ADBcbDccbbADcb")

mincounterexbraid="ADcbccbbAD"
mincell="11110x1011"
mincell2="111010101Y"

cyc=explicit_cycle_from(mincounterexbraid,mincell2)
print(cyc)

"""



"""
#singlebraid("ADBcbDccbbAD")
startComputing=False



csv_file_path = 'braid_reps_from_ki/knots_up_to_12.csv'
#csv_file_path = 'knotinfo_braids13.csv'

# Open the CSV file
with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    
    # skip header
    next(csv_reader)  

    # Iterate through each row in the CSV file
    for line in csv_reader:
        #print(line)

        braid_name=line[0]
        ki_braid=knotinfo_string_to_integer_array(line[1].strip())
        ks_braid=integer_array_to_knotscape_string(ki_braid)

        if braid_name=="12n_785":
            startComputing=True
        
        if not startComputing:
            continue
        
        singlebraid(ks_braid)


        print(braid_name)
        print(ks_braid)

        
"""