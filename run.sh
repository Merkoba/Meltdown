#!/usr/bin/env bash
root="$(dirname "$(readlink -f "$0")")"
cd "$root"

# Keep this running, to restart the program just press Up arrow key

launch_program() {
    venv/bin/python -m meltdown.main "$@" &
    program_pid=$!
}

restart_program() {
    kill -9 "$program_pid" >/dev/null 2>&1
    launch_program
}

main() {
    launch_program

    while true; do
        read -rsn1 key
        if [[ "$key" == $'\x1b' ]]; then
            read -rsn2 key
            if [[ "$key" == '[A' ]]; then
                echo "Restarting program..."
                restart_program
            fi
        fi
    done
}

main