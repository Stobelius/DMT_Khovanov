import sys

def tau(word):
    return (-len(word)+word.count("1")+3*word.count("x")-3*word.count("y"))/4



def main():
    if len(sys.argv) != 2:        
        sys.exit(1)
    word=sys.argv[1]

     
    print(tau(word))


if __name__ == "__main__":
    main()
