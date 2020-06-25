#include <iostream>
#include <cstring>
using namespace std;
class Matrix {
private:
	int dim;
	double* m_data;
public:
	Matrix(int d);
	Matrix(const Matrix& a);	// 添加声明
	~Matrix();
};
Matrix::Matrix(int d) {
	dim = d;
	m_data = new double[dim * dim];
	cout << "Matrix" << endl;
}

// 定义的拷贝构造函数:
Matrix::Matrix(const Matrix& a) {
	this->dim = a.dim;
	this->m_data = new double[dim * dim];	// 申请资源.
	// 把内容复制到新的对象指向的内存空间中.
	for (int i = 0; i < dim * dim; ++i) {
		m_data[i] = a.m_data[i];
	}
}

Matrix::~Matrix() {
	cout << "~Matrix " << (int)m_data << endl;
	delete[] m_data;
	m_data = NULL;
}

int main()
{
	{
		Matrix m1(5);
		Matrix m2(m1);
	}


	system("pause");
	return 0;
}