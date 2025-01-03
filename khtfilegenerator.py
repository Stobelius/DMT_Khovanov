# This code generates .kht files from knotinfo database and runs kht++ on them. The paths included are hardcoded.


import os
import subprocess, sys

def knotinfo_string_to_integer_array(input_string):
    cleaned_string = input_string.strip("[{}]")
    cleaned_string = cleaned_string.split("};{")
    cleaned_string = cleaned_string[0]
    elements = cleaned_string.split(";")

    # Convert each element to an integer
    integer_array = [int(element) for element in elements]

    return integer_array

def convert_numbers_to_kht(numbers):

    result = []
    for n in numbers:
        if n > 0:
            result.append(f"x{n-1}")
        else:
            result.append(f"y{abs(n)-1}")
    return result

def generate_output(arr, num_repeats):
    # Join array elements with "."
    arr_string = ".".join(map(str, arr))
    
    # Create the repeated "1" string
    ones_string = "1," * num_repeats
    ones_string = ones_string.rstrip(",")  # Remove trailing comma
    
    # Combine the two parts
    output_string = f"{arr_string}\n,{ones_string}"
    return output_string





def main():
    
    folder_name = "braid_data"
    try:
        os.mkdir(folder_name)
        print(f"Directory '{folder_name}' created!")
    except FileExistsError:
        print(f"Directory '{folder_name}' already exists")    
    
    
    f=open("knotinfo_braids13.csv", "r")
    
    f.readline() #discard 1st line
    
    
    
    testamount=100000
    testcount=0
    
    while True:
        testcount=testcount+1
        if testamount==testcount:
            break
    
        #generate .kht file
        line=f.readline().split(",")
        if len(line)==1:
            #print("asd")
            break
        #print(line)
        braid=line[1].strip()
        braid=knotinfo_string_to_integer_array(braid)
        braid_name=line[0].strip()
        print(braid_name)

  
        stringarray=convert_numbers_to_kht(braid)
        number_of_strands=max([max(braid), -min(braid)])+1
        khtstring=generate_output(stringarray,number_of_strands)



        #file_path = os.path.join(folder_name, braid_name+'.kht')
        #os.mkdir(folder_name+"/"+braid_name+"/") 
        try:
            os.mkdir(folder_name+"/"+braid_name+"/")
        except FileExistsError:
            pass
        file_path = folder_name+"/"+braid_name+"/"+braid_name+'.kht'
        

        #cx_file_path=folder_name+"/"+braid_name+"/cx-c2"
        cx_file_path=folder_name+"/"+braid_name+"/"+braid_name+"/cx-c2"
        if os.path.exists(cx_file_path):
            continue
        
        
        with open(file_path, 'w', encoding='utf-8') as asd:
            asd.write(khtstring)
        #    asd.close()
        
        #asd= open(file_path, 'w')
        #asd.write(khtstring)
        #asd.close()
        #if os.path.exists(file_path):
        #    print("asdasddsa")



        #run the kht++ program on the generated file
        subprocess.run(["../kht/khtpp/./kht++", "/"+folder_name+"/"+braid_name+"/"+braid_name+"/"])
        
        if os.path.exists(folder_name+"/"+braid_name+".html"):
            os.remove(folder_name+"/"+braid_name+".html")
        


if __name__ == "__main__":
    main()
    
