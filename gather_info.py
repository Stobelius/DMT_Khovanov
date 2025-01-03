from khtfilegenerator import knotinfo_string_to_integer_array
from outputcomparer import khtfile_parser
import os, pickle

f=open("knotinfo_braids13.csv", "r")

f.readline() #discard 1st line



testamount=30
testcount=0

while True:
    testcount=testcount+1
    if testamount==testcount:
        break

    line=f.readline().split(",")
    if len(line)==1:
        break
    
    braid=line[1].strip()
    braid_name=line[0].strip()

    folderpath="braid_data/"+braid_name+"/"


    #get unmatched cell count
    unm_filepath=folderpath+"unmatched_cells.pkl"
    unmcount=None
    with open(unm_filepath, 'rb') as file:
        unmcount=len(pickle.load(file))
    
    
    #get lex cell count
    lex_filepath=folderpath+"lex_cells.pkl"
    lexcount=0
    with open(lex_filepath, 'rb') as file:
        lexcount=len(pickle.load(file))

    #get total cell count
    tot_filepath=folderpath+"totalcellcount.txt"
    tot=open(tot_filepath)
    totcount=int(tot.readline())


    #get stringcount
    
    stringcount=max(max(knotinfo_string_to_integer_array(braid)),-min(knotinfo_string_to_integer_array(braid)))+1
    
    #get kht cell count
    khtcount=0
    if stringcount==2:
        khtcount=unmcount
    elif stringcount<10:
        kht_filepath=folderpath+braid_name+"/cx-c2"
        kht_dict=khtfile_parser(kht_filepath)

        for key in kht_dict:
            khtcount+=kht_dict[key]
    else:
        pass



    print(braid_name)
    print(stringcount)
    print(khtcount)
    print(unmcount)
    print(lexcount)
    print(totcount)
    
    print("")


    #write counts to csv

