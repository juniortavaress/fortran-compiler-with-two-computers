# fortran-compiler-with-two-computers

This project facilitates the workflow of compiling `.for` (Fortran) files on one computer and running the compiled output (`DLL`) on another. It is ideal for distributed environments where simulation and compilation processes are handled by separate machines.

---

## Project Overview

- **`hiwi-pc.py`**: Manages the preparation, parameterization, and monitoring of `.for` files on the simulation machine.
- **`fortran.py`**: Monitors the shared folder, compiles `.for` files into `DLL` (or equivalent compiled output), and transfers the compiled files back to the shared folder.

---

## Workflow

### 1. Parameterization and File Preparation (`hiwi-pc.py`)
- Reads an Excel file containing simulation parameters.
- Updates the `.for` file with the parameter values.
- Saves the updated `.for` file in simulation-specific folders.
- Transfers `.for` files to the shared folder for compilation.

### 2. Compilation (`fortran.py`)
- Monitors the shared folder for `.for` files.
- Compiles the `.for` files into `DLL` files using Abaqus or another compilation tool.
- Returns the compiled files to the shared folder.

### 3. Simulation (`hiwi-pc.py`)
- Retrieves the compiled files from the shared folder.
- Executes the simulation (e.g., using Abaqus) with the compiled files.

---

## Future Improvements

### Run Continuously (24/7)
Enhance `fortran.py` to run continuously as a system service, ensuring it resumes automatically after a system reboot. This could include:

- **Task Scheduler (Windows)**: Configure the script to start at system startup using the Task Scheduler.
- **Systemd (Linux)**: Create a systemd service to manage the script as a background process.
- **Automatic Logging**: Implement logging mechanisms to capture detailed activity logs, errors, and debug information.
- **Restart Mechanisms**: Add functionality to handle unexpected script failures and ensure the service restarts automatically.
