import pickle
import os
from braidalgo import qdeg_of_word, hdeg_of_word, count_starting_ones

########### Utilities:  Loading precalculated cells and paths

def load_cells(twistnumber):
    #Currently 44 is highest doable out of legit ones. There is 100 twist synthetic ones also.
    if twistnumber>44:
        file_path="Torus4braid_paths/"+str(twistnumber)+"synthetic_cells.pkl"
        with open(file_path, 'rb') as file:
            return pickle.load(file)
   
    file_path="Torus4braid_paths/44twistcells.pkl"

    history=None

    with open(file_path, 'rb') as file:
        history = pickle.load(file)
    unmatched_cells=history[3*twistnumber]
    return unmatched_cells


def load_paths(twistnumber):

    file_path="Torus4braid_paths/4string"+str(twistnumber)+"twist.pkl"
    paths=None
    with open(file_path, 'rb') as file:
        paths = pickle.load(file)

    return paths

def load_new_T4_paths(twistnumber):
    #Current maximum is 11
    file_path="Torus4braid_paths/new4string"+str(twistnumber)+"twist.pkl"
    paths=None
    with open(file_path, 'rb') as file:
        paths = pickle.load(file)
    return paths


########### Utilities:  functions on cells 
#All of these seem silly


def silly_ones_snake_line(cell):
    xcount=cell.count("x")

    onecount=cell.count("1")

    #here I do not cut out more cells in the larger twist case 
    return xcount/onecount-0.33

def ones_count(my_string):
    count = 0
    for char in my_string:
        if char == "1":
            count += 1
        else:
            break 
    return count

def lk_count(string):    
    sub_string="0101x"
    count = 0
    sub_len = len(sub_string)
    for i in range(len(string) - sub_len + 1):
        if string[i:i + sub_len] == sub_string:
            count += 1
    return count


def snake_count(string):    
    sub_string="x0011x101011"
    count = 0
    sub_len = len(sub_string)
    for i in range(len(string) - sub_len + 1):
        if string[i:i + sub_len] == sub_string:
            count += 1
    return count



def double_cut_index(enh_word):
    for i in range(len(enh_word)-1):
        if(i%3==2):
            if((enh_word[i]=="0" or enh_word[i]=="x") and (enh_word[i+1]=="0" or enh_word[i+1]=="x") ):
                return i
    #special case at the end            
    i=len(enh_word)-1
    if (enh_word[i]=="0" or enh_word[i]=="x") and (enh_word[i-2]=="0" or enh_word[i-2]=="x"):
        return i
    return 1000


#Twist adding functors on cells

def add_lk(cell):
    return(cell.replace("x0101x","x0101xx0101x",1))

def add_snake(cell):
    snake_pattern="101011x0011x"
    cod_cell=cell.replace(snake_pattern,2*snake_pattern,1)
    return cod_cell

def lk_to_triple(triple):
    if triple[2]<len(triple[0])-6:
        return (add_lk(triple[0]),add_lk(triple[1]),triple[2])
    else:
        return (add_lk(triple[0]),add_lk(triple[1]),triple[2]+6)
    

########### Utilities:  functions on paths


def remove_dups_sort(l):
    return sorted(list(set(l)))

def one_zero_diff_index(start_string,end_string):
    #print(start_string)
    #print(end_string)
    for i in range(len(start_string)):
        s_char=start_string[i]
        e_char=end_string[i]
        #print("")
        #print(s_char)
        #print(e_char)
        
        start_is_zero=True
        end_is_zero=True
        if(s_char=="1" or s_char=="X" or s_char=="Y"):
            start_is_zero=False
        if(e_char=="1" or e_char=="X" or e_char=="Y"):
            end_is_zero=False
        
        if (start_is_zero and (not end_is_zero)) or ((not(start_is_zero)) and end_is_zero):
            return i 

def first_L(path):
    return one_zero_diff_index(path[0],path[1])

def qdeg_diffs_and_Ls_from_path(path):
    list_of_Ls=list()

    for i in range(len(path)-1):
        current_word=path[i]
        next_word=path[i+1]
        qdiff=qdeg_of_word("a",next_word)-qdeg_of_word("a",current_word)
        if qdiff>0:
            list_of_Ls.append(str(one_zero_diff_index(current_word,next_word))+" Q: "+str(qdiff))
        else:
            list_of_Ls.append(one_zero_diff_index(path[i],path[i+1]))
    return list_of_Ls


def list_of_Ls_from_path(path):
    list_of_Ls=list()

    for i in range(len(path)-1):
        current_word=path[i]
        next_word=path[i+1]
        #qdiff=qdeg_of_word("a",next_word)-qdeg_of_word("a",current_word)
        list_of_Ls.append(one_zero_diff_index(path[i],path[i+1]))
    return list_of_Ls

    #return sorted(list(set_of_Ls))

def sign_of_path(path):
    length_term=(len(path)-1)/2
    if length_term%2==0:
        length_term=1
    else:
        length_term=-1
    
    def count_characters_in_string(mystring):
        count_1 = mystring.count("1")
        count_X = mystring.count("X")
        count_Y = mystring.count("Y")
    
        return count_1+ count_X+ count_Y

    total_ones_before_L_s=0
    list_of_Ls=list_of_Ls_from_path(path)

    for i in range(len(path)-1):
        current_L=list_of_Ls[i]
        current_word=path[i]
        ones_before_L_s=count_characters_in_string(current_word[:current_L])

        #print(ones_before_L_s)
        total_ones_before_L_s+=ones_before_L_s
    
    if(total_ones_before_L_s%2==0):
        return length_term
    else:
        return -length_term











"""
def qdeg_diffs_and_Ls_from_path(path):
    list_of_Ls=list()

    for i in range(len(path)-1):
        current_word=path[i][0]
        next_word=path[i+1][0]
        qdiff=qdeg_of_word("a",next_word)-qdeg_of_word("a",current_word)
        if qdiff>0:
            list_of_Ls.append(str(one_zero_diff_index(current_word,next_word))+" Q: "+str(qdiff))
        else:
            list_of_Ls.append(one_zero_diff_index(path[i][0],path[i+1][0]))
    return list_of_Ls


def list_of_Ls_from_path(path):
    list_of_Ls=list()

    for i in range(len(path)-1):
        current_word=path[i][0]
        next_word=path[i+1][0]
        #qdiff=qdeg_of_word("a",next_word)-qdeg_of_word("a",current_word)
        list_of_Ls.append(one_zero_diff_index(path[i][0],path[i+1][0]))
    return list_of_Ls

    #return sorted(list(set_of_Ls))

def sign_of_path(path):
    length_term=(len(path)-1)/2
    if length_term%2==0:
        length_term=1
    else:
        length_term=-1
    
    def count_characters_in_string(mystring):
        count_1 = mystring.count("1")
        count_X = mystring.count("X")
        count_Y = mystring.count("Y")
    
        return count_1+ count_X+ count_Y

    total_ones_before_L_s=0
    list_of_Ls=list_of_Ls_from_path(path)

    for i in range(len(path)-1):
        current_L=list_of_Ls[i]
        current_word=path[i][0]
        ones_before_L_s=count_characters_in_string(current_word[:current_L])

        #print(ones_before_L_s)
        total_ones_before_L_s+=ones_before_L_s
    
    if(total_ones_before_L_s%2==0):
        return length_term
    else:
        return -length_term
"""

def sign_string(sign):
    if sign==1:
        return "+"
    if sign==-1:
        return "-"



def sorter(array):
    
    if(array==None):
            return ("Z",-1000)
    # Sort by lexicographic order of the last element
    last_element = (array[-1])[0]
    #print(last_element)
    # Get the integer value from the "first_L" function
    first_L_value =(list_of_Ls_from_path(array))[0]  
    #print(first_L_value)
    return (last_element, first_L_value)


def arrange_paths_from_cell(paths_from_cell):

    sorted_arrays = sorted(paths_from_cell, key=sorter)
    return sorted_arrays


def dom_cod_first_L_to_paths_dict(paths):
    #works with new path convention
    dictionary=dict()
    for cell in paths.keys():
        paths_from_cell=paths[cell]
        for path in paths_from_cell:
            triple=(path[0],path[-1],first_L(path))
            if triple in dictionary.keys():
                dictionary[triple].append(path)
            else:
                dictionary[triple]=[path]
    
    #consider sorting here

    return dictionary

def dom_cod_noL_path_dict(paths):
    dictionary=dict()
    for cell in paths.keys():
        paths_from_cell=paths[cell]
        for path in paths_from_cell:
            pair=(path[0],path[-1])
            if pair in dictionary.keys():
                dictionary[pair].append(path)
            else:
                dictionary[pair]=[path]
    return dictionary


def print_path(path):
    print(sign_string((sign_of_path(path)))+"  "+path[0]+" "+path[-1]+"  "+str(qdeg_diffs_and_Ls_from_path(path)))



























#### Conjectural path generation for lk:


def lk_path_x01_L1_diff_end(list_of_Ls):
    new_array=[]
    for i in range(2):
        new_array.append(list_of_Ls[i]+6)
    for i in range(len(list_of_Ls)):
        new_array.append(list_of_Ls[i])
    for i in range(-2,0,1):
        new_array.append(list_of_Ls[i]+6)
    return new_array

def lk_path_x01_L1_same_end(list_of_Ls):
    arrays=([],[],[],[])
    for arr in arrays:    
        for i in range(4):
            arr.append(list_of_Ls[i]+6)

    for i in range(2,len(list_of_Ls)-2):
        arrays[0].append(list_of_Ls[i])
    for i in range(0,len(list_of_Ls)-0):
        arrays[1].append(list_of_Ls[i])
    for i in range(0,len(list_of_Ls)-0):
        arrays[2].append(list_of_Ls[i])
    
    #fourth one    
    for i in range(0,2):
        arrays[3].append(list_of_Ls[i]+2)

    for i in range(0,len(list_of_Ls)-0):
        arrays[3].append(list_of_Ls[i])
    
    for i in range(len(list_of_Ls)-2,len(list_of_Ls)-0):
        arrays[3].append(list_of_Ls[i]+2)



    for arr in arrays:    
        for i in range(-2,0,1):
            arr.append(list_of_Ls[i]+6)
    return arrays

def lk2_path_x01_L1_same_end(list_of_Ls):
    new_array=[]
    for i in range(4):
        new_array.append(list_of_Ls[i]+12)
    for i in range(2,4):
        new_array.append(list_of_Ls[i]+7)
    for i in range(2):
        new_array.append(list_of_Ls[i]+2)
    for i in range(len(list_of_Ls)):
        new_array.append(list_of_Ls[i])
    
    for i in range(-2,0,1):
        new_array.append(list_of_Ls[i]+2)
    
    for i in range(-2,0,1):
        new_array.append(list_of_Ls[i]+12)
   
    return new_array







def lk2_path_x01_L2(list_of_Ls):
    #print(list_of_Ls)
    new_array=[]
    for i in range(8):
        new_array.append(list_of_Ls[i]+12)
    for i in range(len(list_of_Ls)):
        new_array.append(list_of_Ls[i])
    for i in range(-4,0,1):
        new_array.append(list_of_Ls[i]+12)
    return new_array



def lk_path_x01_L2(list_of_Ls):
    arrays=([],[],[],[])
    for arr in arrays:    
        for i in range(8):
            arr.append(list_of_Ls[i]+6)

    for i in range(6,len(list_of_Ls)-4):
        arrays[0].append(list_of_Ls[i])
    for i in range(4,len(list_of_Ls)-2):
        arrays[1].append(list_of_Ls[i])
    for i in range(4,len(list_of_Ls)-2):
        arrays[2].append(list_of_Ls[i])
    for i in range(2,len(list_of_Ls)-0):
        arrays[3].append(list_of_Ls[i])
    
    for arr in arrays:    
        for i in range(-4,0,1):
            arr.append(list_of_Ls[i]+6)
    return arrays


def lk_path_x01_L3(list_of_Ls):
    arrays=([],[],[],[])
    for arr in arrays:    
        for i in range(2):
            arr.append(list_of_Ls[i]+6)
    
    arrays[1].append(list_of_Ls[0]+2)
    arrays[1].append(list_of_Ls[0]+3)

    arrays[2].append(list_of_Ls[0]+2)
    arrays[2].append(list_of_Ls[0]+3)
    
    arrays[3].append(list_of_Ls[0]+4)
    arrays[3].append(list_of_Ls[0]+5)
    arrays[3].append(list_of_Ls[0]+2)
    arrays[3].append(list_of_Ls[0]+3)

    
    for arr in arrays:    
        for i in range(len(list_of_Ls)):
            arr.append(list_of_Ls[i])
    
    arrays[1].append(list_of_Ls[0]+2)
    arrays[1].append(list_of_Ls[0]+3)

    arrays[2].append(list_of_Ls[0]+2)
    arrays[2].append(list_of_Ls[0]+3)
    
    arrays[3].append(list_of_Ls[0]+2)
    arrays[3].append(list_of_Ls[0]+3)
    arrays[3].append(list_of_Ls[0]+4)
    arrays[3].append(list_of_Ls[0]+5)
    
    return arrays

def lk2_path_x01_L3(list_of_Ls):
    arr=[]

    f=list_of_Ls[0]

    arr.append(f+12)
    arr.append(f+12)
    arr.append(f+7)
    arr.append(f+7)
    arr.append(f+4)
    arr.append(f+5)
    arr.append(f+2)
    arr.append(f+3)

    arr=arr+list_of_Ls
    
    arr.append(f+2)
    arr.append(f+3)
    arr.append(f+4)
    arr.append(f+5)
    
    return arr

def lk_path_01x_L2(list_of_Ls):
    arrays=([],[],[],[])
    for arr in arrays:    
        for i in range(6):
            arr.append(list_of_Ls[i]+6)

    for i in range(4,len(list_of_Ls)-4):
        arrays[0].append(list_of_Ls[i])
    for i in range(2,len(list_of_Ls)-2):
        arrays[1].append(list_of_Ls[i])
    for i in range(2,len(list_of_Ls)-2):
        arrays[2].append(list_of_Ls[i])
    for i in range(0,len(list_of_Ls)-0):
        arrays[3].append(list_of_Ls[i])
    
    for arr in arrays:    
        for i in range(-4,0,1):
            arr.append(list_of_Ls[i]+6)
    return arrays

def lk2_path_01x_L2(list_of_Ls):
    arr=[]

    f=list_of_Ls[0]
    
    for i in range(6):
        arr.append(list_of_Ls[i]+12)
    
    arr.append(f+3)
    arr.append(f+3)

    arr=arr+list_of_Ls
    
    for i in range(-4,0,1):
        arr.append(list_of_Ls[i]+12)
    return arr


def conj_lk_paths(orig_triple, orig_path_dict, lk_triple,lk_path_dict):
    paths=orig_path_dict[orig_triple]
    
    conj_array=[]

    word_endsx01=False
    if orig_triple[0].endswith("x01"):
        word_endsx01=True
    word_ends01x=False
    if orig_triple[0].endswith("01x"):
        word_ends01x=True
    filterL=len(orig_triple[0])-orig_triple[2]-1
    
    
    if (word_endsx01,filterL)==(True,1):
        
        #split cases on whether codomain has same or different ending
        if(orig_triple[1].endswith("01x")):
            for path in paths:
                conj_array.append(lk_path_x01_L1_diff_end(lk_path_x01_L1_diff_end(list_of_Ls_from_path(path))))

        else:
            for path in orig_path_dict[orig_triple]:
                #print(len(list_of_Ls_from_path(path)))

                conj_array.append(lk2_path_x01_L1_same_end(list_of_Ls_from_path(path))) 


                #print(len(conj_array[-1]))



            for path in lk_path_dict[lk_triple]:
                conj_paths=lk_path_x01_L1_same_end(list_of_Ls_from_path(path))
                for arr in conj_paths:
                    conj_array.append(arr)
            




        return conj_array
    
    
    elif (word_endsx01,filterL)==(True,2):
        
        for path in orig_path_dict[orig_triple]:
            conj_array.append(lk2_path_x01_L2(list_of_Ls_from_path(path))) 
        for path in lk_path_dict[lk_triple]:
            conj_paths=lk_path_x01_L2(list_of_Ls_from_path(path))
            for arr in conj_paths:
                conj_array.append(arr)
        return conj_array

    elif (word_endsx01,filterL)==(True,3):
        for path in orig_path_dict[orig_triple]:
            conj_array.append(lk2_path_x01_L3(list_of_Ls_from_path(path))) 
        
        for path in lk_path_dict[lk_triple]:
            conj_paths=lk_path_x01_L3(list_of_Ls_from_path(path))
            for arr in conj_paths:
                conj_array.append(arr)

        return conj_array
    elif word_endsx01==True and filterL>6:
        for path in paths:
            conj_array.append(list_of_Ls_from_path(path))
        return conj_array
    
    if (word_ends01x,filterL)==(True,0):
        ##Magically this is the same as ends x01 L3 
        #Due to lazyness, I just copied that
        
        for path in orig_path_dict[orig_triple]:
            conj_array.append(lk2_path_x01_L3(list_of_Ls_from_path(path))) 
        
        for path in lk_path_dict[lk_triple]:
            conj_paths=lk_path_x01_L3(list_of_Ls_from_path(path))
            for arr in conj_paths:
                conj_array.append(arr)

        return conj_array

    elif (word_ends01x,filterL)==(True,2):
        for path in orig_path_dict[orig_triple]:
            conj_array.append(lk2_path_01x_L2(list_of_Ls_from_path(path))) 
        
        for path in lk_path_dict[lk_triple]:
            conj_paths=lk_path_01x_L2(list_of_Ls_from_path(path))
            for arr in conj_paths:
                conj_array.append(arr)

        return conj_array
    elif (word_ends01x,filterL)==(True,4):
        
        #magically these are same as ends x01 L1 diff end
        for path in paths:
            conj_array.append(lk_path_x01_L1_diff_end(lk_path_x01_L1_diff_end(list_of_Ls_from_path(path))))


        return conj_array
    elif word_ends01x==True and filterL>6:
        for path in paths:
            conj_array.append(list_of_Ls_from_path(path))        
        return conj_array


    print("something is strange")






























############## Analysis/tests



def cell__bijection_testing():

    domain_twistcount=40
    codomain_twistcount=domain_twistcount+4

    domain_cells=load_cells(domain_twistcount)
    codomain_cells=load_cells(codomain_twistcount)

    dom_braid=domain_twistcount*"abc"
    cod_braid=codomain_twistcount*"abc"

    min_hdeg_dom=100000
    max_hdeg_dom=-100000
    min_qdeg_dom=100000
    max_qdeg_dom=-100000

    for cell in domain_cells:
        min_hdeg_dom=min(min_hdeg_dom,hdeg_of_word(dom_braid,cell))
        min_qdeg_dom=min(min_qdeg_dom,qdeg_of_word(dom_braid,cell))

        max_hdeg_dom=max(max_hdeg_dom,hdeg_of_word(dom_braid,cell))
        max_qdeg_dom=max(max_qdeg_dom,qdeg_of_word(dom_braid,cell))

    min_hdeg_cod=100000
    max_hdeg_cod=-100000
    min_qdeg_cod=100000
    max_qdeg_cod=-100000

    for cell in codomain_cells:
        min_hdeg_cod=min(min_hdeg_cod,hdeg_of_word(cod_braid,cell))
        min_qdeg_cod=min(min_qdeg_cod,qdeg_of_word(cod_braid,cell))

        max_hdeg_cod=max(max_hdeg_cod,hdeg_of_word(cod_braid,cell))
        max_qdeg_cod=max(max_qdeg_cod,qdeg_of_word(cod_braid,cell))

    #print(min_hdeg_dom)
    #print(max_hdeg_dom)
    #print(min_qdeg_dom)
    #print(max_qdeg_dom)

    #print(min_hdeg_cod)
    #print(max_hdeg_cod)

    #print(len(domain_cells))

 
    ################Adding ones map bijection

    #Specifying the dom and cod of the map

    ones_margin_of_error=2

    testing_min_h=-(3/2)*domain_twistcount+ones_margin_of_error
    ones_dom_cells=set()

    for cell in domain_cells:
        if hdeg_of_word(dom_braid,cell)>=testing_min_h:
            ones_dom_cells.add(cell)

    ones_cod_cells=set()
    for cell in codomain_cells:
        if hdeg_of_word(cod_braid,cell)>=testing_min_h:
            ones_cod_cells.add(cell)

    #check that the injective map is actually a well defined function
    for cell in ones_dom_cells:
        if not "111111111111"+cell in ones_cod_cells:
            print("halp")

    #check that the set are of the same size (hence the map is surjection)
    if len(ones_dom_cells)!=len(ones_cod_cells):
        print("halphalp")
    
    #for cell in ones_dom_cells:
    #    print(cell)


    ##############Adding lion king map bijection
    #the addition map ads 1111xxxx0000 characters in some clever way
    
    """
    number_of_chars=21
    last_chars_dom=set()

    for cell in domain_cells:
        last_chars_dom.add(cell[-number_of_chars:])

    last_chars_cod=set()

    for cell in codomain_cells:
        last_chars_cod.add(cell[-number_of_chars:])

    print(len(last_chars_dom))
    print(len(last_chars_cod))

    #last_char_list=sorted(list(last_chars_dom))
    #for word in last_char_list:
    #    print(word)

    #for string in last_chars_dom:
    #    print(string)
    
    """
    lk_margin_of_error=3

    #Rather than this silly definition, we should define dom and cod here with qdeg and hdeg

    lk_dom_cells=set()

    for cell in domain_cells:
        #h=hdeg_of_word(dom_braid,cell)
        #q=qdeg_of_word(dom_braid,cell)

        "x0101x"

        #snake_rel=silly_ones_snake_line(cell)

        #print(h,q,snake_rel)
        #if "x0101x" in cell:
        #    lk_dom_cells.add(cell)
        if qdeg_of_word(dom_braid,cell)+lk_margin_of_error<= -3*domain_twistcount +(4/3)*hdeg_of_word(dom_braid,cell)+2 :
            lk_dom_cells.add(cell)

    lk_cod_cells=set()

    for cell in codomain_cells:
        #h=hdeg_of_word(dom_braid,cell)
        #q=qdeg_of_word(dom_braid,cell)

        #snake_rel=silly_ones_snake_line(cell)

        #print(h,q,snake_rel)
        #if "x0101xx0101xx0101x" in cell:
        #    lk_cod_cells.add(cell)
        if qdeg_of_word(cod_braid,cell)+lk_margin_of_error<= -3*codomain_twistcount +(4/3)*hdeg_of_word(cod_braid,cell)+(2/3)-8+8: 
            #This is a guessed formula which did not match my paper calculations.
            #my paper calculations did not have the last +8
            #my inductive proof calculations arrived to the above formula. Hence it should be correct and I can use it
            lk_cod_cells.add(cell)

    #print(lk)

    #check for well defined map
    for cell in lk_dom_cells:
        #print(cell)
        mapped_cell=cell.replace("x0101x","x0101xx0101xx0101x",1)
        if not (mapped_cell in lk_cod_cells):
            print("halp2")
             

    #check that the set are of the same size (hence the map is surjection)
    if len(lk_dom_cells)!=len(lk_cod_cells):
        print("halphalp2")
        

    #print(len(lk_dom_cells))
    #print(len(lk_cod_cells))

    """
    a=0
    for cell in lk_dom_cells:
        if not "x0101x" in cell:
            a=a+1
            print(cell)

    print(a)

    b=0
    for cell in lk_cod_cells:
        if not "x0101xx0101xx0101x" in cell:
            b=b+1
            print(cell)

    print(b)
    """

    ############ Adding snake bijection
    snake_dom_cells=set()
    snake_cod_cells=set()

    snake_margin_or_error=-5
    #this is mad margin of error. When I will have more accurate cell classification, this can also become better

    snake_pattern="x0011x101011"
    
    for cell in domain_cells:
        if qdeg_of_word(dom_braid,cell)-snake_margin_or_error>= -3*domain_twistcount +(3/2)*hdeg_of_word(dom_braid,cell)+12:
            snake_dom_cells.add(cell)
    

    for cell in snake_dom_cells:
        if not(snake_pattern in cell):
            print(cell)

    for cell in codomain_cells:
        if qdeg_of_word(cod_braid,cell)-snake_margin_or_error>= -3*codomain_twistcount +(3/2)*hdeg_of_word(cod_braid,cell)+13:
            snake_cod_cells.add(cell)
    

    

    
    """
    #silly definitions
    for cell in domain_cells:
        if snake_pattern in cell:
            snake_dom_cells.add(cell)
    
    for cell in codomain_cells:
        if (snake_pattern+snake_pattern) in cell:
            snake_cod_cells.add(cell)
    """
    
    #check for well defined map
    for cell in snake_dom_cells:
        mapped_cell=cell.replace(snake_pattern,snake_pattern+snake_pattern,1)
        if not (mapped_cell in snake_cod_cells):
            print("halp3")

    #check that the set are of the same size (hence the map is surjection)
    if len(snake_dom_cells)!=len(snake_cod_cells):
        print("halphalp3")
    
    print(len(snake_dom_cells))
    print(len(snake_cod_cells))

    #print(len(ones_cod_cells))
    #print(len(snake_cod_cells))
    #print(len(lk_cod_cells))


    cod_union=ones_cod_cells.union(snake_cod_cells.union(lk_cod_cells))
    print(len (cod_union))
    print(len(codomain_cells))

    #for cell in codomain_cells:
    #    if cell not in cod_union:
    #        print((hdeg_of_word(cod_braid,cell),qdeg_of_word(cod_braid,cell)))

    #print(cod_union==codomain_cells)

    #Specifying the dom and cod of the map

    #print(len(ones_dom_cells))
    #print(len(ones_cod_cells))

    #print(len(domain_cells))


def path_testing():
    twistnumber=9
    #twistnumber 3 there are examples of non minimal complexes


    braid=twistnumber*"abc"
    paths=load_paths(twistnumber)
    unmatched_cells=paths.keys()
    #print(type(unmatched_cells))
    #print(len(unmatched_cells))

    #sillydefs
    ones=set()
    lk=set()
    snake=set()

    ones_pattern="111111"
    #lk_pattern="x0101x"
    #lk_pattern="01xx0101xx0101xx0101xx01"
    #lk_pattern="01xx0101xx0101xx0101x"
    
    #lk_pattern="x0101xx0101xx0101xx01011"
    
    
    lk_pattern="11000101xx0101xx0101xx0101x"#x01"
    #11000101xx0101xx0101xx0101xx01 cell is decent for lk 10 twist
    

    #lk_pattern="11111000101xx0101xx0101xx0101x"
    #11111000101xx0101xx0101xx0101x  cell is quite interesting for lk twist 10
    
    
    #lk_pattern="11000101xx0101xx0101xx0101xx01"
    #11111000101xx0101xx0101xx0101x  cell is quite interesting for lk twist 10


    #snake_pattern="101011x0011x"
    #snake_pattern="11x101011x0011x10"
    #snake_pattern="11x101011x0011x101011x00"

    #snake_pattern="00011x101011x0011x101011x10"
    snake_pattern="00011x101011x0011x101011x0011x"

    #cell 00011x101011x0011x101011x0011x  is interesting for snake 10 twist


    for cell in unmatched_cells:
        if ones_pattern in cell:
            ones.add(cell)
        if lk_pattern in cell:
            lk.add(cell)
        if snake_pattern in cell:
            snake.add(cell)

    
    #print(len(ones))
    #print(len(lk))
    #print(len(snake))

   # differences=set()
    last_end_vertex=None
    last_cell=None
    a=0
    cumulative_sign=0

    same_dom_cod_count=0
    max_cum_sign=0

    for cell in lk:  
        paths_from_cell=paths[cell]
        paths_from_cell=sorted(paths_from_cell, key=lambda arr: arr[-1])
        #print(len(paths_from_cell))
        for i in range(len(paths_from_cell)):
            path=paths_from_cell[i]            
            end_vertex=(path[len(path)-1])[0]
            first_L=(path[len(path)-1])[1]
            
            #diff_tuple=(ones_count(end_vertex)-ones_count(cell),snake_count(end_vertex)-snake_count(cell),lk_count(end_vertex)-lk_count(cell))
            
            sign=(sign_of_path(path))

            if((end_vertex!=last_end_vertex or cell != last_cell)):
                if(i>0):
                    print("number of paths above: "+str(same_dom_cod_count))
                    print("their cumulative sign: "+str(cumulative_sign))
                    max_cum_sign=max(max_cum_sign,abs(cumulative_sign))
                print("")
                cumulative_sign=0
                same_dom_cod_count=0
            same_dom_cod_count+=1
            last_end_vertex=end_vertex
            last_cell=cell
            cumulative_sign+=sign
            

            qdiff=(qdeg_of_word(braid,end_vertex)-qdeg_of_word(braid,cell))
            
            a=max(a,qdiff)
            print(cell+" "+end_vertex+"  "+str(qdeg_diffs_and_Ls_from_path(path)))
            #print(sign_of_path(path))

            #dc_diff=double_cut_index(end_vertex)-double_cut_index(cell)
            #print(dc_diff)
            #printing=False
            
            
            #print(str(qdiff)+"  "+cell+" "+end_vertex+"  "+str(list_of_Ls_from_path(path)))
            #if(qdeg_of_word(braid,end_vertex)-qdeg_of_word(braid,cell)==3):
            #    print(cell+" "+end_vertex+"  "+str(list_of_Ls_from_path(path)))



            #print(len(path))
            
            #if(printing):
            #for p in path:
            #    print(p[0])
            #print(path)

            #differences.add(diff_tuple)
            
            
            
            
            #if(diff_tuple[0]==9):
            #    print(cell+"      "+ end_vertex)

            #print(diff_tuple)
            
            #print(end_vertex)
        #print(same_dom_cod_count)
    
    print(max_cum_sign)
    #print(a)

    #print(paths)
    #for a in differences:
    #    print(a)
    
    #print(len(differences))

def forbidden_structures_testing():
    twistnumber=12
    paths=load_new_T4_paths(twistnumber)

    teststring="y00x"

    for critcell in paths:
        for path in paths[critcell]:
            for vertex in path:
                for i in range(len(vertex)-len(teststring)):
                    if vertex[i:i+len(teststring)]==teststring:
                        #print(vertex[i:(len(vertex))])
                        #print(vertex)
                        if not ("y" in vertex[i:(len(vertex))]):
                            print(vertex)
                
                
                
                #if teststring in vertex:
                    #print(path)
                #    print(vertex)


def path_dom_cod_pairs_testing():
    twistnumber=44
    unmatched_cells=load_cells(twistnumber)
    
    braid=twistnumber*"abc"

    crossings=3*twistnumber

    dcs=set()
    max_ones_diff=0    


    #two_doms=False

    for dom in unmatched_cells:
        dom_hdeg=hdeg_of_word(braid,dom)
        dom_qdeg=qdeg_of_word(braid,dom)
        #if "x0101xx0101xx0101x" in dom:
        #    continue

        #count=0
        for cod in unmatched_cells:
            cod_hdeg=hdeg_of_word(braid,cod)
            cod_qdeg=qdeg_of_word(braid,cod)

            if (cod_hdeg!=dom_hdeg+1) or (cod_qdeg<dom_qdeg):
                continue
            if ones_count(cod)<ones_count(dom):
                continue

            dc1=double_cut_index(dom)
            dc2=double_cut_index(cod)
            dcdiff=0
            if(dc1!=1000 and dc2!=1000):
                dcdiff=dc2-dc1

            dcs.add(dcdiff)

            ones_diff=ones_count(cod)-ones_count(dom)
            max_ones_diff=max(max_ones_diff,ones_diff)

            #if ones_diff==15:
            #    print(dom)
            #    print(cod)

            qdiff=cod_qdeg-dom_qdeg
            #if qdiff>=0:
            #    count+=1
            
            if qdiff>3:
                print(str(qdiff)+"  "+ str(ones_count(dom)%3)+"   "+str(ones_count(cod)-ones_count(dom)) +"   "+dom+"   "+cod)
                
                #if(two_doms):
                #    print("asdasd")

                #two_doms=True
        #two_doms=False

        #print(count)
    #print(max_ones_diff)
    print(dcs)

def snake_functoriality_testing():

    domain_twistcount=6
    codomain_twistcount=domain_twistcount+4

    domain_paths=load_paths(domain_twistcount)
    codomain_paths=load_paths(codomain_twistcount)

    dom_braid=domain_twistcount*"abc"
    cod_braid=codomain_twistcount*"abc"

    snake_pattern="101011x0011x"


    dom_snake=set()
    for cell in domain_paths:
        if snake_pattern in cell:
            dom_snake.add(cell)
    
    cod_snake=set()
    for cell in codomain_paths:
        if (2*snake_pattern) in cell:
            cod_snake.add(cell)



    for cell in dom_snake:  
        cod_cell=cell.replace(snake_pattern,2*snake_pattern,1)
        
        dom_paths_from_cell=domain_paths[cell]  
        #dom_paths_from_cell=sorted(dom_paths_from_cell, key=lambda arr: arr[-1])
        dom_paths_from_cell=arrange_paths_from_cell(dom_paths_from_cell)


        cod_paths_from_cell=codomain_paths[cod_cell]        
        #cod_paths_from_cell=sorted(cod_paths_from_cell, key=lambda arr: arr[-1])
        cod_paths_from_cell=arrange_paths_from_cell(cod_paths_from_cell)


        number_of_dom_paths=0
        for i in range(len(dom_paths_from_cell)):
            dom_path=dom_paths_from_cell[i]            
            dom_end_vertex=(dom_path[len(dom_path)-1])[0]
            if not dom_end_vertex in dom_snake:
                continue
            
            number_of_dom_paths+=1

        print("cell in domain: "+cell+" number of paths from it: " +str(number_of_dom_paths))

        number_of_cod_paths=0
        for i in range(len(cod_paths_from_cell)):
            cod_path=cod_paths_from_cell[i]            
            cod_end_vertex=(cod_path[len(cod_path)-1])[0]
            if not cod_end_vertex in cod_snake:
                continue
            
            number_of_cod_paths+=1

        #print("cod"+str(number_of_cod_paths)+"  " +cod_cell)
        #print("")
        
 
        if number_of_dom_paths!=number_of_cod_paths or True:
            print("dom")
            for i in range(len(dom_paths_from_cell)):
                dom_path=dom_paths_from_cell[i]            
                dom_end_vertex=(dom_path[len(dom_path)-1])[0]
                if not dom_end_vertex in dom_snake:
                    continue
                print(str(sign_of_path(dom_path))+"  "+cell+" "+dom_end_vertex+"  "+str(qdeg_diffs_and_Ls_from_path(dom_path)))
                
                


            print("cod:")
            for i in range(len(cod_paths_from_cell)):
                cod_path=cod_paths_from_cell[i]            
                cod_end_vertex=(cod_path[len(cod_path)-1])[0]
                if not cod_end_vertex in cod_snake:
                    continue
                print(str(sign_of_path(cod_path))+"   "+cod_cell+" "+cod_end_vertex+"  "+str(qdeg_diffs_and_Ls_from_path(cod_path)))

        print("")


def lk_functoriality_testing():
    domain_twistcount=8
    codomain_twistcount=domain_twistcount+2

    domain_paths=load_paths(domain_twistcount)
    codomain_paths=load_paths(codomain_twistcount)

    dom_braid=domain_twistcount*"abc"
    cod_braid=codomain_twistcount*"abc"

    lk_pattern="x0101x"


    dom_lk=set()
    for cell in domain_paths:
        #if 2*lk_pattern in cell:
        if cell.endswith(lk_pattern):
            dom_lk.add(cell)

    
    cod_lk=set()
    for cell in codomain_paths:
        #if (3*lk_pattern) in cell:
        if cell.endswith(2*lk_pattern):
            cod_lk.add(cell)

    for dom_cell in dom_lk:  
        #cod_cell=dom_cell.replace(2*lk_pattern,3*lk_pattern,1)
        cod_cell=dom_cell.replace(lk_pattern,2*lk_pattern,1)
        

        dom_paths_from_cell=domain_paths[dom_cell]        
        #dom_paths_from_cell=sorted(dom_paths_from_cell, key=lambda arr: arr[-1])
        dom_paths_from_cell=arrange_paths_from_cell(dom_paths_from_cell)

        cod_paths_from_cell=codomain_paths[cod_cell]        
        #cod_paths_from_cell=sorted(cod_paths_from_cell, key=lambda arr: arr[-1])
        cod_paths_from_cell=arrange_paths_from_cell(cod_paths_from_cell)

        number_of_dom_paths=0
        for i in range(len(dom_paths_from_cell)):
            dom_path=dom_paths_from_cell[i]            
            dom_end_vertex=(dom_path[len(dom_path)-1])[0]
            if not dom_end_vertex in dom_lk:
                continue
            
            number_of_dom_paths+=1


        print("cell in domain: "+dom_cell+" number of paths from it: " +str(number_of_dom_paths))

        


        number_of_cod_paths=0
        for i in range(len(cod_paths_from_cell)):
            cod_path=cod_paths_from_cell[i]            
            cod_end_vertex=(cod_path[len(cod_path)-1])[0]
            if not cod_end_vertex in cod_lk:
                continue
            
            number_of_cod_paths+=1
        print("cell in codomain: "+cod_cell+" number of paths from it: " +str(number_of_cod_paths)) #This might be misleading as it counts also pairs which are not in the between the functored stuff
        #print("cod"+str(number_of_cod_paths)+"  " +cod_cell)
        #print("")

        similar_cod_L_count=1
        last_array=None

        

        if number_of_dom_paths!=number_of_cod_paths or True:
            print("dom:")
            for i in range(len(dom_paths_from_cell)):
                dom_path=dom_paths_from_cell[i]            
                dom_end_vertex=(dom_path[len(dom_path)-1])[0]
                if not dom_end_vertex in dom_lk:
                    continue
                
                if sorter(dom_path)[0]==sorter(last_array)[0]:
                    similar_cod_L_count+=1
                else:
                    print(similar_cod_L_count)
                    similar_cod_L_count=1
                last_array=dom_path
                print(sign_string((sign_of_path(dom_path)))+"  "+dom_cell+" "+dom_end_vertex+"  "+str(qdeg_diffs_and_Ls_from_path(dom_path)))
                
                

                
            #last_array=None
            print("cod:")
            for i in range(len(cod_paths_from_cell)):
                cod_path=cod_paths_from_cell[i]            
                cod_end_vertex=(cod_path[len(cod_path)-1])[0]
                if not cod_end_vertex in cod_lk:
                    continue
                
                if (sorter(cod_path))[0]==(sorter(last_array))[0] and (sorter(cod_path))[1]==(sorter(last_array))[1]:
                    similar_cod_L_count+=1
                else:
                    print(similar_cod_L_count)
                    similar_cod_L_count=0
                last_array=cod_path
                
                print(sign_string((sign_of_path(cod_path)))+"   "+cod_cell+" "+cod_end_vertex+"  "+str(qdeg_diffs_and_Ls_from_path(cod_path)))
                
                #print(sorter(cod_path))

                
                
        print("")


def new_lk_functoriality_testing():
    #test first with adding a single lk
    
    #domain and codomain of paths and functors are mixed up here
    
    orig_twistcount=8
    lk_twistcount=orig_twistcount+2
    lk2_twistcount=orig_twistcount+4

    orig_paths=load_new_T4_paths(orig_twistcount)
    orig_path_dict=dom_cod_first_L_to_paths_dict(orig_paths)
    #orig_path_dict=dom_cod_noL_path_dict(orig_paths)


    lk_paths=load_new_T4_paths(lk_twistcount)
    lk_path_dict=dom_cod_first_L_to_paths_dict(lk_paths)
    #lk_path_dict=dom_cod_noL_to_path_dict(lk_paths)
    

    lk2_paths=load_new_T4_paths(lk2_twistcount)
    lk2_path_dict=dom_cod_first_L_to_paths_dict(lk2_paths)
    #lk2_path_dict=dom_cod_noL_to_path_dict(lk_paths)
    

    orig_braid=orig_twistcount*"abc"
    lk_braid=lk_twistcount*"abc"
    lk2_braid=lk2_twistcount*"abc"

    lk_pattern="x0101xx0101x"

    #Options: Allow the following through:
    endsx01_L1=True     #ok  
    endsx01_L2=True     #ok
    endsx01_L3=True     #ok
    endsx01_lowL=False   #ok
    
    ends01x_L0=False     #ok
    ends01x_L2=False     #ok
    ends01x_L4=False     #ok      
    ends01x_lowL=False   #ok
    
    #Print paths:
    print_paths=True




    succcount=0
    failcount=0
    triplescount=0
    unfiltered=0


    for orig_triple in orig_path_dict:

        ### Filter non-lk cells out
        if not((lk_pattern) in orig_triple[0] and (lk_pattern) in orig_triple[1]):
            continue

        triplescount+=1
        
        #Based on options, filter out paths
        word_endsx01=False
        if orig_triple[0].endswith("x01"):
            word_endsx01=True

        word_ends01x=False
        if orig_triple[0].endswith("01x"):
            word_ends01x=True
        
        filterL=len(orig_triple[0])-orig_triple[2]-1

        if (word_endsx01,filterL)==(True,1) and  not endsx01_L1:
            continue
        elif (word_endsx01,filterL)==(True,2) and  not endsx01_L2:
            continue
        elif (word_endsx01,filterL)==(True,3) and  not endsx01_L3:
            continue
        elif word_endsx01==True and filterL>6 and not endsx01_lowL:
            continue

        if (word_ends01x,filterL)==(True,0) and  not ends01x_L0:
            continue
        elif (word_ends01x,filterL)==(True,2) and  not ends01x_L2:
            continue
        elif (word_ends01x,filterL)==(True,4) and  not ends01x_L4:
            continue
        elif word_ends01x==True and filterL>6 and not ends01x_lowL:
            continue

        unfiltered+=1


        ### Original
        print("")
        print("Original: "+str(orig_triple))
        orig_cum_sign=0
        for path in orig_path_dict[orig_triple]:
            orig_cum_sign+=sign_of_path(path)
        print("number of paths:                                            "+str(len(orig_path_dict[orig_triple])))
        print("their cumulative sign: "+str(orig_cum_sign))

        if print_paths:
            for path in orig_path_dict[orig_triple]:
                #print(path)
                print_path(path)
        
        ###LK

        #lk_triple=(add_lk(orig_triple[0]),add_lk(orig_triple[1]),orig_triple[2]+6)
        lk_triple=lk_to_triple(orig_triple)


        lk_adds_L6=False
        if lk_triple[2]!=orig_triple[2]:
            lk_adds_L6=True    
        #print("LK with first_L -> +6")
        
        lk_cum_sign=0
        for path in lk_path_dict[lk_triple]:
            lk_cum_sign+=sign_of_path(path)
        print("number of paths:                                         "+str(len(lk_path_dict[lk_triple])))
        print("their cumulative sign: "+str(lk_cum_sign))
        if print_paths:
            for path in lk_path_dict[lk_triple]:
                print_path(path)
        


        """
        if lk_triple in lk_path_dict.keys():
            lk_adds_L6=True    
            print("LK with first_L -> +6")
            lk_cum_sign=0
            for path in lk_path_dict[lk_triple]:
                lk_cum_sign+=sign_of_path(path)
            print("number of paths:                                         "+str(len(lk_path_dict[lk_triple])))
            print("their cumulative sign: "+str(lk_cum_sign))

            if print_paths:
                for path in lk_path_dict[lk_triple]:
                    print_path(path)
        else:
            print("LK with first_L -> +0")
            lk_triple=(lk_triple[0],lk_triple[1],lk_triple[2]-6)
            lk_cum_sign=0
            for path in lk_path_dict[lk_triple]:
                lk_cum_sign+=sign_of_path(path)
            if print_paths:
                for path in lk_path_dict[lk_triple]:
                    print_path(path)

            print("number of paths:                                          "+str(len(lk_path_dict[lk_triple])))
            print("their cumulative sign: "+str(lk_cum_sign))
        """
        

        ###LK2
        
        #lk2_triple=(add_lk(add_lk(orig_triple[0])),add_lk(add_lk(orig_triple[1])),orig_triple[2]+12)
        lk2_triple=lk_to_triple(lk_triple)
        
        lk2_cum_sign=0
        for path in lk2_path_dict[lk2_triple]:
            lk2_cum_sign+=sign_of_path(path)
        print("number of paths:                                          "+str(len(lk2_path_dict[lk2_triple])))
        print("their cumulative sign: "+str(lk2_cum_sign))
        if print_paths:
            for path in lk2_path_dict[lk2_triple]:
                print_path(path)



        """
        if lk2_triple in lk2_path_dict.keys():
            print("LK2 with first_L -> +12")
            lk2_cum_sign=0
            for path in lk2_path_dict[lk2_triple]:
                lk2_cum_sign+=sign_of_path(path)
            print("number of paths:                                          "+str(len(lk2_path_dict[lk2_triple])))
            print("their cumulative sign: "+str(lk2_cum_sign))

            if print_paths:
                for path in lk2_path_dict[lk2_triple]:
                    print_path(path)
        else:
            print("LK2 with first_L -> +0")
            lk2_triple=(lk2_triple[0],lk2_triple[1],lk2_triple[2]-12)
            lk2_cum_sign=0
            for path in lk2_path_dict[lk2_triple]:
                lk2_cum_sign+=sign_of_path(path)
            if print_paths:
                for path in lk2_path_dict[lk2_triple]:
                    print_path(path)

            print("number of paths:                                           "+str(len(lk2_path_dict[lk2_triple])))
            print("their cumulative sign: "+str(lk2_cum_sign))
        """    

        ### Trying to guess LK2 from Orig and LK
        actual_array_of_lk2=[]
        
        for path in lk2_path_dict[lk2_triple]:
            actual_array_of_lk2.append(list_of_Ls_from_path(path))

        """
        if lk_adds_L6:
            lk2_triple=(add_lk(add_lk(orig_triple[0])),add_lk(add_lk(orig_triple[1])),orig_triple[2]+12)
            for path in lk2_path_dict[lk2_triple]:
                actual_array_of_lk2.append(list_of_Ls_from_path(path))
        else:
            lk2_triple=(add_lk(add_lk(orig_triple[0])),add_lk(add_lk(orig_triple[1])),orig_triple[2]+0)
            for path in lk2_path_dict[lk2_triple]:
                actual_array_of_lk2.append(list_of_Ls_from_path(path))
        """

        conj_array_of_lk2=[]

        conj_array_of_lk2=conj_lk_paths(orig_triple,orig_path_dict,lk_triple,lk_path_dict)
        #print(conj_array_of_lk2)

        """
        if lk_adds_L6:
            for path in orig_path_dict[orig_triple]:
                conj_array_of_lk2.append(conj_lk2_path(list_of_Ls_from_path(path)))
            
            lk_triple=(add_lk(orig_triple[0]),add_lk(orig_triple[1]),orig_triple[2]+6)
            for path in lk_path_dict[lk_triple]:
                conj_paths=conj_lk_paths(list_of_Ls_from_path(path))
                for arr in conj_paths:
                    conj_array_of_lk2.append(arr)
        else:
            for path in orig_path_dict[orig_triple]:
                conj_array_of_lk2.append(list_of_Ls_from_path(path))
        """

        """
        
        samecount=0
        allcount=0
        for i in range(len(sorted(actual_array_of_lk2))):
            allcount+=1
            if sorted(actual_array_of_lk2)[i]==sorted(conj_array_of_lk2)[i]:
                samecount+=1 
                
            else:
                pass
                #print("")
                #print(sorted(conj_array_of_lk2)[i])
                #print(sorted(actual_array_of_lk2)[i])

        print("countssaasdsad")
        print(samecount)
        print(allcount)
        """



        """
        diff_values=set()
        diff_index=1000000
        previous_L_list=actual_array_of_lk2[0]
        for L_list in actual_array_of_lk2:
            index=10000000000
            for i in range(len(L_list)):
                if i>=len(previous_L_list):
                    index=i
                    break
                elif L_list[i]!=previous_L_list[i]:
                    index=i 
                    break
            if index<diff_index:
                diff_values=set()
                #print("asd")
                #print(diff_values)
                diff_values.add(L_list[index])
                diff_values.add(previous_L_list[index])
                diff_index=index
            elif diff_index==index: 
                diff_values.add(L_list[index])

        print(diff_index)
        print(diff_values)
        """


        if sorted(actual_array_of_lk2)==sorted(conj_array_of_lk2):
            succcount+=1
            print("succeeded")
        else:
            print("failed")
            failcount+=1
    print("")
    print("successes :" +str(succcount))
    print("fails :"+ str(failcount))
    print("filtered: "+ str(triplescount-unfiltered))






def unmatched_cells_generation_testing():


    ones_cells=set()
    ones_cells.add("")
    
    snake_cells=set()
    lk_cells=set()

    ready_cells=set()

    ones_cap=110
    lk_cap=round(ones_cap/2)
    snake_cap=round(lk_cap/2)

    #ones_cap=1
    #lk_cap=1
    #snake_cap=1



    added=set()
    for word in ones_cells:
        for i in range(ones_cap):
            added.add(word+(i*"111"))
    ones_cells=added

    for word in ones_cells:
        ready_cells.add(word)
        ready_cells.add(word+"000")
        snake_cells.add(word+"00011x")
        lk_cells.add(word+"00011x001")

        ready_cells.add(word+"001")
        ready_cells.add(word+"010")
        ready_cells.add(word+"011")
        
        ready_cells.add(word+"100")
        lk_cells.add(word+"100001")
        
        snake_cells.add(word+"100")
        snake_cells.add(word)

        ready_cells.add(word+"110")
        #lk_cells.add(word+"101011")
        lk_cells.add(word+"110001")
        snake_cells.add(word+"110")

    added=set()
    for word in snake_cells:
        for i in range(snake_cap):
            added.add(word+(i*"101011x0011x"))
    
    snake_cells=added

    for word in snake_cells:
        ready_cells.add(word)
        lk_cells.add(word+"101011x0011x001")
        
        ready_cells.add(word+"101")
        ready_cells.add(word+"101010")

        ready_cells.add(word+"101011")
        lk_cells.add(word+"101010x01")

        ready_cells.add(word+"101011x00")
        ready_cells.add(word+"101011x10")
        ready_cells.add(word+"101011x11")

        ready_cells.add(word+"101011x01")

    for word in lk_cells:
        for i in range(lk_cap):
            ready_cells.add(word+(i*"01xx01"))

            ready_cells.add(word+(i*"01xx01")+"01x")


    """
    
    #Printing stuff:
    #ready_cells.add("11111111111100000000xxxx")
    glue_triples=set()
    for word in ready_cells:
        xcount=word.count("x")
        onecount=word.count("1")
        triple=(onecount,xcount,len(word))
        glue_triples.add(triple)
    
    glue_triples=sorted(list(glue_triples))
    for triple in glue_triples:
        print(triple)
        print(triple[0]/(-3)-triple[1]+triple[2]/3)
    """
    
    #Saving the generated critical cells into a file
    twistcount=71
    # ones count should be a bit, say 5, higher than twistcount 
    generated_cells=set()
    for word in ready_cells:
        if len(word)==3*twistcount:
            generated_cells.add(word)

    file_path="Torus4braid_paths/"+str(twistcount)+"synthetic_cells.pkl"
    if os.path.exists(file_path):
        pass
    else:      
        with open(file_path, 'wb') as file:
            pickle.dump(generated_cells, file)



    """
    #Testing against the real critical cells
                
    testnum=44

    generated_cells=set()
    for word in ready_cells:
        if len(word)==3*testnum:
            generated_cells.add(word)

    
    
    true_cells=load_cells(testnum)
    print("numb of generateds"+str(len(generated_cells)))
    print("numb of true"+ str(len(true_cells)))
    if generated_cells==true_cells:
        print("yeyye")

    print("generated but not truly critical")
    for word in generated_cells:
        if not word in true_cells:
            print(word)
    print("critical but not generated")
    for word in true_cells:
        if not word in generated_cells:
            print(word)
    """



def noL_lk_functoriality_testing():
    orig_twistcount=8
    lk2_twistcount=orig_twistcount+4

    orig_paths=load_new_T4_paths(orig_twistcount)
    #orig_path_dict=dom_cod_first_L_to_paths_dict(orig_paths)
    orig_path_dict=dom_cod_noL_path_dict(orig_paths)

    lk2_paths=load_new_T4_paths(lk2_twistcount)
    #sn_L_path_dict=dom_cod_first_L_to_paths_dict(sn_paths)
    lk2_path_dict=dom_cod_noL_path_dict(lk2_paths)

    #print(orig_paths)

    print_paths=False
    lk_pattern="x0101xx0101x"


    for orig_triple in orig_path_dict:

        ### Filter non-lk cells out
        if not((lk_pattern) in orig_triple[0] and (lk_pattern) in orig_triple[1]):
            continue


        ### Original
        print("")
        print("Original: "+str(orig_triple))
        orig_cum_sign=0
        for path in orig_path_dict[orig_triple]:
            orig_cum_sign+=sign_of_path(path)
        print("number of paths:                                            "+str(len(orig_path_dict[orig_triple])))
        print("their cumulative sign: "+str(orig_cum_sign))

        if print_paths:
            for path in orig_path_dict[orig_triple]:
                print(path)
                print_path(path)
        


        ###LK2
        lk2_dom=orig_triple[0].replace("x0101x","x0101xx0101xx0101x",1)
        lk2_cod=orig_triple[1].replace("x0101x","x0101xx0101xx0101x",1)



        #lk2_triple=(add_lk(add_lk(orig_triple[0])),add_lk(add_lk(orig_triple[1])),orig_triple[2]+12)
        #lk2_triple=lk_to_triple(lk_triple)
        lk2_triple=(lk2_dom,lk2_cod)

        lk2_cum_sign=0
        for path in lk2_path_dict[lk2_triple]:
            lk2_cum_sign+=sign_of_path(path)
        print("number of paths:                                          "+str(len(lk2_path_dict[lk2_triple])))
        print("their cumulative sign: "+str(lk2_cum_sign))
        if print_paths:
            for path in lk2_path_dict[lk2_triple]:
                print_path(path)




def new_snake_functoriality_testing():
    orig_twistcount=8
    sn_twistcount=orig_twistcount+4

    orig_paths=load_new_T4_paths(orig_twistcount)
    orig_path_dict=dom_cod_first_L_to_paths_dict(orig_paths)
    orig_noL_path_dict=dom_cod_noL_path_dict(orig_paths)

    sn_paths=load_new_T4_paths(sn_twistcount)
    sn_L_path_dict=dom_cod_first_L_to_paths_dict(sn_paths)
    sn_noL_path_dict=dom_cod_noL_path_dict(sn_paths)

    orig_braid=orig_twistcount*"abc"
    sn_braid=sn_twistcount*"abc"

    sn_pattern="101011x0011x"
    #sn_pattern="10101011x0011x"
    
    
    """
    for orig_triple in orig_path_dict:
        ### Filter bad ones out
        if not((sn_pattern) in orig_triple[0] and (sn_pattern) in orig_triple[1]):
            continue

        #if orig_triple[2]==20:
        #    continue
        
        #if orig_triple[0].endswith("01x") or orig_triple[1].endswith("01x"):
        #    continue

        #Filter to look at only a specific one
        #if orig_triple != ('11000101xx0101xx0101xx01', '11100011x00101xx0101xx01', 21):
        #    continue

        
        ### Original
        print("")
        print("Original: "+str(orig_triple))
        orig_cum_sign=0
        #for path in orig_path_dict[orig_triple]:
        #    orig_cum_sign+=sign_of_path(path)
        print("number of paths:                                            "+str(len(orig_path_dict[orig_triple])))
        print("their cumulative sign: "+str(orig_cum_sign))

        #for path in orig_path_dict[orig_triple]:
        #    print_path(path)

        ###LK
        sn_triple=(add_snake(orig_triple[0]),add_snake(orig_triple[1]),orig_triple[2]+12)

        sn_adds_L12=False
        

        if sn_triple in sn_L_path_dict.keys():
            sn_adds_L12=True    
            print("sn with first_L -> +12")
            sn_cum_sign=0
            for path in sn_L_path_dict[sn_triple]:
                sn_cum_sign+=sign_of_path(path)
            print("number of paths:                                         "+str(len(sn_L_path_dict[sn_triple])))
            print("their cumulative sign: "+str(sn_cum_sign))

            #for path in sn_L_path_dict[sn_triple]:
            #    print_path(path)
        else:
            print("sn with first_L -> +0")
            sn_triple=(sn_triple[0],sn_triple[1],sn_triple[2]-12)
            sn_cum_sign=0
            #for path in sn_L_path_dict[sn_triple]:
            #    sn_cum_sign+=sign_of_path(path)
            print("number of paths:                                          "+str(len(sn_L_path_dict[sn_triple])))
            print("their cumulative sign: "+str(sn_cum_sign))

    """
    for orig_pair in orig_noL_path_dict.keys():
        ### Filter bad ones out
        if not((sn_pattern) in orig_pair[0] and (sn_pattern) in orig_pair[1]):
            continue
        
        
        ### Original
        print("")
        print("Original: "+str(orig_pair))
        orig_cum_sign=0
        orig_L_array=[]
        for path in orig_noL_path_dict[orig_pair]:
            orig_cum_sign+=sign_of_path(path)
            orig_L_array.append(first_L(path))
        print("number of paths:                                            "+str(len(orig_noL_path_dict[orig_pair])))
        print("their cumulative sign: "+str(orig_cum_sign))
        print("L_array: "+str(orig_L_array))

        #for path in orig_path_dict[orig_triple]:
        #    print_path(path)
        
        ### Snake
        sn_pair=(add_snake(orig_pair[0]),add_snake(orig_pair[1]))
        sn_L_array=[]
        sn_cum_sign=0
        for path in sn_noL_path_dict[sn_pair]:
            sn_cum_sign+=sign_of_path(path)
            sn_L_array.append(first_L(path))
        print("number of paths:                                            "+str(len(sn_noL_path_dict[sn_pair])))
        print("their cumulative sign: "+str(sn_cum_sign))
        print("L_array: "+str(sn_L_array))

def lk_start_L_testing():
    paths=load_new_T4_paths(12)

    for cell in paths:
        if not ("x0101xx0101x" in cell):
            continue
        print(cell)
        firstLs_set=set()

        for path in paths[cell]:
            firstLs_set.add(first_L(path))
        
        print(firstLs_set)
        print("")

def inequalities_testing():
    
    def f_lk(word):
        m=0
        #higher fails
        
        O=word.count("1")
        X=word.count("x")
        L=len(word)

        return O/2 +(3/2)*X -L/2+m


    def f_ones(word):
        m=-1
        #higher fails
        
        O=word.count("1")
        X=word.count("x")
        L=len(word)

        return O +X -(2*L)/3+m
    
    def f_snake(word):
        m=-2.5 
        #higher fails

        O=word.count("1")
        X=word.count("x")
        L=len(word)

        return -(O/2 +X -L/2-m)
    
    def g_lk(word):
        m=-2
        #higher seems to fail

        # in some formulation, this m was -m
        
        O=word.count("1")
        X=word.count("x")
        L=len(word)
        
        return L/2 - O+m

    for twistnumber in range(30):
        cells=load_cells(twistnumber)
        """
        for cell in cells:
            #print(str(cell.count("01xx01"))+"    "+str(f_lk(cell)))
            #if f_lk(cell)>0:
            #    print(cell)
            
            #the -0.01 is for floating point fuckery
            if f_lk(cell)-0.01>cell.count("01xx01"):
                print(cell)
                print(f_lk(cell))
        
        
        for cell in cells:
            #if f_snake(cell)>0:
            #    print(cell)
            #print(str(cell.count("101011x0011x"))+"    "+str(f_snake(cell)))
            
            #print(cell)
            #print(f_snake(cell))
            if f_snake(cell)-0.01>cell.count("101011x0011x"):
                print(cell)
                print(f_snake(cell))
        

        for cell in cells:
            #print(str(cell.count("111"))+"    "+str(f_ones(cell)))
            #if f_ones(cell)>0:
            #    print(cell)
            if f_ones(cell)-0.01>cell.count("111"):
                print(cell)
                print(f_ones(cell))

        """


        for cell in cells:

            #print(str(cell.count("01xx01"))+"    "+str(g_lk(cell)))

            if g_lk(cell)-0.01>cell.count("01xx01"):
                print(cell)
                print(g_lk(cell))






    



def qdeg_up_testing():
    
    for i in range(25):
        cells=load_cells(i)

        for cella in cells:
            oa=cella.count("1")
            xa=cella.count("x")
            odega=count_starting_ones(cella)

            for cellb in cells:
                ob=cellb.count("1")
                xb=cellb.count("x")
                odegb=count_starting_ones(cellb)
                
                if oa+1==ob and odega<=odegb and xa>xb+2:

                    print("halp")
                
                
def top_homology_testing():
    braid=12*"abc"
    paths=load_new_T4_paths(12)
    path_dict=dom_cod_first_L_to_paths_dict(paths)
    """
    for cell in paths:
        if qdeg_of_word(braid,cell)==-66 and hdeg_of_word(braid,cell)==-22:
            print(cell)
            print(len(paths[cell]))
            #print(paths[cell])
            for path in paths[cell]:
                print_path(path)
    """
    for triple in path_dict:
        if qdeg_of_word(braid,triple[0])==-66 and hdeg_of_word(braid,triple[0])==-22:
            print(triple[0])
            print(len(path_dict[triple]))
            #print(paths[cell])
            for path in path_dict[triple]:
                print_path(path)


def main():

    #unmatched_cells_generation_testing()
    #cell__bijection_testing()
    #path_testing()
    #path_dom_cod_pairs_testing()
    #snake_functoriality_testing()
    #lk_functoriality_testing()
    
    #new_lk_functoriality_testing()

    top_homology_testing()
    
    
    #new_snake_functoriality_testing()

    
    #noL_lk_functoriality_testing()

    #lk_start_L_testing()

    #forbidden_structures_testing()
    #inequalities_testing()
    #qdeg_up_testing()
    """
    twistnumber=1
    file_path="Torus4braid_paths/snake1twist.pkl"
    paths=None
    with open(file_path, 'rb') as file:
        paths = pickle.load(file)
    print(paths)
    """

    """
    paths=load_new_T4_paths(3)
    path_dict=dom_cod_first_L_to_paths_dict(paths)
    for a in path_dict:
        print("")
        print(a)
        print(path_dict[a])
    """

if __name__ == "__main__":
    main()


