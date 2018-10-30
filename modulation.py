import matplotlib.pyplot as plot
import numpy as np
import sys
from scipy import signal

# m = 0.2
# freq = 10
# freqs = 2
Fs = 150.0;  # sampling rate
Ts = 1.0/Fs; # sampling interval


""" for frequency spectrum """
def calc_fft(y):
	n = len(y) # length of the signal
	k = np.arange(n)
	T = n/Fs
	frq = k/T # two sides frequency range
	frq = frq[range(n//2)] # one side frequency range
	Y = np.fft.fft(y)/n # fft computing and normalization
	Y = Y[range(n//2)]
	return(Y, frq)


def get_y(arr, name, f):
	freq = int(f)
	bit_arr = np.array(arr)
	samples_per_bit = 2*Fs/bit_arr.size 
	dd = np.repeat(bit_arr, samples_per_bit)

	if name == "fsk":
		return np.sin(2 * np.pi * (freq + dd) * t)
	elif name == "psk":
		return np.sin(2 * np.pi * (freq) * t+(np.pi*dd/180))
	else:
		return dd*np.sin(2 * np.pi * freq * t)


t = np.arange(0,2,Ts)

###fsk = [5,5,-5,5,-5]
###psk = [180,180,0,180,0]
###ask = [1, 0, 1, 1, 0]

""" START OF GRAPH """
fig,myplot = plot.subplots(3, 1)

def get_input():
	frequency = input("Enter frequency: ")
	return frequency


def plot_():
	# binary = 11010
	f = get_input()
	fsk = [5,5,-5,5,-5]
	psk = [180,180,0,180,0]
	ask = [1, 1, 0, 1, 0]
	ys = []
	ys.append(get_y(fsk, "fsk", f))
	ys.append(get_y(psk, "psk", f))
	ys.append(get_y(ask, "ask", f))

	# Y, frq = calc_fft(y)
	for i in range(0, 3):
		if (i == 0):
			lbl = "  (FSK)"
		elif (i == 1):
			lbl = "  (PSK)"
		else:
			lbl = "  (ASK)"

		myplot[i].plot(t,ys[i])
		myplot[i].set_xlabel('Time')
		myplot[i].set_ylabel('Amplitude' + lbl)


if __name__ == "__main__":
	plot_()
	plot.show()
