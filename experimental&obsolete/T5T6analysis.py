import pickle

def split_string_by_n(s, n):
    return [s[i:i+n] for i in range(0, len(s), n)]

def load_cells6():
    file_path="Torusbraid_cell_dumps/6string20.pkl"

    history=None

    with open(file_path, 'rb') as file:
        history = pickle.load(file)
    unmatched_cells=history[100]
    return unmatched_cells


def load_cells5():
    file_path="Torusbraid_cell_dumps/5string40twistLhack.pkl"

    history=None

    with open(file_path, 'rb') as file:
        history = pickle.load(file)
    unmatched_cells=history[160]
    return unmatched_cells


def load_cells4():
    file_path="Torusbraid_cell_dumps/71synthetic_cells.pkl"

    cells=None

    with open(file_path, 'rb') as file:
        cells = pickle.load(file)
    return cells






def double_pattern_from_cell(cell, step):
    substrings=split_string_by_n(cell, step)

    found_patterns=set()

    for i in range(len(substrings)):
        #looks for pattern of length step*(step+1)

        add_pattern=True

        for j in range(i,i+step+1):
            if not add_pattern:
                break

            if j+step+1>=len(substrings):
                add_pattern=False
            else:
                if substrings[j]!=substrings[j+step+1]:
                    add_pattern=False
            
        if add_pattern:
            pattern=""
            for j in range(i,i+step+1):
                pattern=pattern+substrings[j]
            
            found_patterns.add(pattern)
            
    #print(found_patterns)
    return found_patterns

def varying_pattern_finder(cell, step):
    substrings=split_string_by_n(cell, step)

    def find_size_m_pats(subwordlist,m):
        found_patterns=set()

        for i in range(len(substrings)):
            add_pattern=True

            for j in range(i,i+m):
                if not add_pattern:
                    break

                if j+m>=len(substrings):
                    add_pattern=False
                else:
                    if substrings[j]!=substrings[j+m]:
                        add_pattern=False
                
            if add_pattern:
                pattern=""
                for j in range(i,i+m):
                    pattern=pattern+substrings[j]
                
                found_patterns.add(pattern)
                
        #print(found_patterns)
        return found_patterns

    all_pats=set()

    for i in range(1,len(substrings)):
        all_pats=all_pats.union(find_size_m_pats(cell,i))
    
    return all_pats

def varying_pattern_finder2(cell, step):
    substrings=split_string_by_n(cell, step)

    def find_size_m_pats(subwordlist,m):
        found_patterns=set()

        for i in range(len(substrings)):
            add_pattern=True

            for j in range(i,i+2*m):
                if not add_pattern:
                    break

                if j+2*m>=len(substrings):
                    add_pattern=False
                else:
                    if substrings[j]!=substrings[j+m] or substrings[j]!=substrings[j+2*m]:
                        add_pattern=False
                
            if add_pattern:
                pattern=""
                for j in range(i,i+2*m):
                    pattern=pattern+substrings[j]
                
                found_patterns.add(pattern)
                
        #print(found_patterns)
        return found_patterns

    all_pats=set()

    for i in range(1,len(substrings)):
        all_pats=all_pats.union(find_size_m_pats(cell,i))
    
    return all_pats


def remove_cyclic_permutations(string_set):
    
    def is_cyclic_permutation(string1, string2):
        if len(string1) != len(string2):
            return False
        return string1 in (string2 + string2)
    def single_removal(sset):
        for i in sset:
            for j in sset:
                if is_cyclic_permutation(i,j)and i<j:
                    new_set=sset.copy()
                    new_set.remove(i)
                    return(new_set)
                    
        return(sset)
                
    smaller=string_set.copy()
    while(True):
        if smaller!=single_removal(smaller):
            smaller=single_removal(smaller)
        else:
            return smaller
def remove_superstrings(string_set):
    strings = list(string_set)
    to_remove = set()
    
    for i in range(len(strings)):
        for j in range(len(strings)):
            if i == j:
                continue
            s1, s2 = strings[i], strings[j]
            if s1 in s2 and len(s1) < len(s2):
                to_remove.add(s2)
            elif s2 in s1 and len(s2) < len(s1):
                to_remove.add(s1)
    
    return set(strings) - to_remove


def print_set_GOR_pairing(string_set):
    for s in string_set:
        xcount=s.count('x')
        zerocount=s.count('0')

        row= "("+str(xcount+zerocount)+","+str(xcount+xcount+zerocount)+")   "+s

        print(row)


print("T6")

T6cells=load_cells6()

print(len(T6cells))

T6patterns=set()

for c in T6cells:
    #print(cells)

    #patterns=patterns.union(double_pattern_from_cell(c,5))
    T6patterns=T6patterns.union(varying_pattern_finder(c,5))


T6patterns=remove_cyclic_permutations(remove_superstrings(T6patterns))

print(T6patterns)
print_set_GOR_pairing(T6patterns)




print("T5")
T5cells=load_cells5()

print(len(T5cells))

T5patterns=set()

for c in T5cells:
    #print(cells)

    #patterns=patterns.union(double_pattern_from_cell(c,5))
    T5patterns=T5patterns.union(varying_pattern_finder(c,4))
    

    #the cleaning of patterns from superstrings and cyclic permutations should be done here, not elsewhere

T5patterns=remove_cyclic_permutations(remove_superstrings(T5patterns))

print(T5patterns)

print_set_GOR_pairing(T5patterns)


"""
print("T4")

T4cells=load_cells4()
print(len(T4cells))

T4patterns=set()

for c in T4cells:
    #print(cells)

    #patterns=patterns.union(double_pattern_from_cell(c,5))
    T4patterns=T4patterns.union(varying_pattern_finder(c,3))
    

    #the cleaning of patterns from superstrings and cyclic permutations should be done here, not elsewhere

T4patterns=remove_cyclic_permutations(remove_superstrings(T4patterns))

print(T4patterns)
"""