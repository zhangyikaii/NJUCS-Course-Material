#include "string_operator.h"


///////////////// 自己写的部分:
// 构造函数
CustomString::CustomString() : p(NULL), len(0) { }
CustomString::CustomString(const char* str) : len(strlen(str) + 1) {
	p = new char[len];
	strcpy(p, str);
}

// 注意不要漏了拷贝构造函数:
CustomString::CustomString(const CustomString& a) : len(a.len) {
	p = new char[a.len];
	strcpy(p, a.p);
}



char& CustomString::operator [](int idx) {
	if (idx >= len) {
		printf("index ERROR!");
		exit(0);
	}
	return p[idx];
}

// 重载加号, 返回和传进去都是const A&, 返回的都是函数内创建的临时对象
CustomString CustomString::operator +(const CustomString& a) {
	char* arr = new char[this->len + a.len];
	int cnt = 0;
	for (int i = 0; p[i] != '\0'; ++i) {
		arr[cnt++] = p[i];
	}
	for (int i = 0; a.p[i] != '\0'; ++i) {
		arr[cnt++] = a.p[i];
	}
	arr[cnt++] = '\0';

	CustomString tmp(arr);

	delete[]arr;
	return tmp;
}
// 重载+=, 返回和传进去和重载+一样, 但是是直接修改本身(就是第一个参数), 返回*this
CustomString CustomString::operator +=(const CustomString& a) {
	char *arr = new char[this->len + a.len];
	int cnt = 0;
	for (int i = 0; p[i] != '\0'; ++i) {
		arr[cnt++] = p[i];
	}
	for (int i = 0; a.p[i] != '\0'; ++i) {
		arr[cnt++] = a.p[i];
	}
	arr[cnt++] = '\0';
	this->len = cnt;

	delete[]this->p;
	p = new char[this->len];
	strcpy(p, arr);

	return *this;
}

bool CustomString::operator ==(const CustomString& a) {
	if (strcmp(this->p, a.p) == 0) {
		return true;
	}

	return false;
}

bool CustomString::operator !=(const CustomString& a) {
	return !(*this == a);
}
// 重载 << 操作符函数应把ostream&作为其第一个参数，对类类型const对象的引用作为第二个参数，并返回对ostream形参的引用, 类内声明为友元.
ostream& operator <<(ostream& out, const CustomString& a) {
	out << a.p;
	return out;
}

// 注意输入这里就不需要 const A& 了.
istream& operator >>(istream& in, CustomString& a) {
	delete[]a.p;
	char arr[100010] = "";
	in >> arr;
	a.len = strlen(arr) + 1;

	a.p = new char[a.len];
	strcpy(a.p, arr);
	return in;
}

///////////////// 自己写的部分

// 析构函数
CustomString::~CustomString()
{
	delete[] p;
	p = NULL;
}

int main() {
	CustomString mystr("this is e CustomString class for testing!");
	cout << mystr[8] << endl;
	mystr[8] = 'a';
	cout << mystr << endl;
	CustomString mystr2 = mystr;			// 注意这里是调用拷贝构造函数, 不是赋值操作符重载!
	cout << mystr2 << endl;
	CustomString mystr3;
	mystr3.operator=(mystr + mystr2);
	cout << mystr3 << endl;
	cout << mystr + mystr2 << endl;
	mystr3 += mystr;
	cout << mystr3 << endl;
	cout << (mystr == mystr2) << endl;
	cout << (mystr != mystr3) << endl;
	CustomString mystr4;
	cout << "Input any string to test the overloaded input operator >>: " << endl;
	cin >> mystr4;
	cout << mystr4 << endl;
	cout << "Congratulations! testing passed!" << endl;
	
	return 0;
}