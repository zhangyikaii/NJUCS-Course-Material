#include <iostream>
#include <iomanip>
#include <string>
#include <cstdio>
#include <cstdlib>
#include <stdlib.h>
#include <stdio.h>
#include <cmath>
#include <stack>
#include <cstring>
#include <vector>
#include "complex.h"

const int MAX_NUM = 100;




using namespace std;

vector<int> error_vec;
vector<string> his_vec;
vector<string> ans_vec;

char Precede(char a, char b) {
	int i, j;
	char Table[11][11] = {
		{ ' ', '+', '-', '*', '/', '^', '[', ']', '(', ')', '=' },
		{ '+', '>', '>', '<', '<', '<', '<', '>', '<', '>', '>' },
		{ '-', '>', '>', '<', '<', '<', '<', '>', '<', '>', '>' },
		{ '*', '>', '>', '>', '>', '<', '<', '>', '<', '>', '>' },
		{ '/', '>', '>', '>', '>', '<', '<', '>', '<', '>', '>' },
		{ '^', '>', '>', '>', '>', '<', '<', '>', '>', '>', '>' },
		{ '[', '<', '<', '<', '<', '<', '<', '=', '<', '<', ' ' },
		{ ']', '>', '>', '>', '>', '<', ' ', '>', '>', ' ', '>' },
		{ '(', '<', '<', '<', '<', '<', '<', ' ', '<', '=', ' ' },
		{ ')', '>', '>', '>', '>', '<', '<', ' ', ' ', '>', '>' },
		{ '=', '<', '<', '<', '<', '<', '<', ' ', '<', ' ', '=' }
	}; 
	for (i = 0; i < 11; i++) {
		if (Table[0][i] == a) 
			break;
	}
	for (j = 0; j < 11; j++) {
		if (Table[j][0] == b)
			break;
	}
	return Table[j][i];
}

bool Calcu_temp(Complex a, char theta, Complex b, Complex &r) {
	if (theta == '+')
		r = a + b;
	else if (theta == '-')
		r = a - b;
	else if (theta == '*')
		r = a * b;
	else if (theta == '^') {
		
		Complex tempa = a;
		for (int i = 0; i < b.real - 1; ++i)
			tempa = tempa * a;

		r = tempa;
	}
	else {
		if (fabs(b.real - 0.0) < 1e-8 && fabs(b.imag - 0.0) < 1e-8) 
			return false;
		else
			r = a / b;
	}
	return true;
}

bool IsOper(char ch) {
	char ptr[10] = { '+', '-', '*', '/', '(', ')', '=', '^', '[',']' };
	int i;
	for (i = 0; i < 10; i++) {
		if (ch == ptr[i])
			return true;
	}
	return false;
}



bool Calculate(string s, Complex &result) {
	stack<Complex> num_stack; 
	stack<char> oper_stack; 
	string ansStr;
	ansStr += "结果为：";	

	int n = s.size();
	char theta;
	int i = 0, j, point = 0;
	Complex a, b, r, tempParse;
	double num = 0;
	oper_stack.push('=');

	while (s[i] != '=' || oper_stack.top() != '=') {					    
		if ((s[i] >= '0' && s[i] <= '9') || s[i] == '.') {					
			num = 0;														
			tempParse.Init();
			point = 0;					 
			
			if (s[i] == '.')
				point = 10;
			else
				num = s[i] - '0';

			j = i + 1;
			while (!IsOper(s[j]) && s[j] != 'i' && s[j] != 'I') {   
				if (s[j] == '.') {
					point = 10;
					j++;
					continue;
				}
				if (!point) 
					num = num * 10 + (s[j] - '0');
				else {
					num = num + 1.0 * (s[j] - '0') / point; 
					point *= 10; 
				}
				j++;
			}
			if (s[j] != 'i' && s[j] != 'I') {
				i = j;
				tempParse.real = num;
			}
			else {
				i = j + 1;
				tempParse.imag = num;
			}
			num_stack.push(tempParse); 
		}

		else if (IsOper(s[i])) {
			switch (Precede(s[i], oper_stack.top())) {
			case '<':
				oper_stack.push(s[i]);
				++i;
				break;
			case '=':
				if (oper_stack.top() == '[') {
					tempParse.Init();
					tempParse.real = num_stack.top().magCalc();
					num_stack.pop();
					num_stack.push(tempParse);
				}
				oper_stack.pop();
				i++;
				break;
			case '>':
				if (!oper_stack.empty())
					theta = oper_stack.top(); 
				else {
					cout << "Calculate error" << endl;
				}

				oper_stack.pop();

				if (!oper_stack.empty())
					b = num_stack.top(); 
				else {
					cout << "Calculate error" << endl;
				}

				num_stack.pop();
				if (!num_stack.empty()) {
					a = num_stack.top();
					num_stack.pop();
				}

				else {
					cout << "Calculate error" << endl;
				}


				if (Calcu_temp(a, theta, b, r)) 
					num_stack.push(r); 
				else
					return false; 
				break;
			}
		}

		
		else if (i + 3 < n && s[i] == 'c' && s[i + 1] == 'j' && s[i + 2] == 'g') {
			int braNum = 0, k = i + 4;
			string subStr;
			for (k = i + 4; k < n; ++k) {
				if (s[k] == '(')
					++braNum;
				else if (s[k] == ')' && braNum != 0)
					--braNum;
				else if (s[k] == ')' && braNum == 0)
					break;
			}
			if (k != n) {
				Complex subResult;
				subStr = s.substr(i + 4, k - i - 4);
				subStr += "=";
				if (Calculate(subStr, subResult)) {
					i = k + 1;
					subResult = subResult.conjCreate();
					num_stack.push(subResult);
				}
				
			}
		}

		else if (i + 3 < n && s[i] == 'a' && s[i + 1] == 'r' && s[i + 2] == 'g') {
			int braNum = 0, k = i + 4;
			string subStr;
			for (k = i + 4; k < n; ++k) {
				if (s[k] == '(')
					++braNum;
				else if (s[k] == ')' && braNum != 0)
					--braNum;
				else if (s[k] == ')' && braNum == 0)
					break;
			}
			if (k != n) {
				Complex subResult, addResult;
				subStr = s.substr(i + 4, k - i - 4);
				subStr += "=";
				if (Calculate(subStr, subResult)) {
					i = k + 1;
					addResult.real = subResult.angleCalc();
					num_stack.push(addResult);
				}
			}
		}
	}
	result = num_stack.top(); 

	char addTemp[MAX_NUM] = "";

	sprintf(addTemp, "%.6f", result.real);
	ansStr += addTemp;
	if (fabs(result.imag) >= 1e-6 && result.imag < 0)
		ansStr += " - ";

	else if (fabs(result.imag) >= 1e-6 && result.imag > 0)
		ansStr += " + ";

	if (fabs(result.imag) >= 1e-6) {
		sprintf(addTemp, "%.6f", result.imag);
		ansStr += addTemp;
		ansStr += "i";
	}

	ans_vec.push_back(ansStr);
	return true;
}


int CheckandInitModu(string &s) {
	int flag = 0, i, modulusFlag = 0, n = s.size();

	
	for (i = 0; i < n; i++) {

		if (i + 1 < n && s[i] == '+' || s[i] == '-' || s[i] == '*' || s[i] == '/' || s[i] == '^') {
			if (s[i + 1] == ')' || s[i + 1] == '+' || s[i + 1] == '-' || s[i + 1] == '*' || s[i + 1] == '/' || s[i + 1] == '^')
				error_vec.push_back(i + 1);
		}

		else if (i + 1 < n && s[i] <= '9' && s[i] >= '0') {
			if (s[i + 1] == '(' || s[i + 1] == '|')
				error_vec.push_back(i + 1);
		}

		else if (i + 1 < n && s[i] == 'i'){
			if (i - 2 >= 0 && s[i - 1] == ')' && s[i - 2] == 'i')
				error_vec.push_back(i);
			if ((s[i + 1] <= '9' && s[i + 1] >= '0') || s[i + 1] == '(' || s[i + 1] == 'i' || s[i + 1] == '|')
				error_vec.push_back(i + 1);
		}

		else if (i + 1 < n && s[i] == '(') {
			if (s[i + 1] == ')' || s[i + 1] == '+' || s[i + 1] == '-' || s[i + 1] == '*' || s[i + 1] == '/')
				error_vec.push_back(i + 1);
		}

		else if (i + 1 < n && s[i] == ')') {
			if (s[i + 1] == '|' || (s[i + 1] <= '9' && s[i + 1] >= '0') || s[i + 1] == '(')
				error_vec.push_back(i + 1);
		}

		if (s[i] == '(')
			flag++;
		else if (s[i] == ')')
			flag--;
		
		else if (s[i] == '|' && modulusFlag == 0) {
			s[i] = '[';
			++modulusFlag;
		}
		else if (s[i] == '|' && modulusFlag == 1) {
			s[i] = ']';
			--modulusFlag;
		}
	}

	
	if (!error_vec.empty())
		return -1;

	
	if (flag != 0 || modulusFlag != 0)
		return 0;
	
	return 1;
}

string EraseSpacing(string a) {
	string res;
	int i = 0;
	int n = a.size();
	if (n >= 1 && a[0] == '-')
		res += "0";
	if (n >= 1 && a[0] == 'i')
		res += '1';
	for (i = 0; i < n; ++i) {
		if (i - 1 >= 0 && a[i] == '-' && a[i - 1] == '(')
			res += "0";

		
		if (i != 0 && a[i] == 'i' && res.size() != 0) {
			int endRes = res.size() - 1;
			if (endRes >= 0) {
				if (res[endRes] == '*' || res[endRes] == '/' || res[endRes] == '+' || res[endRes] == '-')
					res += "1i";

				else if (res[endRes] == ')' || res[endRes] == '|')
					res += "*1i";

				else
					res += "i";
			}
		}

		else if (a[i] <= '9' && a[i] >= '0')
			res += a[i];

		else {
			switch (a[i])
			{
			case '+':
			case '-':
			case '*':
			case '/':
			case '|':
			case '(':
			case ')':
			case 'a':
			case 'r':
			case 'g':
			case 'c':
			case 'j':
			case '^':
			case '.':
				res += a[i];
				break;
			default:
				break;
			}
		}
	}

	his_vec.push_back(res);
	return res;
}

void ShowHis(int num) {
	
	cout << "- - - - - - - - - - - - - - - - - - - - - - - - - - -" << endl;
	int sum = his_vec.size();
	for (int i = sum - num - 1; i < sum; ++i) {
		cout << his_vec[i] << endl;
		cout << ans_vec[i] << endl;
		cout << "- - - - - - - - - - - - - - - - - - - - - - - - - - -" << endl;
	}
}

bool CalculateAll() {
	string reaExp;
	char ch;
	cout << "请输入您要计算的表达式：" << endl;
	getline(cin, reaExp);
	if (reaExp.compare("*") == 0) {
		//ch = _getch();
		ch = '1';
		ShowHis(ch - '0');
		return true;
	}
	if (reaExp.compare("quit") == 0) {
		cout << "退出程序." << endl;
		return false;
	}

	int i, j, checkFlag = false;
	Complex result;
	reaExp = EraseSpacing(reaExp);
	reaExp += "=\0";
	checkFlag = CheckandInitModu(reaExp);
	if (checkFlag == 1) {                      
		if (Calculate(reaExp, result))                   
			result.Print();
		else
			printf("error: Divide or mod by zero!\n");
	}
	else if (checkFlag == 0) {
		printf("error: Bracket or modu mismatch!\n");
	}
	else if (checkFlag == -1) {
		int n = error_vec.size();
		for (int i = 0; i < n; ++i)
			cout << error_vec[i] << " ";
		cout << endl;
	}

	cout << "- - - - - - - - - - - - - - - - - - - - - - - - - - -" << endl;
	return true;
}


int main() {	
	while (CalculateAll() != false) {

	}
	
	return 0;
}
