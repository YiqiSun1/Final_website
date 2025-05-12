#!/bin/sh

python3 load_tweets.py --db postgresql://postgres:pass@localhost:10648/postgres --inputs "$1" --print_every 10000

