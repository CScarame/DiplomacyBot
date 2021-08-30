#! /bin/bash

echo "Pulling new changes:"
git pull


echo "Running thread test:"
python3 ./Testing/test_parent.py
