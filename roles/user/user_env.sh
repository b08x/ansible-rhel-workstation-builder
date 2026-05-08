if [ -d "$HOME/.rvm/bin" ]; then
    # Detect OS name from /etc/os-release
    os_name=""
    if [ -r /etc/os-release ]; then
        os_name=$(grep -E '^NAME=' /etc/os-release | cut -d= -f2 | tr -d '"' | tr '[:upper:]' '[:lower:]')
    fi

    if [[ "$os_name" != "bluefin" ]]; then
        # Add RVM to PATH for scripting. Make sure this is the last PATH variable change.
        export PATH="$PATH:$HOME/.rvm/bin"
    fi
fi
