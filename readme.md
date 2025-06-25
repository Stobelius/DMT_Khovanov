This is a code repository/data bank for the paper Morse matchings and Khovanov homology of 4-strand torus links *add arxiv link once it is uploaded*. It serves the following four purposes: 
1. The file braidalgo.py computes for any user specified braid diagram $B$ the unmatched cells and paths between them in the greedy matching $M_{gr}B$. The mathematical validity of the paper does not depend on this code being correct (apart from the numerical Section 7). 
2. The files *asd* and *asd* contain the unreduced and reduced Khovanov homologies of negative torus links T(4,-1),...,T(4,-100) which are computed with Khoca *link Khoca*. They serve as a base case for Theorem 1.2 and Proposition 4.10. The file complex_files.csv is an expanded speadsheet of the numerical data in Numerical Result 7.1. 
3. It contains short python file *basecases.py* which verifies the base cases for the inductions in Lemmas X Y Z W and short Mathematica file *GOR-comparison.nb* which verifies base cases for the induction in Proposition X.
4. The file *lin_ineq_implications.lean* contains lean verified statements, which are of the form: (a set of linear inequalities) implies (a linear inequality). These are used as parts of proofs in Lemmas X Y Z.


How to use:
*braidalgo.py*
This is run as a python file with a mandatory parameter "braid diagram" and optional flags "-a" "-c" "-p" "-o". The braid is represented with X-notation where a sigma_1 b sigma_2  C sigma_3^{-1} etc.  Running

python3 braidalgo.py aaa

computes the unmatched cells of the braid (sigma_1^3) (whose closure is the trefoil knot) and writes them in the console. The flag "-o" with an additional parameter specifying the outputfile writes the output into a file instead: e.g.

python3 braidalgo.py aaa -o trefoilbraid.txt

Adding the flag "-p" computes all paths between the unmatched cells in the graph GGG. The flag "-a" tries to verify whether the graph GGG is acyclic e.g.

python3 braidalgo.py abcabcabc -a

If this terminates (which it does), then the graph GGG is acyclic. Running

python3 braidalgo.py ***** -a

crashes due to "recursion depth exceeded" which means that then the graph GGG contains a cycle. The flag "-c" computes the unmatched cells (they are also computed if no other flag is given or when "-p" is given). Many flags can be present at the same time: 

python3 braidalgo.py abababababab -p -a -c -o T(3,6)braid.txt

verifies that GGG is acyclic, computes its unmatched cells and paths between them and stores it all into file T(3,6)braid.txt.


*basecases.py*
Simply run 

python3 basecases.py

to verify the base cases for the induction in Lemmas. This took around 10 min on my laptop.


*lin_ineq_implications.lean* and *GOR-comparison.nb* should be self-explanatory once you have Lean and Mathematica installed on your system. As of *date*, the contents of *lin_ineq_implications.lean* can be copy-pasted to *url* to run them if you prefer not to install Lean. 









Run this to get dependencies right when messing around with statistical stuff

source venv/bin/activate


