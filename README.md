# PythonModuleHelper: Simplifying Package Management

PythonModuleHelper is a versatile Python script designed to simplify package management by providing easy installation, updating, and uninstalling of Python modules. This script utilizes the `pip` package manager to handle module operations, making it a powerful tool for developers seeking an efficient and user-friendly package management experience.

## Prerequisites

Before using PythonModuleHelper, ensure that you have the following installed on your system:

- Python 3.x
- `pip` package manager

## Getting Started

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/username/PythonModuleHelper.git
   cd PythonModuleHelper
   ```

2. Install the required modules:

   Before running the script, you need to install the prerequisite modules `termcolor` and `tabulate`. PythonModuleHelper provides a built-in function to do this:

   ```bash
   python script_name.py install_prereq_modules
   ```

   If you encounter any issues during the installation, please check your Python and `pip` installations and ensure they are up-to-date.

3. Execute PythonModuleHelper commands:

   The script can be used to perform various tasks related to package management. Here are the available commands:

   - **Install Required Modules**:

     To install a list of required modules, provide the module names as arguments:

     ```bash
     python script_name.py install_required_modules module1 module2 module3
     ```

     The script will attempt to install the specified modules along with their dependencies. If a module is already installed, it will be skipped.

   - **Uninstall Modules**:

     To uninstall unwanted modules, provide the module names as arguments:

     ```bash
     python script_name.py uninstall_required_modules module1 module2 module3
     ```

     The script will check if each module is installed and prompt you to confirm the uninstallation. If you choose to proceed, it will uninstall the module from your environment.

   - **Check for Updates**:

     To check for updates for installed modules, use the following command:

     ```bash
     python script_name.py check_for_updates module1 module2 module3
     ```

     The script will compare the currently installed versions of the specified modules with the latest versions available on PyPI. If any updates are found, it will display a table with the outdated modules.

## Logging

PythonModuleHelper generates log files to keep track of its operations. The logs are stored in the directory specified by `get_user_home_directory()`. The log filenames are `install_log.txt` for installation-related logs and `uninstall_log.txt` for uninstallation-related logs.

## Feedback and Support

If you encounter any issues, have suggestions, or need assistance with PythonModuleHelper, please feel free to [open an issue](link_to_issues) on the GitHub repository. Our responsive community and maintainers will be glad to help.

## Contribution

We welcome contributions from the community to enhance PythonModuleHelper's functionality and usability. To contribute, please follow our [contribution guidelines](link_to_contributing.md).

Join us in simplifying Python package management with PythonModuleHelper! Happy coding! 🐍💻
