#!/usr/bin/env bash

if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

docker-compose up --scale web=3 --build
