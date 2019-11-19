main: main.o CTable.o CSameFunction.o CFile.o
	g++ -o main main.o CTable.o CSameFunction.o CFile.o
main.o: main.cpp
	g++ -c -o main.o main.cpp
CTable.o:CTable.cpp
	g++ -c -o CTable.o CTable.cpp
CSameFunction.o:CSameFunction.cpp
	g++ -c -o CSameFunction.o CSameFunction.cpp
CFile.o:CFile.cpp
	g++ -c -o CFile.o CFile.cpp
clean:
	rm main *.o

