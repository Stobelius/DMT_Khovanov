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
#This error was not obtained with any real braid representative, but with some artificial testing.

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
            to_be_verified=verify(to_be_verified,v)
        to_be_verified.discard(cell)

        return to_be_verified

    verified=all_words
    while(len(verified)!=0):
        cell=verified.pop()
        verified.add(cell)
        verified=verify(verified,cell)


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

        #if braid_name=="9_35":
        singlebraid(ks_braid)


        print(braid_name)
        print(ks_braid)

        