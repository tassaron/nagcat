#!/usr/bin/env bash


find_python() {
    python=$(which python)
    if [ $? -ne 0 ]; then
        python=$(which python3)
    fi
    if [ $? -ne 0 ]; then
        echo "Couldn't find Python interpreter"
        exit 1
    fi
    echo "$python"
}


NAGCAT_PYTHON=$(find_python)
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

nagcat_str="\#{nagcat}"
nagcat_cmd="#($NAGCAT_PYTHON $CURRENT_DIR/src/nagcat.py)"

get_tmux_option() {
    local option=$1
    local default_value=$2
    local option_value="$(tmux show-option -gqv "$option")"

    if [[ -z "$option_value" ]]; then
        echo "$default_value"
    else
        echo "$option_value"
    fi
}

WHY_KEY=$(get_tmux_option "@nagcat_why" "e")
PET_KEY=$(get_tmux_option "@nagcat_pet" "r")

tmux bind-key $WHY_KEY run-shell "$NAGCAT_PYTHON $CURRENT_DIR/src/nagcat.py why"
tmux bind-key $PET_KEY run-shell "$NAGCAT_PYTHON $CURRENT_DIR/src/nagcat.py pet"


set_tmux_option() {
    local option=$1
    local value=$2
    tmux set-option -gq "$option" "$value"
}

do_interpolation() {
    local result="$1"
    result="${result//${nagcat_str}/${nagcat_cmd}}"
    echo "$result"
}

update_tmux_option() {
	local option=$1
	local option_value=$(get_tmux_option "$option")
	local new_option_value=$(do_interpolation "$option_value")
	set_tmux_option "$option" "$new_option_value"
}

main() {
	update_tmux_option "status-right"
	update_tmux_option "status-left"
}
main