def generate_W_n(twistnumber):
    ones_cap=twistnumber+10
    I_3_cap=round(ones_cap/2)
    I_2_cap=round(ones_cap/4)
    
    def ones(set_of_words,cap):
        newset=set()
        for word in set_of_words:
            for i in range(cap):
                newset.add(word+i*"111")
        return newset
    
    def glu1(set_of_words):
        newset=set()
        for word in set_of_words:
            newset.add(word+"000")
            newset.add(word+"001")
            newset.add(word+"010")
            newset.add(word+"011")
        return newset

    def glu2(set_of_words):
        newset=set()
        for word in set_of_words:
            newset.add(word)
            newset.add(word+"100")
            newset.add(word+"110")
            newset.add(word+"00011x")
        return newset
    
    def I_2(set_of_words,cap):
        newset=set()
        for word in set_of_words:
            for i in range(cap):
                newset.add(word+i*"101011x0011x")
        return newset

    def glu4(set_of_words):
        newset=set()
        for word in set_of_words:
            newset.add(word)
            newset.add(word+"101")
            newset.add(word+"101010")
            newset.add(word+"101011")
            newset.add(word+"101011x00")
            newset.add(word+"101011x01")
            newset.add(word+"101011x10")
            newset.add(word+"101011x11")
        return newset
    
    def glu5(set_of_words):
        newset=set()
        for word in set_of_words:
            newset.add(word+"101011x0011x001")
            newset.add(word+"101010x01")
        return newset
    
    def I_3(set_of_words,cap):
        newset=set()
        for word in set_of_words:
            for i in range(cap):
                newset.add(word+i*"01xx01")
        return newset
    
    def glu6(set_of_words):
        newset=set()
        for word in set_of_words:
            newset.add(word)
            newset.add(word+"01x")
        return newset

    def glu3(set_of_words):
        newset=set()
        for word in set_of_words:
            newset.add(word+"00011x001")
            newset.add(word+"100001")
            newset.add(word+"110001")
        return newset

    initial_set=set()
    initial_set.add("")

    W1=glu1(ones(initial_set,ones_cap))
    W2=glu4(I_2(glu2(ones(initial_set,ones_cap)),I_2_cap))
    W3=I_2(glu2(ones(initial_set,ones_cap)),I_2_cap)
    W3=glu6(I_3(glu5(W3),I_3_cap))
    W4=glu6(I_3(glu3(ones(initial_set,ones_cap)),I_3_cap))

    W= W1 | W2 | W3 | W4

    lengthfiltered=set()
    for word in W:
        if len(word)==3*twistnumber:
            lengthfiltered.add(word)
    
    return lengthfiltered

def hdeg(word):
    return -len(word)+word.count("1")

def qdeg(word):
    return -word.count("x")+hdeg(word)-len(word)

def t_A(word):
    return (-1/2)*(len(word)/3)+(1/2)*hdeg(word)-(1/4)*qdeg(word) -1

def t_B(word):
    return 3*(len(word)/3)-(3/2)*hdeg(word)+qdeg(word) -(5/2)

def t_C(word):
    return (-9/4)*(len(word)/3)+hdeg(word)-(3/4)*qdeg(word) -1/4

#Lemma 4.5
print("verifying Lemma 4.5")
for n in range(24):
    W_n=generate_W_n(n)
    for w in W_n:
        if t_A(w) <-3/2 or t_C(w)<-3/2:
            print("verification failed")

print("Base cases for Lemma 4.5 verified")

#Lemma 5.3
print("verifying Lemma 5.3")
for n in range(24):
    W_n=generate_W_n(n)
    for w in W_n:
        if w.count("111111111111")<t_A(w) or w.count("101011x0011x")< t_B(w) or w.count("01xx01") <t_C(w):
            print("verification falied")

print("Base cases for Lemma 5.3 verified")

#Lemma 6.2
def o(cell):
    count = 0
    for char in cell:
        if char == "1":
            count += 1
        else:
            break 
    return count

print("verifying Lemma 6.2")

for n in range(0,83):
    W_n=generate_W_n(n)
    for a in W_n:
        for b in W_n:
            if hdeg(a)+1== hdeg(b) and o(a) <=o(b): 
                if not qdeg(b)<= qdeg(a) +3:
                    print("verification failed")

    print("verified: "+str(n)+"/82")
        
print("Base cases for Lemma 6.2 verified")