#!/usr/bin/env bash
root="$(dirname "$(readlink -f "$0")")"
cd "$root"

################################################
# To restart the program just press Up arrow key
################################################

# Function to launch the program
launch_program() {
    # Replace 'your_program' with the actual command to launch your program
    venv/bin/python -m meltdown.main "$@" &
    program_pid=$!
}

# Function to stop and restart the program
restart_program() {
    kill -9 "$program_pid" >/dev/null 2>&1
    launch_program
}

# Cleanup function to execute before exiting
cleanup() {
    echo "Exiting script..."
    kill -9 "$program_pid" >/dev/null 2>&1
    exit 0
}

# Trap Ctrl+C and call cleanup function
trap cleanup SIGINT

# Main function
main() {
    launch_program

    # Loop to capture keypresses and check program status
    while true; do
        # Read with a timeout of 1 second
        if read -rsn1 -t 1 key; then
            if [[ "$key" == $'\x1b' ]]; then  # Check if the key is escape (starting sequence for arrow keys)
                read -rsn2 -t 1 key  # Capture the next 2 characters
                if [[ "$key" == '[A' ]]; then  # Check if it's the Up arrow key
                    echo "Restarting program..."
                    restart_program
                fi
            fi
        fi
        if ! ps -p "$program_pid" >/dev/null 2>&1; then  # Check if program is still running
            echo "Program exited. Exiting script."
            exit 0
        fi
    done
}

main