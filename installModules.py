import os
import sys
import subprocess
import importlib.util
import pkg_resources
import logging

script_filename = os.path.basename(sys.argv[0])

def is_module_installed(module_name):
    spec = importlib.util.find_spec(module_name)
    return spec is not None

def setup_logging(log_file, console_output=True):
    level = logging.ERROR if not console_output else logging.INFO
    handlers = [logging.FileHandler(log_file)]
    if console_output:
        handlers.append(logging.StreamHandler(sys.stdout))

    logging.basicConfig(
        level=level,
        format=f'[{script_filename}] [%(asctime)s] %(levelname)s: %(message)s',  # Include script filename in the format
        handlers=handlers
    )

def get_user_home_directory():
    return os.path.expanduser("/Users/h.clewlow/Desktop/ElixirLabs/PythonScripts/File Organiser/Logs")

def log_table(table):
    logging.info("\nInstalled Modules:\n" + table)

def log_info(message, newline=True):
    if newline:
        logging.info('\n' + message)
    else:
        logging.info(message)

def log_success(message):
    log_info(colored(message, 'green'), False)

def log_warning(message):
    log_info(colored(message, 'yellow'), False)

def log_error(message):
    logging.error(message)

def install_prereq_modules():
    required_modules = ['termcolor', 'tabulate']

    for module in required_modules:
        if not is_module_installed(module):
            log_info(f"Starting installation of '{module}' module...")
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', module], check=True)
                log_success(f"Successfully installed '{module}' module.")
            except subprocess.CalledProcessError:
                log_error(f"Failed to install '{module}' module.")
        else:
            log_success(f"'{module}' module is already installed.")

try:
    from termcolor import colored
    from tabulate import tabulate
except ImportError as e:
    log_warning(f"Some required modules are not installed: {e}")
    install_prereq_modules()

    try:
        from termcolor import colored
        from tabulate import tabulate
    except ImportError as e:
        log_error("Error: Failed to install required modules. Exiting...")
        sys.exit(1)

def get_module_info(module_name):
    version = pkg_resources.get_distribution(module_name).version
    return {'Module Name': module_name, 'Version': version}

def uninstall_required_modules(modules_to_uninstall):
    log_file = os.path.join(get_user_home_directory(), 'uninstall_log.txt')  # Change this file name as needed
    setup_logging(log_file)

    try:
        uninstalled_modules = set()
        not_uninstalled_modules = set()

        total_modules = len(modules_to_uninstall)
        for idx, module in enumerate(modules_to_uninstall, 1):
            if is_module_installed(module):
                log_warning(f"[{idx}/{total_modules}] Module '{module}' is installed.")
                choice = input(f"Do you want to uninstall '{module}'? (y/n): ").lower()
                if choice == 'y':
                    while True:  # Loop until the uninstallation succeeds or the user chooses to skip
                        log_warning(f"[{idx}/{total_modules}] Uninstalling '{module}'...")
                        try:
                            subprocess.run([sys.executable, '-m', 'pip', 'uninstall', module, '-y'], check=True)
                            uninstalled_modules.add(module)
                            log_success(f"[{idx}/{total_modules}] Successfully uninstalled module: {module}")
                            break  # Uninstallation successful, break out of the loop
                        except subprocess.CalledProcessError:
                            log_error(f"[{idx}/{total_modules}] Failed to uninstall module: {module}")
                            retry_choice = input(f"Do you want to retry uninstalling '{module}'? (y/n): ").lower()
                            if retry_choice != 'y':
                                break  # User chooses to skip, break out of the loop
                            # Otherwise, retry the uninstallation
                else:
                    not_uninstalled_modules.add(module)
                    log_info(f"[{idx}/{total_modules}] Skipping uninstallation of module: {module}", newline=False)
            else:
                log_success(f"[{idx}/{total_modules}] '{module}' module is not installed.", newline=False)

        if uninstalled_modules:
            log_info("Uninstalled Modules:", newline=False)
            log_info(", ".join(uninstalled_modules), newline=False)

        if not_uninstalled_modules:
            log_info("Modules Not Uninstalled:", newline=False)
            log_info(", ".join(not_uninstalled_modules), newline=False)

        return uninstalled_modules, not_uninstalled_modules

    except Exception as e:
        log_error("An unexpected error occurred:")
        log_error(str(e))


def install_required_modules(required_modules):
    log_file = os.path.join(get_user_home_directory(), 'install_log.txt')  # Change this file name as needed
    setup_logging(log_file)

    try:
        install_prereq_modules()

        installed_modules = set()
        not_installed_modules = set()

        total_modules = len(required_modules)
        for idx, module in enumerate(required_modules, 1):
            # Check if the module is installed
            if is_module_installed(module):
                installed_modules.add(module)
                log_success(f"[{idx}/{total_modules}] Module '{module}' is already installed.")
            else:
                # Attempt to install the module along with its dependencies using pip
                while True:  # Loop until the installation succeeds or the user chooses to skip
                    log_warning(f"[{idx}/{total_modules}] Module '{module}' is not installed. Attempting to install...")
                    try:
                        subprocess.run([sys.executable, '-m', 'pip', 'install', module, '--user'], check=True)
                        installed_modules.add(module)
                        log_success(f"[{idx}/{total_modules}] Successfully installed module: {module}")
                        break  # Installation successful, break out of the loop
                    except subprocess.CalledProcessError:
                        log_error(f"[{idx}/{total_modules}] Failed to install module: {module}")
                        choice = input(f"Do you want to retry installing '{module}'? (y/n): ").lower()
                        if choice != 'y':
                            break  # User chooses to skip, break out of the loop
                        # Otherwise, retry the installation

        installed_modules_info = [get_module_info(module) for module in installed_modules]

        if installed_modules_info:
            table = tabulate(installed_modules_info, headers="keys", tablefmt="grid")
            log_table(table)

        if not_installed_modules:
            log_info("\nModules Not Installed:", newline=False)
            log_info(", ".join(not_installed_modules), newline=True)

        return installed_modules, not_installed_modules

    except Exception as e:
        log_error("An unexpected error occurred:")
        log_error(str(e))
        
def check_for_updates(required_modules):
    try:
        import pip
    except ImportError:
        log_error("pip module is not available. Cannot check for updates.")
        return

    outdated_modules = []
    installed_dists = [dist.key for dist in pkg_resources.working_set]
    
    for module_name in required_modules:
        try:
            if module_name in installed_dists:
                for dist in pkg_resources.working_set:
                    if dist.key == module_name:
                        current_version = dist.version
                        latest_version = pip.__version__  # Use pip version as a fallback in case pip is not available
                        latest_version = pkg_resources.get_distribution(module_name).version
                        if current_version != latest_version:
                            outdated_modules.append((module_name, current_version, latest_version))
                        break
        except Exception as e:
            log_error(f"Error checking for updates for module: {module_name}, {str(e)}")

    if outdated_modules:
        log_info("\nOutdated Modules:", newline=False)
        headers = ["Module Name", "Installed Version", "Latest Version"]
        table = tabulate(outdated_modules, headers=headers, tablefmt="grid")
        log_table(table)
    else:
        log_success("All modules are up to date.")
        
