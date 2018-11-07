# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 12:09:45 2018

@author: Vivian Wong Kah Ong
"""
import sys, traceback

###################################For Encoding###############################
def encoder(encode_file_path):
    '''
    Function to compress file with 8-bit encoded characters to LZW-compressed 12-bit encoding file
    Input 'encode_file' is file path (str)
    '''
    def read30k():
        #Read chunk size of 30kb
        return f.read(30*1024)
    # Open file to be compressed in binary format
    f = open(encode_file_path,'rb')
    # Create compressed file which we will write to
    w = open(encode_file_path[:encode_file_path.rfind('.')]+'.z',"wb")
    # Initialise parameters (needed because file is read chunk by chunk)
    P=''
    binstring=''
    end=False
    table=[chr(c) for c in range(256)] #Initialise table with 256 length 1 characters
    # Compress file chunk by chunk
    for piece in iter(read30k, ''): 
         # Check if reach the end of file
        if len(piece)<(30*1024):
            end=True
            print('end')
        try:
            # perform LZW compression. The compressed data is int (max value 4096)
            output,P,table=compress(piece,P,end,table)
            # Convert int(12bit) to 8-bit char
            string,binstring=int12ToChar8(output,binstring,end)
            # Write output to file
            w.write(string)
        except:
            break
    # Close the files
    f.close()
    w.close()
    return

def compress(string,P='',end=True,table=[chr(c) for c in range(256)]):
    '''
    Function to perform LZW compression. The compressed data is int with max value 4096
    Input 'string' is a string
    Optional input are used when reading file by chunk.
    '''
    # Store list of int code (max value 4096)
    output=[]
    for i in range(len(string)):
        C = string[i]
        #Find code for string in table
        if P + C in table: 
            P += C
        else:
            # Output code
            output.append(table.index(P))
            # Add code for string into table
            table.append(P+C) 
            # Increment code P
            P = C
        # If last character in file, output the code for P
        if i==(len(string)-1) and end: 
            output.append(table.index(P))
        # When all the possible codes have been used, the table is reset
        if len(table)>=4096: 
            table=[chr(c) for c in range(256)]
    return output,P,table
    
def int12ToChar8(data,bits='',end=True):
    '''
    Function to break down int(12bit) to int(8 bit) and then to 8-bit char
    '''
    # Store string of 8-bit char
    n=''
    # Iterator of data
    i=0
    while i<len(data) or len(bits)>=8:
        # While there are still data to be converted
        if i<len(data):
            d=data[i]
            #Convert int (12 bit) to 12-bit binary string.
            bits+='{0:012b}'.format(d) 
        # While there are still 8-bit binary strings to be converted
        while len(bits)>=8: 
            #Convert the binary string to 8-bit char
            n+=chr(int(bits[:8],2))
            #Remove converted binary strings
            bits=bits[8:]
        i+=1
    #If odd number of codes, append 0000 to binary string of the last code
    if len(bits) and end: 
        n+=chr(int(bits+'0000',2))
        bits=''
    return n,bits
###################################For Decoding###############################

def decoder(decode_file_path):
    '''
    Function to decompress LZW-compressed file with 12-bit-width code
    Input 'decode_file' is file path (str)
    '''
    def read300k():
        #Read chunk size of 300kb
        return f.read(300*1024) 
    
    # Open file to be compressed in binary format
    f = open(decode_file_path,'rb')
    # Create .txt file which we will write to
    w = open(decode_file_path[:decode_file_path.rfind('.')]+'.txt',"w+")
    # Initialise parameters (needed because file is read chunk by chunk)
    start=True #var to indicate first chunk in file
    p=0
    table=[0]
    # Compress file chunk by chunk
    for piece in iter(read300k, ''): 
        try:
            # Convert 8-bit char to 12-bit int (max value 4096)
            output=bytesTo12Bits(piece)
            # Decompress 12-bit int (max value 4096) and encode the output as string of 8-bit char
            output,table,p=decompress(output,start,p,table)
            # Write output to file
            w.write(output)
            start=False
        except Exception as e:
            t,v,tb = sys.exc_info()
            print(str(t)+'\n'+str(v)+'\n'+str(traceback.format_tb(tb)))            
            break
    # Close the files
    f.close()
    w.close()
    return

def bytesTo12Bits(data):
    '''
    Function to convert 8-bit char to 12-bit int (max value 4096)
    '''
    # Store list of 12-bit int
    n=[]
    for i,byte in enumerate(data):
        # Convert each 8=bit char to binary form
        bits='{0:08b}'.format(ord(byte))
        # Break down and combine binary strings. Convert the binary string to int
        if i%3==0: 
            whole=bits
        elif i%3==1:
            front=bits[:4]
            end=bits[-4:]
            n.append(int(whole+front,2))
        elif i%3==2:
            n.append(int(end+bits,2))
    return n

def decompress(data,start=True,p=0,table=[0]):
    '''
    Function to decompress 12-bit int (max value 4096) and encode the output as string of 8-bit char
    Input 'data' is an iterable containing 12-bit int (max value 4096)
    Optional input are used when reading file by chunk. 
        -If first chunk of file: start=TRUE, 'p' and 'table' would be ignored
        -If not first chunk of file: start=FALSE, 'p' and 'table' should be obtained from previous func call
    '''
    # Initialise output string
    output=''
    # If the data chunk is the first chunk of the entire file
    if start:
        # Initialise table with 256 length 1 characters
        table=[chr(c) for c in range(256)] 
        # Read first code
        p=data[0]
        # Decode and output first code
        output+=table[p]
        # Remove first code
        data=data[1:]
    for c in data:
        # Show error message for corrupted encoding file
        if p>=len(table):
            print('Decoding Error. File might not be encoded with LZW properly.', p, len(table))
        # Translate code to string
        if c >=len(table):
            s=table[p]+ch
        else:
            s=table[c]
        # Output code
        output+=s
        # get first character of s
        ch=s[0]
        # Add to table
        table.append(table[p]+ch)
        # Increment p to current code
        p=c
        # When all the possible codes have been used, the table is reset
        if len(table)>=4096: 
            table=[chr(c) for c in range(256)]
    return output,table,p