## Code/Data for *Morse matchings and Khovanov homology of 4-strand torus links*
This is a code repository/data bank for the paper *Morse matchings and Khovanov homology of 4-strand torus links* **add arxiv link once it is uploaded**. It serves the following four purposes: 
1. The file **braidalgo.py** computes for any user specified braid diagram $B$ the unmatched cells and paths between them in the greedy matching $M_{gr}[B]$. The mathematical validity of the paper does not depend on this code being correct (apart from the numerical Section 7). Additionally, **braidalgo.py** was used to generate the file **complex_sizes.csv** which provides a detailed speadsheet of Numerical Result 7.1. 
2. The files **T4_100_unred.pdf** and **T4_100_reduced.pdf** contain the unreduced and reduced Khovanov homologies of negative torus links T(4,-1),...,T(4,-100) which are computed with [Khoca](https://people.math.ethz.ch/~llewark/khoca.php) (machine readable results are also provided). They serve as a base case for Theorem 1.2 and Proposition 4.9.
3. The short files **basecases.py** and **GOR-comparison.nb** verify the base cases for the inductions in Lemmas 4.5, 5.3 and 6.2 and in Proposition 4.9.
4. The file **lin_ineq_implications.lean** contains lean verified statements, which are of the form: (a set of linear inequalities) implies (a linear inequality). These are used as parts of proofs in Theorem 1.2, Corollary 4.2, Proposition 4.10 and Lemma 6.2.

## How to use:
#### **braidalgo.py**
This is run as a python file with a mandatory parameter "braid diagram" and optional flags "-a", "-c", "-p", "-o". The braid is represented with knotscape notation where $a \leftrightarrow  \sigma_1$,  $b \leftrightarrow \sigma_2$,  $C \leftrightarrow \sigma_3^{-1}$ etc.  Running

> python3 braidalgo.py aaa

computes the unmatched cells of the complex $M_{gr}\Psi[\sigma_1^3]$ (whose closure is the trefoil knot) and writes them in the console. The flag "-o" with an additional parameter specifying the outputfile writes the output into a file instead: e.g.

> python3 braidalgo.py aaa -o trefoilbraid.txt

Adding the flag "-p" computes all paths between the unmatched cells in the graph $G([\sigma_1^3], M_{gr})$. The flag "-a" tries to verify whether the graph $G([B],M_{gr})$ is acyclic e.g.

> python3 braidalgo.py abcabcabc -a

If this terminates (which it does), then the graph $G([(\sigma_1\sigma_2\sigma_3)^3], M_{gr})$ is acyclic. Running

> python3 braidalgo.py ADcbccbbAD -a

crashes due to "recursion depth exceeded" which means that then the graph $G([\sigma_1^{-1} \sigma_4^{-1} \sigma_3 \sigma_2 \sigma_3 \sigma_3\sigma_2 \sigma_2 \sigma_1^{-1} \sigma_4^{-1}],M_{gr})$ contains a cycle. The flag "-c" computes the unmatched cells (they are also computed if no other flag is given or when "-p" is given). Many flags can be present at the same time: 

> python3 braidalgo.py abababababab -p -a -c -o T(3,6)braid.txt

verifies that $G([(\sigma_1\sigma_2)^6], M_{gr})$ is acyclic, computes its unmatched cells and paths between them and stores it all into file T(3,6)braid.txt.

#### **T4_100_unred.pdf** and **T4_100_reduced.pdf**
Pick a pdf-viewer, which can zoom into very large pdf:s ;) 

#### **basecases.py**
Simply run 

> python3 basecases.py

to verify the base cases for the induction in Lemmas. Running it took around 10 min on my laptop.

#### **lin_ineq_implications.lean** and **GOR-comparison.nb** 
These should be self-explanatory once you have Lean and Mathematica installed on your system. 

(In order not to flood github with lean-packages, I added to **.gitignore** the **.lake** folder. I do not know the best practices of sharing Lean-code, so this might break some things. As of 27.6.2025, the contents of **lin_ineq_implications.lean** can also be copy-pasted to https://live.lean-lang.org/ to verify them if you prefer not to install Lean on your system.)
