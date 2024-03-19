#!/usr/bin/env bash
root="$(dirname "$(readlink -f "$0")")"
cd "$root"
args=("$@")

# Function to launch the program
launch_program() {
    # Replace 'your_program' with the actual command to launch your program
    venv/bin/python -m meltdown.main "${args[@]}" &
    program_pid=$!
    disown $program_pid
}

# Function to stop and restart the program
restart_program() {
    kill -9 "$program_pid" 2>/dev/null
    launch_program
}

# Cleanup function to execute before exiting
cleanup() {
    kill -9 "$program_pid" 2>/dev/null
    wait $program_pid 2>/dev/null
    exit 0
}

# Trap Ctrl+C and call cleanup function
trap cleanup SIGINT

# Main function
main() {
    launch_program
    echo "Enter: Restart | Ctrl-c: Exit"

    # Loop to capture keypresses and check program status
    while true; do
        # Read with a timeout of 1 second
        if read -rs -t 1 key; then
            if [[ "$key" == "" ]]; then  # Check if it's the Enter key
                restart_program
            fi
        fi
        if ! ps -p "$program_pid" >/dev/null 2>&1; then  # Check if program is still running
            exit 0
        fi
    done
}

main