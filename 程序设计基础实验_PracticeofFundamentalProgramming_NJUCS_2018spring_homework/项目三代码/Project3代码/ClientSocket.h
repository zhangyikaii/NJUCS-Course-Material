#pragma once

#include "Define.h"
#include <windows.h>
#include <iostream>

#include <string>

#define BUFSIZE	16			



class ClientSocket
{
private:
	//server address
	SOCKADDR_IN server;

	//client SOCKET that connect to the server
	SOCKET clientSocket;

	//the message buffer that is received from the server
	char recvBuf[BUFSIZE];

	//the message buffer that is sent to the server
	char sendBuf[BUFSIZE];

public:
	ClientSocket()	;
	~ClientSocket(void);

	//connect to the server
	int connectServer();

	//receive message from server
	int recvMsg();

	//send message to server
	int sendMsg(const char* msg);

	//close socket
	void close();


	//get the received message
	char* getRecvMsg();

};

