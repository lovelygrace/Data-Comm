import re
import numpy as np
import matplotlib.pyplot as plt
import sys
import math
from tabulate import tabulate
from scipy import signal

def get_bin_input():
	valid = False
	user_input = ""
	while not valid:
		user_input = input("Input valid binary value: ")
		valid = re.match("^[0-1]*$", user_input)
	return user_input


""" ----------  LAB 2 RZ, NRZL, NRZI ---------------- """

def to_rz_nrzl(binary):
	rz, nrzl = [], []
	prev1, prev2 = 0, 0
	for bit in binary:
		if bit == "1":
			rz.append(int(5))
			nrzl.append(int(5))
			prev1, prev2 = 5, 5
		else:
			rz.append(int(bit))
			nrzl.append(int(-5))
			prev1, prev2 = 0, -5
	# for last dot in the plot
	rz.append(prev1)
	nrzl.append(prev2)
	return rz, nrzl

def to_nrzi(binary):
	nrzi_format = []
	prev = 0
	for bit in binary:
		if len(nrzi_format)==0:
			if(int(bit)==1):
				nrzi_format.append(5)
				prev = 5
			else:
				nrzi_format.append(-5)
				prev = -5
		else:
			if (bit=="1" and prev==5):
				nrzi_format.append(-5)
				prev=-5
			elif (bit=="1" and prev==-5):
				nrzi_format.append(5)
				prev=5
			else:
				nrzi_format.append(prev)
	# for last dot in the plot
	nrzi_format.append(prev)
	return nrzi_format


def encoding_plot(rz_format, nrzl_format, nrzi_format, user_input):
	plt.figure("Binary input = " + user_input)
	lbl, color, data = "", "", []
	for i in range(1, 4):
		if (i == 1): 
			lbl = "RZ Graph"
			color = "blue"
			data = rz_format
		elif (i == 2):
			lbl = "NRZ-L Graph"
			color = "green"
			data = nrzl_format
		else:
			lbl = "NRZ-I Graph"
			color = "red"
			data = nrzi_format
		pos = str(22) + str(i)
		plt.subplot(int(pos))
		plt.plot(data, color=color, drawstyle='steps-post')
		plt.grid(True)
		plt.ylabel("Amplitude")
		plt.xlabel("Time")
		plt.title(lbl)
		plt.yticks(np.arange(min(data), max(data)+1, 5.0))
	plt.show()


def encoding_main(user_input):
    rz_format, nrzl_format = to_rz_nrzl(user_input)
    nrzi_format = to_nrzi(user_input)
    print("You input " + user_input)
    print("rz_format = ")
    print(rz_format)
    print("nrzl_format ")
    print( nrzl_format)
    print("nrzi_format ")
    print(nrzi_format)
    encoding_plot(rz_format, nrzl_format, nrzi_format, user_input)


""" ----------  LAB 4 FSK, PSK, ASK ---------------- """

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

""" START OF GRAPH """

def get_frequency_input():
	frequency = input("Enter frequency: ")
	return frequency

def to_fsk_psk(binary):
    fsk, psk = [], []
    for bit in binary:
        if bit == "1":
            fsk.append(int(5))
            psk.append(int(180))
        else:
            fsk.append(int(-5))
            psk.append(int(bit))
    return fsk, psk


def modulation_plot(binary):
	# binary = 11010
    fig,myplot = plt.subplots(3, 1)
    f = get_frequency_input()
    fsk, psk, ask = [], [], []
    fsk, psk = to_fsk_psk(binary)
    ask = [int(x) for x in list(binary)]
    print(fsk)
    print(psk)
    print(ask)
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
    plt.show()

def modulation_main(user_input):
    modulation_plot(user_input)



""" ----------  LAB 5 HAMMING CODE ---------------- """


""" To install tabulate, run: pip install tabulate  """

""" HAMMING CODE """

def get_bits(pt, data):
    comb = []
    h2 = ["PARITY BIT", "POS", "BITS", "VALUE"]
    d2 = []
    for i in range(0, len(pt)):
        a = []
        b = []
        ctr = 0
        s = 0
        for j in range(pt[i] - 1, len(data)):
            if (ctr != pt[i]) and (s == 0):
                a.append(data[j])
                b.append(j + 1)
                ctr = ctr + 1
            else:
                ctr = 0
                
            if (ctr == 0):
                s = s + 1
            
            if (s == pt[i]):
                s = 0
        comb.append(a)
        bit = 0 if (sum(a) % 2 == 0) else 1
        l = str(b[1:]).strip('[]')
        l2 = str(a[1:]).strip('[]')
        dd = ['r' + str(pt[i]), l, l2, bit]
        d2.append(dd)
    print(tabulate(d2, headers=h2))
    return comb


def psOfTwo(r):
    return list(map(lambda x: 2 ** x, range(r)))
    

def unfilled(r, bitstr, ps):
    h3 = list(range(1, len(bitstr) + r + 1))
    d3 = []
    bitstr = bitstr[::-1]
    arr = [c for c in bitstr]
    for i in range(0, r):
        index = ps[i]
        arr.insert(index - 1, 'r' + str(index))
    d3.append(arr)
    return h3, d3


def fill(r, bitstr, powers_two):
    bitstr = bitstr[::-1]
    arr = list(bitstr)
    arr = [int(c) for c in arr]
    for i in range(0, r):
        index = powers_two[i]
        arr.insert(index - 1, 0)

    c = get_bits(powers_two, arr)
    for i in range(0, len(powers_two)):
        bit = 0 if (sum(c[i]) % 2 == 0) else 1
        arr[powers_two[i] - 1] = bit
    return arr 


def redundancy(bitstr):
    m = len(bitstr)
    r = 1
    while (True):
        left = math.pow(2, r)
        right = m + r + 1

        if (left >= right):
            return r
        else:
            r = r + 1


def binToDec(binary):
    decimal, i, n = 0, 0, 0
    while (binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1
    return decimal


def hamming_main(user_input):
    h1 = ["DATA", "LENGTH", "REDUNDANCY", "PARITY BITS POS"]
    bitstr = user_input
    r = redundancy(bitstr)
    ps = psOfTwo(r)
    sp = str(ps).strip('[]')
    d1 = [[bitstr, len(bitstr), r, sp]]

    """ display data details """
    print("\n\n")
    print(tabulate(d1, headers=h1))
    print("\n")

    """ end """


    """ display unfilled data """

    h3, d3 = unfilled(r, bitstr, ps)
    print(tabulate(d3, headers=h3))
    print("\n")

    """ end """

    filled = fill(r, bitstr, ps)



    """ display filled data """
    print("\n\n\t\t\tDATA TO SEND\n")
    print(tabulate([filled], headers=h3))
    print("\n")

    """ end """


    index = input("Enter flipped bit position: ")
    index = int(index)
    filled[index - 1] = 0 if (filled[index - 1] == 1) else 1
    
    
    """ display corrupted data """

    print("\n\n\t\t\tCORRUPTED DATA\n")
    print(tabulate([filled], headers=h3))
    print("\n")

    """ end """


    c = get_bits(psOfTwo(r), filled)
    res = []
    for ar in c[::-1]:
        bit = 0 if (sum(ar) % 2 == 0) else 1
        res.append(str(bit))


    locs = "".join(res)
    loc = int(locs)
    locd = binToDec(loc)
    print("\n\nPOSITION OF CORRUPTED BIT IN BINARY: " + locs + "  =  " + str(locd))
    print("\n\n\t\t\tCORRECTED DATA\n")
    filled[locd - 1] = 0 if (filled[locd - 1] == 1) else 1
    print(tabulate([filled], headers=h3))



""" -------  COMPILATION ---------- """

if __name__ == "__main__":
    print("\n\n\t\t\tCOMPILATION OF CSMSC 137 LABO EXERCISES\n")
    user_input = get_bin_input()
    print("\n\n\t\t\tLAB 2 - RZ, NRZ-L, NRZ-I ENCODING\n")
    encoding_main(user_input)
    print("\n\n\t\t\tLAB 4 - FSK, PSK, ASK MODULATION\n")
    modulation_main(user_input)
    print("\n\n\t\t\tLAB 5 - HAMMING CODE FOR ERROR CORRECTION\n")
    hamming_main(user_input)
    print("\n\n\t\t\tend.\n")
