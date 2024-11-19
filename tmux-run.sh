#!/bin/sh

# default session name, personal preference
DEFAULT_SESSION="main"

if [ -z "$TMUX" ]; then
    # open a session with the default name if it doesnt exist
    SESSION=$DEFAULT_SESSION
    tmux new-session -d -s $SESSION
else
    # get the name of the current session
    SESSION=$(tmux display-message -p '#S')
fi

# run the bot compose detatched
docker compose up -d

# set up session and clear window
tmux kill-window -t $SESSION:sneaksbot
tmux new-window -t $SESSION -n sneaksbot

# attach to docker and open a terminal
tmux split-window -h -l 38% -t $SESSION:sneaksbot
tmux send-keys -t $SESSION:sneaksbot.0 "docker attach sneaksbot" C-m

# attach to session if not already in tmux
if [ -z "$TMUX" ]; then
    tmux attach -t $SESSION
fi