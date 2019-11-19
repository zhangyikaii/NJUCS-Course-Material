// Complex Number Class decaration
// Mac Clayton, 2012
// ECE3090 Lab 1

#include <iostream>
#include <string>
using namespace std;


class Complex {
public:
    //Default Constructor
    Complex();
    //Double Constructor
    Complex(double& r, double& i);
    //String Parsing Constructor
    Complex(string& st);

	// Initialization function
	void Init();
        
    //Member functions:
    double magCalc();       //Gives the magnitude of the two numbers
    double angleCalc();     //Gives the angle between the real and imaginary
    void Print();           //Print the complex number
    Complex conjCreate();   //Create the complex conjugate
    
    //Plus and minus overload operators:
    Complex operator+(const Complex& rhs);
    Complex operator-(const Complex& rhs);
    
    //Multiplication and division operators:
    Complex operator*(const Complex& rhs);
    Complex operator/(const Complex& rhs);
        
public:
    //Define variables
    double real;
    double imag;
    //num is used to implement NaN
    bool num;
    
};







