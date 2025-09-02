#!/bin/bash
# UV Package Manager Enforcement Script
# This script intercepts pip commands and redirects to UV

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if UV is installed
check_uv_installed() {
    if ! command -v uv &> /dev/null; then
        echo -e "${YELLOW}⚠️ UV is not installed. Installing now...${NC}"
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.cargo/bin:$PATH"
        
        if ! command -v uv &> /dev/null; then
            echo -e "${RED}❌ Failed to install UV. Please install manually:${NC}"
            echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
            exit 1
        fi
        echo -e "${GREEN}✅ UV installed successfully!${NC}"
    fi
}

# Convert pip command to UV command
convert_pip_to_uv() {
    local pip_cmd="$@"
    local uv_cmd=""
    
    # Parse pip command and convert to UV equivalent
    if [[ "$pip_cmd" == *"install"* ]]; then
        if [[ "$pip_cmd" == *"-r"* ]]; then
            # pip install -r requirements.txt → uv pip install -r requirements.txt
            uv_cmd="${pip_cmd//pip/uv pip}"
            uv_cmd="${uv_cmd//pip3/uv pip}"
        elif [[ "$pip_cmd" == *"-e"* ]]; then
            # pip install -e . → uv pip install -e .
            uv_cmd="${pip_cmd//pip/uv pip}"
            uv_cmd="${uv_cmd//pip3/uv pip}"
        else
            # pip install package → uv pip install package
            uv_cmd="${pip_cmd//pip/uv pip}"
            uv_cmd="${uv_cmd//pip3/uv pip}"
        fi
    elif [[ "$pip_cmd" == *"uninstall"* ]]; then
        # pip uninstall package → uv pip uninstall package
        uv_cmd="${pip_cmd//pip/uv pip}"
        uv_cmd="${uv_cmd//pip3/uv pip}"
    elif [[ "$pip_cmd" == *"freeze"* ]]; then
        # pip freeze → uv pip freeze
        uv_cmd="uv pip freeze"
    elif [[ "$pip_cmd" == *"list"* ]]; then
        # pip list → uv pip list
        uv_cmd="uv pip list"
    else
        # Default fallback
        uv_cmd="${pip_cmd//pip/uv pip}"
        uv_cmd="${uv_cmd//pip3/uv pip}"
    fi
    
    echo "$uv_cmd"
}

# Main enforcement function
enforce_uv() {
    local original_cmd="$@"
    
    echo -e "${RED}🚫 PIP COMMAND BLOCKED!${NC}"
    echo -e "${YELLOW}You tried to run: ${NC}$original_cmd"
    echo ""
    
    # Check and install UV if needed
    check_uv_installed
    
    # Convert to UV command
    local uv_cmd=$(convert_pip_to_uv "$original_cmd")
    
    echo -e "${GREEN}✅ Use this instead:${NC}"
    echo -e "${BLUE}$uv_cmd${NC}"
    echo ""
    
    # Ask if user wants to run the UV command
    read -p "Run the UV command now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}Executing: $uv_cmd${NC}"
        eval "$uv_cmd"
    else
        echo -e "${YELLOW}Command not executed. Please run manually:${NC}"
        echo "$uv_cmd"
    fi
}

# Create pip/pip3 wrapper functions for shell environments
create_shell_wrappers() {
    cat << 'EOF'
# UV Enforcement: Override pip and pip3 commands
pip() {
    echo -e "\033[0;31m🚫 PIP COMMAND BLOCKED!\033[0m"
    echo "Use UV instead: uv pip $@"
    echo ""
    echo "Examples:"
    echo "  pip install package     → uv pip install package"
    echo "  pip install -r reqs.txt → uv pip install -r reqs.txt"
    echo "  pip freeze              → uv pip freeze"
    return 1
}

pip3() {
    pip "$@"
}

python_m_pip() {
    echo -e "\033[0;31m🚫 PYTHON -M PIP BLOCKED!\033[0m"
    echo "Use UV instead: uv pip $@"
    return 1
}

# Alias python -m pip to our wrapper
alias "python -m pip"="python_m_pip"
alias "python3 -m pip"="python_m_pip"

# Export functions for subshells
export -f pip
export -f pip3
export -f python_m_pip
EOF
}

# If sourced, set up shell wrappers
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
    create_shell_wrappers
else
    # If executed directly, enforce UV for the given command
    enforce_uv "$@"
fi