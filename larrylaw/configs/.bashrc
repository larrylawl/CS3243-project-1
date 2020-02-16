alias chrome="open -a 'Google Chrome'"
alias python="python3"

# JDK 11 for 2103
export JAVA_HOME=`/usr/libexec/java_home -v 11.0.4`

# Colors for prompt
export CLICOLOR=1
export LSCOLORS=GxBxCxDxexegedabagaced
export PS1="\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[01;31m\]\$(parse_git_branch)\[\033[00m\]$ "

# ls aliases
alias ls='ls -G'
alias ll='ls -GalF'
alias la='ls -GA'

# Grep Aliases
alias grep='grep --color'
alias fgrep='fgrep --color'
alias egrep='egrep --color'

# Git helpers
source ~/.git-completion.bash
alias gs="git status"
alias gf="git fetch"
alias gl="git pull"
alias gp="git push"
alias gpu="git push -u origin"
alias ga="git add"
alias gcm="git commit -m"
alias gb="git branch"
alias gc="git checkout"
alias gcb="git checkout -b"
alias gbd="git branch -d"
alias gdr="git push origin --delete"
alias gm="git merge --no-edit"
alias gd="git diff"
alias grs="git reset --soft"
alias grh="git reset --hard"

# Misc aliases
alias stat="stat -x"

# Add git branch if its present to PS1
parse_git_branch() {
  local g="$(git rev-parse --git-dir 2>/dev/null)"
  if [ -n "$g" ]; then
    local r
    local b
    if [ -d "$g/rebase-apply" ]
    then
      if test -f "$g/rebase-apply/rebasing"
      then
        r="|REBASE"
      elif test -f "$g/rebase-apply/applying"
      then
        r="|AM"
      else
        r="|AM/REBASE"
      fi
      b="$(git symbolic-ref HEAD 2>/dev/null)"
    elif [ -f "$g/rebase-merge/interactive" ]
    then
      r="|REBASE-i"
      b="$(cat "$g/rebase-merge/head-name")"
    elif [ -d "$g/rebase-merge" ]
    then
      r="|REBASE-m"
      b="$(cat "$g/rebase-merge/head-name")"
    elif [ -f "$g/MERGE_HEAD" ]
    then
      r="|MERGING"
      b="$(git symbolic-ref HEAD 2>/dev/null)"
    else
      if [ -f "$g/BISECT_LOG" ]
      then
        r="|BISECTING"
      fi
      if ! b="$(git symbolic-ref HEAD 2>/dev/null)"
      then
        if ! b="$(git describe --exact-match HEAD 2>/dev/null)"
        then
          b="$(cut -c1-7 "$g/HEAD")..."
        fi
      fi
    fi

    if [ -n "${1-}" ]; then
      printf "$1" "${b##refs/heads/}$r"
    else
      printf "(%s)" "${b##refs/heads/}$r"
    fi
  fi
}

