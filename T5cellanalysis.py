import pickle

def load_cells5(twistnumber):
    file_path="Torus5braids/5string40twistLhack.pkl"

    history=None

    with open(file_path, 'rb') as file:
        history = pickle.load(file)
    unmatched_cells=history[4*twistnumber]
    return unmatched_cells


for i in range(15,41,5):
    
    print(len(load_cells5(i)))

