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
        
    R = C = 0
    dim = raw_input("Enter dimensions for cypher table, in range 3-10, in form # rows x #cols (empty for default): ")
    if len(dim) == 0:
        # default
        R = C = 3
    else:    
    # Parse input
        p1 = p2 = 0
        if ' ' in dim: p1 = dim.index(' ')
        else: p1 = len(dim)
        if 'x' in dim: p2 = dim.index('x')
        else:
            print("Invalid input format")
            quit()
        
        if p2 < p1: p1 = p2
        R = dim[0:p1]
        if len(R) == 0: R = 3
        else: R = int(R)
        if R < 3: 
            print("Value must be greater than or equal to 3. Defaulting to 3")
            R = 3
        elif R > 10: 
            print("Value must be less than or equal to 10. Defaulting to 10")
            R = 10
        
       
        dim = dim[p2:]
        p1 = p2 = 0
        if 'x' in dim: p2 = dim.index('x')
        else:
            print("Invalid input format")
            quit()
        if ' ' in dim: p1 = dim.index(' ')
        
        if p1 > p2: p2 = p1
        C = dim[p2 + 1:]
        if len(C) == 0: C = 3
        else: C = int(C)
        if C < 3: 
            print("Value must be greater than or equal to 3. Defaulting to 3")
            C = 3
        if C > 10: 
            print("Value must be less than or equal to 10. Defaulting to 10")
            C = 10
    
    print "Depth = ", N, "\nTable size = ", R, " x ", C
    
    size = R * C # table size (constant decided by dimensions)
    
    char_set = "ABCDEFGHIJKLMNOPQRSTUVWXYZ.,?!:;\'\"/\\|<>+-=(){}[]`~@#$%^&*1234567890 \n"
    # repeat char set to fill (R*C)^2 spaces
    # i.e 3x3 = 9 tables slots with 9 tables holding characters in last level
    # = 9^2 = 81 characters
    while len(char_set) < pow(size, 2):
        char_set += char_set
    char_set = char_set[0:pow(size,2)]
    
    phrase = raw_input("Enter phrase to be encrypted: ")
    if len(phrase) == 0:
        print("Error: passphrase required")
        quit()
    
    off_in = raw_input("Enter offset variable to shift text (empty = 0): ")
    offset = 0
    if len(off_in) != 0: offset = int(off_in)
    
    encoding = ""
    path_full = ""
    OTP = []
    outs = []
    key = 0 # location in passphrase for mapping path
    shift = 0
    for i in range(0, len(phrase)):
        shift = 0 # comment out for continuous shift value
        pad = ""
        for j in range(0, N-2):
            pos = char_set.index(phrase[key % len(phrase)]) % size 
            # character's position in set 
            # mod by table size for wrapping
            # key mod len(phrase) gives each character of passphrase in sequence
            # and wraps back to beginning
            
            # Get coord
            cx = pos / C + 1
            cy = pos % C + 1
            if cx == 10: cx = 0
            if cy == 10: cy = 0
            
            pad += (str(cx) + str(cy))
            shift += (cx - cy) # x-y or row - col
            key += 1
            
        OTP.append(pad)
        path_full += pad
        
        # Determine set to utilize for encoding
        shifted_set = ""
        if shift == 0:
            shifted_set = char_set
        else:
            shifted_set = char_set[shift:] + char_set[0:shift]
            
        # print char_set
        # print shift
        # print shifted_set
        
        # index holds all locations of character to be encoded
        index = findOccurences(shifted_set, phrase[i])
        # 'Randomly' select one of those locations
        rand_loc = random.randint(0, sys.maxint) % len(index)
        rand_choice = index[rand_loc]
        
        # Get coord for which Nth table to go to
        d2 = rand_choice / size
        d2x = d2/C + 1
        d2y = d2%C + 1
        if d2x == 10: d2x = 0
        if d2y == 10: d2y = 0
        s = str(d2x) + str(d2y)
        
        # Get coord char in Nth table
        dN = rand_choice % size
        dNx = dN/C + 1
        dNy = dN%C + 1
        if dNx == 10: dNx = 0
        if dNy == 10: dNy = 0
        s += str(dNx) + str(dNy)
        
        encoding += s
        path_full += s
        outs.append(s)
    
    print "Unaltered:"
    print path_full
    print OTP
    print outs
    print encoding
    
    
    
    
    c_enc = ""
    # 'Random' path wrapping
    # Decides to alter each value in path by row/col size or leave it alone
    for i in range(len(encoding)):
        x = int(encoding[i])
        r = random.randint(0, sys.maxint)
        w = 1 # Number of possible wraps in row or column
        t = x
        
        if i%2 == 0: # row
            t += R
            while t < 10: # This loop gets wrap number
                w += 1
                t += R
            if x == R:
                x = 0
                w += 1
            # 'Randomly' alter character mapping values
            # Important: does not affect actual location, obscures
            # table size in analysis
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
            
        c_enc += str(x)
        
    print "Full Cypher:"
    cOTP = OTP
    c_outs = []
    # Formatting for testing
    # for i in range(len(phrase)):
    #     cOTP.append(path_final[2*i*N : 2*i*N + 2*(N-2)])
    #     c_outs.append(path_final[2*i*N + 2*(N-2) : 2*i*N + 2*N])
    #     c_enc += c_outs[i]
    
    path_final = ""
    for i in range(len(phrase)*2):
        if i%2 == 0:
            path_final += cOTP[i/2]
        else:
            t = c_enc[2*(i-1) : 2*(i-1) + 4]
            c_outs.append(t)
            path_final += t
            
    print path_final
    print cOTP
    print c_outs
    print c_enc
    
else:
    if "-h" in sys.argv:
        print "help"
        
