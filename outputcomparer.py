from braidalgo import generate_unmatched_words_with_degs, generate_next_unmatched_words,connectivity_tuple_of_cell,generate_all_enhanced_words,generate_next_enhanced_words, generate_lex_unmatched_words, generate_unmatched_cell_history
from khtfilegenerator import knotinfo_string_to_integer_array
import os.path
import pickle
import sys

#idea: generate dictionaries from both programs with keys being integer pairs (hdeg,qdeg) and values being positive integers (#number of generator of that deg)

def collapse_dictionarycounts(braid,old_dict):
    collapsed_dict=dict()
    while len(old_dict)>0:

        
        (key,value)=old_dict.popitem()
        #print(key)
        #print(value)
        #print(old_dict)

        
        conn=connectivity_tuple_of_cell(braid,key)

        sum_of_counts=value
        for cell in old_dict.keys():
            if conn==connectivity_tuple_of_cell(braid,cell):
                sum_of_counts+=old_dict[cell]
                old_dict[cell]=0

        collapsed_dict[key]=sum_of_counts
    
    cleaned_from_zeros=dict()
    for cell in collapsed_dict:
        if collapsed_dict[cell]>0:
            cleaned_from_zeros[cell]=collapsed_dict[cell]

    return cleaned_from_zeros




def total_number_of_cells(braid):
    count_dict=dict()
    count_dict[""]=1
    #print(count_dict)

    
    for i in range(len(braid)):
        new_cells=generate_next_enhanced_words(count_dict.keys(),braid[:(i+1)])
        
        #copying the multiplicities from the previous ones
        new_dict=dict()
        for cell in new_cells:
            new_dict[cell]=count_dict[cell[:-1]]
        #print(new_dict)

        
        #collapsing the new dictionary to a representative
        if i>0:        
            count_dict=collapse_dictionarycounts(braid[:(i+1)],new_dict)
            #print(count_dict)
        else:
            count_dict=new_dict

    #print(count_dict)

    sum_of_values=0
    for key in count_dict:
        sum_of_values+=count_dict[key]

    return sum_of_values

def total_cell_counting_fails(braid):
    if(len(generate_all_enhanced_words(braid))!=total_number_of_cells(braid)):
        print("AASDDDSADASDASDSADSDSADSDASADADS")


def mirror_connectivity(connectivity):
    #return connectivity
    stringcount=0
    for pair in connectivity:
        stringcount=max(stringcount, max(pair))
    stringcount=round(stringcount/2)

    def mirror_pos(pos,stringcount):
        if pos<=stringcount:
            return pos +stringcount
            #return pos
            #return stringcount-pos+1
        else:
            return pos - stringcount
            #return pos
            #return 3*stringcount-pos+1

    new_list_of_pairs=[]

    for pair in connectivity:
        new_pair=[mirror_pos(pair[0],stringcount),mirror_pos(pair[1],stringcount)]
        new_pair=tuple(sorted(new_pair))
        new_list_of_pairs.append(new_pair)
    return(tuple(sorted(new_list_of_pairs)))

def integer_array_to_knotscape_string(arr):
    result = ""
    for num in arr:
        if num > 0:
            # Convert positive integers to lowercase letters (1 -> 'a', 2 -> 'b', etc.)
            result += chr(ord('a') + num - 1)
        elif num < 0:
            # Convert negative integers to uppercase letters (-1 -> 'A', -2 -> 'B', etc.)
            result += chr(ord('A') - num - 1)
        else:
            # Handle zero (optional, you can omit this part if needed)
            result += "0"
    return result

def khtfile_parser(file_path):
    result_dict = {}
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            # Check if we've reached the "=== diffs ===" section
            if line == "=== diffs ===":
                return result_dict

            
            if line.startswith("object"):
                # Extract data from the line
                start_index = line.find("(h=")
                end_index = line.find(")", start_index)
                if start_index != -1 and end_index != -1:
                    data = line[start_index + 3:end_index]
                    data=data.split(',')
                    h=int(data[0])
                    qstring=(data[1])[3:]
                    q=int(qstring)
                    key = (h, q)        
                    # Update the dictionary
                    if key in result_dict:
                        result_dict[key] += 1
                    else:
                        result_dict[key] = 1        
    print("failed to stop reading file")
    return result_dict

def khtfile_parser2(file_path):
    result_dict = {}
    new_object_key=(None,None,None)
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            # Check if we've reached the "=== diffs ===" section
            if line == "=== diffs ===":
                return result_dict

            
            if line.startswith("object"):
                # Extract h,q
                start_index = line.find("(h=")
                end_index = line.find(")", start_index)
                if start_index != -1 and end_index != -1:
                    data = line[start_index + 3:end_index]
                    data=data.split(',')
                    h=int(data[0])
                    qstring=(data[1])[3:]
                    q=int(qstring)
                    new_object_key = (h, q, None)
            connectivity=[]
            if line.startswith("arcs:  "):
                data = line[7:len(line)]
                data=data.split(" ")
                for pair in data:
                    pair=pair.split("–")
                    s=int(pair[0])+1
                    e=int(pair[1])+1
                    connectivity.append((s,e)) 
                new_object_key=(new_object_key[0],new_object_key[1],tuple(mirror_connectivity(connectivity)))
                #print(new_object_key)
                # Update the dictionary
                if new_object_key in result_dict:
                    result_dict[new_object_key] += 1
                else:
                    result_dict[new_object_key] = 1        
    print("failed to stop reading file")
    return result_dict




def unmatched_words_with_degs_into_degs_dictionary(unmatched_words):

    result_dict={}

    for word_deg_tuple in unmatched_words:
        key= (word_deg_tuple[1],word_deg_tuple[2])
        if key in result_dict:
            result_dict[key] += 1
        else:
            result_dict[key] = 1
    return result_dict               

def unmatched_words_with_degs_into_degs_dictionary2(braid,unmatched_words):

    result_dict={}

    for word_deg_tuple in unmatched_words:
        key= (word_deg_tuple[1],word_deg_tuple[2],tuple(connectivity_tuple_of_cell(braid,word_deg_tuple[0])))
        if key in result_dict:
            result_dict[key] += 1
        else:
            result_dict[key] = 1
    return result_dict               





def dictionary_size(dictionary):
    s=0
    for key in dictionary:
        s+=dictionary[key]
    return s

def dictionary_difference(DMT_degs, khtpp_degs):
    DMT_minus_kht={}
    kht_minus_DMT={}
    
    for key in DMT_degs:
        if key in khtpp_degs:
            D_minus_k=DMT_degs[key]-khtpp_degs.pop(key)

            if D_minus_k>0:
                DMT_minus_kht[key]=D_minus_k
            elif D_minus_k<0:
                kht_minus_DMT[key]=-D_minus_k
        else:
            DMT_minus_kht[key]=DMT_degs[key]
    #union
    kht_minus_DMT.update(khtpp_degs)
    
    return (DMT_minus_kht,kht_minus_DMT)







def main():
    #braid="aaaaaaaaaaaaaaaaa"

    #print(len(generate_all_enhanced_words(braid)))
    #a=total_number_of_cells(braid)
    #print(a)


    #sys.exit(1)
    


    
    
    f=open("braid_reps_from_ki/knots_up_to_12.csv", "r")
    f.readline() #discard 1st line

    DMT_cell_amounts=0
    kht_cell_amounts=0

    testamount=1000000
    testcount=0

    tot_cell_amounts=0
    
    total_number_of_braids=0
    minimality_obtained=0
    
    while True:
        testcount=testcount+1
        if testamount==testcount:
            break


        #read knotinfo database line by line and extract the name of the braid and its knotscape notation 
        line=f.readline().split(",")
        if len(line)==1:
            break

        braid_name=line[0]
        ki_braid=knotinfo_string_to_integer_array(line[1].strip())
        ks_braid=integer_array_to_knotscape_string(ki_braid)

        #if braid_name!="9_32":
        #    continue

        print(braid_name)
        print(ks_braid)
        #total_cell_counting_fails(ks_braid)


        filepath='braid_data/'+braid_name+'/gr_lex_tot_counts.txt'

        #if file is not found
        if os.path.exists(filepath):
           continue 


        gr_cell_count=0
        lex_cell_count=0
        tot_cell_count=0

        #calculate the counts here
        gr_cells=generate_unmatched_cell_history(ks_braid)
        gr_cells=gr_cells[-1]
        gr_cell_count=len(gr_cells)

        lex_cells=generate_lex_unmatched_words(ks_braid)
        lex_cell_count=len(lex_cells)

        tot_cell_count=total_number_of_cells(ks_braid)

        
        #write lines to file
        firstline="knot name, braid representative, gr cell count, lex cell count, tot cell count"
        secondline=braid_name+"," +ks_braid+","+str(gr_cell_count)+","+str(lex_cell_count)+","+str(tot_cell_count)

        print(firstline)
        print(secondline)

        resultfile = open(filepath, 'w')
        resultfile.write(firstline+ "\n")
        resultfile.write(secondline)
        resultfile.close

        

        
        
        #Load or calculate total number of cells in the complex
        cell_count=None
        cell_count_path='braid_data/'+braid_name+'/totalcellcount.txt'
        if os.path.exists(cell_count_path):
            ffff=open(cell_count_path,"r")
            cell_count=int(ffff.read())
            ffff.close()
        else:
            cell_count=total_number_of_cells(ks_braid)
            ffff = open(cell_count_path, "w")
            ffff.write(str(cell_count))
            ffff.close()
        print(cell_count)
        tot_cell_amounts+=cell_count
        #print(tot_cell_amounts)
        

        #Load or calculate unmatched cells of the braid 
        unmatched_words=None
        #unmatched_words_path='braid_data/'+braid_name+'/unmatched_cells.pkl'
        #unmatched_words_path='braid_data/'+braid_name+'/lex_cells.pkl'
        unmatched_words_path='khtfiles/'+braid_name+'/unmatched_words.pkl'

        if os.path.exists(unmatched_words_path):
            with open(unmatched_words_path, 'rb') as file:
                unmatched_words = pickle.load(file)
        
        #else:      
        #    unmatched_words=generate_unmatched_words_with_degs(ks_braid)
        #    with open(unmatched_words_path, 'wb') as file:
        #        pickle.dump(unmatched_words, file)

        

        #Reformat the DMT-calculated data into a dictionary
        DMT_degs=unmatched_words_with_degs_into_degs_dictionary(unmatched_words)  #TOGGLE CONNECTIVITY CHECK HERE
        #DMT_degs=unmatched_words_with_degs_into_degs_dictionary2(ks_braid,unmatched_words)
        




        


        #Recover the cells calculated by kht++ from a file and read them into a dictionary
        two_string_braid=True
        if max(max(ki_braid), -min(ki_braid))>1:
            two_string_braid=False

        cx_file_path="khtfiles/"+braid_name+"/cx-c2"
        khtpp_degs=None
        if os.path.exists(cx_file_path):
            khtpp_degs=khtfile_parser(cx_file_path)     #TOGGLE CONNECTIVITY CHECK HERE
            #khtpp_degs=khtfile_parser2(cx_file_path)
        elif not two_string_braid:
            print("did not find cx-c2 file and the tangle has more than 4 outputs")


        #Compare the two dictionaries

        if not (khtpp_degs==None):

            DMT_degs_copy=DMT_degs.copy()
            khtpp_degs_copy=khtpp_degs.copy()
            (DMT_minus_kht,kht_minus_DMT)=dictionary_difference(DMT_degs_copy,khtpp_degs_copy)


            DMT_cell_amounts+=dictionary_size(DMT_degs)
            kht_cell_amounts+=dictionary_size(khtpp_degs)

            
            total_number_of_braids+=1
            if len(DMT_minus_kht)==0:
                minimality_obtained+=1
            

            #Alert if unwanted things happen    
            if len(kht_minus_DMT)>0:
                print("")
                print("DMT")
                print(DMT_degs)
                print("kht++")
                print(khtpp_degs)
                print("Difference")
                print(DMT_minus_kht)
                print(kht_minus_DMT)
            




            """
            if not(len(DMT_minus_kht)==0 or len(khtpp_degs)==0):
                print("")
                print("DMT")
                print(DMT_degs)
                print("kht++")
                print(khtpp_degs)
                print("Difference")
                print((DMT_minus_kht,kht_minus_DMT))
                #print(len(DMT_minus_kht))
            """



            #print("")
            #print("DMT")
            #print(DMT_degs)
            #print("kht++")
            #print(khtpp_degs)
            #print(dictionary_difference(DMT_degs,khtpp_degs))


        #print(braid_name)
        #print(ki_braid)
        #print(ks_braid)
        #print(unmatched_words)
    

    return

    #Print some results
    print("#cells in Morse complexes: " + str(DMT_cell_amounts))
    print("#cells in minimal complexes: " + str(kht_cell_amounts))
    print("ratio of Morse to minimal: "+str(DMT_cell_amounts/kht_cell_amounts))
    print("#cells in total complexes: "+ str(tot_cell_amounts))
    print("ratio of total to minimal: "+str(tot_cell_amounts/kht_cell_amounts))
    

    print("total number of braids: "+str(total_number_of_braids))
    print("#braids with minimality obtained: "+str(minimality_obtained))
    
    #dictionary=khtfile_parser("khtfiles/5_2/cx-c2")
    #print(dictionary)




   




if __name__ == "__main__":
    main()
    
