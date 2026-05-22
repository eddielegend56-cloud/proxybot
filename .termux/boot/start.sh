#!/data/data/com.termux/files/usr/bin/sh

termux-wake-lock

sleep 15

tmux new-session -d "python /data/data/com.termux/files/home/proxybot.py"
