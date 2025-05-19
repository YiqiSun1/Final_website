#!/bin/sh
cd "$(dirname "$0")"
python3 ./fake_data.py --db=postgresql://postgres:pass@localhost:11666/postgres --rows=10
