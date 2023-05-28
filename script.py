import os
import subprocess
import time

# Function to install Python
def install_python():
    print("Installing Python...")
    subprocess.call(['/usr/sbin/softwareupdate', '-i', 'python'])
    print("Python installation complete.")

# Function to install Homebrew
def install_homebrew():
    print("Installing Homebrew...")
    subprocess.call(['/usr/bin/ruby', '-e', '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)'])
    print("Homebrew installation complete.")

# Function to get a list of applications in the Applications folder
def get_application_list():
    app_folder = '/Applications'
    app_list = [filename for filename in os.listdir(app_folder) if filename.endswith('.app')]
    return app_list

# Function to install applications via Homebrew
def install_applications(app_list):
    not_yet = []
    total_apps = len(app_list)
    completed_apps = 0

    print("Installing Applications:")

    for app_name in app_list:
        completed_apps += 1
        print("{}/{}: {}".format(completed_apps, total_apps, app_name))

        command = 'brew info --json=v2 {}'.format(app_name)
        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = result.communicate()
        output = output.strip().decode('utf-8')

        if 'No available formula or cask with the name' in output:
            not_yet.append(app_name)
        else:
            subprocess.call(['brew', 'install', app_name])
            time.sleep(0.1)

    return not_yet

# Main script
def main():
    print("Welcome to the Application Manager!")
    print("Choose an option:")
    print("1. Pre-Wipe: Create Application List")
    print("2. Post-Wipe: Restore Applications")

    choice = int(input("Enter your choice (1 or 2): "))

    if choice == 1:
        # Pre-Wipe: Create Application List
        app_list = get_application_list()
        with open('App List.txt', 'w') as file:
            file.write('\n'.join(app_list))
        print("App List created.")

    elif choice == 2:
        # Post-Wipe: Restore Applications
        install_python()
        install_homebrew()

        app_list_file = input("Enter the path to the App List file: ")

        with open(app_list_file, 'r') as file:
            app_list = file.read().splitlines()

        not_yet = install_applications(app_list)

        print("Applications not yet installed:")
        print('\n'.join(not_yet))

    else:
        print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
