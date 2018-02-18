# Sniph trial

import sys, random

def findOccurences(S, c):
    return [i for i, letter in enumerate(S) if letter == c]
    
if len(sys.argv) == 1:
    print "Welcome to Sniph V 1.0.3:\n"
    
    inp = raw_input("Input # of dimensions, N, for cypher (empty for default): ")
    if len(inp) == 0:
        N = 4
    else:
        N = int(inp)
        
    if N < 4:
        N = 4
        
    dim = raw_input("Enter dimensions for cypher table, in range 3-9, in form # rows x #cols : ")
    # Parse input
    R = int(dim[0])
    if R == 1:
        c = dim[1]
        if c == '0':
            R = 10
    if R < 3:
        R = 3
    elif R > 9:
        R = 9
    
    C = 0
    c = dim[len(dim)-2:]
    if c[0] == '1':
        if c[1] == '0':
            C = 10
    else:
        C = int(c[1])
        if C < 3:
            C = 3
        elif C > 9:
            C = 9
            
    # print R
    # print C
    # print N
    
    size = R * C # table size (constant decided by dimensions)
    
    char_set = "ABCDEFGHIJKLMNOPQRSTUVWXYZ.,?!:;\'\"/\\|<>+-=(){}[]`~@#$%^&*1234567890 \n"
    # repeat char set to fill (R*C)^2 spaces
    # i.e 3x3 = 9 tables slots with 9 tables holding characters in last level
    # = 9^2 = 81 characters
    while len(char_set) < pow(size, 2):
        char_set += char_set
    char_set = char_set[0:pow(size,2)]
    
    word = raw_input("Enter word to be encrypted: ")
    
    encoding = ""
    path_full = ""
    OTP = []
    outs = []
    key = 0
    shift = 0
    for i in range(0, len(word)):
        shift = 0 # comment out for continuous shifting
        pad = ""
        for j in range(0, N-2):
            pos = char_set.index(word[key % len(word)]) % size 
            # character's position in set 
            # mod by table size for wrapping
            
            # Get coord
            cx = pos / C + 1
            cy = pos % C + 1
            
            pad += (str(cx) + str(cy))
            shift += (cx - cy)
            key += 1
        OTP.append(pad)
        path_full += pad
        
        shifted_set = ""
        if shift == 0:
            shifted_set = char_set
        else:
            shifted_set = char_set[shift:] + char_set[0:shift]
            
        # print char_set
        # print shift
        # print shifted_set
        
        index = findOccurences(shifted_set, word[i])
        # choose random from index
        rand_loc = random.randint(0, sys.maxint) % len(index)
        rand_choice = index[rand_loc]
        
        d2 = rand_choice / size
        s = str(d2/C + 1) + str(d2%C + 1)
        
        dN = rand_choice % size
        s += str(dN/C + 1) + str(dN%C + 1)
        encoding += s
        path_full += s
        outs.append(s)
    
    print "Unaltered:"
    print path_full
    path_final = ""
    for i in range(len(path_full)):
        x = int(path_full[i])
        z = x
        r = random.randint(0, sys.maxint)
        w = 1
        t = x
        
        if i%2 == 0: # row
            t += R
            while t < 10:
                w += 1
                t += R
            if x == R:
                x = 0
                w += 1
            x += (r % w) * R
            
        else: # column
            t += C
            while t < 10:
                w += 1
                t += C
            if x == C:
                x = 0
                w += 1
            x += (r % w) * C
            
        path_final += str(x)
        
        
    
    print OTP
    print outs
    print encoding
    
    print "Full Cypher:"
    cOTP = []
    c_outs = []
    c_enc = ""
    for i in range(len(word)):
        cOTP.append(path_final[2*i*N : 2*i*N + 2*(N-2)])
        c_outs.append(path_final[2*i*N + 2*(N-2) : 2*i*N + 2*N])
        c_enc += c_outs[i]
        
    print path_final
    print cOTP
    print c_outs
    print c_enc
    
else:
    if "-h" in sys.argv:
        print "help"
        
