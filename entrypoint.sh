#!/usr/bin/env bash

# Start docker
/etc/init.d/docker start

# Start app
cd /app/src || exit
python main.py