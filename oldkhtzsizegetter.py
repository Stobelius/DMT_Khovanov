import re
import sys

def find_highest_object_number(file_path):
    highest_number = None
    pattern = re.compile(r'^object (\d+):')

    try:
        with open(file_path, 'r') as file:
            for line in file:
                #print(line)
                match = pattern.match(line)
                if match:
                    number = int(match.group(1))
                    if highest_number is None or number > highest_number:
                        highest_number = number

        if highest_number is not None:
            print(f"number of objects: {highest_number+1}")
        else:
            print("No object numbers found in the file.")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    find_highest_object_number(file_path)

if __name__ == '__main__':
    main()

