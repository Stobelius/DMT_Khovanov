f=open("complex_sizes.csv", "r")
    
f.readline() #discard 1st line

def strand_count(ki_braid_rep):
    #print(ki_braid_rep)
    ki_braid_rep = ki_braid_rep.replace("{", "").replace("}", "")
    str_seq=ki_braid_rep.split(";")

    int_seq=[]
    for s in str_seq:
        int_seq.append(int(s))
    
    return max(max(int_seq),-min(int_seq))+1

def braid_is_alternating(ki_braid_rep):
    #print(ki_braid_rep)
    ki_braid_rep = ki_braid_rep.replace("{", "").replace("}", "")
    str_seq=ki_braid_rep.split(";")

    int_seq=[]
    for s in str_seq:
        int_seq.append(int(s))
    
    #print(int_seq)
    
    if int_seq[0]==-1:
        for i in range(len(int_seq)):
            int_seq[i]=int_seq[i]*(-1)
    #print(int_seq)
    
    for i in int_seq:
        if i%2==0 and i>0:
            return False
        elif i%2==1 and i<0:
            return False

    return True

min_count=0
mgr_count=0
mlex_count=0
delooped_count=0

braid_count=0
alternating_count=0

minimality_obtained_alt_mgr=0
minimality_obtained_nonalt_mgr=0
minimality_obtained_alt_lex=0
minimality_obtained_nonalt_lex=0

#testcount=20

#print(braid_is_alternating("{-1;-1;2;-1;-1;2;-1;2}"))


while True:

    line=f.readline().split(",")
    #print(line)
    if len(line)==1:
        break

    #check for acyclic
    if line[-1]=="no\n":
        print(line[0])
        continue

    alternating=braid_is_alternating(line[1])
    
    

    #print(line[1])
    #print(alternating)

    minbr=int(line[2])
    mgrbr=int(line[3])
    mlexbr=int(line[4])
    delbr=int(line[5])

    #print(minbr)
    #print(mgrbr)

    #if(minbr==mgrbr):
    #    print(line[0])

    min_count=min_count+minbr
    mgr_count=mgr_count+mgrbr
    mlex_count=mlex_count+mlexbr
    delooped_count=delooped_count+delbr

    braid_count=braid_count+1
    if(alternating):
        alternating_count=alternating_count+1

        if mgrbr==minbr:
            minimality_obtained_alt_mgr=minimality_obtained_alt_mgr+1
        if mlexbr==minbr:
            minimality_obtained_alt_lex+=1
    else:
        if mgrbr==minbr:
            minimality_obtained_nonalt_mgr+=1
        if mlexbr==minbr:
            minimality_obtained_nonalt_lex+=1
    


print("total cell count min: "+str(min_count))
print("total cell count mgr: "+str(mgr_count))
print("total cell count mlex: "+str(mlex_count))
print("total cell count delooped: "+str(delooped_count))

print("")
print("ratios")
print((min_count*1.0)/(min_count*1.0))
print((mgr_count*1.0)/min_count)
print((mlex_count*1.0)/min_count)
print((delooped_count*1.0)/min_count)

print("")
print("braids :"+str(braid_count))
print("alternating braids: " +str(alternating_count))

print("")
print("minimalities")
print("mgr alt: "+str(minimality_obtained_alt_mgr))
print("mgr nonalt: "+str(minimality_obtained_nonalt_mgr))
print("mgr both"+str(minimality_obtained_alt_mgr+minimality_obtained_nonalt_mgr))
print("mlex alt: "+str(minimality_obtained_alt_lex))
print("mlex nonalt: "+str(minimality_obtained_nonalt_lex))
