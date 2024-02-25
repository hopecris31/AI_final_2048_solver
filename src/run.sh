#!/bin/bash

# Check if the correct number of arguments was passed
if [ "$#" -lt 3 ] || [ "$#" -gt 4 ]; then
    echo "Usage: $0 <algorithm> <number_of_runs> <to_reach> [--graph]"
    exit 1
fi

algorithm=$1
number_of_runs=$2
to_reach=$3
generate_graph=false

# Check if the --graph flag is set
if [ "$#" -eq 4 ] && [ "$4" == "--graph" ]; then
    generate_graph=true
fi

# Run the specified algorithm the specified number of times
for ((i=1; i<=number_of_runs; i++))
do
   echo "Running $algorithm iteration $i"
   python main.py $algorithm 1 $to_reach
done

# If graph generation is requested, call a Python script to generate the graph
if $generate_graph ; then
    python generate_graph.py $algorithm
fi
