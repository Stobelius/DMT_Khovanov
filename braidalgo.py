import pickle
import sys
import time
import os
from collections import deque
import argparse


negative_braid=False #global boolean variable which is set at the end of the file
#Some optimation is done only for negative braids

################## Utilities for geometry inside a single smoothing

def number_of_strands(word):
    word=word.lower()
    alphabet_chars = [char for char in word if char.isalpha()]
    if alphabet_chars:
        return ord(max(alphabet_chars))-ord('a')+2
    else:
        print("bad characters on the braidword")
        return None

def x_position_of_crossing(braid_word,y_pos):
    char=braid_word[y_pos]
    return ord(char.lower())-ord('a')

def crossing_is_negative(braid_word,y_pos):
    char=braid_word[y_pos]
    if(char==char.lower()):
        return True
    return False
        
def smoothing_northeast_is_Vert(position,braid_word,enhanced_word):
    xcoord=x_position_of_crossing(braid_word, position[1])
    negative_crossing=crossing_is_negative(braid_word,position[1])
    
    
    zero_smoothing=False
    if(enhanced_word[position[1]]=="0" or enhanced_word[position[1]]=="x" or enhanced_word[position[1]]=="y"):
        zero_smoothing=True  
    
    if(xcoord==position[0] and zero_smoothing and negative_crossing):
        return True
    if(xcoord==position[0] and (not zero_smoothing) and (not negative_crossing)):
        return True
    return False

def out_of_bounds(position, braid_word):
    if(position[0]<0 or position[0]> number_of_strands(braid_word)-1 or position[1]<=0 or position[1]>= len(braid_word)):
       return True
    return False
    
        
def next_step_in_smoothing(current_pos, previous_pos, braid_word, enh_word):
    previous_direction=(current_pos[0]-previous_pos[0],current_pos[1]-previous_pos[1])
    
    smoothing_ne_is_Vert=smoothing_northeast_is_Vert((current_pos[0],current_pos[1]),braid_word,enh_word)
    smoothing_nw_is_Vert=smoothing_northeast_is_Vert((current_pos[0]-1,current_pos[1]),braid_word,enh_word)
    smoothing_se_is_Vert=smoothing_northeast_is_Vert((current_pos[0],current_pos[1]-1),braid_word,enh_word)
    smoothing_sw_is_Vert=smoothing_northeast_is_Vert((current_pos[0]-1,current_pos[1]-1),braid_word,enh_word)
    

    if(previous_direction==(0,1)):
        if(smoothing_ne_is_Vert):
            return (current_pos[0]+1,current_pos[1])
        elif(smoothing_nw_is_Vert):
            return (current_pos[0]-1,current_pos[1])
        else:
            return (current_pos[0],current_pos[1]+1)

    if(previous_direction==(0,-1)):
        if(smoothing_se_is_Vert):
            return (current_pos[0]+1,current_pos[1])
        elif(smoothing_sw_is_Vert):
            return (current_pos[0]-1,current_pos[1])
        else:
            return (current_pos[0],current_pos[1]-1)
    
    if(previous_direction==(1,0)):
        if(smoothing_nw_is_Vert and smoothing_sw_is_Vert):
            return (current_pos[0]-1,current_pos[1])
        elif(smoothing_nw_is_Vert and not smoothing_se_is_Vert):
            return (current_pos[0],current_pos[1]-1)
        elif(smoothing_sw_is_Vert and not smoothing_ne_is_Vert):
            return (current_pos[0],current_pos[1]+1)        
        else:
            return (current_pos[0]+1,current_pos[1])        

    if(previous_direction==(-1,0)):
        if(smoothing_ne_is_Vert and smoothing_se_is_Vert):
            return (current_pos[0]+1,current_pos[1])
        elif(smoothing_ne_is_Vert and not smoothing_sw_is_Vert):
            return (current_pos[0],current_pos[1]-1)
        elif(smoothing_se_is_Vert and not smoothing_nw_is_Vert):
            return (current_pos[0],current_pos[1]+1)        
        else:
            return (current_pos[0]-1,current_pos[1]) 
        
    print("wierd stuff with prev and next position when searching for loops")
    return(-1,-1)



def array_of_positions_from_edge(start_pos,next_pos,braid_word,enh_word):
    position_list=[start_pos,next_pos]
    if out_of_bounds( next_pos,braid_word):
        return position_list
    
    while(True):
        index=len(position_list)
        lead_pos=next_step_in_smoothing(position_list[index-1], position_list[index-2], braid_word, enh_word)
        
        position_list.append(lead_pos)
        
        if(lead_pos==start_pos):
            return position_list
        elif(out_of_bounds(lead_pos,braid_word)):
            return position_list





def there_is_loop_starting_from_edge2(start_pos,next_pos,braid_word,enh_word):
    potential_loop=array_of_positions_from_edge(start_pos,next_pos,braid_word,enh_word)
    if(potential_loop[len(potential_loop)-1]==potential_loop[0]):
        return True
    return False




def smoothing_of_last_crossing_created_loop(braid_word,enh_word):
  
    y_pos=len(braid_word) -1
    if(y_pos==0):
        return False
    
    x_pos=x_position_of_crossing(braid_word,y_pos)
    position=(x_pos,y_pos)
    
    
    if(not smoothing_northeast_is_Vert(position,braid_word,enh_word)):
        return False
    if(there_is_loop_starting_from_edge2(position,(x_pos+1,y_pos),braid_word,enh_word)):
        return True
    
    return False

############## Generation of all enhanced words without matching

def generate_next_enhanced_words(set_of_enh_words,concatenated_braid_word):
    
    if(len(set_of_enh_words)==0):
        return {"0","1"}
    
    appending_index=len(next(iter(set_of_enh_words)))-1
    
    
    new_words=set()
    
    for enh_word in set_of_enh_words:
        if(smoothing_of_last_crossing_created_loop(concatenated_braid_word,enh_word+"0")):
            new_words.add(enh_word+"x")
            new_words.add(enh_word + "y")
            #print("asdasdasd")
        else:
            new_words.add(enh_word+"0")
        
        if(smoothing_of_last_crossing_created_loop(concatenated_braid_word,enh_word+"1")):
            new_words.add(enh_word+ "X")
            new_words.add(enh_word+"Y")
        else:
            new_words.add(enh_word +"1")
    
    return new_words
    
def generate_all_enhanced_words(braid_word):
    all_enhanced_words={}
    
    
    for i in range(len(braid_word)):
        
        #print("asd")
        all_enhanced_words=generate_next_enhanced_words(all_enhanced_words,braid_word[:(i+1)])  
        
        print(braid_word[:i+1])
        #print(all_enhanced_words)  
        
    return all_enhanced_words


################## String utilities for matching the cells

def count_starting_ones(my_string):
    count = 0
    for char in my_string:
        if char == "1":
            count += 1
        else:
            break 
    return count

    
def replace_char(string,index,char):
    changed=string[:index] + char + string[index+1:]
    return changed    
    
def remove_xy_coding_from_char(enh_word, index):
    if(enh_word[index]=="x" or enh_word[index]=="y"):
        changed=enh_word[:index] + "0" + enh_word[index+1:]
        return changed
    elif(enh_word[index]=="X" or enh_word[index]=="Y"):
        changed=enh_word[:index] + "1" + enh_word[index+1:]
        return changed
    return enh_word
    
def put_x_coding_to_char(enh_word,index):
    if(enh_word[index]=="0" or enh_word[index]=="y"):
        changed=enh_word[:index] + "x" + enh_word[index+1:]
        return changed
    elif(enh_word[index]=="1" or enh_word[index]=="Y"):
        changed=enh_word[:index] + "X" + enh_word[index+1:]
        return changed
    return enh_word

def put_y_coding_to_char(enh_word,index):
    if(enh_word[index]=="0" or enh_word[index]=="x"):
        changed=enh_word[:index] + "y" + enh_word[index+1:]
        return changed
    elif(enh_word[index]=="1" or enh_word[index]=="X"):
        changed=enh_word[:index] + "Y" + enh_word[index+1:]
        return changed
    return enh_word
    

def highest_and_decoration_of_component(position_array,enh_word):
    if(not(position_array[0]==position_array[len(position_array)-1])):
        return (-10,None)
    highest=highest_ycoord_of_loop(position_array)
    decoration=(enh_word[highest]).lower()
    return (highest,decoration)
    

def highest_ycoord_of_loop(position_array):
    maximum=-10
    for pos in position_array:
        maximum=max(maximum,pos[1])
    return maximum


################ Matching a cell and generating all unmatched cells

def isopair(braid_word,enh_word,L,u):

    #speedhack for negative braids
    if(negative_braid and L<count_starting_ones(enh_word)):
        return None
    


    enh_at_L_is_0_or_lowercase=False
    if(enh_word[L]=="0" or enh_word[L]=="x"or enh_word[L]=="y"):
        enh_at_L_is_0_or_lowercase=True
     
    Lx=x_position_of_crossing(braid_word,L)
    Ly=L
    L_is_vert=smoothing_northeast_is_Vert((Lx,Ly),braid_word,enh_word)
    
    
    L_edge1=((Lx,Ly),(Lx+1,Ly))
    L_edge2=((Lx,Ly+1),(Lx+1,Ly+1))
    
    if(not L_is_vert):
        L_edge1=((Lx,Ly),(Lx,Ly+1))
        L_edge2=((Lx+1,Ly),(Lx+1,Ly+1))
    
    component1=array_of_positions_from_edge(L_edge1[0],L_edge1[1],braid_word,enh_word)    
    
    component1_is_loop=False
    if(component1[0]==component1[len(component1)-1]):
            component1_is_loop=True
    
    two_components_exist=False
    if(not(L_edge2[0] in component1)):
        if(component1_is_loop):
            two_components_exist=True    
        else:
            reverse_direction_comp1=array_of_positions_from_edge(L_edge1[1],L_edge1[0],braid_word,enh_word)
            if(not(L_edge2[0] in reverse_direction_comp1)):
                two_components_exist=True
    
    
    ##### look into rev-merge and split here
    
    if( not two_components_exist):
        prelim_word=None
        if(enh_at_L_is_0_or_lowercase):
            prelim_word=replace_char(enh_word, L ,"1")
        else:
            prelim_word=replace_char(enh_word, L ,"0")
        
        prelim_comp1=array_of_positions_from_edge(L_edge1[0],L_edge2[0],braid_word,prelim_word)
        prelim_comp2=array_of_positions_from_edge(L_edge1[1],L_edge2[1],braid_word,prelim_word)
        
        comp1_high_dec=highest_and_decoration_of_component(prelim_comp1,prelim_word)
        comp2_high_dec=highest_and_decoration_of_component(prelim_comp2,prelim_word)
        
        u_comp=None
        u_comp_h_d=None
        other_comp=None
        other_comp_h_d=None
        
        if(comp1_high_dec[0]==u):
            u_comp=prelim_comp1
            u_comp_h_d=comp1_high_dec
            other_comp=prelim_comp2
            other_comp_h_d=comp2_high_dec
        elif(comp2_high_dec[0]==u):
            u_comp=prelim_comp2
            u_comp_h_d=comp2_high_dec
            other_comp=prelim_comp1
            other_comp_h_d=comp1_high_dec
        else:
            #did not find isomorphism with u
            return (None)
            
        other_comp_is_loop=True
        if(other_comp_h_d[0]==-10):
            other_comp_is_loop=False
        
        u_comp_is_lower=True
        if(other_comp_is_loop and other_comp_h_d[0]<u_comp_h_d[0]):
            u_comp_is_lower=False
            
        orig_component_h_d=highest_and_decoration_of_component(component1,enh_word)
        
        #### look for split
        if(enh_at_L_is_0_or_lowercase):
            
            #split from non-loop
            if(not other_comp_is_loop):
                matched = put_x_coding_to_char(prelim_word,u)           
                return(matched)
            
            #split from higher loop
            if(u_comp_is_lower):
                matched = put_x_coding_to_char(prelim_word,u)
                return(matched)
            
            #split from lower loop with x (we do not allow for these as they will be matched away previously in the final recursive definition of M)
            if(orig_component_h_d[1]=="x"):
                return(None)
            
            #split from lower loop with y                
            matched = put_y_coding_to_char(prelim_word,other_comp_h_d[0])
            matched = put_x_coding_to_char(matched,u_comp_h_d[0])
            #print("wierd split up is found, one that I would expect to only see in reducible braids")
            return(matched)
        
        #### look for rev-merge
        if(not enh_at_L_is_0_or_lowercase):
            
            #rev-merge from non-loop
            if(not other_comp_is_loop):
                matched = put_y_coding_to_char(prelim_word,u)           
                return(matched)
            
            #rev-merge from higher loop
            if(u_comp_is_lower):
                matched = put_y_coding_to_char(prelim_word,u)
                return(matched)
            
            #rev-merge from lower loop with y (we do not allow for these as they will be matched away previously in the final recursive definition of M)
            if(orig_component_h_d[1]=="y"):
                return(None)
            
            #rev-merge from lower loop with x                
            matched = put_x_coding_to_char(prelim_word,other_comp_h_d[0])
            matched = put_y_coding_to_char(matched,u_comp_h_d[0])
            #print("wierd revmerge up is found, one that I would expect to only see in reducible braids")
            #print(enh_word +"   "+ matched)
            return(matched)
            
    ##### look for merge and rev-split here
    
    if(two_components_exist):
        component2=array_of_positions_from_edge(L_edge2[0],L_edge2[1],braid_word,enh_word)
        
        component2_is_loop=False
        if(component2[0]==component2[len(component2)-1]):
            component2_is_loop=True
        
        #find saddle morphism
        if((not component1_is_loop) and (not component2_is_loop)):
            return (None)
        
        comp1_high_dec=highest_and_decoration_of_component(component1,enh_word)
        comp2_high_dec=highest_and_decoration_of_component(component2,enh_word)
        
        u_comp=None
        u_comp_h_d=None
        other_comp=None
        other_comp_h_d=None
        
        if(comp1_high_dec[0]==u):
            u_comp=component1
            u_comp_h_d=comp1_high_dec
            other_comp=component2
            other_comp_h_d=comp2_high_dec
        elif(comp2_high_dec[0]==u):
            u_comp=component2
            u_comp_h_d=comp2_high_dec
            other_comp=component1
            other_comp_h_d=comp1_high_dec
        else:
            #did not find isomorphism with u
            return (None)
            
        other_comp_is_loop=True
        if(other_comp_h_d[0]==-10):
            other_comp_is_loop=False
        
        u_comp_is_lower=True
        if(other_comp_is_loop and other_comp_h_d[0]<u_comp_h_d[0]):
            u_comp_is_lower=False
        
        
        ### look for merge
        if(enh_at_L_is_0_or_lowercase and u_comp_h_d[1]=="y"):
            
            ##merge to non-loop
            if(not other_comp_is_loop):
                matched = remove_xy_coding_from_char(enh_word,u)           
                matched = replace_char(matched, L ,"1")
                return(matched)
            
            ## merge to higher loop
            if(u_comp_is_lower):
                matched = remove_xy_coding_from_char(enh_word,u)           
                matched = replace_char(matched, L ,"1")
                return(matched)
            
            ## merge to a lower loop with y (we do not allow for these as they will be matched away previously in the final recursive definition of M)
            if(other_comp_h_d[1]=="y"):
                return (None)
            
            ## merge to lower loop with x
            matched = remove_xy_coding_from_char(enh_word,other_comp_h_d[0])           
            matched = replace_char(matched, L ,"1")
            matched = put_x_coding_to_char(matched,u)
            #print("wierd merge-up is found, one that I would expect to only see in reducible braids")
            return(matched)
               
        #look for rev-split
        if((not enh_at_L_is_0_or_lowercase) and u_comp_h_d[1]=="x"):
            
            ##rev-split to non-loop
            if(not other_comp_is_loop):
                matched = remove_xy_coding_from_char(enh_word,u)           
                matched = replace_char(matched, L ,"0")
                return(matched)
            
            ##rev-split to higher loop
            if(u_comp_is_lower):
                matched = remove_xy_coding_from_char(enh_word,u)           
                matched = replace_char(matched, L ,"0")
                return(matched)
            
            ## rev-split to a lower loop with x (we do not allow for these as they will be matched away previously in the final recursive definition of M)
            if(other_comp_h_d[1]=="x"):
                return (None)
            
            ## rev-split to lower loop with y
            matched = remove_xy_coding_from_char(enh_word,other_comp_h_d[0])           
            matched = replace_char(matched, L ,"0")
            matched = put_y_coding_to_char(matched,u)
            #print("wierd rev-split is found, one that I would expect to only see in reducible braids")
            return(matched)
    
    return (None)

def concatenated_isopair(braid_word,enh_word,L,u):
    #used in finding paths. Concatenates the input for mattching_a_cell

    concatenated_match=isopair(braid_word[:(u+1)],enh_word[:(u+1)],L,u)

    if concatenated_match==None:
        return None
    matching=concatenated_match+enh_word[(u+1):len(enh_word)]
    #print(matching)
    return matching




#def generate_words_and_possible_matching_list(set_of_enh_words, concatenated_braid_word):





def remove_L_u_matched_words_from_set(set_of_enh_words,braid_word,L,u):
    remaining_words=set()
    #print(set_of_enh_words)
    
    
    # A possible big time-improvement:
    # Check whether a matching could be possible by glancing at whether some unmatched cell with different L exist in set_of_enh_words.
    # In other words, do a prior quick check before running the slow isopair function
    while(len(set_of_enh_words)>0):
        word=set_of_enh_words.pop()

        potential_match=isopair(braid_word,word,L,u)
        if(potential_match==None):
            remaining_words.add(word)
        elif(potential_match in set_of_enh_words):
            set_of_enh_words.remove(potential_match)
            #######Code can be inserted here to see, what kind of arrows are matched in certain braids
            
            #if(L<u-4):
            #    print(str(L) + "asd " +str(u))
            #    print(word)
            #    print(potential_match)
            #    print("")
        else:
            remaining_words.add(word)
            
    return remaining_words

   
def generate_next_unmatched_words(set_of_enh_words, concatenated_braid_word):
    if(len(concatenated_braid_word)==1):
        return {"0","1"}
    new_words=generate_next_enhanced_words(set_of_enh_words,concatenated_braid_word)
    
    u=len(concatenated_braid_word) -1
    
    for L in range(u,-1,-1):
        

        #uncomment this to try for lexicographic match
        #if not( L==u):
        #    continue
        #print("")
        #print(L)

        #print(len(new_words))
        new_words=remove_L_u_matched_words_from_set(new_words,concatenated_braid_word,L,u)
        #print(len(new_words))
    return new_words

#This is obsolate, since I will be using generate unmatched cell history in order to check paths    
def generate_all_unmatched_words(braid_word):
    all_unmatched_words={}
    for i in range(len(braid_word)):
        all_unmatched_words=generate_next_unmatched_words(all_unmatched_words,braid_word[:(i+1)])  
        print(braid_word[:i+1]) #THIS WORKS AS A PROGRESS BAR 
    return all_unmatched_words

def generate_unmatched_cell_history(braid_word):
    history=[{}]
    for i in range(len(braid_word)):
        history.append(generate_next_unmatched_words(history[i],braid_word[:(i+1)]))  
        print(braid_word[:i+1]) #THIS WORKS AS A PROGRESS BAR 
        #print(len(history[len(history)-1]))
    return history

def generate_lex_unmatched_words(braid_word):
    
    def generate_next_lex_words(set_of_enh_words, concatenated_braid_word):
        if(len(concatenated_braid_word)==1):
            return {"0","1"}
        new_words=generate_next_enhanced_words(set_of_enh_words,concatenated_braid_word)

        u=len(concatenated_braid_word) -1

        new_words=remove_L_u_matched_words_from_set(new_words,concatenated_braid_word,u,u)
        return new_words

    lex_unmatched={}

    for i in range(len(braid_word)):
        lex_unmatched=generate_next_lex_words(lex_unmatched,braid_word[:(i+1)])  
        print(braid_word[:i+1]) #THIS WORKS AS A PROGRESS BAR 
    
    return lex_unmatched
    


####################### Optimisation which did not make it faster here
"""

def remove_L_u_matched_words_from_set_v2(set_of_enh_word_pairs,braid_word,L,u):
    remaining_words=set()

    filtered_pairs = set()

    for pair in set_of_enh_word_pairs:
        _, second_element = pair 
        if L in second_element:
            filtered_pairs.add(pair)


    #Does not 

    while(len(filtered_pairs)>0):
        word=filtered_pairs.pop()

        potential_match=isopair(braid_word,word[0],L,u)

        if not (potential_match==None):
            #match_inside_the_set=False
            for pair in set_of_enh_word_pairs:
                if potential_match==pair[0]:
                    set_of_enh_word_pairs.remove(pair)
                    set_of_enh_word_pairs.remove(word)
                    match_inside_the_set=True
                    #print("asd")
                    break

    return set_of_enh_word_pairs

def potential_L_matchings_max_u(braid_word, enh_word):
    #returns a set of potentials which can be reached with merge or rev-split
    potentials=set()
    if enh_word[len(enh_word)-1]=="0" or enh_word[len(enh_word)-1]=="1":
        return frozenset(potentials)
    if len(braid_word)==0 or len(braid_word)==1:
        return frozenset(potentials)

    
    y_pos=len(braid_word) -1
    if(y_pos==0):
        return False    
    x_pos=x_position_of_crossing(braid_word,y_pos)
    
    points_along_circle=array_of_positions_from_edge((x_pos,y_pos),(x_pos+1,y_pos),braid_word,enh_word)

    #print(points_along_circle)

    for point in points_along_circle:
        
        x_of_crossing_at=x_position_of_crossing(braid_word,point[1])
        if x_of_crossing_at==point[0]:
            potentials.add(point[1])
        if x_of_crossing_at==point[0]+1:
            potentials.add(point[1])
        
        x_of_crossing_below=x_position_of_crossing(braid_word,point[1]-1)
        if x_of_crossing_below==point[0]:
            potentials.add(point[1]-1)
        if x_of_crossing_below==point[0]+1:
            potentials.add(point[1]-1)
    
    #Do x and y filtering here also
    potentials=frozenset(potentials)
    return potentials




#def generate next  unmatched words while removing L=u words



def generate_next_unmatched_words_v2(set_of_enh_words, concatenated_braid_word):
    if(len(concatenated_braid_word)==1):
        return {"0","1"}
    new_words=generate_next_enhanced_words(set_of_enh_words,concatenated_braid_word)
    new_word_pairs=set()

    for word in new_words:
        word_pair=(word,potential_L_matchings_max_u(concatenated_braid_word,word))
        #print(type(word_pair))
        #print(word_pair[1])
        #print(type(word_pair[1]))
        new_word_pairs.add(word_pair)


    u=len(concatenated_braid_word) -1
    
    for L in range(u,-1,-1):
        
        new_word_pairs=remove_L_u_matched_words_from_set_v2(new_word_pairs,concatenated_braid_word,L,u)

        #print(L)
        #print(new_word_pairs)
    
    filtered_words=set()

    for pair in new_word_pairs:
        filtered_words.add(pair[0])

    return filtered_words

"""

################## Homological and quantum degree on cells

#conventions of hdeg and qdeg from https://arxiv.org/pdf/math/0606464.pdf
def hdeg_of_word(braid_word,enh_word):
    def count_characters_in_string(mystring):
        count_1 = mystring.count("1")
        count_X = mystring.count("X")
        count_Y = mystring.count("Y")
    
        return count_1+ count_X+ count_Y

    num_of_neg_crossings=len(list(filter(str.islower, braid_word)))
    num_of_one_smoothings=count_characters_in_string(enh_word)

    return num_of_one_smoothings-num_of_neg_crossings

def qdeg_of_word(braid_word,enh_word):
    def count_xX(mystring):
        count_X = mystring.count("X")
        count_x = mystring.count("x")
        return count_X +count_x

    def count_yY(mystring):
        count_Y = mystring.count("Y")
        count_y = mystring.count("y")
        return count_Y +count_y
    
    deg=count_yY(enh_word)-count_xX(enh_word)
    num_of_neg_crossings=len(list(filter(str.islower, braid_word)))
    num_of_pos_crossings=len(braid_word)-num_of_neg_crossings

    hdeg=hdeg_of_word(braid_word,enh_word)    
    return deg+hdeg+num_of_pos_crossings-num_of_neg_crossings
   

def add_degs(braid_word, set_of_enh_words):
    array_of_triples=[]
    for word in set_of_enh_words:
        triple=(word,hdeg_of_word(braid_word,word),qdeg_of_word(braid_word,word))
        array_of_triples.append(triple)
    return array_of_triples

def sort_by_hdeg(array_of_triples):
    sorted_tuples = sorted(array_of_triples, key=lambda x: x[1])
    return sorted_tuples


def generate_unmatched_words_with_degs(braid_word):
    words=generate_all_unmatched_words(braid_word)
    degwords=add_degs(braid_word,words)
    return degwords

################### Connectivity diagrams on crtitical cells


#connectivity will be a list of pairs of postive integers
# as is kht++ cx-c2 files the top vertices will be labeled by 1,...,n from left to right and bottom ones n+1,...,2n

def endpoint_label_to_coord(braid_word,end_point_label):
    strands=number_of_strands(braid_word)
    #we are at bottom
    if end_point_label>strands:
        return (end_point_label-strands-1,0)
    #we are at top
    return (end_point_label-1,len(braid_word))

def single_connectivity(braid_word,enh_word,coord):
    strands=number_of_strands(braid_word)
    #Bottom
    if coord[1]==0:
        #check a direct match left if possible
        if coord[0]>0:
            if smoothing_northeast_is_Vert((coord[0]-1,coord[1]),braid_word,enh_word):
                return (coord[0]-1,coord[1])
        #check direct right
        if coord[0]<strands-1:
            if smoothing_northeast_is_Vert((coord[0],coord[1]),braid_word,enh_word):
                return (coord[0]+1,coord[1])
        #general case 
        #might have a problem with length 1 braid
        #print("looping from")
        #print(coord)
        path=array_of_positions_from_edge(coord,(coord[0],coord[1]+1),braid_word,enh_word)
        return path[len(path)-1]
    
    #Top
    #check a direct match left if possible
    if coord[0]>0:
        if smoothing_northeast_is_Vert((coord[0]-1,coord[1]-1),braid_word,enh_word):
            return (coord[0]-1,coord[1])
    #check direct right
    if coord[0]<strands-1:
        if smoothing_northeast_is_Vert((coord[0],coord[1]-1),braid_word,enh_word):
            return (coord[0]+1,coord[1])
    #general case 
    #might have a problem with length 1 braid
    #print("looping from")
    #print(coord)
    #print(enh_word)
    path=array_of_positions_from_edge(coord,(coord[0],coord[1]-1),braid_word,enh_word)
    return path[len(path)-1]




def coord_to_endpoint_label(braid_word,coord):
    strands=number_of_strands(braid_word)
    if coord[1]==0:
        return(strands+coord[0]+1)
    return(coord[0]+1)

def connectivity_tuple_of_cell(braid_word,enh_word):
    strands=number_of_strands(braid_word)
    connectivity=[]
    connection_found=set()
    
    for i in range(1,2*strands+1):
        if i in connection_found:
            continue
                
        start_coord=endpoint_label_to_coord(braid_word,i)
        end_coord=single_connectivity(braid_word,enh_word,start_coord)
        end_label=coord_to_endpoint_label(braid_word,end_coord)

        connection_found.add(i)
        connection_found.add(end_label)

        connectivity.append((i,end_label))
    
    return connectivity



################### Finding paths between critical cells

def next_steps_up(braid_word,enh_word,previous_u):
    #returns a list of pair (word, L)
    #Also includes reversed arrows in the list, these need to be filtered separately
    #At the moment, this works in the dotted Bar-Natan category 
    
    words_up=[]
    for L in range(0,min(len(enh_word),previous_u+1),1):        
        if enh_word[L]=="1" or enh_word[L]=="X" or enh_word[L]=="Y":
            continue
        
        Lx=x_position_of_crossing(braid_word,L)
        Ly=L
        L_is_vert=smoothing_northeast_is_Vert((Lx,Ly),braid_word,enh_word)
        
        
        L_edge1=((Lx,Ly),(Lx+1,Ly))
        L_edge2=((Lx,Ly+1),(Lx+1,Ly+1))
        
        if(not L_is_vert):
            L_edge1=((Lx,Ly),(Lx,Ly+1))
            L_edge2=((Lx+1,Ly),(Lx+1,Ly+1))
        
        component1=array_of_positions_from_edge(L_edge1[0],L_edge1[1],braid_word,enh_word)    
        
        component1_is_loop=False
        if(component1[0]==component1[len(component1)-1]):
                component1_is_loop=True
        
        two_components_exist=False
        if(not(L_edge2[0] in component1)):
            if(component1_is_loop):
                two_components_exist=True    
            else:
                reverse_direction_comp1=array_of_positions_from_edge(L_edge1[1],L_edge1[0],braid_word,enh_word)
                if(not(L_edge2[0] in reverse_direction_comp1)):
                    two_components_exist=True

  
        # Generate merge-arrows up
        if(two_components_exist):
            component2=array_of_positions_from_edge(L_edge2[0],L_edge2[1],braid_word,enh_word)

            component2_is_loop=False
            if(component2[0]==component2[len(component2)-1]):
                component2_is_loop=True

            comp1_high_dec=highest_and_decoration_of_component(component1,enh_word)
            comp2_high_dec=highest_and_decoration_of_component(component2,enh_word)

            # Neither component is a loop
            if((not component1_is_loop) and (not component2_is_loop)):
                new_word=replace_char(enh_word,L,"1")
                words_up.append((new_word,L))
                continue

            # Component 1 is a loop and component 2 is not
            if component1_is_loop and (not component2_is_loop):
                new_word=replace_char(enh_word,L,"1")
                new_word=remove_xy_coding_from_char(new_word,comp1_high_dec[0])
                words_up.append((new_word,L))
                continue

            # Component 2 is a loop and component 1 is not
            if (not component1_is_loop) and component2_is_loop:
                new_word=replace_char(enh_word,L,"1")
                new_word=remove_xy_coding_from_char(new_word,comp2_high_dec[0])
                words_up.append((new_word,L))
                continue

            # Both components are loops
            if component1_is_loop and component2_is_loop:
                
                # Both components are marked with x
                if comp1_high_dec[1]=="x" and comp2_high_dec[1]=="x":
                    continue
                
                comp1_is_higher=True
                if comp1_high_dec[0]<comp2_high_dec[0]:
                    comp1_is_higher=False
                                
                
                # Both components are marked with y
                if comp1_high_dec[1]=="y" and comp2_high_dec[1]=="y":                  
                    new_word=replace_char(enh_word,L,"1")
                    if comp1_is_higher:
                        new_word=remove_xy_coding_from_char(new_word,comp2_high_dec[0])
                    else:
                        new_word=remove_xy_coding_from_char(new_word,comp1_high_dec[0])
                    
                    words_up.append((new_word,L))
                    continue
                
                #One component is marked x one is marked y
                new_word=replace_char(enh_word,L,"1")
                if comp1_is_higher:
                    new_word=remove_xy_coding_from_char(new_word,comp2_high_dec[0])
                    new_word=put_x_coding_to_char(new_word,comp1_high_dec[0])
                else:
                    new_word=remove_xy_coding_from_char(new_word,comp1_high_dec[0])
                    new_word=put_x_coding_to_char(new_word,comp2_high_dec[0]) 
                
                words_up.append((new_word,L))
                continue
        
        #Generate split arrows up
        prelim_word=replace_char(enh_word, L ,"1")

        prelim_comp1=array_of_positions_from_edge(L_edge1[0],L_edge2[0],braid_word,prelim_word)
        prelim_comp2=array_of_positions_from_edge(L_edge1[1],L_edge2[1],braid_word,prelim_word)
        
        prelim_comp1_high_dec=highest_and_decoration_of_component(prelim_comp1,prelim_word)
        prelim_comp2_high_dec=highest_and_decoration_of_component(prelim_comp2,prelim_word)
        
        prelim_comp1_is_loop=True
        if prelim_comp1_high_dec[0]==-10:
            prelim_comp1_is_loop=False
        
        prelim_comp2_is_loop=True
        if prelim_comp2_high_dec[0]==-10:
            prelim_comp2_is_loop=False
        
        #The split is from non-loop component
        if not prelim_comp1_is_loop:
            words_up.append((put_x_coding_to_char(prelim_word,prelim_comp2_high_dec[0]),L))
            words_up.append((put_y_coding_to_char(prelim_word,prelim_comp2_high_dec[0]),L))
            continue
        
        if not prelim_comp2_is_loop:
            words_up.append((put_x_coding_to_char(prelim_word,prelim_comp1_high_dec[0]),L))
            words_up.append((put_y_coding_to_char(prelim_word,prelim_comp1_high_dec[0]),L))
            continue
        
        #The split is from a loop
        prelim_comp1_is_higher=True
        if prelim_comp1_high_dec[0]<prelim_comp2_high_dec[0]:
            prelim_comp1_is_higher=False
        
        orig_component_h_d=highest_and_decoration_of_component(component1,enh_word)
        
        #The original loop had x coding
        if orig_component_h_d[1]=="x":
            prelim_word=put_x_coding_to_char(prelim_word,prelim_comp1_high_dec[0])
            prelim_word=put_x_coding_to_char(prelim_word,prelim_comp2_high_dec[0])
            words_up.append((prelim_word,L))
            continue
        
        #The original loop had y coding
        new_word1=put_x_coding_to_char(prelim_word,prelim_comp1_high_dec[0])
        new_word1=put_y_coding_to_char(new_word1,prelim_comp2_high_dec[0])

        new_word2=put_y_coding_to_char(prelim_word,prelim_comp1_high_dec[0])
        new_word2=put_x_coding_to_char(new_word2,prelim_comp2_high_dec[0])
        
        words_up.append((new_word1,L))
        words_up.append((new_word2,L))

    return words_up


def prefers_back2(braid_word,A,B,L,u,unmatched_cells_history):
    #we assume that A prefers B with an (L,u) arrow. 
    # The function returns True if B prefers A back and false, if not.

    if not (B[:(u)] in unmatched_cells_history[u]):
        return False
    
    for current_L in range(u,L-1,-1):
        matching=concatenated_isopair(braid_word,B,current_L,u)

        if matching==A:
            return True

        if  matching!= None:
            if(prefers_back2(braid_word,B,matching,current_L,u,unmatched_cells_history)):
                return False

    print("something is strange")
    return True
    
#### This does not check if the current vertex is matched down
def next_step_down(braid_word,enh_word,previous_L,unmatched_cells_history):
    #returns -1 if unmatched cell is found. Returns -2, if the cell is matched upwards.
    
    for u in range(previous_L,len(braid_word),1):
        for L in range(u,-1,-1):
            matching=concatenated_isopair(braid_word,enh_word,L,u)

            if(matching!= None):

                if prefers_back2(braid_word,enh_word,matching,L,u,unmatched_cells_history): 
                    if(hdeg_of_word(braid_word, enh_word)<hdeg_of_word(braid_word, matching)):
                        return -2
                    return (matching,u)
    if not enh_word in unmatched_cells_history[len(unmatched_cells_history)-1]:
        print("something is fishy")
        print(enh_word)
        #print((unmatched_cells_history[len(unmatched_cells_history)-1]).pop())
    return -1


def hdeg_to_maximal_qdeg(braid,unmatched_words):
    hdeg_to_qdeg = {}  
    for string in unmatched_words:
        hdeg=hdeg_of_word(braid,string)
        qdeg=qdeg_of_word(braid,string)

        if hdeg not in hdeg_to_qdeg or qdeg > hdeg_to_qdeg[hdeg]:
            hdeg_to_qdeg[hdeg] = qdeg

    return hdeg_to_qdeg
    


def hdeg_to_maximal_ones(braid,unmatched_words):
    if not braid==braid.lower():
        return None

    hdeg_to_ones = {}  
    for string in unmatched_words:
        hdeg=hdeg_of_word(braid,string)
        ones=count_starting_ones(string)

        if hdeg not in hdeg_to_ones or ones > hdeg_to_ones[hdeg]:
            hdeg_to_ones[hdeg] = ones

    return hdeg_to_ones



def zig_zag_paths_from2(braid_word,enh_word,unmatched_cells_history,hdeg_max_qdeg,hdeg_to_max_ones):
    

    #Some optimisation to cut hopeless paths earlier on
    hdeg=hdeg_of_word(braid_word,enh_word)+1
    max_qdeg=100000000
    max_ones=100000000
    if hdeg in hdeg_max_qdeg:
        max_qdeg=hdeg_max_qdeg[hdeg]
    if not(hdeg_to_max_ones==None) and hdeg in hdeg_to_max_ones:
        max_ones=hdeg_to_max_ones[hdeg]

    # I would have prefered to keep the paths from criticals as a "global variable inside zig_zag_paths_from2
    # Since I did not manage to do that, I am passing it around
     
    def update_dict_from_vertex2(down_word,previous_u,paths_from_cell_to_criticals):
        steps_up=next_steps_up(braid_word,down_word,previous_u)
        not_a_step_up=None #next steps up include reversed arrows in the wrong direction

        for (up_word,L) in steps_up:

            if up_word in paths_from_cell_to_criticals.keys():
                continue
            
            if(qdeg_of_word(braid_word,up_word)>max_qdeg) or (count_starting_ones(up_word)>max_ones):
                paths_from_cell_to_criticals[up_word]=[]
                continue

            next_down=next_step_down(braid_word,up_word,L,unmatched_cells_history)
            #down2=next_step_down2(braid_word,up_word,L,unmatched_cells_history,None)
            #if next_down!=down2:
            #    print("asddasdsaadssaddddddddddddddddddddddddddddddddd")
            

            if next_down==-2: #the vertex is not matched up and thus not down. Hence the paths cannot continue.
                paths_from_cell_to_criticals[up_word]=[]              
            elif next_down==-1: #the vertex is critical
                paths_from_cell_to_criticals[up_word]=[[up_word]]
            elif next_down[0]==down_word:
                not_a_step_up=up_word
            else:

                paths_from_cell_to_criticals=update_dict_from_vertex2(next_down[0],next_down[1],paths_from_cell_to_criticals)
                if paths_from_cell_to_criticals[next_down[0]]==[]:
                    paths_from_cell_to_criticals[up_word]=[]
                else:
                    new_paths=[]
                    for path in paths_from_cell_to_criticals[next_down[0]]:
                        path_copy=path.copy()
                        path_copy.append(up_word)
                        new_paths.append(path_copy)
                    paths_from_cell_to_criticals[up_word]=new_paths

        steps_are_empty=True
        paths_from_down_word=[]

        for (up_word,L) in steps_up:
            if up_word==not_a_step_up:
                continue
            if paths_from_cell_to_criticals[up_word]==[]:
                continue
            steps_are_empty=False
            for path in paths_from_cell_to_criticals[up_word]:
                path_copy=path.copy()
                path_copy.append(down_word)
                paths_from_down_word.append(path_copy)

        paths_from_cell_to_criticals[down_word]=paths_from_down_word
        
        return paths_from_cell_to_criticals


    path_dictionary=update_dict_from_vertex2(enh_word,len(enh_word),dict())
    
    #To do this hdeg by hdeg, I could have the previous command run in a for loop of  and pass the path dictionary allways to the next one.
    #this function would need to return all paths and in the function generate all zig-zag paths I would need to take some unions  



    
    def reverse_all_paths(path_list):
        new_list=[]
        for path in path_list:
            path.reverse()
            new_list.append(path)
        return new_list   

    return reverse_all_paths(path_dictionary[enh_word])

    

            
def generate_all_zig_zag_paths(braid, history):
    #time1=time.time()
    
    #history=generate_unmatched_cell_history(braid)
    unmatched_words=history[len(history)-1]
    size=len(unmatched_words)   

    time2=time.time()

    #print("unmatched cells found: " + str(size))
    #print("time elapsed in generating unmatched cells: " + str(time2-time1))

    hdeg_to_max_qdeg=hdeg_to_maximal_qdeg(braid,unmatched_words)
    hdeg_to_max_ones=hdeg_to_maximal_ones(braid,unmatched_words)
    zig_zags={}

    paths_done=0

    print("Negative braid optimizations are on: "+str(negative_braid))


    total_path_count=0
    for word in unmatched_words:
        
        zig_zags[word]=zig_zag_paths_from2(braid,word,history,hdeg_to_max_qdeg,hdeg_to_max_ones)
        total_path_count+=len(zig_zags[word])
        
        #print(len(zig_zags[word]))

        paths_done=paths_done+1
        text = f"finding paths between unmatched cells: {round((paths_done*100)/size)}%"
        print(f"\r{text}", end='')

    time3=time.time()

    print("")
    print("total number of paths found: "+ str(total_path_count))
    print("time elapsed in generating paths: " + str(time3-time2))
    
    #print(hdeg_to_max_ones)

    return zig_zags


################### Check for acyclicity of the Mgr

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

def verify_acyclicity(braid, history):

    print("Generating all cells of the graph:")
    all_words=generate_all_enhanced_words(braid)
    print("total number of cells in the graph: "+str(len(all_words)))
    
    print("verifying acyclicity...")

    def verify(to_be_verified, cell):
        
        N=updown_next_steps(braid,cell,history)

        for v in N:
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









####################################### CLEAN THESE UP AT SOME POINT
"""
def calc_and_save_T4_paths(twistnumber):

    braid=twistnumber*"abc"
    file_path="Torus4braid_paths/new4string"+str(twistnumber)+"twist.pkl"
    zig_zags=None  
    if os.path.exists(file_path):
        pass
    else:      
        zig_zags=generate_all_zig_zag_paths(braid)
        with open(file_path, 'wb') as file:
            pickle.dump(zig_zags, file)


def calc_and_save_T4_cells(twistnumber):
    braid=twistnumber*"abc"
    file_path="Torusbraid_cell_dumps/4string"+str(twistnumber)+"twist.pkl"
    if os.path.exists(file_path):
        pass
    else:      
        history=generate_unmatched_cell_history(braid)
        with open(file_path, 'wb') as file:
            pickle.dump(history, file)

def calc_and_save_T5_cells(twistnumber):
    braid=twistnumber*"abcd"
    file_path="Torus5braids/5string"+str(twistnumber)+"twistLhack.pkl"
    if os.path.exists(file_path):
        pass
    else:      
        history=generate_unmatched_cell_history(braid)
        with open(file_path, 'wb') as file:
            pickle.dump(history, file)

def calc_and_save_T6_cells(twistnumber):
    braid=twistnumber*"abcde"
    file_path="Torus6braids/6string"+str(twistnumber)+".pkl"
    if os.path.exists(file_path):
        pass
    else:      
        history=generate_unmatched_cell_history(braid)
        with open(file_path, 'wb') as file:
            pickle.dump(history, file)



def save_the_snake(twistnumber):
    braid=(4*twistnumber)*"abc"

    history=generate_unmatched_cell_history(braid)



    snake=twistnumber*"101011x0011x"
    
    unmatched_words=history[-1]
    
    #hdeg_to_max_qdeg=hdeg_to_maximal_qdeg(braid,unmatched_words)
    hdeg_to_max_qdeg=dict()
    hdeg_to_max_qdeg[hdeg_of_word(braid,snake)]=qdeg_of_word(braid,snake)+3
    #slightly scared that I made something aweful here

    hdeg_to_max_ones=hdeg_to_maximal_ones(braid,unmatched_words)
    
    zig_zags={}
    zig_zags[snake]=zig_zag_paths_from2(braid,snake,history,hdeg_to_max_qdeg,hdeg_to_max_ones)


    output_file_path="Torus4braid_paths/snake"+str(twistnumber)+"twist.pkl"
      
    if os.path.exists(output_file_path):
        pass
    else:      
        with open(output_file_path, 'wb') as file:
            pickle.dump(zig_zags, file)
"""




#repeating code in a bad style

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

    




################## Main, no functionality there so far 
parser = argparse.ArgumentParser()


def main():

    #Parsing user arguments

    parser.add_argument("braid")
    parser.add_argument("-o", "--output", dest = "outputfile", default = False)
    parser.add_argument('-a', '--acyclicity', action='store_true') 
    parser.add_argument('-c', '--cells', action='store_true') 
    parser.add_argument('-p', '--paths', action='store_true')
    
    args = parser.parse_args()

    outputfile=args.outputfile
    braid= args.braid

    calc_acyclicity=args.acyclicity
    calc_cells=args.cells
    calc_paths=args.paths

    global negative_braid
    if(braid==braid.lower()):
        negative_braid=True



    #Computing stuff and displaying progress bars etc
    
    print("Cells")
    print("Generating unmatched cells:")

    time1=time.time()

    history=generate_unmatched_cell_history(braid)

    unmatched_words=history[len(history)-1]
    size=len(unmatched_words)   
    time2=time.time()
    print("unmatched cells found: " + str(size))
    print("time elapsed in generating unmatched cells: " + str(time2-time1))

    acyclicity_verified=False
    if( calc_acyclicity):
        print("")
        print("Acyclicity")
        verify_acyclicity(braid, history)
        acyclicity_verified=True
        print("Greedy matching is acyclic for the braid!")
        time_acyc=time.time()
        print("time elapsed in verifying acyclicity: " + str(time_acyc-time1))

    sorted_cells=None
    if calc_cells or calc_paths:
        sorted_cells=sort_by_hdeg(add_degs(braid,history[-1]))
        
    zig_zags=None
    if(calc_paths):
        print("")
        print("Paths")
        zig_zags=generate_all_zig_zag_paths(braid, history)

    


    #Writing results to console or to given outputfile
    summary_strings=[]
    summary_strings.append("Results summary")
    summary_strings.append("Braid: "+ braid)
    summary_strings.append("Number of cells in the greedy matching: "+ str(size))
    if calc_paths:
        path_count=0
        for cell in zig_zags:
            path_count+=len(zig_zags[cell])
        
        summary_strings.append("Number of paths between unmatched cells: "+ str(path_count))
    else:
        summary_strings.append("Number of paths between unmatched cells: paths not computed")
    
    if acyclicity_verified:
        summary_strings.append("Acyclicity verified: Greedy matching is acyclic for the braid!")
    else:
        summary_strings.append("Acyclicity not verified")
    summary_strings.append("")

    
    if outputfile:
        with open(outputfile, 'w') as f:
            for s in summary_strings:
                f.writelines(s+"\n")
            if calc_cells or calc_paths:
                f.write("Cells: \n")
                for triple in sorted_cells:
                    f.write("hdeg: "+ str(triple[1])+ " qdeg: "+ str(triple[2])+ " cell: "+triple[0]+"\n")
            if calc_paths:
                f.write(""+ "\n")
                f.write("Paths:"+ "\n")
                for cell in zig_zags:
                    f.write(str(cell) +";" +str(zig_zags[cell])+"\n")

            

        print("Results written in file:"+ outputfile)

    else:
        print("")
        for s in summary_strings:
            print(s)
        if calc_cells or calc_paths:
            print("Cells:")
            for triple in sorted_cells:
                print("hdeg: "+ str(triple[1])+ " qdeg: "+ str(triple[2])+ " cell: "+triple[0])
        if calc_paths:
            print("")
            print("Paths:")
            for cell in zig_zags:
                print(str(cell) +";" +str(zig_zags[cell]))

        

if __name__ == "__main__":

    #if(sys.argv[1]==sys.argv[1].lower()):
    #    negative_braid=True
    
    main()
    
