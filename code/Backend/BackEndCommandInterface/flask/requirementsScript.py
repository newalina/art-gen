import pkg_resources

def check_installed_versions(requirements_path='requirements.txt'):
    # Read the requirements file
    with open(requirements_path, 'r') as file:
        requirements = file.readlines()

    # Check each required package against the installed version
    for requirement in requirements:
        requirement = requirement.strip()
        if not requirement:
            continue  # skip empty lines

        # Parse the requirement package and version
        package_name, required_version = requirement.split('==')

        try:
            # Get the currently installed version of the package
            installed_version = pkg_resources.get_distribution(package_name).version
            if installed_version == required_version:
                print(f"{package_name}: Version is correct ({installed_version})")
            else:
                print(f"{package_name}: Version mismatch (Required: {required_version}, Installed: {installed_version})")
        except pkg_resources.DistributionNotFound:
            print(f"{package_name}: Not installed")

import subprocess

def create_requirements_txt(output_file='requirements.txt'):
    # Execute pip freeze and capture the output
    result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True)

    if result.returncode != 0:
        print("Failed to run pip freeze")
        return

    # Write the output to the specified output file
    with open(output_file, 'w') as file:
        file.write(result.stdout)

    print(f"'{output_file}' has been created with the current environment's package list.")


if __name__ == "__main__":
    check_installed_versions()
    # create_requirements_txt()