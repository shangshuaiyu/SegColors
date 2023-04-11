import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from collections import Counter
import pandas as pd

def read_color_data():
    df = pd.read_csv('colors.csv')
    color_dict = {}
    for index, row in df.iterrows():
        color_dict[row['HEX']] = row['Name']
    return color_dict

def analyze_image(image_file, color_dict):
    image = Image.open(image_file)
    pixels = list(image.getdata())
    counter = Counter(pixels)

    result = []
    for color, count in counter.items():
        hex_color = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
        if hex_color.upper() in color_dict:
            result.append((hex_color, f"{hex_color} ({color_dict[hex_color.upper()]}) 出现了 {count} 次"))
    return result

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if file_path:
        image = Image.open(file_path)
        image.thumbnail((400, 400))
        photo = ImageTk.PhotoImage(image)
        label_image.config(image=photo)
        label_image.image = photo

        color_data = read_color_data()
        results = analyze_image(file_path, color_data)
        text_colors.delete('1.0', tk.END)
        for item in results:
            hex_color, text = item
            text_colors.insert(tk.END, "■", hex_color)
            text_colors.insert(tk.END, text + '\n')
            text_colors.tag_configure(hex_color, foreground=hex_color)

app = tk.Tk()
app.title("SegColors by QQ448287820")

# Create a top menu bar
menu_bar = tk.Menu(app)
app.config(menu=menu_bar)

# Add a "File" menu item
file_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add the "Open Image" option to the "File" menu item
file_menu.add_command(label="Open Image", command=open_file)

frame_left = tk.Frame(app)
frame_left.pack(side=tk.LEFT, padx=10, pady=10)

label_image = tk.Label(frame_left)
label_image.pack()

frame_right = tk.Frame(app)
frame_right.pack(side=tk.RIGHT, padx=10, pady=10)

text_colors = tk.Text(frame_right, width=50, height=20, wrap=tk.NONE)
text_colors.pack()

app.mainloop()
