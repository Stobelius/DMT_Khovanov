
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
            #print("wierd split up is found, one that I would expect to only see in reducible braids")
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
            
            #rev-merge from lower loop with x                
            matched = put_x_coding_to_char(prelim_word,other_comp_h_d[0])
            matched = put_y_coding_to_char(matched,u_comp_h_d[0])
            #print("wierd revmerge up is found, one that I would expect to only see in reducible braids")
            #print(enh_word +"   "+ matched)
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
            #print("wierd merge-up is found, one that I would expect to only see in reducible braids")
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
            #print("wierd rev-split is found, one that I would expect to only see in reducible braids")
            return(True,matched)
    
    
    return (False,"")

def remove_L_u_matched_words_from_set(set_of_enh_words,braid_word,L,u):
    remaining_words=set()
    #print(set_of_enh_words)
    
    # A possible big time-improvement:
    # Check whether a matching could be possible by glancing at whether some unmatched cell with different L exist in set_of_enh_words.
    # In other words, do a prior quick check before running the slow matching_a_cell function
    while(len(set_of_enh_words)>0):
        word=set_of_enh_words.pop()
        potential_pair=matching_a_cell(braid_word,word,L,u)
        if(not potential_pair[0]):
            remaining_words.add(word)
            #print("adding word with no pair"+word)
        elif(potential_pair[1] in set_of_enh_words):
            set_of_enh_words.remove(potential_pair[1])
            #print("removing pair"+word+"   "+potential_pair[1])
        else:
            #print("adding word1 with no pair in the set"+word)

            remaining_words.add(word)
            
    return remaining_words

   
def generate_next_unmatched_words(set_of_enh_words, concatenated_braid_word):
    if(len(concatenated_braid_word)==1):
        return {"0","1"}


    new_words=generate_next_enhanced_words(set_of_enh_words,concatenated_braid_word)
    
    u=len(concatenated_braid_word) -1 #CHEK THIS -1
    
    for L in range(u,-1,-1):
        new_words=remove_L_u_matched_words_from_set(new_words,concatenated_braid_word,L,u)
        
    
    return new_words
    
def generate_all_unmatched_words(braid_word):
    all_unmatched_words={}
    #all_enh_words={}
    
    for i in range(len(braid_word)):
        all_unmatched_words=generate_next_unmatched_words(all_unmatched_words,braid_word[:(i+1)])  
        #all_enh_words=generate_next_enhanced_words(all_enh_words,braid_word[:(i+1)])  
        
        print(braid_word[:i+1]) #THIS WORKS AS A PROGRESS BAR 
        #print(all_unmatched_words)  
        
        #print(all_enh_words)
    
        
    return all_unmatched_words


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
   

def add_degs_and_arrange_words(braid_word, set_of_enh_words):
    array_of_triples=[]
    for word in set_of_enh_words:
        triple=(word,hdeg_of_word(braid_word,word),qdeg_of_word(braid_word,word))
        array_of_triples.append(triple)
    
    sorted_tuples = sorted(array_of_triples, key=lambda x: x[1])
    return sorted_tuples


   
   

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
    #print(generate_all_enhanced_words(sys.argv[1]))
    #print(smoothing_of_last_crossing_created_loop(sys.argv[1], [0,0,0,0,0]))
    #print(smoothing_of_last_crossing_created_loop(sys.argv[1], "00000"))
    
    #print(loop_starting_at_edge_touches_square_of_crossing_from_corners(sys.argv[1],"00000",(2,4), (3,4), 2))
    
    #print(opposite_edge_of_corner_array([(2,4),(2,3)],(1,3)))
    
    #print(there_is_isomorphism_with_cell_L_u(sys.argv[1],"0000yx",3,4))
    
    #print(matching_a_cell(sys.argv[1],"0000xy",3,5))
    
    #print(matching_a_cell(sys.argv[1],"11101Y",5,5))
    braid=sys.argv[1]
    unmatched_words=generate_all_unmatched_words(braid)
    arranged_unmatched_words=add_degs_and_arrange_words(braid,unmatched_words)

    for a in arranged_unmatched_words:
        print(a)


    #testset=generate_all_unmatched_words(braid)
    

    #sorted_set = sorted(testset)
    #for string in sorted_set:
    #    print(string+str(hdeg_of_word(braid,string))+ str(qdeg_of_word(braid,string)))


    
    #print(matching_a_cell("bbb","0yy",1,1))
    #print(remove_L_u_matched_words_from_set({"0x"},"aa",1,1))

    #print(matching_a_cell("AA","10",0,1))
    #print(remove_L_u_matched_words_from_set({"00","0y","01","11"},"aa",0,1))

if __name__ == "__main__":
    main()
    
