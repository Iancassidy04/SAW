# Ian Cassidy
# IDT GUI
# 02/03/2025

from idtpy import designer, model, GdsAssistant
from tkinter import messagebox, font as tkFont
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
import time
import os

# Create main title
main = tk.Tk()
main.geometry("1000x800")  # Set window size
main.config(bg="#FFFFFF") # Background Color

font_1 = tkFont.Font(family='Helvetica', size=36) # Title Font
font_2 = tkFont.Font(family="Helvetica", size=10) # Text Font

label = tk.Label(main, text="IDT Autodesigner", font=(font_1), fg="#006747", bg="#FFFFFF") # Title
label.pack(pady=20)

bg_image = tk.PhotoImage(file=r"C:\Users\ianbc\Downloads\Saw Research\uvm_logo.png") # IMPORTANT: How do I get this onto others computers
bg_image_resized = bg_image.subsample(4, 4) # Resize logo
background_label = tk.Label(main, image=bg_image_resized, bg="#FFFFFF") # Background color and labeling
background_label.place(x=0, y=0) # Places logo in top left


def change_color():
    submit.config(bg='red')  # Change the color when clicked once
    main.after(150, reset_color)  # Reset after 1 second

def reset_color():
    submit.config(bg="SystemButtonFace")  # Reset button to default color


def get_input():
    freq = int(freq_ask.get()) # Frequency
    vsaw = int(vsaw_ask.get()) # SAW Velocity
    Np = int(Np_ask.get()) # Periods
    w = int(w_ask.get()) # Overlay Width
    l = int(l_ask.get()) # Length Overlay
    nehp = int(nehp_ask.get()) # Number of electrodes per half
    t = int(t_ask.get()) # Thickness Factor

    
    display_idt(freq, vsaw, Np, w, l, nehp, t) # Call display for preview with chosen variables
    export(freq, vsaw, Np, w, l, nehp, t) # Export IDT design to GDS

def display_idt(freq, vsaw, Np, w, l, nehp, t):
    reg = designer.Regular(
        freq=freq,  # resonant frequency
        vsaw=vsaw,  # SAW speed
        Np=Np,  # number of periods
        w=w,  # overlap width between opposite electrodes
        l=l,  # vertical length after the overlap
        Nehp=nehp,  # number of electrodes per half period. 1=single-finger, 2=double-finger
        tfact=t,  # thickness factor
    )

    fig, ax = plt.subplots(1) # Plot
    reg.show(ax, color='k')
    plt.xlabel('um') #IMPORTATN: Figure out what actual scale is
    plt.ylabel('um')
    plt.show()

def export(freq, vsaw, Np, w, l, nehp, t):
    idt = designer.Regular(freq=freq,vsaw=vsaw,Np=Np,w=w,l=l,Nehp=nehp,tfact=t)
    gds = GdsAssistant('library')
    top = gds.new_cell('top')
    top.add(gds.get_gds_polygons(idt,layer=0))
    gds.save('idt.gds')
    messagebox.showinfo("Current working directory:", os.getcwd())

freq_label = tk.Label(main, text="\nFrequency", font=(font_2), bg="#FFFFFF") # Label for frequency input,
freq_label.pack() 

freq_ask = tk.Entry(main) # Entry for frequency
freq_ask.pack()

vsaw_label = tk.Label(main, text="\nSAW Velocity", font=(font_2), bg="#FFFFFF") # Label for SAW velocity input
vsaw_label.pack()

vsaw_ask = tk.Entry(main) # Entry for SAW velocity
vsaw_ask.pack()

Np_label = tk.Label(main, text="\nNumber of Periods", font=(font_2), bg="#FFFFFF") # Label for periods input
Np_label.pack()

Np_ask = tk.Entry(main) # Entry for periods
Np_ask.pack()

w_label = tk.Label(main, text="\nOverlap Width", font=(font_2), bg="#FFFFFF") # Label for width input
w_label.pack()

w_ask = tk.Entry(main) # Entry for width
w_ask.pack()

l_label = tk.Label(main, text="\nVertical Length Overlap", font=(font_2), bg="#FFFFFF") # Label for length input
l_label.pack()

l_ask = tk.Entry(main) # Entry for length
l_ask.pack()

nehp_label = tk.Label(main, text="\nNumber of electrodes per half period", font=(font_2), bg="#FFFFFF") # Label for finger number input
nehp_label.pack()

nehp_ask = tk.Entry(main) # Entry for number of fingers in a period
nehp_ask.pack()

t_label = tk.Label(main, text="\nThickness Factor", font=(font_2), bg="#FFFFFF") # Label for thickness input
t_label.pack()

t_ask = tk.Entry(main) # Entry for thickness
t_ask.pack()

submit= tk.Button(main, text="Show Preview and Download GDS", font=(font_2), bg="#FFFFFF", command=lambda: [get_input(), change_color()])
submit.pack()


main.mainloop() # Run application