import re
import os
import time
import shutil
import pandas as pd

# Reads the Fortran and Excel files in the simulation data folder.
def read_and_get_params_values(simulation_main_folder):
    """
    For each row in the Excel file, it updates the Fortran parameters and saves 
    a new Fortran file in a simulation-specific folder.
    """
    path_to_datas = os.path.join(simulation_main_folder, 'simulation-datas')

    for file in os.listdir(path_to_datas):
        if file.endswith('.for'):
            fortrar_path = os.path.join(path_to_datas, file)

    for file in os.listdir(path_to_datas):
        if file.endswith('.xlsx'):
            file_path = os.path.join(path_to_datas, file)
            df = pd.read_excel(file_path)

            for index, row in df.iterrows():
                new_values = {'A': f"{row['A']}",'B': f"{row['B']}",'n': f"{row['n']}",'C1': f"{row['C1']}",'C2': f"{row['C2']}",'C3': f"{row['C3']}",'k': f"{row['k']}",'Ts': f"{row['Ts']}"}
                update_fortran_parameters(fortrar_path, simulation_main_folder, index, new_values)
   

# Updates the parameters in the Fortran file and saves it in a simulation-specific folder.
def update_fortran_parameters(fortrar_inp_path, simulation_main_folder, simulation_number, values):
    """
    Args:
        fortrar_inp_path (str): Path to the original Fortran file.
        simulation_main_folder (str): Path to the main simulation folder.
        simulation_number (int): The simulation index for folder naming.
        values (dict): Dictionary containing the new parameter values.
    """
    with open(fortrar_inp_path, 'r') as file:
        content = file.read()

    for param, new_value in values.items():
        content = re.sub(rf'({param}\s*=\s*)[0-9D\.\-]+', rf'\g<1>{new_value}', content)

    fortrar_out_path = os.path.join(simulation_main_folder, f'simulation-{simulation_number}')
    fortran_file_path = os.path.join(fortrar_out_path, os.path.basename(fortrar_inp_path))

    if not os.path.exists(fortrar_out_path):
        os.makedirs(fortrar_out_path)

    with open(fortran_file_path, 'w') as file:
        file.write(content)


# Function to check for .for files in any subfolder of a given directory
def check_for_update(fortran_folder):
    """
    Checks if there is a .for file in any subfolder of the fortran_folder.
    Returns the folder and the full path to the .for file if found, otherwise returns None, None.
    """
    for folder, subfolders, files in os.walk(fortran_folder):
        if folder != 'simulation-datas':
            for file in files:
                if file.endswith(".for"):
                    path_to_file = os.path.join(folder, file)
                    return folder, path_to_file
    return None, None


# Function to send the .for file to the shared folder
def send_fortran_to_shared_folder(fortran_file, shared_folder):
    """
    Sends the specified Fortran file to the shared folder.
    """
    shared_path = os.path.join(shared_folder, os.path.basename(fortran_file))
    shutil.copy(fortran_file, shared_path)


# Function to receive a DLL file from the shared folder and move it to the simulation folder
def receive_dll_from_shared_folder(shared_folder, simulation_folder):
    """
    Checks if a DLL file (explicitU.dll) exists in the shared folder and moves it 
    to the specified simulation folder.
    Returns True if the file was moved successfully, otherwise False.
    """
    shared_dll = os.path.join(shared_folder, "explicitU.dll")
    local_dll = os.path.join(simulation_folder, "explicitU.dll")

    if os.path.exists(shared_dll):
        shutil.move(shared_dll, local_dll)
        print(f"File {os.path.basename(local_dll)} received from the shared folder.") 
        return True
    return False


# Function to execute the simulation using Abaqus
def run_simulation(simulation_folder, abaqus_command):
    """
    Executes an Abaqus simulation for all .inp files in the simulation folder.
    """
    for file in os.listdir(simulation_folder):
        if file.endswith(".inp"):
            job_path = os.path.join(simulation_folder, file)
            # command = f'call {abaqus_command} job={job_path} cpus=4 interactive'
            # os.system(command)
    print(f"Simulation {os.path.basename(job_path)} completed successfully.")


# Main loop to monitor, process, and execute simulations
if __name__ == "__main__":
    print("======================================")
    print("\nINITIALIZING THE CODE\n")
    print("======================================\n")

    # Configuration variables
    abaqus_command = r"C:\SIMULIA\Commands\abq2021.bat"
    job_path = r"simulation-folder\123"
    
    # Paths
    local_folder = os.getcwd()  
    aux_folder = os.path.join(local_folder, "aux-folder")
    fortran_folder = os.path.join(local_folder, "fortran-files-hiwi-pc")
    shared_folder = os.path.join(local_folder, "shared-folder")
    simulation_main_folder = os.path.join(local_folder, "simulation-folder")

    read_and_get_params_values(simulation_main_folder)

    # Infinite loop to continuously monitor for updates
    while True:
        simulation_folder, fortran_file = check_for_update(simulation_main_folder)

        if fortran_file:
            # Send the .for file to the shared folder
            send_fortran_to_shared_folder(fortran_file, shared_folder)
            os.remove(fortran_file)
            print(f"File {os.path.basename(fortran_file)} sent to the shared folder")

            # Wait for the compiled DLL to be returned
            print("Waiting for the compiled DLL...")
            while not receive_dll_from_shared_folder(shared_folder, simulation_folder):
                time.sleep(10)  # Verifica a cada 10 segundos

            # Wait for the compiled DLL to be returned
            # run_simulation(simulation_folder, abaqus_command)

            print("Process completed, waiting for the next request...\n")
            print("======================================\n")

        time.sleep(20)  # Check for updates every 20 seconds
