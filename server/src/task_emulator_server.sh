#!/usr/bin/env bash

set -ex

PIDS=""

cleanup()
{
    kill $PIDS
    wait $PIDS
}

trap cleanup 1 2 3 15

python src/task_emulator_server.py &
PIDS="$!"

WORKER=1 python src/task_emulator_server.py &
PIDS="$PIDS $!"

wait $PIDS
