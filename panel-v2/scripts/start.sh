#!/bin/bash

nohup gunicorn app:app -b 0.0.0.0:80 -w 4 --reload -t 30 &