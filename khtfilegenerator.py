
#import subprocess
import os
import subprocess, sys

def parse_string_to_array(input_string):
    # Remove the curly braces and split the string by semicolons
    #print(input_string)
    #cleaned_string = input_string.strip("[]")    
    cleaned_string = input_string.strip("[{}]")
    #print(cleaned_string)
    cleaned_string = cleaned_string.split("};{")
    cleaned_string = cleaned_string[0]
    elements = cleaned_string.split(";")

    # Convert each element to an integer
    integer_array = [int(element) for element in elements]

    return integer_array

def convert_numbers(numbers):

    result = []
    for n in numbers:
        if n > 0:
            result.append(f"x{n-1}")
        else:
            result.append(f"y{abs(n)-1}")
    return result

def generate_output(arr, num_repeats):
    """
    Generates a formatted string based on the input array and integer.
    
    Args:
        arr (list): List of elements.
        num_repeats (int): Number of times to repeat "1".
    
    Returns:
        str: Formatted output string.
    """
    # Join array elements with "."
    arr_string = ".".join(map(str, arr))
    
    # Create the repeated "1" string
    ones_string = "1," * num_repeats
    ones_string = ones_string.rstrip(",")  # Remove trailing comma
    
    # Combine the two parts
    output_string = f"{arr_string}\n,{ones_string}"
    return output_string

"""

def run_external_program(program_path, input_string):
    
    Runs an external program as a subprocess, passing the input string to it.

    Args:
        program_path (str): Path to the external program executable.
        input_string (str): Input string to be passed to the program.

    Returns:
        str: Output from the external program.
    
    try:
        # Run the external program as a subprocess
        result = subprocess.run(
            [program_path],
            input=input_string.encode(),  # Convert input string to bytes
            #stdout=subprocess.PIPE,
            #stderr=subprocess.PIPE,
            #text=True,  # Return output as text (string)
            #check=True  # Raise an error if the subprocess returns a non-zero exit code
        )
        return result.stdout  # Return the standard output from the subprocess
    except subprocess.CalledProcessError as e:
        # Handle any errors (e.g., non-zero exit code)
        return f"Error executing {program_path}: {e.stderr}"

"""





folder_name = "khtfiles"
try:
    os.mkdir(folder_name)
    print(f"Directory '{folder_name}' created!")
except FileExistsError:
    print(f"Directory '{folder_name}' already exists")    


f=open("knotinfodb.csv", "r")

f.readline() #discard 1st line


testamount=20

while True:

    line=f.readline().split(",")
    if len(line)==1:
        #print("asd")
        break
    #print(line)
    braid=line[1].strip()
    braid=parse_string_to_array(braid)
    print(line[0])

    testamount=testamount+1
    if testamount==20:
        break

    stringarray=convert_numbers(braid)

    number_of_strands=max([max(braid), -min(braid)])+1

    khtstring=generate_output(stringarray,number_of_strands)

    file_path = os.path.join(folder_name, line[0].strip()+'.kht')
    with open(file_path, 'w', encoding='utf-8') as asd:
        asd.write(khtstring)
    #try to run kht here

    subprocess.run(["../kht/khtpp/./kht++", "/khtfiles/"+line[0]])




# Example usage:
#program_path = "../kht/khtpp/kht++"  # Replace with the actual path
#input_string = khtstring

#output = run_external_program(program_path, input_string)
#print(output)



#print(khtstring)

