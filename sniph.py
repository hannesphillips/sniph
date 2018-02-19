#!/bin/python
# Sniph trial

import sys, random

# returns list of indices where c is in S
def findOccurences(S, c):
    return [i for i, letter in enumerate(S) if letter == c]
    
if len(sys.argv) == 1:
    print('Welcome to Sniph Version 1.0.3:\n')
    
    N = 4 # N = cipher depth
    inp = input('Input # of dimensions, N, for cipher (empty for default): ')
    if len(inp) == 0:
        N = 4
    else:
        N = int(inp)
    if N < 4:
        N = 4
        
    R = 0 # table rows
    C = 0 # table columns
    dim = input('Enter dimensions for cipher table, in range 3-10, in form # rows x #cols (empty for default): ')
    if len(dim) == 0:
        # default
        R = 3
        C = 3
    else:    
    # Parse input
        p1 = 0 # location of a space if there is one
        p2 = 0 # location of 'x'
        if ' ' in dim: p1 = dim.index(' ')
        else: p1 = len(dim)
        if 'x' in dim: p2 = dim.index('x')
        else:
            # if there is no 'x' can not seperate rows from columns -> quit
            print('Invalid input format')
            quit()
        
        if p2 < p1: p1 = p2 # 'x' appears before ' '
        R = dim[0:p1] # Get 1st set of numbers
        if len(R) == 0: R = 3 # if empty, default
        else: R = int(R)
        if R < 3: 
            print('Value must be greater than or equal to 3. Defaulting to 3')
            R = 3
        elif R > 10: 
            print('Value must be less than or equal to 10. Defaulting to 10')
            R = 10
        
       
        dim = dim[p2:] # Cut out input we used above
        p1 = 0 # Location of ' ' if there is one
        p2 = 0 # Locaton of 'x'
        if 'x' in dim: p2 = dim.index('x')
        else:
            print('Invalid input format')
            quit()
        if ' ' in dim: p1 = dim.index(' ')
        
        if p1 > p2: p2 = p1 # If there is ' ' after 'x'
        C = dim[p2 + 1:] # Get set of numbers
        if len(C) == 0: C = 3
        else: C = int(C)
        if C < 3: 
            print('Value must be greater than or equal to 3. Defaulting to 3')
            C = 3
        if C > 10: 
            print('Value must be less than or equal to 10. Defaulting to 10')
            C = 10
    
    # Verify input was parsed correctly
    print('Depth = {} \nTable size = {} x {}'.format(N, R, C))
    
    size = R * C # table size, area of the table
    
    
    char_set = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ.,?!:;\'\"/\\|<>+-=(){}[]`'
    '~@#$%^&*1234567890 \n')
    # repeat char set to fill (R*C)^2 spaces
    # i.e 3x3 = 9 tables slots with 9 tables holding characters in last level
    # = 9^2 = 81 characters
    while len(char_set) < pow(size, 2):
        char_set += char_set
    char_set = char_set[0:pow(size,2)]
    
    
    # phrase = passphrase
    phrase = input('Enter phrase to be encrypted: ')
    if len(phrase) == 0:
        print('Error: passphrase required')
        quit()
    phrase = phrase.upper()
    
    # offset shifts output
    off_in = input('Enter offset variable to shift text (empty = 0): ')
    offset = 0
    if len(off_in) != 0: offset = int(off_in)
    
    # path_full will hold the complete path of each character in the passphrase
    # Encoding with contain the last 4 digits representing each character
    # OTP and outs are lists holding the digits of the path from root to N-2 and 
    # from N-1 to N respectively
    # These lists are just to visualize results in testing
    encoding = ''
    path_full = ''
    OTP = []
    outs = []
    key = 0 # current index in passhprase
    shift = 0 # holds shift value for each character's path
    for i in range(0, len(phrase)):
        shift = 0 # comment out for continuous shift value
        temp = '' # holds path to (N-2)th table
        for j in range(0, N-2):
            pos = char_set.index(phrase[key % len(phrase)]) % size 
            # character's position in set 
            # mod by table size to wrap in table
            # key mod len(phrase) gives each character of passphrase in sequence
            # and goes back to the 1st character after all are used
            
            # Get coord
            row_loc = pos // C + 1
            col_loc = pos % C + 1
            if row_loc == 10: row_loc = 0
            if col_loc == 10: col_loc = 0
            
            temp += (str(row_loc) + str(col_loc))
            shift += (row_loc - col_loc) # x-y or row - col
            key += 1 # Index for next character in passphrase
            
        OTP.append(temp) # Store path to (N-2)th table
        path_full += temp # Add path thus far to full path
        
        # Shift character set by previously calculated value
        shifted_set = char_set[shift:len(char_set)] + char_set[0:shift]
            
        # print(char_set)
        # print(shift)
        # print(shifted_set)
        
        # index holds all locations of character to be encoded within the
        # shifted character set
        index = findOccurences(shifted_set, phrase[i])
        
        # 'Randomly' select one of those locations
        rand_loc = random.randint(0, sys.maxsize) % len(index)
        rand_choice = index[rand_loc]
        
        # Get coord for which Nth table to go to
        # d2 represents depth 1 above leaves aka N-1
        d2 = rand_choice // size
        d2_row = d2 // C + 1
        d2_col = d2 % C + 1
        if d2_row == 10: d2_row = 0
        if d2_col == 10: d2_col = 0
        s = str(d2_row) + str(d2_col)
        
        # Get coord char in Nth table
        # dN represents depth of N
        dN = rand_choice % size
        dN_row = dN // C + 1
        dN_col = dN % C + 1
        if dN_row == 10: dN_row = 0
        if dN_col == 10: dN_col = 0
        s += str(dN_row) + str(dN_col)
        # s now holds 4 integers representing a character's location in the last
        # 2 tables taking into account the shift
        
        encoding += s # encoding is the concatenation of the 4 values for each character
        path_full += s # add s to the full path as well
        outs.append(s) # output is a list of the 4 values for each character
    
    # See outputs constrained to table size
    print('Unaltered:')
    print('path: ', path_full)
    print('otp: ', OTP)
    print('outputs: ', outs)
    print('encoded msg :', encoding)
    
    
    
    encoding_final = ''
    # 'Random' path wrapping
    # Decides to alter each value in path by row/col size or leave it alone
    for i in range(len(encoding)):
        x = int(encoding[i]) # Each value in encoding
        r = random.randint(0, sys.maxsize) # random integer
        w = 1 # Number of possible wraps in row or column
        t = x # temp val to determine w
        
        if i%2 == 0: # row
            t += R
            while t < 10: # This loop gets wrap number
                w += 1
                t += R
            if x == R: # if val = # of rows, 0 is also a possible index
                x = 0
                w += 1
            # 'Randomly' alter character mapping values
            # Note: does not affect actual location, obscures
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
            
        encoding_final += str(x) # Add new value to final output
        
    # Formatting for testing
    outs_final = []
    path_final = ''
    # Construct complete path and new list of sets of 4 for each character
    for i in range(len(phrase)*2):
        if i%2 == 0:
            path_final += OTP[i//2]
        else:
            t = encoding_final[2*(i-1) : 2*(i-1) + 4]
            outs_final.append(t)
            path_final += t
    
    # Output to visualize results (will not be present in final)
    print('\nFull Cipher:')
    print('path :', path_final)
    print('otp: ', OTP)
    print('outputs: ', outs_final)
    print('encoded msg :', encoding_final)
    
    # This will be the only output
    print('\nActual output:')
    encoding_final = encoding_final[offset:] + encoding_final[0:offset]
    print(encoding_final)
    
else:
    if '-h' in sys.argv:
        print('help')
        
