from khtfilegenerator import knotinfo_string_to_integer_array
from outputcomparer import khtfile_parser
import os, pickle
import csv

f=open("braid_reps_from_ki/knots_up_to_12.csv", "r")
f.readline() #discard 1st line


output_csv_data=[]


testamount=100000
testcount=0

while True:
    testcount=testcount+1
    if testamount==testcount:
        break

    line=f.readline().split(",")
    if len(line)==1:
        break
    
    braid=line[1].strip()
    knot_name=line[0].strip()

    #folderpath="braid_data/"+knot_name+"/"

    """
    #get unmatched cell count
    unm_filepath="khtfiles/"+knot_name+"/unmatched_words.pkl"
    unmcount=None
    with open(unm_filepath, 'rb') as file:
        unmcount=len(pickle.load(file))
    
    
    #get lex cell count
    lex_filepath=folderpath+"lex_cells.pkl"
    lexcount=0
    with open(lex_filepath, 'rb') as file:
        lexcount=len(pickle.load(file))
    

    #get total cell count
    tot_filepath="khtfiles/"+knot_name+"cellcount.txt"
    tot=open(tot_filepath)
    totcount=int(tot.readline())
    
    lexcount=-1
    #totcount=-1

    """

    
    #get gr/lex/tot cell counts
    file_path="../../vanhan_koneen_tikku/braid_data/"+knot_name+"/gr_lex_tot_counts.txt"
    fff=open(file_path, "r")
    fff.readline() #discard 1st line
    data=fff.readline()
    #print("asdadsdasdsa")
    #print(data)
    data=data.split(",")
    unmcount=int(data[2])
    lexcount=int(data[3])
    totcount=int(data[4])
    

    #get stringcount
    
    stringcount=max(max(knotinfo_string_to_integer_array(braid)),-min(knotinfo_string_to_integer_array(braid)))+1
    
    #get kht cell count
    khtcount=-222222222
    #if stringcount==2:
    #    khtcount=unmcount
    print(knot_name)
    if 2<stringcount<7:
        kht_filepath="../../vanhan_koneen_tikku/braid_data/"+knot_name+"/"+knot_name+"/cx-c2"
        kht_dict=khtfile_parser(kht_filepath)
        #print(kht_dict)
        khtcount=0

        for key in kht_dict:
            khtcount+=kht_dict[key]
        
        #print(knot_name,khtcount)
    elif stringcount==2:
        khtcount=unmcount
        #print(knot_name)
        #print(stringcount)
    

    ki_braid=braid.split(";{")
    ki_braid=ki_braid[0]
    #print(khtcount)
    #print((knot_name,ki_braid,khtcount,unmcount,lexcount, totcount))
    
    output_csv_data.append((knot_name,ki_braid,khtcount,unmcount,lexcount, totcount))
        


"""
    print(knot_name)
    print(stringcount)
    print(khtcount)
    print(unmcount)
    print(lexcount)
    print(totcount)
    
    print("")
"""


#write counts to csv
with open('output.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    headers=("knot name","braid rep","min cell count from kht++","greedy matching cell count","lex matching cell count", "total cell count of delooped complex")
    writer.writerow(headers)
    
    for row in output_csv_data:
        writer.writerow(row)



