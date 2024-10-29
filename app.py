import tkinter as tk
from tkinter import ttk, messagebox
import Molly
import concurrent.futures
import threading

# Initialize a thread lock for exclusive access
transcription_lock = threading.Lock()

# Create a ThreadPoolExecutor to handle long-running tasks
executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

# Define the function for video editing with thread-based locking
def edit_video(description, output_folder, file_path, chunking, log_widget):
    try:
        # Attempt to acquire the lock
        if not transcription_lock.acquire(blocking=False):
            log_widget.insert(tk.END, "Another transcription is currently running. Please wait.\n")
            log_widget.see(tk.END)
            return

        # Define the task to run in a separate thread
        def task():
            editor = Molly.molly()
            log_widget.insert(tk.END, "Starting video editing...\n")
            log_widget.see(tk.END)

            log_widget.insert(tk.END, f"Description: {description}\n")
            log_widget.insert(tk.END, f"Output Folder: {output_folder}\n")
            log_widget.insert(tk.END, f"File Path: {file_path}\n")
            log_widget.insert(tk.END, f"Chunking Size: {chunking}\n")
            log_widget.see(tk.END)

            editor.create_Timeline(video_path=file_path, output_folder=output_folder, chunking_size=chunking, description=description, log=log_widget)
            log_widget.insert(tk.END, "Video edited successfully!\n")
            log_widget.see(tk.END)
            messagebox.showinfo("Success", "Video edited successfully!")

        # Submit the task to the executor
        future = executor.submit(task)
        
        # Use future.result() to get the output and release the lock afterward
        future.result()
    except Exception as e:
        log_widget.insert(tk.END, f"An error occurred: {e}\n")
        log_widget.see(tk.END)
        messagebox.showerror("Error", "An error occurred during video editing.")
    finally:
        transcription_lock.release()

# Create the tkinter main window with dark blue background
root = tk.Tk()
root.title("Molly, the AI Video Editor")
root.configure(bg="#1c1f4a")  # Dark blue background

# Set up the interface elements with light text for readability
tk.Label(root, text="Molly, the AI Video Editor", font=("Helvetica", 24, "bold"), fg="white", bg="#1c1f4a").grid(row=0, column=0, columnspan=2, pady=10)

# Input fields
tk.Label(root, text="Input Video Path:", fg="white", bg="#1c1f4a").grid(row=1, column=0, padx=10, pady=5, sticky="e")
video_entry = tk.Entry(root, width=50)
video_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Output Folder:", fg="white", bg="#1c1f4a").grid(row=2, column=0, padx=10, pady=5, sticky="e")
output_entry = tk.Entry(root, width=50)
output_entry.insert(0, "./output")
output_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Video Description:", fg="white", bg="#1c1f4a").grid(row=3, column=0, padx=10, pady=5, sticky="e")
description_entry = tk.Entry(root, width=50)
description_entry.insert(0, "A simple gaming video.")
description_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Chunk Size:", fg="white", bg="#1c1f4a").grid(row=4, column=0, padx=10, pady=5, sticky="e")
chunking_entry = tk.Entry(root, width=50)
chunking_entry.insert(0, "500")
chunking_entry.grid(row=4, column=1, padx=10, pady=5)

# Function to get input and start editing
def start_editing():
    description = description_entry.get()
    output_folder = output_entry.get()
    file_path = video_entry.get()
    try:
        chunking = int(chunking_entry.get())
        log_widget.delete(1.0, tk.END)  # Clear the log widget
        threading.Thread(target=edit_video, args=(description, output_folder, file_path, chunking, log_widget)).start()
    except ValueError:
        messagebox.showerror("Error", "Chunk Size must be a number.")

# Style the button to be orange with rounded edges
style = ttk.Style()
style.map("TButton",
          background=[("active", "#ff8b66")],  # Lighter shade on hover
          foreground=[("active", "orange")])

# Edit button with rounded edges
edit_button = ttk.Button(root, text="One Click Edit", style="TButton", command=start_editing)
edit_button.grid(row=5, column=0, columnspan=2, pady=10)

# Log text widget for displaying progress
log_widget = tk.Text(root, width=70, height=10, wrap="word", bg="#333333", fg="white", font=("Helvetica", 10))
log_widget.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Run the tkinter main loop
root.mainloop()
