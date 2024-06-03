from braidalgo import qdeg_of_word, hdeg_of_word, generate_unmatched_cell_history, connectivity_tuple_of_cell, add_degs,sort_by_hdeg, number_of_strands
from path_and_cell_analysis_forT4 import load_cells
import sys, pickle
from collections import deque

paperwidth=200  #cm
paperheight=100  #cm

def number_to_letter(number):
    if 1 <= number <= 26:
        return chr(ord('A') + number - 1)
    elif number<=52:
        return  chr(ord('a') + number - 1-26)
    return("Ö"+str(number))


def order_pairs(list_of_pairs):
    new_list=[]
    for a in list_of_pairs:
        if a[0]>a[1]:
            new_list.append((a[1],a[0]))
        else:
            new_list.append(a)
    return new_list

def list_to_pair_list(orig_list):
    pair_list=[]
    for i in range(int(len(orig_list)/2)):
        pair=(orig_list[2*i],orig_list[2*i+1])
        pair_list.append(pair)
    
    return pair_list

def mirror_bottom_row(orig_list,strands):
    new_list=[]
    for i in range(len(orig_list)):
        orig_num=orig_list[i]
        #print(orig_num)
        if orig_num>strands:
            new_list.append(3*strands-orig_num+1)
        else:
            new_list.append(orig_num)
    return new_list


def generate_connectivity_array(strands):
    connectivities_under_construction=deque()
    connectivities_under_construction.append([1])

    ready_connections=[]

    while len(connectivities_under_construction)>0:
        con_list=connectivities_under_construction.pop()
        #print(con_list)
        

        if(len(con_list)==2*strands):
            ready_connections.append(con_list)

        if len(con_list)%2==1:
            last_item=con_list[len(con_list)-1]
            for n in range(1,2*strands+1,1):
                if not(n in con_list) and (n+last_item)%2==1:
                    nonplanarity=False
                    for i in range(last_item+1,n,1):
                        if(i in con_list):
                            nonplanarity=True
                    
                    if not nonplanarity:
                        copied_list=con_list.copy()
                        copied_list.append(n)
                        connectivities_under_construction.append(copied_list)
        else:
            for n in range(1,2*strands+1,1):
                if not(n in con_list):
                    copied_list=con_list.copy()
                    copied_list.append(n)
                    connectivities_under_construction.append(copied_list)
                    break

    for i in range(len(ready_connections)):
        ready_connections[i]=mirror_bottom_row(ready_connections[i],strands)    
    readys_as_pairs=[]

    for a in ready_connections:
        pair_list=list_to_pair_list(a)
        #print("ereer")
        #print(pair_list)

        pair_list=order_pairs(pair_list)
        pair_list=sorted(pair_list, key=lambda p: p[0])
        #print(pair_list)


        readys_as_pairs.append(pair_list)

    return readys_as_pairs

    



def connectivity_symbol(table, connectivity):
    for i in range(len(table)):
        if table[i]==connectivity:
            return number_to_letter(i+1)
    print(connectivity)
    print(table)


#output is dictionary with keys (h,q) pairs and and values are dictionaries of with keys as characters outputted by number to char representing connectivity diagrams and values representing the amounts of cells of those kinds 
def degs_to_connectivity_counts(braid,word_deg_triples):
    strands=number_of_strands(braid)
    conn_table=generate_connectivity_array(strands)

    degs_to_conns=dict()

    for triple in word_deg_triples:
        hq_key=(triple[1],triple[2])
        connectivity=connectivity_tuple_of_cell(braid,triple[0])
        
        #print(connectivity)
        #print(conn_table)
        
        conn_symbol=connectivity_symbol(conn_table,connectivity)
                
        if not (hq_key in degs_to_conns):
            #print("asddsa")
            new_dict=dict()
            new_dict[conn_symbol]=1
            degs_to_conns[hq_key]=new_dict
        else:
            old_dict=degs_to_conns[hq_key]            
            new_dict=old_dict.copy()
            if conn_symbol in new_dict:
                
                new_dict[conn_symbol]=new_dict[conn_symbol]+1
            else:
                
                new_dict[conn_symbol]=1
            degs_to_conns[hq_key]=new_dict
    
    return degs_to_conns
            

def entry_dict_to_str(entry_dict):
    keys=entry_dict.keys()
    keys=sorted(keys)
    output=""
    first=True
    for key in keys:
        if first:
            first=False
        else:
            output=output+"+"
        output=output+str(entry_dict[key])+key
    return output
    



#Fix this in order to read both odd and even rows



def create_latex_table2(polynomial_dict):
    t_min = min([key[0] for key in polynomial_dict.keys()])
    t_max = max([key[0] for key in polynomial_dict.keys()])
    q_min = min([key[1] for key in polynomial_dict.keys()])
    q_max = max([key[1] for key in polynomial_dict.keys()])
    print(t_min)
    print(t_max)
    print(q_min)
    print(q_max)
    
    rows = t_max - t_min + 2
    columns = (q_max - q_min) + 2
    table = [["" for j in range(columns)] for i in range(rows)]
    
    # Add row and column headers
    row_headers = ["$" + str(t_max+t_min-t) + "$" for t in range(t_max +1, t_min - 1,-1)]
    column_headers = ["$" + str(q_max+q_min-q) + "$" for q in range(q_min - 1, q_max + 1,1)]
    column_headers[0] = ""
    
    # Fill table with values from dictionary
    for key, value in polynomial_dict.items():
        row_index = key[0] - t_min + 1
        column_index = columns-(key[1] - q_min) - 1
        table[row_index][column_index] = entry_dict_to_str(value) #muuta tämä latexiksi
        
    # Add row and column headers to table
    for i in range(rows):
        table[i][0] = row_headers[i]
    for j in range(columns):
        table[0][j] = column_headers[j]
        
    ###################### Notice that we have been accidentally working with the transpose of the original diagram, lets fix it
    #table = list(zip(*table))
	    
    transpose = []
    for i in range(len(table[0])):
        row = []
        for j in range(len(table)):
            #row.append(table[len(table)-j-1][len(table[0])-i-1])
            row.append(table[j][i])
        transpose.append(row)
   
    table=transpose
    temp=columns
    columns=rows
    rows=temp
    ###
    
     
        
    latex_table = "\\begin{tabular}{|" + "c|" * columns + "}\n"
    latex_table += "\\hline\n"
    
    # Add column headers to table
    latex_table += " & ".join(table[0]) + "\\\\\n"
    
    # Add rows to table
    latex_table += "\\hline\n"
    for row_index, row in enumerate(table[1:]):
        latex_table += " & ".join(row) + "\\\\\n"
        latex_table += "\\hline\n"
        
    latex_table += "\\end{tabular}"
    
    return latex_table


def create_latex_table(polynomial_dict):
    t_min = min([key[0] for key in polynomial_dict.keys()])
    t_max = max([key[0] for key in polynomial_dict.keys()])
    q_min = min([key[1] for key in polynomial_dict.keys()])
    q_max = max([key[1] for key in polynomial_dict.keys()])
    rows = t_max - t_min + 2
    columns = (q_max - q_min)//2 + 2
    table = [["" for j in range(columns)] for i in range(rows)]
    
    # Add row and column headers
    row_headers = ["$" + str(t_max+t_min-t) + "$" for t in range(t_max +1, t_min - 1,-1)]
    column_headers = ["$" + str(q_max+q_min-q) + "$" for q in range(q_min - 2, q_max + 2,2)]
    column_headers[0] = ""
    
    # Fill table with values from dictionary
    for key, value in polynomial_dict.items():
        row_index = key[0] - t_min + 1
        column_index = columns-(key[1] - q_min)//2 - 1
        table[row_index][column_index] = entry_dict_to_str(value) #muuta tämä latexiksi
        
    # Add row and column headers to table
    for i in range(rows):
        table[i][0] = row_headers[i]
    for j in range(columns):
        table[0][j] = column_headers[j]
        
    ###################### Notice that we have been accidentally working with the transpose of the original diagram, lets fix it
    #table = list(zip(*table))
	    
    transpose = []
    for i in range(len(table[0])):
        row = []
        for j in range(len(table)):
            #row.append(table[len(table)-j-1][len(table[0])-i-1])
            row.append(table[j][i])
        transpose.append(row)
   
    table=transpose
    temp=columns
    columns=rows
    rows=temp
    ###
    
     
        
    latex_table = "\\begin{tabular}{|" + "c|" * columns + "}\n"
    latex_table += "\\hline\n"
    
    # Add column headers to table
    latex_table += " & ".join(table[0]) + "\\\\\n"
    
    # Add rows to table
    latex_table += "\\hline\n"
    for row_index, row in enumerate(table[1:]):
        latex_table += " & ".join(row) + "\\\\\n"
        latex_table += "\\hline\n"
        
    latex_table += "\\end{tabular}"
    
    return latex_table


def write_latex_file(braid,latex_table):
    with open('latex_plots/'+braid+'.tex', 'w') as f:
    # Write the LaTeX header to the output file
       f.write("\\documentclass{article}\n")
       f.write("\\usepackage{graphicx}\n")
       f.write("\\usepackage{amssymb}\n")
       f.write("\\usepackage[paperwidth="+str(paperwidth)+"cm,paperheight="+str(paperheight)+"cm,margin=1in]{geometry}\n")
       f.write("\\title{Khovanov tables test}\n")
       f.write("\\author{tuomas.kelomaki }\n")
       f.write("\\date{June 2023}\n")
       f.write("\\begin{document}\n")
       f.write("\\maketitle\n")
       
       f.write(braid+"\n")
       f.write(latex_table)
       
       """
       # Iterate over the data list
       for item in data:
           # Write the braidname to the output file
           f.write(item['braidname'] + '\n \n')
           
           # Parse the polynomial and create the LaTeX table
           table = create_latex_table(flip_dict(parse_polynomial(item['polynomial'])))
           
           # Write the table to the output file
           f.write(table + '\\newpage \n')


       # Write the LaTeX footer to the output file
       """
       
       f.write("\\end{document}\n")



def load_T5_cells(twistcount):
    file_path="Torus5braids/5string23twist.pkl"

    history=None

    with open(file_path, 'rb') as file:
        history = pickle.load(file)
    unmatched_cells=history[4*twistcount]
    return unmatched_cells


def number_of_diagonals(array_of_triples):
    diagonals=set()
    for triple in array_of_triples:
        diagonals.add(2*triple[1]-triple[2])

    return len(diagonals)







def main():
    if len(sys.argv) != 2:
        print("Give me a braid")
        sys.exit(1)
    braid=sys.argv[1]

    
    history=generate_unmatched_cell_history(braid)
    unmatched_cells=history[len(history)-1]
    
    #unmatched_cells=load_cells(44)
    #braid=44*"abc"


    #unmatched_cells=load_T5_cells(23)
    #braid=23*"abcd"

    word_deg_triples=sort_by_hdeg(add_degs(braid,unmatched_cells))
    degs_dict=degs_to_connectivity_counts(braid,word_deg_triples)
    latex_table=create_latex_table2(degs_dict)

    print(create_latex_table(degs_dict))
    print("number of diagonals: " +str(number_of_diagonals(word_deg_triples)))

    write_latex_file(braid,latex_table)
    


    """
    manyT5_tabulars=""
    for i in range(1,44):
        unmatched_cells=load_cells(i)
        braid=i*"abc"

        word_deg_triples=sort_by_hdeg(add_degs(braid,unmatched_cells))
    
        degs_dict=degs_to_connectivity_counts(braid,word_deg_triples)
        latex_table=create_latex_table2(degs_dict)

        manyT5_tabulars=manyT5_tabulars+"abcd"+str(i)+"\n"+latex_table +"\n \pagebreak \n"


    """








if __name__ == "__main__":
    main()
