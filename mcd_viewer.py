import shutil
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import subprocess
import os

import sys
import os
import subprocess
from pathlib import Path

def get_tool_path(tool_name):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath('.'))
    # First try current directory
    tool_path = os.path.join(base_path, tool_name)
    if os.path.exists(tool_path):
        return tool_path
    # Fall back to mymcplusplus directory
    return os.path.join(base_path, 'mymcplusplus', tool_name)

# Get path to mymcplusplus.exe
mymcplusplus = get_tool_path('mymcplusplus.exe')



class MCDViewer:
    
    def __init__(self, root):
        self.root = root
        self.root.title("PSXMemCard MCD Viewer")
        self.root.geometry("800x600")
        
        # Configure grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # File selection frame
        self.file_frame = tk.Frame(self.root, padx=10, pady=10)
        self.file_frame.grid(row=0, column=0, sticky="ew")
        
        self.file_label = tk.Label(self.file_frame, text="MCD File:")
        self.file_label.grid(row=0, column=0, sticky="w")
        
        self.file_entry = tk.Entry(self.file_frame, width=60)
        self.file_entry.grid(row=0, column=1, sticky="ew", padx=5)
        
        self.browse_btn = tk.Button(self.file_frame, text="Browse...", command=self.browse_file)
        self.browse_btn.grid(row=0, column=2, padx=5)
        
        # Configure file frame columns
        self.file_frame.grid_columnconfigure(1, weight=1)
        
        # Treeview frame
        self.tree_frame = tk.Frame(self.root, padx=10, pady=10)
        self.tree_frame.grid(row=1, column=0, sticky="nsew")
        
        # Configure treeview style
        self.style = ttk.Style()
        self.style.configure("Treeview", 
                            font=("Consolas", 10),
                            rowheight=25,
                            indent=40,
                            padding=(10, 5),
                            selectbackground="#0078d7",
                            borderwidth=1,
                            relief="solid")
        self.style.configure("Treeview.Item",
                            padding=(0, 0, 0, 0))
        self.style.layout("Treeview.Item", 
                         [('Treeitem.padding', 
                           {'sticky': 'nswe', 
                            'children': [
                                ('Treeitem.indicator', {'side': 'left', 'sticky': ''}),
                                ('Treeitem.text', {'side': 'left', 'sticky': 'we'})]})])
        self.style.configure("Treeview.Heading", 
                            font=("Consolas", 10, "bold"))
        
        # Create treeview with custom tags
        self.tree = ttk.Treeview(self.tree_frame, 
                                columns=("Name", "Size", "Date", "Protection"), 
                                show="headings",
                                style="Treeview",
                                height=20)
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Add scrollbars
        yscroll = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        yscroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=yscroll.set)
        
        xscroll = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        xscroll.grid(row=1, column=0, sticky="ew")
        self.tree.configure(xscrollcommand=xscroll.set)
        
        # Configure tree frame grid
        self.tree_frame.grid_columnconfigure(0, weight=1)
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree.heading("Name", text="Name")
        self.tree.heading("Size", text="Size")
        self.tree.heading("Date", text="Date") 
        self.tree.heading("Protection", text="Protection")
        
        # Configure tags for folder and file colors and icons
        self.tree.tag_configure("folder", 
                              foreground="blue", 
                              font=("Consolas", 10, "bold"),
                              image="folder_icon")
        self.tree.tag_configure("file", 
                              foreground="black",
                              image="file_icon")
        
        # Load icons from resources.py
        from mymcplusplus.gui import resources
        self.folder_icon = tk.PhotoImage(data=resources.resources["open.png"])
        self.file_icon = tk.PhotoImage(data=resources.resources["icon.png"])
        
        # Bind treeview events
        self.tree.bind("<<TreeviewOpen>>", self.on_tree_open)
        self.tree.bind("<<TreeviewClose>>", self.on_tree_close)
        

        
        # Right click menu
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="Add File", command=lambda: self.add_file(None))
        self.menu.add_command(label="Delete File", command=lambda: self.delete_file(None))
        self.menu.add_command(label="Extract File", command=lambda: self.extract_file(None))
        self.menu.add_command(label="Add New Folder", command=lambda: self.add_folder(None))
        self.menu.add_command(label="Delete Folder", command=lambda: self.delete_folder(None))
        
        # Configure menu style
        self.menu.configure(
            activebackground="#4a4a4a",  # Dark gray background on hover
            activeforeground="white"
        )
        
        # Bind right click event
        self.tree.bind("<Button-3>", self.show_menu)
        
        #Bind left click event
        self.tree.bind("<Button-1>", self.unselect_all)
    
    def unselect_all(self, event):
        """Unselect all items when clicking on empty space in treeview.
        
        Args:
            event: The mouse click event containing coordinates
        """
        item = self.tree.identify_row(event.y)
        if not item:  # Clicked on empty space
            for selected_item in self.tree.selection():
                self.tree.selection_remove(selected_item)
            self.tree.focus_set()
        
    def add_folder(self, selected_item=None):
        """Add folder to selected folder or file's parent folder"""
        selected = selected_item or self.tree.selection()
        
     
            
        # Get folder name from user input
        folder_name = simpledialog.askstring("New Folder", "Enter folder name:")
        if not folder_name:
            return
        # print(f"add file command is: {os.path.join(target_path, folder_name)}") 
        # Create folder in MCD
        try:
            # Create new folder
            result = subprocess.run(
                [mymcplusplus, self.file_entry.get(), "mkdir", folder_name],
                check=True
            )
            print(f"add file command is: {result}") 
          
            
            messagebox.showinfo("Success", "Folder added successfully")
            self.load_mcd(self.file_entry.get())
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to add folder:\n{e.stderr}")
        
    def delete_folder(self, selected_item=None):
        """Delete folder and all its contents"""
        selected = selected_item or self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a folder")
            return
            
        # Get selected item values
        values = self.tree.item(selected, "values")
        if not values or len(values[3]) < 6 or values[3][5] != 'd':
            messagebox.showwarning("Invalid Selection", "Please select a folder")
            return
            
        # Get full path of selected folder
        folder_path = self.get_full_path(selected)
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Delete folder {folder_path} ?"):
            return
            
        try:
            result = subprocess.run(
                [mymcplusplus, self.file_entry.get(), "remove", folder_path],
                check=True
            )
            messagebox.showinfo("Success", "Folder deleted successfully")
            self.load_mcd(self.file_entry.get())
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to delete folder:\n{e.stderr}, Please ensure that there are no files in the folder. Please delete the files first.")
        
    def show_menu(self, event):
        """Show right click menu"""
        item = self.tree.identify_row(event.y)
        print(f"show menu is: {item}")
        if item:
            self.tree.selection_set(item)
            # Check if selected item is a folder or file
            values = self.tree.item(item, "values")
            if not values or len(values[3]) < 6:
                messagebox.showwarning("Invalid Selection", "Invalid item type")
                return
             # If item is a file, get its parent folder
            if values[3][5] == 'd':
                self.menu.entryconfig("Extract File", 
                command=lambda: self.extract_file(item),state = "disable")
                self.menu.entryconfig("Delete Folder", 
                    command=lambda: self.delete_folder(None), state = "active")
            else:
                self.menu.entryconfig("Delete Folder", 
                    command=lambda: self.delete_folder(None), state = "disable")
                self.menu.entryconfig("Extract File", 
                command=lambda: self.extract_file(item), state = "active")
            # Update menu commands with selected item
            self.menu.entryconfig("Add File", 
                command=lambda: self.add_file(item), state = "active")
            self.menu.entryconfig("Delete File", 
                command=lambda: self.delete_file(item), state = "active")
            self.menu.entryconfig("Extract File", 
                command=lambda: self.extract_file(item), state = "active")
            self.menu.entryconfig("Add New Folder", 
                command=lambda: self.add_folder(None),state = "disable")
            
        else:
            # If clicking on empty space, select root directory
                # Update menu commands with root directory
                
                self.menu.entryconfig("Add File", 
                    command=lambda: self.add_file(None), state = "active")
                self.menu.entryconfig("Delete File", 
                    command=lambda: self.delete_file(None), state = "disable")
                self.menu.entryconfig("Extract File", 
                    command=lambda: self.extract_file(None), state = "disable")
                self.menu.entryconfig("Add New Folder", 
                    command=lambda: self.add_folder(None), state = "active")
                self.menu.entryconfig("Delete Folder", 
                    command=lambda: self.delete_folder(None),state = "disable")
        
        self.menu.post(event.x_root, event.y_root)
            
    def add_file(self, selected_item=None):
        """Add file to selected folder or file's parent folder"""
        selected = selected_item or self.tree.selection()
        if selected_item == None:
          # Select file to add
            file_path = filedialog.askopenfilename()
            if not file_path:
                return
                
            try:
                result = subprocess.run(
                    [mymcplusplus, self.file_entry.get(), "add",  file_path],
                    check=True
                )
                print(f"add file command is: {result}") 
                messagebox.showinfo("Success", "File added successfully")
                self.load_mcd(self.file_entry.get())
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to add file:\n{e.stderr}")
        else:    
            # Get selected item path
            item_path = self.get_full_path(selected)
            
            # Check if selected item is a folder or file
            values = self.tree.item(selected, "values")
            if not values or len(values[3]) < 6:
                messagebox.showwarning("Invalid Selection", "Invalid item type")
                return
                
            # If item is a file, get its parent folder
            if values[3][5] != 'd':
                item_path = os.path.dirname(item_path)
            print(f"full path: {item_path}")    
            # Select file to add
            file_path = filedialog.askopenfilename()
            if not file_path:
                return
                
            try:
                result = subprocess.run(
                    [mymcplusplus, self.file_entry.get(), "add", "-d", item_path, file_path],
                    check=True
                )
                print(f"add file command is: {result}") 
                messagebox.showinfo("Success", "File added successfully")
                self.load_mcd(self.file_entry.get())
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to add file:\n{e.stderr}")
            
    def delete_file(self, selected_item=None):
        """Delete selected file/folder"""
        selected = selected_item or self.tree.selection()
        if not selected:
            # If no selection, use root directory
            root_items = self.tree.get_children()
            if root_items:
                selected = root_items[0]
            else:
                messagebox.showwarning("No Selection", "Please select an item")
                return
            
        # Get selected item values
        values = self.tree.item(selected, "values")
        if not values or len(values[3]) < 6:
            messagebox.showwarning("Invalid Selection", "Invalid item type")
            return
             
        # Get full path of selected item
        item_path = self.get_full_path(selected)
        
        print(f"delete file path:{item_path}") 
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Delete {item_path}?"):
            return
            
        try:
            # Check if item is a directory
            if values[3][5] == 'd':
                # Delete directory with -d flag
                result = subprocess.run(
                    [mymcplusplus, self.file_entry.get(), "remove", "-d", item_path],
                    check=True
                )
                print(f"add file command is: {result}") 
            else:
                # Delete single file
                result = subprocess.run(
                    [mymcplusplus, self.file_entry.get(), "remove", item_path],
                    check=True
                )
                print(f"add file command is: {result}") 
            messagebox.showinfo("Success", "Item deleted successfully")
            self.load_mcd(self.file_entry.get())
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to delete item:\n{e.stderr}")
            
    def extract_file(self, selected_item=None):
        """Extract selected file"""
        selected = selected_item or self.tree.selection()
        if not selected:  
            messagebox.showwarning("No Selection", "Please select a file")
            return
            
        # Check if selected item is a file
        values = self.tree.item(selected, "values")
        if values and len(values[3]) >= 6 and values[3][5] == 'd':
            messagebox.showwarning("Invalid Selection", "Please select a file")
            return
        # Get full path of selected file
        file_path = self.get_full_path(selected)
        print(f"mcd file_path is: {os.getcwd()}")
        # Get export path using just the filename portion
        directory = filedialog.askdirectory(title="请选择一个目录")
        try:
            # Export file while preserving original filename
            # export_path = os.path.join(folder, os.path.basename(file_path))
            
            
             # Use absolute paths and avoid shell=True
            args = [mymcplusplus, "-i", os.path.abspath(self.file_entry.get()), "extract", file_path, file_path]
            
            result = subprocess.run(
                args,
                shell=False,
                capture_output=False,
                text=True,
                check=True
            )
            file_path = Path(file_path);

 
            source_file = os.path.abspath(os.path.join(os.getcwd(),file_path.name)) 
            print(f"source file path is: {source_file}")
            print(f"target directory path is: {directory}")
            # 执行剪切操作
            try:
                shutil.move(source_file, directory)
                messagebox.showinfo("Success", "File extracted successfully")
            except FileNotFoundError:
                print("source file not found")
            except PermissionError:
                print("permission denied")
            except Exception as e:
                messagebox.showinfo("An error occurred:", str(e))
          
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to extract file:\n{e.stderr}")
            
    def get_full_path(self, item):
        """Get full path of tree item"""
        path_parts = []
        current = item
        while current:
            # Remove + or - prefix from folder names
            name = self.tree.item(current, "values")[0]
            name = name.strip()
            if name.startswith('+ ') or name.startswith('- '):
                name = name[2:]
            path_parts.insert(0, name)
            current = self.tree.parent(current)
        return "/".join(path_parts)
        
    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("MCD files", "*.mcd")])
        if file_path:
            if not os.path.exists(file_path):
                messagebox.showerror("Error", f"File not found: {file_path}")
                return
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, os.path.abspath(file_path))
            self.load_mcd(os.path.abspath(file_path))
            
    def load_mcd(self, file_path, parent=""):
        # Clear existing items if top level
        if not parent:
            for item in self.tree.get_children():
                self.tree.delete(item)
                
        # Run mymcplusplus command
        try:
            # Use absolute paths and avoid shell=True
            args = [mymcplusplus, "-i", os.path.abspath(file_path), "ls"]
            if parent:
                args.append(f"{parent}/")
                
            result = subprocess.run(
                args,
                shell=False,
                capture_output=True,
                text=True,
                check=True
            )
            self.parse_output(result.stdout, parent)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to read MCD file:\n{e.stderr}")
            
    def parse_output(self, output, parent=""):
        for line in output.splitlines():
            if not line.strip() or "KB Free" in line:
                continue
                
            # Split line into fixed-width columns
            # Format: permissions size date time name
            protection = line[0:15].strip()
            size = line[16:23].strip()
            date = line[24:31].strip()
            time = line[32:42].strip()
            name = line[43:].strip()
            
            # Combine date and time
            file_time = f"{date} {time}"
            
            # Skip . and .. directories
            if name in (".", ".."):
                continue
                
            # Add item with appropriate tag based on type
            if len(protection) >= 6 and protection[5] == 'd':
                # Add folder with + indicator
                item_id = self.tree.insert(parent, tk.END, 
                                        values=(f"+ {name}", size, file_time, protection),
                                        tags=("folder",))
                # Add loading placeholder
                self.tree.insert(item_id, tk.END, 
                                values=("Loading...", "", "", ""),
                                tags=("file",))
            else:
                # Add file with indentation and dot prefix
                if parent == "": 
                    indent = ""
                else:
                    indent = "   " * (len(self.tree.parent(parent)) + 1)
                item_id = self.tree.insert(parent, tk.END, 
                                        values=(f"{indent}- {name}", size, file_time, protection),
                                        tags=("file",))
                
    def on_tree_open(self, event):
        item = self.tree.focus()
        if not item:
            return
            
        values = self.tree.item(item, "values")
        if values and len(values[3]) >= 6 and values[3][5] == 'd':
            # Remove loading placeholder
            for child in self.tree.get_children(item):
                self.tree.delete(child)
            
            # Get folder name and update indicator to -
            folder_name = values[0][2:]  # Remove + prefix
            self.tree.item(item, values=(f"- {folder_name}", *values[1:]))
            
            # Verify folder path exists
            try:
                args = [
                    mymcplusplus,
                    "-i",
                    os.path.abspath(self.file_entry.get()),
                    "ls",
                    folder_name
                ]
                print(f"Executing command: {args}")
                result = subprocess.run(
                    args,
                    shell=False,
                    check=True,
                    capture_output=True,
                    text=True
                )
                self.parse_output(result.stdout, item)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to read folder:\n{e.stderr}")
                # Collapse the folder if error occurs
                self.tree.item(item, open=False)
                
    def on_tree_close(self, event):
        """Handle tree item collapse"""
        item = self.tree.focus()
        if item:
            # Collapse all children
            for child in self.tree.get_children(item):
                self.tree.delete(child)
            # Add loading placeholder if it's a directory
            values = self.tree.item(item, "values")
            if values and len(values[3]) >= 6 and values[3][5] == 'd':
                # Update indicator to + when closing
                folder_name = values[0][2:]  # Remove - prefix
                self.tree.item(item, values=(f"+ {folder_name}", *values[1:]))
                self.tree.insert(item, tk.END, values=("Loading...", "", "", ""))
            
    def export_files(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select files to export")
            return
            
        folder = filedialog.askdirectory()
        if not folder:
            return
            
        file_path = self.file_entry.get()
        for item in selected:
            # Get full path of the selected item
            path_parts = []
            current = item
            while current:
                path_parts.insert(0, self.tree.item(current, "values")[0])
                current = self.tree.parent(current)
                
            full_path = "/".join(path_parts)
            export_path = os.path.join(folder, os.path.basename(full_path))
            
            try:
                subprocess.run(
                    [mymcplusplus, file_path, "export", full_path, export_path],
                    check=True
                )

            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to read folder:\n{e.stderr}")
                # Collapse the folder if error occurs
                self.tree.item(item, open=False)
                
if __name__ == "__main__":
    root = tk.Tk()
    app = MCDViewer(root)
    root.mainloop()
