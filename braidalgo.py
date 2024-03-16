
import sys

def number_of_strands(word):
    word=word.lower()
    alphabet_chars = [char for char in word if char.isalpha()]
    if alphabet_chars:
        return ord(max(alphabet_chars))-ord('a')+1
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
    if(xcoord==position[0] and not zero_smoothing and not negative_crossing):
    	return True
    return False

def out_of_bounds(position, braid_word):
    if(position[0]<0 or position[0]> number_of_strands(braid_word) or position[1]<=0 or position[1]>= len(braid_word)):
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

"""
    
#trying to make this obsolate    
def there_is_loop_starting_from_edge(start_pos,next_pos,braid_word,enh_word):
    previous_pos=start_pos
    #consider to checking for the end the loop at next pos in order to not get problems with the first step being illegal
    
    
    
    #this should be while, but I am scared of mistakes and loops forever
    for i in range(500):
        lead_pos=next_step_in_smoothing(next_pos, previous_pos, braid_word, enh_word)
        #print(lead_pos)
        previous_pos=next_pos
        next_pos=lead_pos
        if(next_pos==start_pos):
            return True
        elif(out_of_bounds(next_pos,braid_word)):
            return False

    print("problem with finding a loop")
    return -1
"""




def smoothing_of_last_crossing_created_loop(braid_word,enh_word):
    if(len(braid_word)!=len(enh_word)):
        print("something is fishy with word lengths")
    
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
        print(all_enhanced_words)  
        
    return all_enhanced_words






























def record_point_touching_a_square(point,square, corner_array):
    #square is encoded by the bijection between points and squares which sends a point to the square at north-east of the point 
    print(type(corner_array))
    print(point)
    print(square)
    print(corner_array)
    
    if(point[0]==square[0] and point[1]==square[1]):
        #corner_array.append((0,0))
        corner_array.append(point)
        return corner_array
    elif(point[0]==square[0] and point[1]==square[1]+1):
        #corner_array.append((0,1))
        corner_array.append(point)
        return corner_array
    elif(point[0]==square[0]+1 and point[1]==square[1]):
        #corner_array.append((1,0))
        corner_array.append(point)
        return corner_array
    elif(point[0]==square[0]+1 and point[1]==square[1]+1):
        #corner_array.append((1,1))
        corner_array.append(point)
        return corner_array
    return corner_array
    
    
def loop_starting_at_edge_touches_square_of_crossing_from_corners(braid_word,enh_word,start_pos, next_pos, cross_index):
    
    #returns whether corners of the square at cross_index are touched by a loop. The returning output is an array of length 0, 2 or 4 containing pairs (0,0),(0,1),(1,0) or (1,1) which correspond to the crossings which are touched. The order of these corner points in the array matters as one can read of the connectivity of a split from it. 
    
    corner_array=[]
    #corner_array.append("asd")
    
    #print(type(corner_array))
    
    if(cross_index>=len(enh_word)):
        print("problem with word length and index")
        return corner_array
        
    x_coord=x_position_of_crossing(braid_word,cross_index)
    square=(x_coord,cross_index)
    
    
    
    # To determine, whether the arcs of the smoothing are used, it is not enough to simply record the corner points as edges above and below can be bent. It is enough for left and right sides. For top and bottom the arcs are used if the smoothing is not vert
    # loops of two vertices are special cases
    # otherwise it should not be too big of an issue
    
    #maybe the loops of size 2 are not special cases either
        
    #if loop of 2 ... then ...  (check this by running next step once)
    #if(next_step_in_smoothing(start_pos, next_pos, braid_word, enh_word)==start_pos):
    #    #we hit a loop of 2
    #    return
    
    
    
    corner_array=record_point_touching_a_square(start_pos,square,corner_array)
    corner_array=record_point_touching_a_square(next_pos,square,corner_array)
    
    previous_pos=start_pos
    #this should be while, but I am scared of mistakes and loops forever
    for i in range(500):
        lead_pos=next_step_in_smoothing(next_pos, previous_pos, braid_word, enh_word)
        #print(lead_pos)
        previous_pos=next_pos
        next_pos=lead_pos
        if(next_pos==start_pos):
            return corner_array
        elif(out_of_bounds(next_pos,braid_word)):
            print("found no loop where one was supposed to be")
            return corner_array
        
        corner_array=record_point_touching_a_square(next_pos,square,corner_array)
        

    print("problem with finding a loop")
    
    
def highest_point_of_loop_from_edge(start_pos, next_pos,braid_word,enh_word):
    #returns -1 if no loop is found
    if(out_of_bounds(start_pos,braid_word) or out_of_bounds(next_pos,braid_word)):
        return -1 
    
    highest=max(start_pos[1],next_pos[1])
    
    previous_pos=start_pos
    
    
    #this should be while, but I am scared of mistakes and loops forever
    for i in range(500):
        lead_pos=next_step_in_smoothing(next_pos, previous_pos, braid_word, enh_word)
        #print(lead_pos)
        previous_pos=next_pos
        next_pos=lead_pos
        
        highest=max(next_pos[1],highest)
        
        if(next_pos==start_pos):
            return highest
        elif(out_of_bounds(next_pos,braid_word)):
            return -1

    print("problem with finding a loop")
    
    return -1
    



#def merge_up_cell_L_u(braid_word,enh_word,L,u):
#    if(not((enh_word[u]=="y" or enh_word[u]=="Y") and (enh_word[L]=="0" or enh_word[L]=="x" or enh_word[L]=="y"))):
#        return(False,"")
#    x_coord=x_position_of_crossing(braid_word,u)
#    u_loop_start=(x_coord,u)
#    u_loop_next=(x_coord+1,u)
#    
#    corner_array=loop_starting_at_edge_touches_square_of_crossing_from_corners(braid_word,enh_word,u_loop_start, u_loop_next, L)
#    
#    #if(l
"""
 
def opposite_edge_of_corner_array(corner_array,point):
    print("")
    print(corner_array)
    print(point)
    if(len(corner_array)!=2):
        print("problem with looking at opposite edge")
    op_point_0=(-corner_array[0][0]+2*point[0]+1,-corner_array[0][1]+2*point[1]+1)
    op_point_1=(-corner_array[1][0]+2*point[0]+1,-corner_array[1][1]+2*point[1]+1)
    
    return (op_point_0,op_point_1)
    
"""
    
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
    return changed

def put_y_coding_to_char(enh_word,index):
    if(enh_word[index]=="0" or enh_word[index]=="x"):
        changed=enh_word[:index] + "y" + enh_word[index+1:]
        return changed
    elif(enh_word[index]=="1" or enh_word[index]=="X"):
        changed=enh_word[:index] + "Y" + enh_word[index+1:]
        return changed
    return changed
    
"""    
def matching_with_merge_upwards(braid_word,enh_word,L_crossing,u_loop_start,u_loop_next,corner_array):
    second_merging_circle=opposite_edge_of_corner_array(corner_array,L_crossing)
    highest_point_of_second_merging_circle=highest_point_of_loop_from_edge(second_merging_circle[0], second_merging_circle[1],braid_word,enh_word)
    u=u_loop_start[0]
    L=L_crossing[0]
    
    #matching to a non-circle
    if(highest_point_of_second_merging_circle==-1):            
        matched = remove_xy_coding_from_char(enh_word,u)           
        matched = replace_char(matched, L ,"1")
        return(True,matched)
    
    #matching to a circle higher above
    if(highest_point_of_second_merging_circle>u):
        matched = remove_xy_coding_from_char(enh_word,u)           
        matched = replace_char(matched, L ,"1")
        return(True,matched)
    
    #MATHEMATICALLY IT IS NON-TRIVIAL CHOICE WHETHER WE ALLOW THE FOLLOWING
    #mathematically one could also consider u and L to be multivalued functions
    #matching to a circle below   
    char_of_second_circle=enh_word[highest_point_of_second_merging_circle]
    print(char_of_second_circle)
    
    if(char_of_second_circle=="y" or char_of_second_circle=="Y"):
        #These ones, if taken to the Morse matching M, are taken already at a previous u
        return(False,"")
    
    matched = remove_xy_coding_from_char(enh_word,highest_point_of_second_merging_circle)           
    matched = replace_char(matched, L ,"1")
    matched = put_x_coding_to_char(matched,u)
      
    print("wierd matching is found, one that I would expect to only see in reducible braids")
        
    return(True,matched)
    
def matching_with_split_downwards(braid_word,enh_word,L_crossing,u_loop_start,u_loop_next,corner_array):
    second_merging_circle=opposite_edge_of_corner_array(corner_array,L_crossing)
    highest_point_of_second_merging_circle=highest_point_of_loop_from_edge(second_merging_circle[0], second_merging_circle[1],braid_word,enh_word)
    
    u=u_loop_start[0]
    L=L_crossing[0]
    
    #matching to a non-circle
    if(highest_point_of_second_merging_circle==-1):            
        matched = remove_xy_coding_from_char(enh_word,u)           
        matched = replace_char(matched, L ,"0")
        return(True,matched)
    
    #matching to a circle higher above
    if(highest_point_of_second_merging_circle>u):
        matched = remove_xy_coding_from_char(enh_word,u)           
        matched = replace_char(matched, L ,"0")
        return(True,matched)
    
    #matching to a circle below   
    char_of_second_circle=enh_word[highest_point_of_second_merging_circle]
    print(char_of_second_circle)
    
    if(char_of_second_circle=="x" or char_of_second_circle=="X"):
        #These ones, if taken to the Morse matching M, are taken already at a previous u
        return(False,"")
    
    matched = remove_xy_coding_from_char(enh_word,highest_point_of_second_merging_circle)           
    matched = replace_char(matched, L ,"0")
    matched = put_x_coding_to_char(matched,u)
      
    print("wierd matching is found, one that I would expect to only see in reducible braids")
        
    return(True,matched)
"""

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




def matching_a_cell(braid_word,enh_word,L,u):
    
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
            return (False,"")
            
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
                return(True,matched)
            
            #split from higher loop
            if(u_comp_is_lower):
                matched = put_x_coding_to_char(prelim_word,u)
                return(True,matched)
            
            #split from lower loop with x (we do not allow for these as they will be matched away previously in the final recursive definition of M)
            if(orig_component_h_d[1]=="x"):
                return(False,"")
            
            #split from lower loop with y                
            matched = put_y_coding_to_char(prelim_word,other_comp_h_d[0])
            matched = put_x_coding_to_char(matched,u_comp_h_d[0])
            print("wierd split up is found, one that I would expect to only see in reducible braids")
            return(True,matched)
        
        #### look for rev-merge
        if(not enh_at_L_is_0_or_lowercase):
            
            #rev-merge from non-loop
            if(not other_comp_is_loop):
                matched = put_y_coding_to_char(prelim_word,u)           
                return(True,matched)
            
            #rev-merge from higher loop
            if(u_comp_is_lower):
                matched = put_y_coding_to_char(prelim_word,u)
                return(True,matched)
            
            #rev-merge from lower loop with y (we do not allow for these as they will be matched away previously in the final recursive definition of M)
            if(orig_component_h_d[1]=="y"):
                return(False,"")
            
            #split from lower loop with y                
            matched = put_x_coding_to_char(prelim_word,other_comp_h_d[0])
            matched = put_y_coding_to_char(matched,u_comp_h_d[0])
            print("wierd split up is found, one that I would expect to only see in reducible braids")
            return(True,matched)
            
    ##### look for merge and rev-split here
    
    if(two_components_exist):
        component2=array_of_positions_from_edge(L_edge2[0],L_edge2[1],braid_word,enh_word)
        
        component2_is_loop=False
        if(component2[0]==component2[len(component2)-1]):
            component2_is_loop=True
        
        #find saddle morphism
        if((not component1_is_loop) and (not component2_is_loop)):
            return (False, "")
        
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
            return (False,"")
            
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
                return(True,matched)
            
            ## merge to higher loop
            if(u_comp_is_lower):
                matched = remove_xy_coding_from_char(enh_word,u)           
                matched = replace_char(matched, L ,"1")
                return(True,matched)
            
            ## merge to a lower loop with y (we do not allow for these as they will be matched away previously in the final recursive definition of M)
            if(other_comp_h_d[1]=="y"):
                return (False,"")
            
            ## merge to lower loop with x
            matched = remove_xy_coding_from_char(enh_word,other_comp_h_d[0])           
            matched = replace_char(matched, L ,"1")
            matched = put_x_coding_to_char(matched,u)
            print("wierd merge-up is found, one that I would expect to only see in reducible braids")
            return(True,matched)
               
        #look for rev-split
        if((not enh_at_L_is_0_or_lowercase) and u_comp_h_d[1]=="x"):
            
            ##rev-split to non-loop
            if(not other_comp_is_loop):
                matched = remove_xy_coding_from_char(enh_word,u)           
                matched = replace_char(matched, L ,"0")
                return(True,matched)
            
            ##rev-split to higher loop
            if(u_comp_is_lower):
                matched = remove_xy_coding_from_char(enh_word,u)           
                matched = replace_char(matched, L ,"0")
                return(True,matched)
            
            ## rev-split to a lower loop with x (we do not allow for these as they will be matched away previously in the final recursive definition of M)
            if(other_comp_h_d[1]=="x"):
                return (False,"")
            
            ## rev-split to lower loop with y
            matched = remove_xy_coding_from_char(enh_word,other_comp_h_d[0])           
            matched = replace_char(matched, L ,"0")
            matched = put_y_coding_to_char(matched,u)
            print("wierd rev-split is found, one that I would expect to only see in reducible braids")
            return(True,matched)
    
    
    return (False,"")

def remove_L_u_matched_words_from_set(set_of_enh_words,braid_word,L,u):
    remaining_words=set()
    print(set_of_enh_words)
    
    while(len(set_of_enh_words)>0):
        word=set_of_enh_words.pop()
        potential_pair=matching_a_cell(braid_word,word,L,u)
        if(not potential_pair[0]):
            remaining_words.add(word)
            print("adding word2")
        elif(potential_pair[1] in set_of_enh_words):
            set_of_enh_words.remove(potential_pair[1])
        else:
            print("adding word1")
            remaining_words.add(word)
            
    return remaining_words

   
def generate_next_unmatched_words(set_of_enh_words, concatenated_braid_word):
    
    new_words=generate_next_enhanced_words(set_of_enh_words,concatenated_braid_word)
    
    #print(new_words)
    
    u=len(concatenated_braid_word) -1 #CHEK THIS -1
    
    for L in range(u,-1,-1):
        new_words=remove_L_u_matched_words_from_set(set_of_enh_words,concatenated_braid_word,L,u)
        
    
    return new_words
    
def generate_all_unmatched_words(braid_word):
    all_unmatched_words={}
    #all_enh_words={}
    
    for i in range(len(braid_word)):
        all_unmatched_words=generate_next_unmatched_words(all_unmatched_words,braid_word[:(i+1)])  
        #all_enh_words=generate_next_enhanced_words(all_enh_words,braid_word[:(i+1)])  
        
        print(braid_word[:i+1])
        print(all_unmatched_words)  
        
        #print(all_enh_words)
    
        
    return all_unmatched_words

   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
    

"""


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
        print(all_enhanced_words)  
        
    return all_enhanced_words






def there_is_isomorphism_with_cell_L_u(braid_word,enh_word,L,u):
    #should one try to look for all matchings in one function, merge up, merge down, split up, split down?
    #these should be all exclusive

    

    if(len(braid_word)!=len(enh_word)):
        print("something is fishy with word lengths")
    
    x_coord_of_u=x_position_of_crossing(braid_word,u)
    u_loop_start=(x_coord_of_u,u)
    u_loop_next=(x_coord_of_u+1,u)
    
    
    #highest might give wrong answer if not used safely
    u_is_vert=smoothing_northeast_is_Vert((x_coord_of_u,u),braid_word,enh_word)
    highest=-1
    if(u_is_vert):
        highest=highest_point_of_loop_from_edge(u_loop_start, u_loop_next,braid_word,enh_word)
    

    
    x_coord_of_L=x_position_of_crossing(braid_word,L)
    L_crossing=(x_coord_of_L,L)
    
    corner_array=loop_starting_at_edge_touches_square_of_crossing_from_corners(braid_word,enh_word,u_loop_start, u_loop_next, L)
    
    
    #############try matching with merge upwards 
    
    if((enh_word[u]=="y" or enh_word[u]=="Y") and (enh_word[L]=="0" or enh_word[L]=="x" or enh_word[L]=="y") and len(corner_array)==2 and highest==u):
        return matching_with_merge_upwards(braid_word,enh_word,L_crossing,u_loop_start,u_loop_next,corner_array)
    
    #############try matching with split downwards
    if((enh_word[u]=="x" or enh_word[u]=="X") and (enh_word[L]=="1" or enh_word[L]=="X" or enh_word[L]=="Y") and len(corner_array)==2 and highest==u):
        return matching_with_split_downwards(braid_word,enh_word,L_crossing,u_loop_start,u_loop_next,corner_array)
    
    #############try matching with merge downwards
    
    if((enh_word[L]=="1" or enh_word[L]=="X" or enh_word[L]=="Y")):
        candidate_word=replace_char(enh_word,L,"0")
        candidate_vert_at_L=smoothing_northeast_is_Vert(L_crossing,braid_word,candidate_word)
        high1=-1
        high2=-1
        if(candidate_vert_at_L):
            high1=highest_point_of_loop_from_edge((L_crossing[0],L_crossing[1]), (L_crossing[0]+1,L_crossing[1]),braid_word,candidate_word)
            high2=highest_point_of_loop_from_edge((L_crossing[0],L_crossing[1]+1), (L_crossing[0]+1,L_crossing[1]+1),braid_word,candidate_word)
        else:
            high1=highest_point_of_loop_from_edge((L_crossing[0],L_crossing[1]), (L_crossing[0],L_crossing[1]+1),braid_word,candidate_word)
            high2=highest_point_of_loop_from_edge((L_crossing[0]+1,L_crossing[1]), (L_crossing[0]+1,L_crossing[1]+1),braid_word,candidate_word)
        
        if(L==u):
            print("asd")
        else:
            if(high1==-1 and high2==u):
                print("asd")

        #here instead if high 1==-1 and so on
        if(high1 != high2):            
            smaller_high=high1
            larger_high=high2
            if(high2<high1 or high1==-1):
                smaller_high=high2
                larger_high=high1
            
            
            
            
            if(high1==L):
                #something smart here
                print("Asd")
            #else
        
            
            
            #something smart here
            print("Asd")
        
        
        
        
    #if(len(corner_array)==4 
    
    
    #This is not the correct if statement, as corner_array can hit only parts when we are merging to a non-loop
    #if((enh_word[L]=="1" or enh_word[L]=="X" or enh_word[L]=="Y") and len(corner_array)==4):
        
        #one possibility would be to try to write matching up as a function and do this by trying different coloring combinations to match there
        #whatever I choose to do, the rules should be symmetric, i.e. A matched to B iff B matched to A
        #somehow it feels more natural to consider multivariate u and L and let the inductive picking do its thing.
        #Next thing on Monday is to verify whether my Alt braid and T4 work with this
      
    
    #############try matching with split upwards
    
    
    
    
    
    return(False,"")


"""


def main():
    if len(sys.argv) != 2:
        print("Give me a braid")
        sys.exit(1)

    #print(number_of_strands(sys.argv[1]))
    #next_step_in_smoothing((5,4), (4,4), sys.argv[1], sys.argv[1])
    #print(smoothing_northeast_is_Vert((1,2),"aBA",[0,1,0]))
    #print(next_step_in_smoothing((1,1), (1,0), sys.argv[1], [0,0,0]))
    #print(len(sys.argv[1]))
    #print(out_of_bounds((3,6),sys.argv[1]))
    #print(there_is_loop_starting_from_edge((2,4), (3,4), sys.argv[1], "00000"))
    #print(array_of_positions_from_edge((2,4), (3,4), sys.argv[1], "00000"))
    
    
    #print(there_is_loop_starting_from_edge((0,3), (1,3), sys.argv[1], [0,0,0,0,0,0]))
    #print(there_is_loop_starting_from_edge((0,0), (1,0), sys.argv[1], [0]))
    print(generate_all_enhanced_words(sys.argv[1]))
    #print(smoothing_of_last_crossing_created_loop(sys.argv[1], [0,0,0,0,0]))
    #print(smoothing_of_last_crossing_created_loop(sys.argv[1], "00000"))
    
    #print(loop_starting_at_edge_touches_square_of_crossing_from_corners(sys.argv[1],"00000",(2,4), (3,4), 2))
    
    #print(opposite_edge_of_corner_array([(2,4),(2,3)],(1,3)))
    
    #print(there_is_isomorphism_with_cell_L_u(sys.argv[1],"0000yx",3,4))
    
    #print(matching_a_cell(sys.argv[1],"0000xy",3,5))
    
    #print(matching_a_cell(sys.argv[1],"11101Y",3,4))
    #print(generate_all_unmatched_words(sys.argv[1]))
    
    #print(matching_a_cell("bbb","0yy",1,1))
    #print(remove_L_u_matched_words_from_set({"0x"},"aa",1,1))

    #print(remove_L_u_matched_words_from_set({"00","11"},"aa",1,1))

if __name__ == "__main__":
    main()
    
