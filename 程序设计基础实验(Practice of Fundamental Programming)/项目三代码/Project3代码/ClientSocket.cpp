#include "ClientSocket.h"

#pragma comment(lib, "Ws2_32.lib")


ClientSocket::ClientSocket()
{
	
}


ClientSocket::~ClientSocket(void)
{
	close();
}

/**	connect to the server
*	return 0 means that connect to the server successfully
*	return >0 means that an error happened.
*/
int ClientSocket::connectServer()
{
	std::cout << "Connect server: " << SERVER_IP << ":" << SERVER_PORT << std::endl;
	int rtn = 0, err = 0;
	WSADATA wsaData;
	// initialize windows socket library
	err = WSAStartup(0x0202, &wsaData);
	if (err != NO_ERROR)
	{
		std::cout << "Failed with WSAStartup error: " << err << std::endl;
		rtn = 1;
		return rtn;
	}
	// creat socket
	clientSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	if (clientSocket == INVALID_SOCKET)
	{
		std::cout << "Socket failed with error: " << WSAGetLastError() << std::endl;
		rtn = 2;
		return rtn;
	}
	// server address
	memset(&server, 0, sizeof(SOCKADDR_IN));
	server.sin_family = PF_INET;
	server.sin_port = htons(SERVER_PORT);
	server.sin_addr.s_addr = inet_addr(SERVER_IP);
	// connect
	err = connect(clientSocket, (struct sockaddr *) &server, sizeof(SOCKADDR_IN));
	if (err < 0)
	{
		std::cout << "Connect failed with error: " << err << std::endl;
		// printf("%d\n", WSAGetLastError);
		rtn = 3;
		return rtn;
	}
	return rtn;
}


/*	send message to the server
*	input the message that you want to send to the message
*	return 0 means that send message successfully
*	return 1 means that an error happened
*/
int ClientSocket::sendMsg(const char* msg)
{
	int rtn = 0, err = 0;

	//set length 
	int len = strlen(msg);
	len = len < BUFSIZE ? len+1 : BUFSIZE;

	//set sendBuf
	memset(sendBuf, 0, BUFSIZE);
	memset(sendBuf, 0, sizeof(sendBuf));
	memcpy(sendBuf, msg, len);

	//send message to the server
	err = send(clientSocket, sendBuf, BUFSIZE, 0);
	if (err < 0)
	{
		std::cout << "Send msg failed with error: " << err << std::endl;
		rtn = 1;
		return rtn;
	}
	return rtn;
}


/*	receive message from the server
*	return 0 means that receives message successfully
*	return 1 means that an error happened
*/
int ClientSocket::recvMsg()
{
	int rtn = 0, err = 0;
	memset(recvBuf, 0, BUFSIZE);

	//receive message
	err = recv(clientSocket, recvBuf, BUFSIZE, 0);
	if (err < 0)
	{
		std::cout << "Receive msg failed with error: " << err << std::endl;
		rtn = 1;
		return rtn;
	}
	return rtn;

}

//get the received message
char* ClientSocket::getRecvMsg(){
	return this->recvBuf;
}

/*close client socket*/
void ClientSocket::close(){
	closesocket(clientSocket);

	std::cout << "Close socket" << std::endl;
}