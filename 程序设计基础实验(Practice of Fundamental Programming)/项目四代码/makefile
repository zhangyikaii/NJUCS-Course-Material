main: main.o complex.o
	g++ -o main main.o complex.o
main.o: main.cpp
	g++ -c -o main.o main.cpp
complex.o:
	g++ -c -o complex.o complex.cpp
clean:
	rm main *.o

