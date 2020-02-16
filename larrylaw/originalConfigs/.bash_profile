# Get the aliases and functions
if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

umask 077

export TERM='ansi'
export PS1='\u@sunfire [\t] \w \$ '
export PAGER='less'

/bin/rm -f ~/.viminfo
