import tkinter as tk
import random

# Define the main window
root = tk.Tk()
root.title("Banker's Algorithm")

# Define the input fields
np_label = tk.Label(root, text="Number of processes:")
np_label.grid(row=0, column=0, padx=10, pady=10)
np_entry = tk.Entry(root, width=10)
np_entry.grid(row=0, column=1, padx=10, pady=10)

nr_label = tk.Label(root, text="Number of resources:")
nr_label.grid(row=1, column=0, padx=10, pady=10)
nr_entry = tk.Entry(root, width=10)
nr_entry.grid(row=1, column=1, padx=10, pady=10)

allocation_label = tk.Label(root, text="Initial allocation matrix:")
allocation_label.grid(row=2, column=0, padx=10, pady=10)
allocation_entry = tk.Text(root, width=20, height=5)
allocation_entry.grid(row=2, column=1, padx=10, pady=10)

max_label = tk.Label(root, text="Max requirement matrix:")
max_label.grid(row=3, column=0, padx=10, pady=10)
max_entry = tk.Text(root, width=20, height=5)
max_entry.grid(row=3, column=1, padx=10, pady=10)

avail_label = tk.Label(root, text="Available resources:")
avail_label.grid(row=4, column=0, padx=10, pady=10)
avail_entry = tk.Entry(root, width=20)
avail_entry.grid(row=4, column=1, padx=10, pady=10)

# Define the output field
output_label = tk.Label(root, text="", font=("Arial", 12))
output_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Define the submit button
def submit():
    # Get the input values
    try:
        np = int(np_entry.get())
        nr = int(nr_entry.get())
        allocation = [[int(x) for x in row.split()] for row in allocation_entry.get("1.0", tk.END).split('\n') if row.strip()]
        max = [[int(x) for x in row.split()] for row in max_entry.get("1.0", tk.END).split('\n') if row.strip()]
        avail = [int(x) for x in avail_entry.get().split()]

        # Check that the input values are valid
        if np <= 0 or nr <= 0 or len(allocation) != np or len(max) != np or len(avail) != nr:
            raise ValueError

        for i in range(np):
            if len(allocation[i]) != nr or len(max[i]) != nr:
                raise ValueError

        if any(avail[i] < 0 for i in range(nr)):
            raise ValueError

    except ValueError:
        output_label.config(text="Invalid input values!")
        return

    # Calculate the need matrix
    need = [[max[i][j] - allocation[i][j] for j in range(nr)] for i in range(np)]

    # Initialize the work and finish arrays
    work = avail.copy()
    finish = [False] * np

    # Initialize the safe sequence
    safe_seq = []

    # Loop through all processes until all have been executed or a deadlock is detected
    while False in finish:
        # Find a process that can be executed
        found = False
        for i in range(np):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(nr)):
                # Execute the process
                for j in range(nr):
                    work[j] += allocation[i][j]
                finish[i] = True
                safe_seq.append(i)
                found = True
                break

        # If no process can be executed, a deadlock has occurred
        if not found:
            output_label.config(text="Deadlock detected!")
            return

    # If all processes have been executed, the system is in a safe state
    output_label.config(text="The system is in safe state! Safe sequence is ==> " + " -> ".join("P" + str(safe_seq[i]) for i in range(np)))

submit_button = tk.Button(root, text="Submit", font=("Arial", 12), command=submit)
submit_button.grid(row=6, column=0, padx=10, pady=10)

# Define the reset button
def reset():
    np_entry.delete(0, tk.END)
    nr_entry.delete(0, tk.END)
    allocation_entry.delete("1.0", tk.END)
    max_entry.delete("1.0", tk.END)
    avail_entry.delete(0, tk.END)
    output_label.config(text="")

reset_button = tk.Button(root, text="Reset", font=("Arial", 12), command=reset)
reset_button.grid(row=6, column=1, padx=10, pady=10)

# Add padding to all widgets
for child in root.winfo_children():
    child.grid_configure(padx=10, pady=10)

root.mainloop()