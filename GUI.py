import tkinter as tk
from tkinter import filedialog

def select_file1():
    file_path1 = filedialog.askopenfilename()
    file1_entry.delete(0, tk.END)
    file1_entry.insert(0, file_path1)

def select_file2():
    file_path2 = filedialog.askopenfilename()
    file2_entry.delete(0, tk.END)
    file2_entry.insert(0, file_path2)

def merge_files():
    file_path1 = file1_entry.get()
    file_path2 = file2_entry.get()
    output_file = output_entry.get()

    with open(file_path1, 'rb') as f1, open(file_path2, 'rb') as f2, open(output_file, 'wb') as out:
        while True:
            chunk1 = f1.read(1024)
            chunk2 = f2.read(1024)
            if not chunk1:
                break
            out.write(chunk1)
            out.write(chunk2)

    result_label.config(text="文件合并成功！")

root = tk.Tk()
root.title("文件合并工具")

file1_label = tk.Label(root, text="文件1:")
file1_label.grid(row=0, column=0, padx=10, pady=10)

file1_entry = tk.Entry(root, width=50)
file1_entry.grid(row=0, column=1, padx=10, pady=10)

file1_button = tk.Button(root, text="选择文件", command=select_file1)
file1_button.grid(row=0, column=2, padx=10, pady=10)

file2_label = tk.Label(root, text="文件2:")
file2_label.grid(row=1, column=0, padx=10, pady=10)

file2_entry = tk.Entry(root, width=50)
file2_entry.grid(row=1, column=1, padx=10, pady=10)

file2_button = tk.Button(root, text="选择文件", command=select_file2)
file2_button.grid(row=1, column=2, padx=10, pady=10)

output_label = tk.Label(root, text="输出文件:")
output_label.grid(row=2, column=0, padx=10, pady=10)

output_entry = tk.Entry(root, width=50)
output_entry.grid(row=2, column=1, padx=10, pady=10)

# output_button = tk.Button(root, text="选择文件", command=select_output)
# output_button.grid(row=2, column=2, padx=10, pady=10)

result_label = tk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

merge_button = tk.Button(root, text="合并文件", command=merge_files)
merge_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
