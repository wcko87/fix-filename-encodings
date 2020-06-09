# Fixes oem-encoded file encodings (if extracted from zip) by changing them to shift-jis
import os, shutil
import tkinter as tk
import tkinter.scrolledtext

HELP_TEXT = "\n".join((
    "Please enter a path to a file or folder in the above field.",
    "",
    "This is a script to fix garbled encodings of FILE NAMES. It does not affect the contents of the files. This script is used when you have extracted a zip file in the wrong locale.",
    "",
    "[Display Fixes] will display the list of encoding fixes this program will make.",
    "",
    "[Fix Encodings] will carry out the actual encoding fixes. It will also display the encoding fixes made.",
))

def fix_encoding(root, s, log):
    try:
        return s.encode('oem').decode('shift_jis', errors='ignore')
    except Exception as e:
        log('Skipped: %s\n' % (s))  
    return s

def fix(root, f, log, apply_fix):
    fixed = fix_encoding(root, f, log)
    if fixed != f:
        original_file = r'%s\%s' % (root, f)
        new_file = r'%s\%s' % (root, fixed)
        log('%s -> %s\n' % (f, fixed))
        if apply_fix:
            shutil.move(original_file, new_file)

def command_button(controller, apply_fix):
    path_text = controller.path_entry_box.get()
    controller.text_clear()
    
    is_folder = os.path.isdir(path_text)
    is_file = os.path.isfile(path_text)
    
    if len(path_text) == 0:
        controller.text_print(HELP_TEXT)
        return
        
    controller.text_print("Path:\n%s\n=====\n" % path_text)
    
    if not is_folder and not is_file:
        controller.text_print('ERROR: Path is not a valid file or folder.\n\n')
        controller.text_print(HELP_TEXT)
        return
    
    if is_folder:
        walk = list(os.walk(path_text))
        walk.sort(key=lambda rdf : -rdf[0].count('\\'))

        for root, dirs, files in walk: # sorted in decreasing order of depth
            for f in files: fix(root, f, controller.text_print, apply_fix)
            for d in dirs: fix(root, d, controller.text_print, apply_fix)
    elif is_file:
        root, f = os.path.split(path_text)
        fix(root, f, controller.text_print, apply_fix)

class MainController(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Fix Folder Encodings")
        self.root.resizable(False, False)
        
        self.pframe = tk.Frame(self.root)
        self.pframe.grid(row=0, column=0)
        #self.pframe.grid_propagate(False)

        tk.Label(self.pframe, text="Enter folder/file path here",
            width=30, height=1).grid(row=1, columnspan=2)
        
        self.path_entry_box = tk.Entry(self.pframe, width=70)
        self.path_entry_box.grid(row=2, columnspan=2)
       
        tk.Label(self.pframe, text="Results",
            width=30, height=1).grid(row=3, columnspan=2)
        
        self.text_box = tk.scrolledtext.ScrolledText(self.pframe, width=60, height=20, state=tk.DISABLED)
        self.text_box.grid(row=4, columnspan=2)
        self.text_print(HELP_TEXT)
        
        
        tk.Button(self.pframe, text="Display Fixes", width=20, height=2, 
            command=lambda:command_button(self, False)).grid(row=0, column=0)
        tk.Button(self.pframe, text="Fix Encodings", width=20, height=2, 
            command=lambda:command_button(self, True)).grid(row=0, column=1)
            
        
    def text_print(self, text):
        self.text_box.configure(state=tk.NORMAL)
        self.text_box.insert(tk.END, text)
        self.text_box.configure(state=tk.DISABLED)
        
    def text_clear(self):
        self.text_box.configure(state=tk.NORMAL)
        self.text_box.delete(1.0, tk.END)
        self.text_box.configure(state=tk.DISABLED)
        
    def start(self):
        self.root.mainloop()
        
def main():
    main_controller = MainController()
    main_controller.start()
    
if __name__ == '__main__':
    main()
    
