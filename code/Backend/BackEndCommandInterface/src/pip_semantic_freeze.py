import subprocess

# Run pip freeze and capture the output
result = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE, text=True)
packages = result.stdout.split('\n')

# Create a new requirements file
with open('requirements_tilde.txt', 'w') as f:
    for package in packages:
        if package:
            name, version = package.split('==')
            # Generate compatible release specifier
            major, minor, *_ = version.split('.')
            f.write(f'{name}~={major}.{minor}\n')
