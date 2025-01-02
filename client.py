import socket
import sys
import struct

SEND = 0
RECEIVE = 1

argument = 0
 
if len(sys.argv) == 1:
    print("No arguments passed")
    exit()
elif sys.argv[1] == "send":
    print("Sending")
    argument = SEND
elif sys.argv[1] == "receive":
    print("Receiving")
    argument = RECEIVE
else:
    print("Malformed argument passed")
    exit()

PORT = 8000
SERVER_ADDR = "127.0.0.1" #local for now

socketfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socketfd.connect((SERVER_ADDR, PORT))

print("Connected to %s" %socketfd.getpeername()[0])

socketfd.send(str(argument).encode())
print("Sent - %s" %(str(argument).encode()))

yardsaleData = {
    "username": "",
    "location": "",
    "dates": "",
    "time": "",
    "description": "",
    "dataSizes": [0]*5
}

if argument == SEND:
    file = open("yardsaleData.txt", "r") 
    entryList = list(yardsaleData.keys())
    i = 0
    for currentLine in file:
        if i != 4:
            entry = currentLine[:(len(currentLine)-1)] + '\0'
        else:
            entry = currentLine + '\0'
        yardsaleData["dataSizes"][i] = len(entry)
        yardsaleData[entryList[i]] = entry
        i += 1
    file.close()
    for currentEntry in entryList:
        print("%s - %s / Length - %d" %(currentEntry, yardsaleData[currentEntry], len(yardsaleData[currentEntry])))
    dataSizesStruct = struct.pack('!5I', *yardsaleData["dataSizes"])
    socketfd.send(dataSizesStruct) #SEND DATA SIZES
    
    for i in range(5):
        socketfd.send(yardsaleData[entryList[i]].encode())
        print("Sent over %s" %yardsaleData[entryList[i]])

    print("Data sent!")
    #print("Wiping previous text file...")
    #open("yardsaleData.txt", "w").close()
    
elif argument == RECEIVE:
    fileSize = int.from_bytes((socketfd.recv(4)), "big")
    print("File size : ", fileSize)
    with open("databaseLocal.txt", "w") as database:
        database.write(socketfd.recv(fileSize).decode())
    print("Database received!")