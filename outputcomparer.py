from braidalgo import generate_unmatched_words_with_degs
from khtfilegenerator import knotinfo_string_to_integer_array
import os.path
import pickle

#idea: generate dictionaries from both programs with keys being integer pairs (hdeg,qdeg) and values being positive integers (#number of generator of that deg)



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

def unmatched_words_with_degs_into_degs_dictionary(unmatched_words):

    result_dict={}

    for word_deg_tuple in unmatched_words:
        key= (word_deg_tuple[1],word_deg_tuple[2])
        if key in result_dict:
            result_dict[key] += 1
        else:
            result_dict[key] = 1
    return result_dict               

def dictionary_size(dict):
    s=0
    for key in dict:
        s+=dict[key]
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
    f=open("knotinfodb.csv", "r")
    f.readline() #discard 1st line

    DMT_cell_amounts=0
    kht_cell_amounts=0

    testamount=100000
    testcount=0

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

        
        print(braid_name)
        
        #Load or calculate unmatched cells of the braid 
        unmatched_words=None
        unmatched_words_path='khtfiles/'+braid_name+'/unmatched_words.pkl'
        if os.path.exists(unmatched_words_path):
            with open(unmatched_words_path, 'rb') as file:
                unmatched_words = pickle.load(file)
        else:      
            unmatched_words=generate_unmatched_words_with_degs(ks_braid)
            with open(unmatched_words_path, 'wb') as file:
                pickle.dump(unmatched_words, file)

        #Reformat the DMT-calculated data into a dictionary
        DMT_degs=unmatched_words_with_degs_into_degs_dictionary(unmatched_words)

        #Recover the cells calculated by kht++ from a file and read them into a dictionary
        two_string_braid=True
        if max(max(ki_braid), -min(ki_braid))>1:
            two_string_braid=False

        cx_file_path="khtfiles/"+braid_name+"/cx-c2"
        khtpp_degs=None
        if os.path.exists(cx_file_path):
            khtpp_degs=khtfile_parser(cx_file_path)
        elif not two_string_braid:
            print("did not find cx-c2 file and the tangle has more than 4 outputs")


        #Compare the two dictionaries

        if not (khtpp_degs==None):
            #DMT_degs.popitem()  
            #khtpp_degs.popitem()
            DMT_degs_copy=DMT_degs.copy()
            khtpp_degs_copy=khtpp_degs.copy()
            (DMT_minus_kht,kht_minus_DMT)=dictionary_difference(DMT_degs_copy,khtpp_degs_copy)

            DMT_cell_amounts+=dictionary_size(DMT_degs)
            kht_cell_amounts+=dictionary_size(khtpp_degs)
            

            #Alert if unwanted things happen    
            if len(kht_minus_DMT)>0:
                print("")
                print("DMT")
                print(DMT_degs)
                print("kht++")
                print(khtpp_degs)
                print("Difference")
                print((DMT_minus_kht,kht_minus_DMT))
            




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
    

    #Print some results
    print(DMT_cell_amounts)
    print(kht_cell_amounts)
    print(DMT_cell_amounts/kht_cell_amounts)
    
    #dictionary=khtfile_parser("khtfiles/5_2/cx-c2")
    #print(dictionary)




   




if __name__ == "__main__":
    main()
    
