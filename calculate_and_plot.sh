if [ $# -eq 0 ]; then
    echo "Usage: $0 <argument>"
    exit 1
fi

# Store the argument in a variable
my_argument="$1"

# Call the Python script with the argument
python3 unmatched_cell_printer.py "$my_argument"

cd latex_plots/

pdflatex -jobname=$my_argument $my_argument.tex

xdg-open $my_argument.pdf
rm $my_argument.log
rm $my_argument.aux

cd ..
