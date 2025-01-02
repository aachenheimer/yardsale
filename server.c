#define WIN32_LEAN_AND_MEAN

#include <stdio.h>
#include <winsock2.h>
#include <windows.h>
#include <ws2tcpip.h>
#include <string.h>
#include <errno.h>

#define PORT "8000"

void receiveData(void* dataPointers[], int dataSizes[], int acceptedSocketfd) {
	printf("\nReceiving rest of data...");
	int dataReceivedSize;
	for (int i = 0; i < 5; i++) {
		//printf("\nTest - %p", ((char*)dataPointers[i]));
		dataReceivedSize = recv(acceptedSocketfd, (char*)dataPointers[i], dataSizes[i], 0);
		printf("\nReceived string : \"%s\" of size %d", ((char*)dataPointers[i]), dataReceivedSize);
	}
}

void writeDataToDatabase(void * dataPointers[]) {
	FILE *database;
	database = fopen("database.txt", "a");
	for (int i = 0; i < 5; i++) {
		fprintf(database, (char*)dataPointers[i]);
		fprintf(database, "\n");
	}
	fclose(database);
}

int main() {
	WSADATA wsaData;
	WSAStartup(MAKEWORD(2,2), &wsaData);
	
	const char RECEIVE = '0';
	const char SEND = '1';
	
	int socketfd, acceptedSocketfd;
	char client_addr[INET_ADDRSTRLEN]; 
	struct addrinfo hints, *res;
	struct sockaddr_in incoming_addr;
	socklen_t incomingAddr_size = sizeof(incoming_addr);
	
	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;
	
	if(getaddrinfo(NULL, PORT, &hints, &res) != 0) {
		printf("getaddrinfo failed: %d\n", WSAGetLastError());
		WSACleanup();
		return 1;
	}//fill out address info, assumes first address is correct
	
	socketfd = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
	if (socketfd == INVALID_SOCKET) {
		printf("Socket creation failed: %d\n", WSAGetLastError());
		WSACleanup();
		return 1;
	} //create socket fd
	
	if (bind(socketfd, res->ai_addr, res->ai_addrlen) == SOCKET_ERROR) {
		printf("Bind failed: %d\n", WSAGetLastError());
		WSACleanup();
        return 1;
	} //bind socketfd to port 8000
	
	if (listen(socketfd, 5) == SOCKET_ERROR) {
		printf("Listen failed: %d\n", WSAGetLastError());
		WSACleanup();
        return 1;
	} //listen for connections on socketfd
	
	while (1) {
		acceptedSocketfd = accept(socketfd, (struct sockaddr*)&incoming_addr, &incomingAddr_size);
		if (acceptedSocketfd == INVALID_SOCKET) {
			printf("Accept call failed: %d\n", WSAGetLastError());
			continue;
		}
		
		inet_ntop(AF_INET, &(incoming_addr.sin_addr), client_addr, INET_ADDRSTRLEN);
		printf("\nAccepted new connection from %s!", client_addr);
		char argument[1];
		recv(acceptedSocketfd, argument, 1, 0);
		printf("\nReceived argument: %c", argument[0]);
		
		if (argument[0] == RECEIVE) {
			printf("\nServer instructed to receive");
			int dataSizes[5];
			int dataReceived;
			dataReceived = recv(acceptedSocketfd, (char *)dataSizes, sizeof(dataSizes), 0);
			printf("\nAmount of data received : %d", dataReceived);
			if (dataReceived == 0) {
				printf("\nSomething went wrong... closing socket");
				closesocket(acceptedSocketfd);
				continue;
			}
			printf("\nReceived data sizes : ");
			for (int i = 0; i < 5; i++) {
				dataSizes[i] = ntohl(dataSizes[i]);
				printf("%d ", dataSizes[i]);
			}
			
			char username[dataSizes[0]];
			char location[dataSizes[1]];
			char dates[dataSizes[2]];
			char time[dataSizes[3]];
			char description[dataSizes[4]];
			void* dataPointers[5] = {&username, &location, &dates, &time, &description};
			printf("\nCreated username space of %d size", sizeof(username));
			printf("\nCreated location space of %d size", sizeof(location));
			printf("\nCreated dates space of %d size", sizeof(dates));
			printf("\nCreated time space of %d size", sizeof(time));
			printf("\nCreated description space of %d size", sizeof(description));
			
			receiveData(dataPointers, dataSizes, acceptedSocketfd);
			
			printf("\nAll data received! Writing to database...");
			
			writeDataToDatabase(dataPointers);
		}
		
		else if (argument[0] == SEND) {
			printf("\nServer instructed to send");
			
			FILE *database;
			int fileSize, networkFileSize, bytesSent;
			database = fopen("database.txt", "r");
			fseek(database, 0L, SEEK_END);
			fileSize = ftell(database);
			rewind(database);
			printf("\nSize of database : %d bytes", fileSize);
			networkFileSize = htonl(fileSize);
			send(acceptedSocketfd, (char *)&networkFileSize, sizeof(networkFileSize), 0);
			printf("\nSent over database size!");
			printf("\nSending database...");
			char databaseBuffer[fileSize] = {};
			fread(databaseBuffer, sizeof(char), fileSize, database);
			bytesSent = send(acceptedSocketfd, databaseBuffer, fileSize - 1, 0);
			printf("Sent over database of size %d", bytesSent);
			fclose(database);
			
			/*FILE *databaseTest;
			databaseTest = fopen("databaseTest.txt", "w");
			printf("\nSize of database buffer : %d", sizeof(databaseBuffer));
			for (int i = 0; i < fileSize; i++) {
				fputc(databaseBuffer[i], databaseTest);
			}
			fclose(databaseTest); */
			
		}
		
		else {
			printf("\nMalformed argument");
		}
		
		printf("\nClosing socket!");
		closesocket(acceptedSocketfd);
	}
	
	printf("\n\nClosing server...");
	
	freeaddrinfo(res);
	closesocket(socketfd);
	WSACleanup();
}