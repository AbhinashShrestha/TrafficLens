import os
import subprocess
import json
import tkinter as tk
from tkinter import filedialog,messagebox

class App:
    def __init__(self, master):
        self.master = master
        master.title("Four Wheeler Overspeeding Detection")
        master.geometry("500x600")
        master.config(bg="#1A2B3C")

        self.file_label = tk.Label(master, text="", font=("SF Pro Display", 20), fg="white", bg="#1A2B3C")
        self.file_label.pack(pady=20)

        self.select_button = tk.Button(master, text="Select Video", font=("SF Pro Display", 20), command=self.selectFile, bg="#008CBA", fg="black", borderwidth=0, padx=20, pady=10, activebackground="#005F7F", activeforeground="white", highlightthickness=0)
        self.select_button.pack(fill=tk.X, padx=50, pady=10)

        self.process_button = tk.Button(master, text="Process Video", font=("SF Pro Display", 20), command=self.processVideo, bg="#008CBA", fg="black", borderwidth=0, padx=20, pady=10, activebackground="#005F7F", activeforeground="white", highlightthickness=0)
        self.process_button.pack(fill=tk.X, padx=50, pady=10)

        self.analyze_button = tk.Button(master, text="Analyze Video", font=("SF Pro Display", 20), command=self.analyzeVideo, bg="#008CBA", fg="black", borderwidth=0, padx=20, pady=10, activebackground="#005F7F", activeforeground="white", highlightthickness=0)
        self.analyze_button.pack(fill=tk.X, padx=50, pady=10)
        
        self.play_button = tk.Button(master, text="Play Output Video", font=("SF Pro Display", 20), command=self.play_video, bg="#008CBA", fg="black", borderwidth=0, padx=20, pady=10, activebackground="#005F7F", activeforeground="white", highlightthickness=0)
        self.play_button.pack(fill=tk.X, padx=50, pady=10)

        self.report_button = tk.Button(master, text="Generate Report", font=("SF Pro Display", 20), command=self.generateReport, bg="#008CBA", fg="black", borderwidth=0, padx=20, pady=10, activebackground="#005F7F", activeforeground="white", highlightthickness=0)
        self.report_button.pack(fill=tk.X, padx=50, pady=10)
        
        self.open_report_button = tk.Button(master, text="Open Report", font=("SF Pro Display", 20), command=self.open_report, bg="#008CBA", fg="black", borderwidth=0, padx=20, pady=10, activebackground="#005F7F", activeforeground="white", highlightthickness=0)
        self.open_report_button.pack(fill=tk.X, padx=50, pady=10)
        
        self.open_graph_button= tk.Button(master, text="Open Graph", font=("SF Pro Display", 20), command=self.open_plot, bg="#008CBA", fg="black", borderwidth=0, padx=20, pady=10, activebackground="#005F7F", activeforeground="white", highlightthickness=0)
        self.open_graph_button.pack(fill=tk.X, padx=50, pady=10)

    
    def selectFile(self):
        global video
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Video", filetypes=(("Video files", "*.mp4 *.avi *.mkv"), ("All files", "*.*")))
        if filename:
            if "traffic_int1" in filename:
                area = "International Highway 1"
            elif "balkumari" in filename:
                area = "Balkumari Area"
            elif "koteshwor" in filename:
                area = "Koteshwor Area"
            elif "satdobato" in filename:
                area = "Satdobato Area"
            elif "traffic_int2" in filename:
                area = "International Highway 2"
            else:
                area = "Unknown Area"
                # Display a pop-up window if the selected video file's area is unknown
                pop_up_window = tk.Toplevel(self.master)
                pop_up_window.title("Error")
                pop_up_window.geometry("1200x600")
                pop_up_window.config(bg="#EEEEE8")
                error_message = tk.Label(pop_up_window, 
                text="SYSTEM IS UNABLE TO PROCEED ANY FURTHER WITH THE GIVEN INPUT VIDEO.\n\nHere are some suggestions that may help:\n\n- Check if the input video file exists and is readable.\n- Make sure that the video file format is supported by the system. (only .mp4 is supported)\n- Place the video in the designated folder (Assets_videos).\n- Rename the file that describes the area the video was taken.\n\nPlease try again with a different video file", font=("SF Pro Display", 30), fg="red", bg="#EEEEE8", wraplength=1200, justify="left")
                error_message.pack(pady=20)
                
                return

            # Write the name of the selected file and area to database_proxy.json
            with open("database_proxy.json", "w") as f:
                json.dump({"filename": os.path.basename(filename), "area": area}, f)
            self.file_label.config(text=f"{os.path.basename(filename)}\nArea: {area}")


    def processVideo(self):
        # Read the name of the selected file from database_proxy.json
        with open("database_proxy.json", "r") as f:
            data = json.load(f)
            filename = data.get("filename")
        if filename:
            # Run ffcomp.py on the selected video file
            subprocess.run(['python3', 'ffcomp.py'])
        else:
            messagebox.showerror("Error", "File Not Selected or File Doesn't Exist", icon="warning")


    def analyzeVideo(self):
        # Read the name of the selected file from database_proxy.json
        with open("database_proxy.json", "r") as f:
            data = json.load(f)
            filename = data.get("processed_filename")
            error = data.get("analyze_error")
        if filename:
            # Run main.py on the selected video file
            subprocess.run(['python3', 'main.py'])
            if not error:
                pass
            else:
                messagebox.showerror("Error","No Overspeeding Detected")
            
        else:
            messagebox.showerror("Error","File Not Processed or File Doesn't Exist", icon="warning")

    def play_video(self):
        # Read the output video path from database_proxy.json
        with open("database_proxy.json", "r") as f:
            data = json.load(f)
            output_video_path = data.get("output_video_path")


        if output_video_path:
            # Play the output video using the default player on the system
            # os.startfile(output_video_path) #windows
            subprocess.run(['open', output_video_path])
        else:
            messagebox.showerror("Error","Output video not found", icon="warning")

    def generateReport(self):
        # Read the name of the selected file from database_proxy.json
        with open("database_proxy.json", "r") as f:
            data = json.load(f)
            filename = data.get("filename")
            errors = data.get("pdf_report_errors")

        if filename:
            # Run report.py on the selected video file
            subprocess.run(['python3', 'report.py'])

            # If there are errors, display them in a pop-up window
            if errors:
                error_window = tk.Toplevel(self.master)
                error_window.title("Error Report")
                error_window.geometry("900x500")
                error_window.config(bg="#1A2B3C")

                error_label = tk.Label(error_window, text="Errors:", font=("SF Pro Display", 40), fg="white", bg="#1A2B3C")
                error_label.pack(pady=30)

                error_listbox = tk.Listbox(error_window, font=("SF Pro Display", 20), fg="white", bg="#1A2B3C")
                error_listbox.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

                for error in errors:
                    for key, value in error.items():
                        error_listbox.insert(tk.END, f"{key}: {value}")
            else:
                messagebox.showinfo("Success","Report Generated Successfully", icon="info")
        else:
            messagebox.showerror("Error","Cannot Generate The Report Since Data Required For The Report Generation Doesn't Exist", icon="warning")
    
    def open_report(self):
        # Load the JSON file
        with open('database_proxy.json', 'r') as f:
            data = json.load(f)
            filename = data.get("filename")
            # # Get the name of the PDF file
            # pdf_filename = data.get("output_pdf")[0]
            
        if filename:
            # Get the name of the PDF file
            pdf_filename = data.get("output_pdf")[0]
            if pdf_filename:
                # Play the output video using the default player on the system
                # os.startfile(output_video_path) #windows
                subprocess.run(['open', pdf_filename])
            else:
                messagebox.showerror("Error","Report not found", icon="warning")
        else:
            messagebox.showerror("Error","Cannot open Report since no pdf is generated yet or the file Doesn't Exist", icon="warning")
    
    def open_plot(self):
        # Load the JSON file
        with open('database_proxy.json', 'r') as f:
            data = json.load(f)
            filename = data.get("filename")
            # # Get the name of the PDF file
            # pdf_filename = data.get("output_pdf")[0]
            
        if filename:
            # Get the name of the PDF file
            graph = data.get("graph")
            if graph:
                # Play the output video using the default player on the system
                # os.startfile(output_video_path) #windows
                subprocess.run(['open', graph])
            else:
                messagebox.showerror("Error","Graph not found", icon="warning")
        else:
            messagebox.showerror("Error","Cannot open graph since no graph is generated yet or the file Doesn't Exist", icon="warning")
        


if __name__ == '__main__':
    # Clear the data in the file at the start of the program
    with open("database_proxy.json", "w") as f:
        json.dump({}, f)
    root = tk.Tk()
    ex = App(root)
    root.mainloop()


