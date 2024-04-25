import pickle
from braidalgo import qdeg_of_word, hdeg_of_word


def load_cells(twistnumber):
    #Currently 26 is highest doable
    file_path="Torus4braid_paths/26twistcells.pkl"

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

    domain_twistcount=22
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

    snake_margin_or_error=-8
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

    #print(cod_union==codomain_cells)

    #Specifying the dom and cod of the map

    #print(len(ones_dom_cells))
    #print(len(ones_cod_cells))

    #print(len(domain_cells))



    
    
    

    













def main():

    cell__bijection_testing()



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
