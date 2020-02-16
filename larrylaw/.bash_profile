# Get the aliases and functions
if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

umask 077

export TERM='ansi'
export PS1='\u@sunfire [\t] \w \$ '
export PAGER='less'

alias python3=/usr/local/Python-3.7/bin/python3

/bin/rm -f ~/.viminfo
