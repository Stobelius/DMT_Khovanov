import pickle
from braidalgo import qdeg_of_word, hdeg_of_word


def load_cells(twistnumber):
    #Currently 44 is highest doable
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

def silly_ones_snake_line(cell):
    xcount=cell.count("x")

    onecount=cell.count("1")

    #here I do not cut out more cells in the larger twist case 
    return xcount/onecount-0.33

"""
def snake_ones_line_as_func_of_hdeg(hdeg,twistnumber):
    #ax+b
    #hdeg=hdeg/twistnumber
    
    
    a=-
    b=-twistnumber
    return a*hdeg+b
"""

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
        print(cell)
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


def ones_count(my_string):
    count = 0
    for char in my_string:
        if char == "1":
            count += 1
        else:
            break 
    return count

def lk_count(string):    
    sub_string="x0101x"
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




def double_cut_index(enh_word):
    for i in range(len(enh_word)-1):
        if(i%3==2):
            if((enh_word[i]=="0" or enh_word[i]=="x") and (enh_word[i+1]=="0" or enh_word[i+1]=="x") ):
                return i

    return 99






















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

    



def path_dom_cod_pairs_testing():
    twistnumber=40
    unmatched_cells=load_cells(twistnumber)
    
    braid=twistnumber*"abc"

    crossings=3*twistnumber

    #two_doms=False

    for dom in unmatched_cells:
        dom_hdeg=hdeg_of_word(braid,dom)
        dom_qdeg=qdeg_of_word(braid,dom)
        for cod in unmatched_cells:
            cod_hdeg=hdeg_of_word(braid,cod)
            cod_qdeg=qdeg_of_word(braid,cod)

            if (cod_hdeg!=dom_hdeg+1) or (cod_qdeg<dom_qdeg):
                continue
            if ones_count(cod)<ones_count(dom):
                continue

            qdiff=cod_qdeg-dom_qdeg
            if qdiff>2:
                print(str(qdiff)+"  "+ str(ones_count(dom)%3)+"   "+str(ones_count(cod)-ones_count(dom)) +"   "+dom+"   "+cod)
                
                #if(two_doms):
                #    print("asdasd")

                #two_doms=True
        #two_doms=False

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

def sign_string(sign):
    if sign==1:
        return "+"
    if sign==-1:
        return "-"


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




def main():

    #cell__bijection_testing()
    #path_testing()
    #path_dom_cod_pairs_testing()
    #snake_functoriality_testing()
    lk_functoriality_testing()

    
if __name__ == "__main__":
    main()


"""
for h in range(min_hdeg,max_hdeg+1):
    for q in range(min_qdeg,max_qdeg+1):
        
        for cell in paths:
            if (h,q)==(hdeg_of_word(braid,cell),qdeg_of_word(braid,cell)):
                print("\n"+cell+" h:"+str(h)+" q:"+str(q))
                paths_from_cell=paths[cell]
                for path in paths_from_cell:
                    print(path[len(path)-1])
            
"""





"""

last_chars=set()

for cell in unmatched_cells:
    last_chars.add(cell[-12:])

for string in last_chars:
    print(string)

"""

"""
for path in paths:
    if path=="00011x101011":
        print((paths[path])[len(paths[path])-1])
        print(len(paths[path]))
"""
