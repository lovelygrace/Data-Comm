import re
import numpy as np
import matplotlib.pyplot as plt

def get_bin_input():
	valid = False
	user_input = ""
	while not valid:
		user_input = input("Input valid binary value: ")
		valid = re.match("^[0-1]*$", user_input)
	return user_input


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

def plot(rz_format, nrzl_format, nrzi_format, user_input):
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


def main():
	user_input = get_bin_input()
	rz_format, nrzl_format = to_rz_nrzl(user_input)
	nrzi_format = to_nrzi(user_input)

	print("You input " + user_input)
	print("rz_format = ")
	print(rz_format)
	print("nrzl_format ")
	print( nrzl_format)
	print("nrzi_format ")
	print(nrzi_format)

	plot(rz_format, nrzl_format, nrzi_format, user_input)


if __name__ == "__main__":
    main()
