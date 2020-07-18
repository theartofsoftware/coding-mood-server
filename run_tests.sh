#!/bin/bash
poetry run pytest | tee /dev/tty | curl -H "Content-Type: text/plain" -X POST -d @- http://localhost:5000/pytest-state
