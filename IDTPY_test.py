# Ian Cassidy
# SAW Research
# IDT 01
# 01/26/2025

'''All code in IDT 01 is sampled from Junliang Wang at https://github.com/Junliang-Wang/idtpy?tab=readme-ov-file'''

from idtpy import designer, model
import matplotlib.pyplot as plt
from idtpy import GdsAssistant
import numpy as np


idt = designer.Regular(freq=2.77,vsaw=2.77,Np=40,w=30,l=50,Nehp=2,tfact=[0.8,0.64,20])
gds = GdsAssistant('library')
top = gds.new_cell('top')
top.add(gds.get_gds_polygons(idt,layer=0))
gds.save('idt.gds')

'''IDT Electrode Design'''
reg = designer.Regular(
    freq=1, # resonant frequency
    vsaw=1, # SAW speed
    Np=10, # number of periods
    w=30, # overlap width between opposite electrodes
    l=20, # vertical length after the overlap
    Nehp=1, # number of electrodes per half period. 1=single-finger, 2=double-finger...
    tfact=1, # thickness factor
)

fig, ax = plt.subplots(1)
reg.show(ax, color='k')
plt.xlabel('um')
plt.ylabel('um')
plt.show()


'''Model of Frequency Response'''
freq = np.arange(1, 6, 0.001)

idt = model.ExpChirp(fmin=2,fmax=5,T=40,phi0=0,t0=0)
f_res = idt.freq_response(freq, apodized=False, db=True, shp=1).real

plt.plot(freq, f_res, 'k')
plt.xlabel('w')
plt.ylabel('Amplitude')
plt.show()

'''Predict the SAW shape with an input voltage'''
dt = 0.001
input_signal = model.ExpChirp(fmin=2,fmax=5,T=40)
ideal_wf = idt.apply_waveform(input_signal, dt)

time = np.arange(0, 80, dt)
t_res = ideal_wf.time_response(time).real

plt.plot(time, t_res, 'k')
plt.xlabel('Time(ns)')
plt.ylabel('Amplitude')
plt.show()
