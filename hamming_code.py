import math
from tabulate import tabulate


""" To install tabulate, run: 
    
    pip install tabulate
"""

""" HAMMING CODE """

def get_input():
    bitstr = input("Enter bit string: ")
    return bitstr


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


def main():
    h1 = ["DATA", "LENGTH", "REDUNDANCY", "PARITY BITS POS"]
    bitstr = get_input()
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



if __name__ == "__main__":
    main()
    print("\n\n\t\t\tend.\n")
