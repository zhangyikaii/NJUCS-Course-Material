#define M_PI 3.14159265358979323846

#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <math.h>
#include "complex.h"

using namespace std;

//Complex default constructor:
Complex::Complex() {
    real = 0;
    imag = 0;
    num = true;
}

// Alternate constructor with doubles:
Complex::Complex(double& r, double& i) {
    real = r;
    imag = i;
    num = true;
}

// Initialization function
void Complex::Init() {
	real = 0;
	imag = 0;
	num = true;
}

    
//Implement member functions:
//Magnitude Calctulator:
double Complex::magCalc() {
    double mag = sqrt(pow(real, 2) + pow(imag, 2)); //uses the cmath library to take the square root of the sum of the squares of the real and imaginary parts.
    return mag;
}

//Angle Calculator:
double Complex::angleCalc() {
    double angle = atan2(imag, real); //arctan(y/x) for the angle  
    return angle;
}

Complex Complex::conjCreate() {
    Complex A;
    A.real = real;
    A.imag = (-1) * imag;
    return A;
}

//Print Member function:
void Complex::Print() {
    if (num == true) {
        if (imag == 0) {
			printf("结果为：%.6f\n", real);
		}
		else if (imag < 0) {
			printf("结果为：%.6f - %.6fi\n", real, -imag);
		}
		else if (imag > 0) {
			printf("结果为：%.6f + %.6fi\n", real, imag);
		}
    }else {
        cout << " = NaN" << endl;
    }
}

//Implement operator overloads:
Complex Complex::operator+(const Complex& rhs) {
    Complex rTemp;
    rTemp.num = num && rhs.num;
    rTemp.real = real + rhs.real;
    rTemp.imag = imag + rhs.imag;
    return rTemp;
}

Complex Complex::operator-(const Complex& rhs) {
    Complex rTemp;
    rTemp.num = num && rhs.num;
    rTemp.real = real - rhs.real;
    rTemp.imag = imag - rhs.imag;
    return rTemp;
}

Complex Complex::operator*(const Complex& rhs) {
    Complex rTemp;
    rTemp.num = num && rhs.num;
    rTemp.real = real * (rhs.real) - (imag * rhs.imag);
    rTemp.imag = (imag * rhs.real) + (real * rhs.imag);

    return rTemp;
}

Complex Complex::operator/(const Complex& rhs) {
    Complex B = rhs;
    Complex A;
    Complex t1;
    A.real = real;
    A.imag = imag;
    A.num = num && rhs.num;
    double temp = B.magCalc();
    if (temp == 0) {
        A.num = false;
    }else {
        Complex C = A * B.conjCreate();
        t1 = B * B;
        double m = t1.magCalc();
        A.real = C.real / m;
        A.imag = C.imag / m;
    }
    return A;
}

