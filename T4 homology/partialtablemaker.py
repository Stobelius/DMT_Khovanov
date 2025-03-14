import re
import json
import math

#this function takes care of the difference in grading convention in khoca
def flip_dict(d):
    return {(k[0], -k[1]): v for k, v in d.items()}

def ignore_one(d):
    if d==1:
    	return ""
    return str(d)
    
def list_to_latex_string(lst):
    result= ""
    for i in range(len(lst)):
    	if (i==len(lst)-1):
    		result += "\\mathbb{{Z}}^{ " + ignore_one(lst[i][0]) + " }_{ " + ignore_one(lst[i][1]) + " }"
    	else:
            result += "\\mathbb{{Z}}^{ " + ignore_one(lst[i][0]) + " }_{ " + ignore_one(lst[i][1]) + " } \\oplus "
    return "$"+result +"$"

def parse_polynomial(polynomial_string):
    polynomial_dict = {}
    polynomial_list = polynomial_string.split(" + ")
    for term in polynomial_list:
        coefficient = term.split()[0]
        if coefficient == "":
            coefficient = "1"
        if "t^" in term and "q^" in term:
            t_exponent = re.findall(r"t\^(-?\d+)", term)[0]
            q_exponent = re.findall(r"q\^(-?\d+)", term)[0]
            key = (int(t_exponent), int(q_exponent))
            if "[" in term:
                monomial_number = int(re.findall(r"\[(\d+)\]", term)[0])
            else:
                monomial_number = 1
            if coefficient[0] == "t":
                value = (1, monomial_number)
            else:
                value = (int(coefficient.split("t")[0]), monomial_number)
            if key in polynomial_dict:
                polynomial_dict[key].append(value)
            else:
                polynomial_dict[key] = [value]
                
    return polynomial_dict
    
def domain_inequality_indicator(i,j,n):
    indicatorstring=""
    return indicatorstring
    a=-9*n+4*i -3* j
    b=-2*n+2*i-j
    
    if a>=41:
        indicatorstring=indicatorstring+"A"
    elif a<-17:
        indicatorstring=indicatorstring+"C"
        
    if b>=14:
        indicatorstring=indicatorstring+"B"
    elif b<-6:
        indicatorstring=indicatorstring+"D"
    
    return indicatorstring

    
def codomain_inequality_indicator(i,j,n):
    indicatorstring=""
    return indicatorstring
    a=-9*n+4*i -3* j
    b=-2*n+2*i-j
    
    if -9*(n-4)+4*(i+8) -3* (j+24)>=41:
        indicatorstring=indicatorstring+"c"
    if a<-17:
        indicatorstring=indicatorstring+"n"
        
    if -2*(n-4)+2*i-(j+12)>=14:
        indicatorstring=indicatorstring+"a"
    if b<-6:
        indicatorstring=indicatorstring+"n"
    
    return indicatorstring



def extract_integer(s):
    match = re.match(r"\$(\-?\d+)\$", s)
    if match:
        return int(match.group(1))
    else:
        raise ValueError("Input string is not in the expected format.")
    
    

def create_latex_table(polynomial_dict,n):

    """
    filtered_dict= {}
    for key in polynomial_dict:
    	if key[0]<=-4*math.floor(n/2)+6:
    	    filtered_dict[key]=polynomial_dict[key]
    if len(filtered_dict)==0:
    	filtered_dict[(0,0)]=[(1, 2)]
    polynomial_dict=filtered_dict
    """

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
        #print(value)
        row_index = key[0] - t_min + 1
        column_index = columns-(key[1] - q_min)//2 - 1
        table[row_index][column_index] = str(list_to_latex_string(value)) #muuta tämä latexiksi
        
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
    
    
    #for row in transpose:
    #    row.insert(0, row.pop())    
    
    table=transpose
    temp=columns
    columns=rows
    rows=temp
    ###
    
    ######Here I could add the inequalities to the mix
    #get i and j from headers
    #get n from the json

    for k in range(1,len(table[0])):
        
        for l in range(1,len(table)):
            string_i=table[0][k]
            i=extract_integer(string_i)
            j=extract_integer(table[l][0])

            table[l][k]=table[l][k]+codomain_inequality_indicator(i,j,n)
        
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

# Opening JSON file
with open('T4_100_unred.json') as f:
    data = json.load(f)

"""
# Open output file
with open('texTableOutput.tex', 'w') as f:
    # Write the LaTeX header to the output file
    f.write("\\documentclass{article}\n")
    f.write("\\usepackage{graphicx}\n")
    f.write("\\usepackage{amssymb}\n")
    f.write("\\usepackage[paperwidth=400cm,paperheight=100cm,margin=1in]{geometry}\n")
    f.write("\\title{Khovanov tables test}\n")
    f.write("\\author{tuomas.kelomaki }\n")
    f.write("\\date{June 2023}\n")
    f.write("\\begin{document}\n")
    f.write("\\maketitle\n")
    # Iterate over the data list
    for item in data:
        # Write the braidname to the output file
        f.write(item['braidname'] + '\n \n')
        n=round(len(item['braidname'])/3)
        #n=61
        #print(item['braidname'])
        #print(n)
        
        # Parse the polynomial and create the LaTeX table
        table = create_latex_table(flip_dict(parse_polynomial(item['polynomial'])),n)
        
        # Write the table to the output file
        f.write(table + '\\newpage \n')


    # Write the LaTeX footer to the output file
    f.write("\\end{document}\n")
"""

def t_satisfies_figure_1_description(t,khdict):
    
    
    if t<27:
        print("t="+ str(t) +"fails")
        return

    #t even
    if t%2==0:
        

        n=round(t/2)

        filtered_dict= {}
        for key in khdict:
            i=key[0]
            j=key[1]

            
            if j<=(3/2)*i -6*n-1:
                print("t="+ str(t) +"failsdsasad")
                return
            cond=(-4*n+11<=i)and(i<=-42)and(j<=((3/2)*i-6*n+5))
    	    

            if cond:
                filtered_dict[key]=khdict[key]
    
    #if t==28:
    #    print(filtered_dict)

        #from consoleoutput of t=28 I copied
        model_dict={(-45, -148): [(2, 1), (2, 2), (1, 4)], (-45, -150): [(1, 1), (2, 2), (1, 4)], (-44, -146): [(2, 1), (2, 2), (1, 4)], (-44, -148): [(1, 1), (1, 2), (1, 4)], (-44, -150): [(1, 1)], (-43, -144): [(2, 1), (2, 2), (1, 4)], (-43, -146): [(2, 1), (2, 2), (1, 4)], (-42, -142): [(2, 1), (2, 2), (1, 4)], (-42, -144): [(1, 1), (2, 2), (1, 4)], (-42, -146): [(1, 1), (1, 2)], (-45, -152): [(1, 2)], (-43, -148): [(1, 2), (1, 4)]}
        
        for key in filtered_dict:
            piecenum=math.floor((-42-key[0])/4)

            
            #print("")
            #print(piecenum)
            model_h=key[0]+4*piecenum
            model_q=key[1]+6*piecenum+(6*(n-14))
            model_key=(model_h,model_q)
            #print(key)
            #print(model_key)
            
            if not(filtered_dict[key]==model_dict[model_key]):
                return
            
        print("success"+str(t))

    #t odd
    if t%2==1:
        n=math.floor(t/2)

        filtered_dict= {}
        for key in khdict:
            i=key[0]
            j=key[1]

            
            if j<=(3/2)*i -6*n-4:
                print("t="+ str(t) +"failsdsasad")
                return
            cond=(-4*n+7<=i)and(i<=-42)and(j<=((3/2)*i-6*n+2))
    	    

            if cond:
                filtered_dict[key]=khdict[key]
        #if t==27:
        #    print(filtered_dict)

        model_dict={(-45, -145): [(2, 1), (2, 2), (1, 4)], (-45, -147): [(1, 1), (2, 2), (1, 4)], (-44, -143): [(2, 1), (2, 2), (1, 4)], (-44, -145): [(1, 1), (1, 2), (1, 4)], (-44, -147): [(1, 1)], (-43, -141): [(2, 1), (2, 2), (1, 4)], (-43, -143): [(2, 1), (2, 2), (1, 4)], (-42, -139): [(2, 1), (2, 2), (1, 4)], (-42, -141): [(1, 1), (2, 2), (1, 4)], (-42, -143): [(1, 1), (1, 2)], (-45, -149): [(1, 2)], (-43, -145): [(1, 2), (1, 4)]}

        for key in filtered_dict:
            piecenum=math.floor((-42-key[0])/4)

            
            #print("")
            #print(piecenum)
            model_h=key[0]+4*piecenum
            model_q=key[1]+6*piecenum+(6*(n-13))
            model_key=(model_h,model_q)
            #print(key)
            #print(model_key)
            
            if not(filtered_dict[key]==model_dict[model_key]):
                return
            
        print("success"+str(t))




#Verifying some early cases of 4 strand torus links, before the induction kicks in
for item in data:
    n=round(len(item['braidname'])/3)
    khdict=flip_dict(parse_polynomial(item['polynomial']))

    t_satisfies_figure_1_description(n,khdict)


#polynomial_dict = parse_polynomial(polynomial_string)
#latex_table = create_latex_table(polynomial_dict)
#print(polynomial_dict)
#print(latex_table)
