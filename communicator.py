from socket import *
import os
import selectors
import json

selector = selectors.DefaultSelector()

PORT = 7999

numOfRooms = 5 #change later obv i forget how many rooms there are / read from json file

def parseInput(rawString):
	parsedText = []
	currentString = ""
	onMessage = False
	for currentChar in rawString:
		#print("%c " %currentChar, end = '')
		if currentChar == " " and onMessage == False:
			if currentString != "":
				parsedText.append(currentString)
			currentString = ""
			continue
		elif currentChar == "\"" and onMessage == False:
			print("TESTING : ENTERING MESSAGE")
			currentString = ""
			onMessage = True
			continue
		elif currentChar == "\"" and onMessage == True:
			print("TESTING : REACHED END OF MESSAGE")
			parsedText.append(currentString)
			currentString = ""
			onMessage = False
			continue
		currentString += currentChar
		#print("appended char \'%c\'" %currentChar, end = '')
		#print("")
	if currentString != "":
		parsedText.append(currentString)
	
	return parsedText

def help(input):
	if len(input) == 1:
		print("\nsendmsg : sends a message, by default to W003")
		print("config : opens config menu")
		print("type \'help\' followed by the name of the command you want more information on\n")
	else:
		if input[1].upper() == "SENDMSG":
			print("\nSend text messages to W003 or other rooms")
			print("sendmsg \"message\" -destination\n")
			
		elif input[1].upper() == "CONFIG":
			print("\nOpens the config menu")
			print("Used to change port, ip, name, and room configuation\n")

def sendmsg(msg):
	#doesnt need to be registered under selectors because its very briefly established
	#also this can be blocking b/c we can wait to send the message
	sendSocketfd = socket(AF_INET, SOCK_STREAM)

def acceptSocket(receiveSocket):
	#also doesnt need to be registered under selectors b/c again, very briefly established
	incomingSocketfd, addr = receiveSocket.accept()
	incomingMsg = incomingSocketfd.recv(1024)
	print("\nReceived connection from %s\n" %addr)

receiveSocketfd = socket(AF_INET, SOCK_STREAM) #FOR RECEIVING MESSAGES FROM OTHER ROOMS
receiveSocketfd.setblocking(False)
receiveSocketfd.listen(numOfRooms)
selector.register(receiveSocketfd, selectors.EVENT_READ, acceptSocket)

while True:
	choice = input("Type \'help\' for more options\n>")

	#print("TESTING %s" %choice)
	
	parsedInput = parseInput(choice)
	#print("TESTING : ", parsedInput)

	if parsedInput[0].upper() == "HELP":
		os.system('cls')
		help(parsedInput)

	if parsedInput[0].upper() == "EXIT":
		os.system('cls')
		exit()
		