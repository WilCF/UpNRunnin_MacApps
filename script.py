import os
import subprocess
import time

# Function to create the 'App List'
def create_app_list():
    app_list = os.listdir('/Applications')
    with open('App List.txt', 'w') as file:
        file.write('\n'.join(app_list))
    print("App List created successfully!")

# Function to install Homebrew
def install_homebrew():
    subprocess.run(['/bin/bash', '-c', '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)'])
    print("Homebrew installation complete!")

# Function to install the latest version of Python using Homebrew
def install_python():
    subprocess.run(['brew', 'install', 'python'])
    print("Python installation complete!")

# Function to check if an application is installed
def is_app_installed(app_name):
    return os.path.exists('/Applications/' + app_name)

# Function to find the latest version of an application using Homebrew
def find_latest_version(app_name):
    result = subprocess.run(['brew', 'search', app_name], capture_output=True, text=True)
    output = result.stdout.strip().split('\n')
    if output:
        return output[-1].split(' ')[0]
    else:
        return None

# Function to install an application using Homebrew
def install_application(app_name):
    subprocess.run(['brew', 'install', app_name])

# Function to display progress
def display_progress(start_time, current_index, total_count):
    elapsed_time = time.time() - start_time
    average_time = elapsed_time / current_index
    remaining_time = (total_count - current_index) * average_time
    print(f"Progress: {current_index}/{total_count} | Elapsed Time: {elapsed_time:.2f}s | Remaining Time: {remaining_time:.2f}s")

# Main script
def main():
    print("Welcome to RockNRollMacInstaller!")
    print("Please select an option:")
    print("1. Create App List")
    print("2. Install Applications")

    option = input("Enter your choice (1 or 2): ")

    if option == '1':
        create_app_list()
    elif option == '2':
        # Part 1: Install Homebrew
        print("Installing Homebrew...")
        install_homebrew()

        # Part 2: Install Python
        print("Installing Python...")
        install_python()

        # Part 3: Check and install missing applications
        with open('App List.txt', 'r') as file:
            app_list = file.read().split('\n')

        not_yet = []
        print("Checking for missing applications...")
        for app in app_list:
            if not is_app_installed(app):
                not_yet.append(app)
        total_count = len(not_yet)

        if total_count > 0:
            print("Installing missing applications:")
            start_time = time.time()
            for i, app in enumerate(not_yet, start=1):
                version = find_latest_version(app)
                if version:
                    print(f"Installing {app} ({version})...")
                    install_application(app)
                else:
                    print(f"Unable to find the latest version of {app}. Skipping installation.")
                display_progress(start_time, i, total_count)
            print("Installation of missing applications complete.")
        else:
            print("No missing applications found.")
    else:
        print("Invalid option. Please try again.")

if __name__ == '__main__':
    main()
