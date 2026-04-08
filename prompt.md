# Themes for prompt
place desired theme in a file in /etc/profile.d/

## physical server theme
```bash
# set prompt colors
## Function to get the Git branch name with parentheses and "git-" prefix
get_git_branch() {
    local branch
    branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    if [ -n "$branch" ]; then
        echo "(git)-[$branch]"
    fi
}

## Function to get the Python virtual environment name with "py-" prefix
get_virtualenv() {
    if [ -n "$VIRTUAL_ENV" ]; then
        echo "(pyenv)-[$(basename "$VIRTUAL_ENV")]"
    fi
}

## Function to set the PS1 variable
set_prompt() {
    local branch_name=$(get_git_branch)
    local venv_name=$(get_virtualenv)

    if [ "$(id -u)" == "0" ]; then
        # Set PS1 for the root user (red prompt)
        PS1='\[\e[1;31m\]\u\[\e[1;33m\]@\h\[\e[1;31m\] \W'
    else
        # Set PS1 for regular users (green prompt)
        PS1='\[\e[1;32m\]\u\[\e[1;33m\]@\h\[\e[1;32m\] \W'
    fi

    if [ -n "$branch_name" ]; then
        PS1+="\[\e[1;37m\] $branch_name"
    fi

    if [ -n "$venv_name" ]; then
        PS1+="\[\e[1;37m\] $venv_name"
    fi

    if [ "$(id -u)" == "0" ]; then
        PS1+='\[\e[1;31m\] \$ \e[0m\]'
    else
        PS1+='\[\e[1;32m\] \$ \e[0m\]'
    fi
}

## Set the PS1 variable
set_prompt

## Function to update the prompt when the directory changes
update_prompt() {
    set_prompt
}
export -f update_prompt

## Hook into the prompt command
export PROMPT_COMMAND="update_prompt; $PROMPT_COMMAND"
```

## VM theme 
```bash
# set prompt colors
## Function to get the Git branch name with parentheses and "git-" prefix
get_git_branch() {
    local branch
    branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    if [ -n "$branch" ]; then
        echo "(git)-[$branch]"
    fi
}

## Function to get the Python virtual environment name with "py-" prefix
get_virtualenv() {
    if [ -n "$VIRTUAL_ENV" ]; then
        echo "(pyenv)-[$(basename "$VIRTUAL_ENV")]"
    fi
}

## Function to set the PS1 variable
set_prompt() {
    local branch_name=$(get_git_branch)
    local venv_name=$(get_virtualenv)

    if [ "$(id -u)" == "0" ]; then
        # Set PS1 for the root user (red prompt)
        PS1='\[\e[1;31m\]\u\[\e[1;33m\]@\h\[\e[1;31m\] \W'
    else
        # Set PS1 for regular users (purple prompt)
        PS1='\[\e[1;35m\]\u\[\e[1;33m\]@\h\[\e[1;35m\] \W'
    fi

    if [ -n "$branch_name" ]; then
        PS1+="\[\e[1;37m\] $branch_name"
    fi

    if [ -n "$venv_name" ]; then
        PS1+="\[\e[1;37m\] $venv_name"
    fi

    if [ "$(id -u)" == "0" ]; then
        PS1+='\[\e[1;31m\] \$ \[\e[1;33m\]'
    else
        PS1+='\[\e[1;35m\] \$ \[\e[1;33m\]'
    fi
}

## Set the PS1 variable
set_prompt

## Function to update the prompt when the directory changes
update_prompt() {
    set_prompt
}
export -f update_prompt

## Hook into the prompt command
export PROMPT_COMMAND="update_prompt; $PROMPT_COMMAND"

# set text color
export LS_COLORS='di=01;34:fi=01;33'  # Example: directories in blue, regular files in yellow
```

## workstation theme
```bash
# set prompt colors
## Function to get the Git branch name with parentheses and "git-" prefix
get_git_branch() {
    local branch
    branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    if [ -n "$branch" ]; then
        echo "(git)-[$branch]"
    fi
}

## Function to get the Python virtual environment name with "py-" prefix
get_virtualenv() {
    if [ -n "$VIRTUAL_ENV" ]; then
        echo "(pyenv)-[$(basename "$VIRTUAL_ENV")]"
    fi
}

## Function to set the PS1 variable
set_prompt() {
    local branch_name=$(get_git_branch)
    local venv_name=$(get_virtualenv)

    if [ "$(id -u)" == "0" ]; then
        # Set PS1 for the root user (red prompt)
        PS1='\[\e[1;31m\]\u\[\e[1;33m\]@\h\[\e[1;31m\] \W'
    else
        # Set PS1 for regular users (green prompt)
        PS1='\[\e[1;33m\]\u\[\e[1;34m\]@\h\[\e[1;33m\] \W'
    fi

    if [ -n "$branch_name" ]; then
        PS1+="\[\e[1;37m\] $branch_name"
    fi

    if [ -n "$venv_name" ]; then
        PS1+="\[\e[1;37m\] $venv_name"
    fi

    if [ "$(id -u)" == "0" ]; then
        PS1+='\[\e[1;31m\] \$ \e[0m\]'
    else
        PS1+='\[\e[1;33m\] \$ \e[0m\]'
    fi
}

## Set the PS1 variable
set_prompt

## Function to update the prompt when the directory changes
update_prompt() {
    set_prompt
}
export -f update_prompt

## Hook into the prompt command
export PROMPT_COMMAND="update_prompt; $PROMPT_COMMAND"
```
