import os
import time
import subprocess
import shutil

# Function to compile a Fortran file into a DLL
def compile_fortran(fortran_file, abaqus_command, shared_folder):
    """
    Compiles the Fortran file to generate a DLL (simulated here as explicitU.txt).
    """

    # Log that the file has been received
    print(f"File {os.path.basename(fortran_file)} received from the shared folder.")

    try:
        command = f'call {abaqus_command} make library={fortran_file}'
        subprocess.run(command, shell=True, check=True)
        print(f"{fortran_file} compilado com sucesso.")

        # Simulate creating a dummy compiled file (explicitU.txt)
        # with open("explicitU.txt", "w") as file:
        #     file.write("")

        # Move the "DLL" (explicitU.txt) to the shared folder
        dll_file = "explicitU.dll"
        # dll_file = "explicitU.txt"
        shared_dll = os.path.join(shared_folder, dll_file)
        if os.path.exists(dll_file):
            shutil.move(dll_file, shared_dll)
            print(f"File {os.path.basename(dll_file)} moved to the shared folder")
    except subprocess.CalledProcessError as e:
        print(f"Error during compilation: {e}")


# Main script to monitor the shared folder and process Fortran files
if __name__ == "__main__":
    print("======================================")
    print("\nINITIALIZING THE CODE\n")
    print("======================================\n")

    # Configuration variables
    abaqus_command = r"C:\SIMULIA\Commands\abq2021.bat"
    
    # Paths
    local_folder = os.path.dirname(os.getcwd())   
    # print(local_folder)
    # local_folder = os.getcwd()
    shared_folder = os.path.join(local_folder, "shared-folder")
    simulation_folder = os.path.join(local_folder, "simulation-folder")

    # Continuous loop to monitor the shared folder
    while True:
        # Check for .for files in the shared folder
        for file in os.listdir(shared_folder):
            if file.endswith(".for"):
                shared_fortran = os.path.join(shared_folder, file)

                # Compile the fortran file
                compile_fortran(shared_fortran, abaqus_command, shared_folder)

                # Remove the processed .for file from the shared folder
                os.remove(shared_fortran)
            
                print("Process completed, waiting for the next request...\n")
                print("======================================\n")

        time.sleep(10)  # Check for updates every 20 seconds
