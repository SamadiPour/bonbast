#!/bin/bash

# Check if the user provided an argument
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 [python|standalone]"
  exit 1
fi

option="$1"

if [[ "$option" != "python" && "$option" != "standalone" ]]; then
  echo "Invalid option: $option"
  echo "Usage: $0 [python|standalone]"
  exit 1
fi

# Check if Homebrew is installed
if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew not found. Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Function to check if a brew package is installed
function is_brew_package_installed() {
  local package_name="$1"
  brew list --versions "$package_name" >/dev/null
  return $?
}

# Ensure jq is installed
if ! is_brew_package_installed "jq"; then
  echo "jq package not found. Installing jq..."
  brew install jq
else
  echo "jq package already installed."
fi

if [ "$option" == "standalone" ]; then
  # Update Homebrew
  echo "Updating Homebrew..."
  brew update

  echo "Installing package..."
  package_name="samadipour/bonbast/bonbast"
  brew install "$package_name"

  echo "Package $package_name installed successfully!"
fi

# Set default directory path to Downloads folder
default_directory_path="${HOME}/Downloads"

# Ask user for directory path
echo "Enter Raycast script commands directory path (default: ${default_directory_path}):"
read -r directory_path

# Use the default directory path if user input is empty
if [ -z "$directory_path" ]; then
  directory_path="$default_directory_path"
fi

# Check if entered path is a valid directory
if [ -d "$directory_path" ]; then
  echo "Using directory path: $directory_path"
else
  echo "Error: The entered path is not a valid directory. Please check the path and try again."
  exit 1
fi

# Download and copy bonbast.sh to the specified directory
echo "Downloading bonbast.sh from GitHub https://github.com/SamadiPour/bonbast/blob/master/raycast_script/bonbast.sh"
curl -sL https://raw.githubusercontent.com/SamadiPour/bonbast/master/raycast_script/bonbast.sh -o "${directory_path}/bonbast.sh"

# Check if the file was downloaded and copied successfully
if [ -f "${directory_path}/bonbast.sh" ]; then
  echo "bonbast.sh has been successfully downloaded to ${directory_path}/bonbast.sh"
else
  echo "Error: Failed to copy bonbast.sh to ${directory_path}. Please check your internet connection and try again."
  exit 1
fi

# After copying the file to the directory
if [ "$option" == "standalone" ]; then
  echo "Modifying the bonbast.sh file for standalone option..."
  sed -i.bak 's|/opt/homebrew/bin/python3 -m ||' "${directory_path}/bonbast.sh"
  rm "${directory_path}/bonbast.sh.bak"
fi

echo "Please read docs to add this script to Raycast."