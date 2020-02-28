#!/usr/bin/env bash

PYTHON_FILE_NAME="CS3243_P1_49_"
PYTHON_EXTENSION=".py"
RUNNER_PY="runner.py"
IDS="1"
MANHATTAN="2"
EUCLIDEAN="3"
LINEAR_CONFLICT="4"
N_3=('1' '2' '3')
N_4=('1' '2' '3' '4')
N_5=('1' '2' '3' '4' '5')
Red='\033[0;31m' 

# Uninformed
PYTHON_FILE="${PYTHON_FILE_NAME}${IDS}${PYTHON_EXTENSION}"
echo -e "\033[1;31m Testing IDS... \033[0m"
for val in "${N_3[@]}"
do
    # echo $PYTHON_FILE
    echo no | python $RUNNER_PY $PYTHON_FILE '3' $val
done

# A* with manhattan
echo -e "\033[1;31m Testing Manhattan... \033[0m"
PYTHON_FILE="${PYTHON_FILE_NAME}${MANHATTAN}${PYTHON_EXTENSION}"
# all test cases of 3x3
for val in "${N_3[@]}"
do
    # echo $PYTHON_FILE
    echo no | python $RUNNER_PY $PYTHON_FILE '3' $val
done

# all test cases of 4x4
for val in "${N_4[@]}"
do
    # echo $PYTHON_FILE
    echo no | python $RUNNER_PY $PYTHON_FILE '4' $val
done

# all test cases of 5x5
for val in "${N_5[@]}"
do
    # echo $PYTHON_FILE
    echo no | python $RUNNER_PY $PYTHON_FILE '5' $val
done

# A* with euclidean
PYTHON_FILE="${PYTHON_FILE_NAME}${EUCLIDEAN}${PYTHON_EXTENSION}"
echo -e "\033[1;31m Testing Euclidean... \033[0m"
# all test cases of 3x3
for val in "${N_3[@]}"
do
    # echo $PYTHON_FILE
    echo no | python $RUNNER_PY $PYTHON_FILE '3' $val
done

# all test cases of 4x4
for val in "${N_4[@]}"
do
    # echo $PYTHON_FILE
    echo no | python $RUNNER_PY $PYTHON_FILE '4' $val
done

# all test cases of 5x5
for val in "${N_5[@]}"
do
    # echo $PYTHON_FILE
    echo no | python $RUNNER_PY $PYTHON_FILE '5' $val
done

# A* with Linear Conflict
echo -e "\033[1;31m Testing Linear Conflict... \033[0m"
PYTHON_FILE="${PYTHON_FILE_NAME}${LINEAR_CONFLICT}${PYTHON_EXTENSION}"
# all test cases of 3x3
for val in "${N_3[@]}"
do
    # echo $PYTHON_FILE
    echo no | python $RUNNER_PY $PYTHON_FILE '3' $val
done

# all test cases of 4x4
for val in "${N_4[@]}"
do
    # echo $PYTHON_FILE
    echo no | python $RUNNER_PY $PYTHON_FILE '4' $val
done

# all test cases of 5x5
for val in "${N_5[@]}"
do
    # echo $PYTHON_FILE
    echo no | python $RUNNER_PY $PYTHON_FILE '5' $val
done