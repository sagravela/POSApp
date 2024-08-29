import subprocess

output_dir = "app"

# Define the PyInstaller command
command = [
    "pyinstaller", 
    "--onefile", 
    "--windowed", 
    "app.py", 
    "--distpath", "./{output_dir}/dist", 
    "--workpath", "./{output_dir}/build", 
    "--specpath", "./{output_dir}/spec"
]

# Run the command
subprocess.run(command, check=True)
