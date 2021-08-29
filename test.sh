#! /bin/bash

echo "Pulling new changes:"
git pull


echo "Running thread test:"
python ./Testing/test_parent.py
