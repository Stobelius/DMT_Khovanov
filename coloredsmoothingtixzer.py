#import argparse
from braidalgo import *
#from path_and_cell_analysis_forT4 import dom_cod_first_L_to_paths_dict, load_new_T4_paths, list_of_Ls_from_path



def up_bend_right(point):
    return "\draw "+str(point)+" to[bend right=50] ("+str(point[0])+", "+str(point[1]+1)+");"
def up_bend_left(point):
    return "\draw "+str(point)+" to[bend left=50] ("+str(point[0])+", "+str(point[1]+1)+");"
def up_no_bend(point):
    return "\draw "+str(point)+" to ("+str(point[0])+", "+str(point[1]+1)+");"

def right_bend_up(point):
    return "\draw "+str(point)+" to[bend left=50] ("+str(point[0]+1)+", "+str(point[1])+");"
def right_bend_down(point):
    return "\draw "+str(point)+" to[bend right=50] ("+str(point[0]+1)+", "+str(point[1])+");"
def right_no_bend(point):
    return "\draw "+str(point)+" to ("+str(point[0]+1)+", "+str(point[1])+");"

def endpoint_to_comp(braid,smoothing,coord):
    strands=number_of_strands(braid)
    #Bottom
    if coord[1]==0:
        #check a direct match left if possible
        if coord[0]>0:
            if smoothing_northeast_is_Vert((coord[0]-1,coord[1]),braid,smoothing):
                ending=(coord[0]-1,coord[1])
                return ([coord,ending],ending)
        #check direct right
        if coord[0]<strands-1:
            if smoothing_northeast_is_Vert((coord[0],coord[1]),braid,smoothing):
                ending=(coord[0]+1,coord[1])
                return ([coord,ending],ending)
        #general case 
        #might have a problem with length 1 braid
        #print("looping from")
        #print(coord)
        path=array_of_positions_from_edge(coord,(coord[0],coord[1]+1),braid,smoothing)
        return (path,path[len(path)-1])
    
    #Top
    #check a direct match left if possible
    if coord[0]>0:
        if smoothing_northeast_is_Vert((coord[0]-1,coord[1]-1),braid,smoothing):
            ending=(coord[0]-1,coord[1])
            return ([coord,ending],ending)
    #check direct right
    if coord[0]<strands-1:
        if smoothing_northeast_is_Vert((coord[0],coord[1]-1),braid,smoothing):
            ending=(coord[0]+1,coord[1])
            return ([coord,ending],ending)
    #general case 
    #might have a problem with length 1 braid
    #print("looping from")
    #print(coord)
    #print(smoothing)
    path=array_of_positions_from_edge(coord,(coord[0],coord[1]-1),braid,smoothing)
    return (path,path[len(path)-1])




def path_to_tikz(braid,smoothing,path):      

    def edge_right(point):
        if point[1]<len(braid):
            if x_position_of_crossing(braid, point[1])==point[0] and smoothing_northeast_is_Vert(point,braid,smoothing):
                return right_bend_up(point)
        if x_position_of_crossing(braid, point[1]-1)==point[0]:
            return right_bend_down(point)
        return right_no_bend(point)


    def edge_up(point):
        if x_position_of_crossing(braid, point[1])==point[0]:
            return up_bend_right(point)
        elif x_position_of_crossing(braid, point[1])==point[0]-1:
            return up_bend_left(point)
        return up_no_bend(point)

    def edge_to_tikz(point0, point1):
        if point0[0]+1==point1[0]:
            return edge_right(point0)
        elif point0[0]==point1[0]+1:
            return edge_right(point1)
        elif point0[1]+1==point1[1]:
            return edge_up(point0)
        elif point0[1]==point1[1]+1:
            return edge_up(point1)

    tikz_list=[]
    

    if len(path)==3:
        p=path[0]
        q=path[1]
        if(p[0]==q[0]+1):
            tikz_list.append(right_bend_up(q))
            tikz_list.append(right_bend_down(q))
            return tikz_list
        else:
            tikz_list.append(right_bend_up(p))
            tikz_list.append(right_bend_down(p))
            return tikz_list
        


    for i in range(len(path)-1):
        #print(path[i])
        tikz_list.append(edge_to_tikz(path[i],path[i+1]))
    return tikz_list

def tikz_of_smoothing(braid,smoothing):
    print(f"braid: {braid}")
    print(f"smoothing: {smoothing}")

    #get connected components from rears and x/y smoothed components
    strands=number_of_strands(braid)
    black_components=[]
    red_components=[]
    blue_components=[]
    endpoints=set()
    for i in range(strands):
        endpoints.add((i,0))
        endpoints.add((i,len(braid)))
    
    while len(endpoints)>0:
        point=endpoints.pop()
        pair=endpoint_to_comp(braid, smoothing, point)
        black_components.append(pair[0])
        endpoints.remove(pair[1])

    middle_comp_redpoints=[]
    for i in range(len(smoothing)):
        colors=["y","Y"]
        if smoothing[i] in colors:
            x=x_position_of_crossing(braid, i)
            middle_comp_redpoints.append((x,i))
    for point in middle_comp_redpoints:
        red_components.append(array_of_positions_from_edge(point,(point[0]+1,point[1]),braid,smoothing))

    middle_comp_bluepoints=[]
    for i in range(len(smoothing)):
        colors=["x","X"]
        if smoothing[i] in colors:
            x=x_position_of_crossing(braid, i)
            middle_comp_bluepoints.append((x,i))
    for point in middle_comp_bluepoints:
        blue_components.append(array_of_positions_from_edge(point,(point[0]+1,point[1]),braid,smoothing))
    
    allcommands=[]
    for path in black_components:
        for command in path_to_tikz(braid,smoothing,path):
            allcommands.append(command)
    
    allcommands.append("\\begin{scope}[color=blue]")
    for path in blue_components:
        for command in path_to_tikz(braid,smoothing,path):
            allcommands.append(command)
    allcommands.append("\\end{scope}")


    allcommands.append("\\begin{scope}[color=red]")
    for path in red_components:
        for command in path_to_tikz(braid,smoothing,path):
            allcommands.append(command)
    allcommands.append("\\end{scope}")


    command_string=""
    for s in allcommands:
        command_string+= s
        command_string+= "\n"

    return command_string


def draw_path_in_a_file(braid, path, number):
    latex_boilerplate = r"""
    \documentclass{article}
    \usepackage{tikz}
    \begin{document}
    """
    begin_diagram= r"""
    \begin{tikzpicture}[scale=0.6]
    """
    
    
    end_diagram= r"""
    \end{tikzpicture}
    \newpage



    """

    latex_end = r"""

    \end{document}
    """

    # File name
    file_name = "tikz_plots/tikz_path"+str(number)+".tex"


    # Open the file in write mode
    with open(file_name, 'w') as f:
        # Write the LaTeX boilerplate to the file
        f.write(latex_boilerplate)

        for cell in path:
            f.write(begin_diagram)
            f.write(tikz_of_smoothing(braid,cell))
            f.write(end_diagram)
        f.write(latex_end)

def draw_paths_as_separate_files(braid,path):
    
    latex_boilerplate = r"""
    \documentclass{standalone}
    \usepackage{tikz}
    \begin{document}

    \begin{tikzpicture}
        % TikZ commands go here
    """

    latex_end = r"""
    \end{tikzpicture}

    \end{document}
    """

    # File name
    print("adssadsaddsadas")
    
    
    path_number=1
    for cell in path:
        file_name = "tikz_plots/path/cell"+str(path_number)+".tex"
        path_number+=1

        with open(file_name, 'w') as f:
            # Write the LaTeX boilerplate to the file
            f.write(latex_boilerplate)
            f.write(tikz_of_smoothing(braid,cell))
            f.write(latex_end)





def draw_smoothing(braid, smoothing):
    
    print(f"braid: {braid}")
    print(f"smoothing: {smoothing}")

    #get connected components from rears and x/y smoothed components
    strands=number_of_strands(braid)
    black_components=[]
    red_components=[]
    blue_components=[]
    endpoints=set()
    for i in range(strands):
        endpoints.add((i,0))
        endpoints.add((i,len(braid)))
    
    while len(endpoints)>0:
        point=endpoints.pop()
        pair=endpoint_to_comp(braid, smoothing, point)
        black_components.append(pair[0])
        endpoints.remove(pair[1])

    middle_comp_redpoints=[]
    for i in range(len(smoothing)):
        colors=["y","Y"]
        if smoothing[i] in colors:
            x=x_position_of_crossing(braid, i)
            middle_comp_redpoints.append((x,i))
    for point in middle_comp_redpoints:
        red_components.append(array_of_positions_from_edge(point,(point[0]+1,point[1]),braid,smoothing))

    middle_comp_bluepoints=[]
    for i in range(len(smoothing)):
        colors=["x","X"]
        if smoothing[i] in colors:
            x=x_position_of_crossing(braid, i)
            middle_comp_bluepoints.append((x,i))
    for point in middle_comp_bluepoints:
        blue_components.append(array_of_positions_from_edge(point,(point[0]+1,point[1]),braid,smoothing))

    black_tikz=[]

    #for path in black_components:
        #print(path_to_tikz(braid,smoothing,path))
    #    for t in path_to_tikz(braid,smoothing,path):
    #        print(t)
        #print("asd")


    latex_boilerplate = r"""
    \documentclass{article}
    \usepackage{tikz}
    %\\input{TuomasLatexFunctions}
    \begin{document}

    \begin{tikzpicture}
        % TikZ commands go here
    """

    latex_end = r"""
    \end{tikzpicture}

    \end{document}
    """

    # File name
    file_name = "tikz_plots/tikz_example.tex"

    PRINT_COMMANDS=False

    # Open the file in write mode
    with open(file_name, 'w') as f:
        # Write the LaTeX boilerplate to the file
        f.write(latex_boilerplate)

        # Write each TikZ command from the list into the file
        for path in black_components:
            for command in path_to_tikz(braid,smoothing,path):
                if(PRINT_COMMANDS):
                    print(command)

                f.write(f"    {command}\n")
        if(PRINT_COMMANDS):
            print("\\begin{scope}[color=blue]")
        f.write("\\begin{scope}[color=blue]\n")

        for path in blue_components:
            for command in path_to_tikz(braid,smoothing,path):
                if(PRINT_COMMANDS):
                    print(command)

                f.write(f"    {command}\n")
        if(PRINT_COMMANDS):
            print("\end{scope}")
            print("\\begin{scope}[color=red]\n")

        f.write("\end{scope}\n")
        f.write("\\begin{scope}[color=red]\n")

        for path in red_components:
            for command in path_to_tikz(braid,smoothing,path):
                if(PRINT_COMMANDS):
                    print(command)
                
                f.write(f"    {command}\n")
        if(PRINT_COMMANDS):
            print("\end{scope}")
        f.write("\end{scope}\n")
        



        # Write the closing LaTeX tags
        f.write(latex_end)





def main(braid, smoothing):
    #draw_smoothing(braid, smoothing)


    #print(tikz_of_smoothing(braid, smoothing))
    """
    #Specific path
    candidate_L_list=[35, 35, 30, 30, 27, 28, 25, 26, 23, 23, 18, 18, 15, 16, 13, 14, 11, 11, 6, 13, 14, 15, 16, 25, 26, 27, 28]
    interesting_path=None
    twistcount=12
    braid=12*"abc"
    
    teststring="11111000101xx0101xx0101xx0101xx0101x"
    paths=load_new_T4_paths(twistcount)
    path_dict=dom_cod_first_L_to_paths_dict(paths)
    for key in path_dict:
        if key[0]==teststring:
            #print(key)
            for path in path_dict[key]:
                if candidate_L_list== list_of_Ls_from_path(path):
                    interesting_path=path
                    for cell in path:
                        print(cell)
                    print("")

    draw_paths_as_separate_files(braid,interesting_path)
    """

    #cycle?
    #cyc=["11010Y11yx1010","11100Y11yx1010","11000111yx1Y10","11010011yx1Y10","11100011yx1Y10","111010y10x1Y10","1111y0010x1Y10","1110110y0x1Y10","1111yY0y0x1X10","1111yX0y0x1Y10","11000111yy1X10","11010011yy1X10","11100011yy1X10","111010y10y1X10","1111y0010y1X10","1110110y0y1X10","1111yX0y0y1X10","1100001011Y110","110010yy11X110","110010yx11Y110","11000011y11110","110010y1011110","1100110y011110","1101100y011110","1111y00y011X10","110011100y1110","110110100y1110","1111y0100y1X10","11000110101Y10","11010010101Y10","11100010101Y10","111010yy101X10","1111y00y101X10","111010yx101Y10","1111y00x101Y10","11010Y10101010","11100Y10101010","11010Y11yx1010"]
    cyc=['111010101Y', '1110101111', '11001011Y1', '1100111111', '110011y111', '1101110111', '1101y10111', '1111010111', '11110y0111', '1111100111', '1111100y11', '1111101011', '111010101Y']

    print("asd")
    draw_path_in_a_file("ADcbccbbAD",cyc,1)

    """
    #Write a milloin paths in separate files
    
    
    twistcount=12
    braid=twistcount*"abc"
    teststring="11000101xx0101xx0101xx0101x"
    paths=load_new_T4_paths(twistcount)
    path_dict=dom_cod_first_L_to_paths_dict(paths)
    path_number=1
    for key in path_dict:
        if key[0]==teststring or True:
            print(key)
            for path in path_dict[key]:
                first_cell=path[0]
                last_cell=path[-1]
                if first_cell[-3:]=="01x" and last_cell[-3:]=="x01":
                    draw_path_in_a_file(braid, path,path_number)
                
                #print(path)
                path_number+=1
    """
       



if __name__ == "__main__":
    print("asd")
    main("a","a")

    # Set up the argument parser
    parser = argparse.ArgumentParser(description="A simple command line program that accepts two parameters.")
    
    # Define the expected parameters
    parser.add_argument("braid", type=str, help="First parameter")
    parser.add_argument("smoothing", type=str, help="Second parameter")
    
    # Parse the command line arguments
    args = parser.parse_args()
    
    # Call the main function with the parsed arguments
    main(args.braid, args.smoothing)
