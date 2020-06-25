#include "DataBase.h"

void CSameFunction::PrintTable(TableHead pri)
{
	if (pri._pTable == NULL)
	{
		cout << "error: 可能找不到这个TABLE !" << endl;
		return;
	}
	CountAllSetw(&pri);
	int priID = -1;
	bool isFirst = true, isEnd = false;

	////// 以下是一行一行输出
	// ID 的边框
	cout << "+----+";
	// 属性的边框
	for (int i = 0; !pri._pTable->_property[i].empty(); ++i)
	{
		cout.fill('-');
		cout << setw(pri._pTable->_setwPro[i]) << "-";
		cout << "+";
	}
	cout << endl;
	cout.fill(' ');

	while (isEnd != true)
	{
		if (isFirst == true)
		{
			isFirst = false;
			cout << "| ID |";
			for (int i = 0; !pri._pTable->_property[i].empty(); ++i)
				cout << setw(pri._pTable->_setwPro[i]) << pri._pTable->_property[i] << '|';
			cout << endl;
		}
		else
		{
			cout << "| " << setw(2) << priID + 1 << " |";
			for (int i = 0; !pri._pTable->_property[i].empty(); ++i)
				cout << setw(pri._pTable->_setwPro[i]) << pri._pTable->_data[priID][i] << '|';
			cout << endl;
		}

		// ID 的边框
		cout << "+----+";
		// 属性的边框
		for (int i = 0; !pri._pTable->_property[i].empty(); ++i)
		{
			cout.fill('-');
			cout << setw(pri._pTable->_setwPro[i]) << "-";
			cout << "+";
		}
		cout << endl;
		cout.fill(' ');

		++priID;

		isEnd = true;
		for (int i = 0; !pri._pTable->_property[i].empty(); ++i)
		{
			if (!pri._pTable->_data[priID][i].empty())
			{
				isEnd = false;
				break;
			}
		}
	}
}


OrderEnum CSameFunction::PriReadTable(string &orderGet, string &his)
{
	orderGet.clear();
	static bool isFi = false;

	if (isFi == false)
	{
		isFi = true;
		string sql;
		while (sql.compare("mySQL") != 0)
		{
			cout << "~$ ";
			sql.clear();
			getline(cin, sql);
		}
	}

	OrderEnum ans = null_mean;
	string order;
	cout << "(mysql)==> ";
	getline(cin, order);

	size_t brack = order.find("(");
	if (order.compare("quit") == 0)
	{
		cout << "~$" << endl;
		return end_mean;
	}

	else if (order.find("CREATE TABLE") == 0)
	{
		if (order.find("TO") != string::npos)
		{
			bool haveFilena = false, havePro = false, haveTable = false;
			size_t TOpos = order.find("TO"), LBracketpos = order.find("("), RBracketpos = order.find(")");

			// 文件名是否存在
			if (TOpos != string::npos)
			{
				for (int i = TOpos + 2; i < order.length(); ++i)
				{
					if (order[i] != ' ')
					{
						haveFilena = true;
						break;
					}
				}
			}
			if (haveFilena == false)
			{
				cout << "error: order CREATE TABLE TO 不能识别到文件名 !" << endl;
				return bad_mean;
			}

			// 属性是否存在
			if (LBracketpos != string::npos && RBracketpos != string::npos && FindBracketExist(order.substr(LBracketpos, RBracketpos - LBracketpos + 1)) == true)
				havePro = true;		
			if (havePro == false)
			{
				cout << "error: order CREATE TABLE TO 不能识别到属性 !" << endl;
				return bad_mean;
			}

			// TABLE名是否存在
			if (order[12] == ' ' && order[LBracketpos - 1] == ' ')
			{
				if (FindSpacingExist(order.substr(12, LBracketpos - 12)) == true)
					haveTable = true;
			}
			if (haveTable == false)
			{
				cout << "error: order CREATE TABLE TO 不能识别到TABLE名 !" << endl;
				return bad_mean;
			}

			orderGet = order;
			ans = CREATE_TABLE1;
		}
		else
		{
			orderGet = order;
			ans = CREATE_TABLE2;
		}
	}

	else if (order.find("INSERT INTO ") == 0 && brack != string::npos && order.find("(", brack + 1) == string::npos)
	{
		size_t VALUEpos = order.find("VALUES "), LBracketpos = order.find("("), RBracketpos = order.find(")");

		// 找TABLE名
		bool havePro = false;
		if (FindSpacingExist(order.substr(11, VALUEpos - 11)) == false)
		{
			cout << "error: order INSERT INTO (1) 不能识别到TABLE名 !" << endl;
			return bad_mean;
		}

		// 找插入数据
		if (LBracketpos != string::npos && RBracketpos != string::npos && FindBracketExist(order.substr(LBracketpos, RBracketpos - LBracketpos + 1)) == true)
			havePro = true;
		if (havePro == false)
		{
			cout << "error: order INSERT INTO (1) 不能识别到要插入的数据 !" << endl;
			return bad_mean;
		}

		ans = INSERT_INTO1;
		orderGet = order;
	}



	else if (order.find("INSERT INTO ") == 0 && brack != string::npos && order.find("(", brack + 1) != string::npos)
	{
		size_t VALUEpos = order.find("VALUES "), LBracketpos = order.find_last_of("("), RBracketpos = order.find_last_of(")"), FirLBracketpos = order.find_first_of("("), FirRBracketpos = order.find_first_of(")");
		if (VALUEpos == string::npos)
		{
			cout << "error: order INSERT INTO (2) 不能识别到VALUES !" << endl;
			return bad_mean;
		}

		// 找TABLE名
		bool havePro = false, haveData = false;

		if (FirLBracketpos == string::npos || FindSpacingExist(order.substr(11, FirLBracketpos - 11)) == false)
		{
			cout << "error: order INSERT INTO (2) 不能识别到TABLE名 !" << endl;
			return bad_mean;
		}

		// 找插入数据
		if (LBracketpos != string::npos && RBracketpos != string::npos && FindBracketExist(order.substr(LBracketpos, RBracketpos - LBracketpos + 1)) == true)
			haveData = true;
		if (haveData == false)
		{
			cout << "error: order INSERT INTO (2) 不能识别到插入数据 !" << endl;
			return bad_mean;
		}

		// 找属性
		if (FirLBracketpos != string::npos && FirRBracketpos != string::npos && FindBracketExist(order.substr(FirLBracketpos, FirRBracketpos - FirLBracketpos + 1)) == true)
			havePro = true;
		if (havePro == false)
		{
			cout << "error: order INSERT INTO (2) 不能识别到属性 !" << endl;
			return bad_mean;
		}

		ans = INSERT_INTO2;
		orderGet = order;
	}

	else if (order.compare("TABLE LIST") == 0)
	{
		ans = TABLE_LIST;
		orderGet = order;
	}

	else if (order.find("DROP TABLE ") == 0)
	{
		bool isTable = false;
		for (int i = 10; i < order.length(); ++i)
		{
			if (order[i] != ' ')
			{
				isTable = true;
				break;
			}
		}
		if (isTable == false)
		{
			cout << "error: order DROP TABLE 不能识别到TABLE名 !" << endl;
			return bad_mean;
		}

		ans = DROP_TABLE;
		orderGet = order;
	}

	// UPDATE student SET 学号 = value1, 年级 = value2
	else if (order.find("UPDATE") != string::npos && order.find("SET") != string::npos && order.find("WHERE") == string::npos)
	{
		size_t SETpos = order.find("SET "), updataPos = order.find("UPDATE ");
		if (SETpos == string::npos || updataPos == string::npos)
		{
			cout << "error: updata (1) 不能识别到正确代码 !" << endl;
			return bad_mean;
		}
		if (FindSpacingExist(order.substr(updataPos + 6, SETpos - updataPos - 6)) == false)
		{
			cout << "error: updata (1) 不能识别到TABLE名 !" << endl;
			return bad_mean;
		}
		ans = UPDATE1;
		orderGet = order;
	}

	else if (order.find("UPDATE") != string::npos && order.find("SET") != string::npos && order.find("WHERE") != string::npos)
	{
		size_t SETpos = order.find("SET "), WHEREpos = order.find("WHERE ");
		
		// 未加判断
		ans = UPDATE2;
		orderGet = order;
	}

	// DELETE FROM student WHERE 年级 = 空间
	else if (order.find("DELETE FROM ") != string::npos && order.find(" WHERE ") != string::npos)
	{
		size_t FROMpos = order.find("FROM "), wherepos = order.find("WHERE");
		if (FindSpacingExist(order.substr(FROMpos + 4, wherepos - FROMpos - 4)) == false)
			return bad_mean;

		ans = DELETE_FROM;
		orderGet = order;
	}

	// DELETE * FROM student
	else if (order.find("DELETE * FROM ") != string::npos)
	{
		bool isHave = false;
		for (int i = 13; i < order.length(); ++i)
		{
			if (order[i] != ' ')
				isHave = true;
		}
		if (order.length() < 15 || isHave == false)
			return bad_mean;

		ans = DELETE_FROM_ALL;
		orderGet = order;
	}

	else if (order.find("SELECT ") != string::npos && order.find("FROM ") != string::npos && order.find("DISTINCT ") == string::npos
		&& order.find("SELECT * FROM ") == string::npos && order.find("WHERE ") == string::npos && order.find("TO ") == string::npos)
	{
		// 未加判断

		ans = SELECT_FROM;
		orderGet = order;
	}

	else if (order.find("SELECT * FROM ") != string::npos && order.find("ASC") == string::npos && order.find("DESC") == string::npos && order.find("WHERE") == string::npos)
	{
		// 未加判断

		ans = SELECT_ALL;
		orderGet = order;
	}

	else if (order.find("SELECT ") != string::npos && order.find("FROM ") != string::npos && order.find("DISTINCT ") != string::npos
		&& order.find("SELECT * FROM ") == string::npos && order.find("WHERE ") == string::npos && order.find("TO ") == string::npos)
	{
		// 未加判断

		ans = SELECT_DISTINCT;
		orderGet = order;
	}

	else if (order.find("SELECT * FROM ") != string::npos && (order.find("ASC") != string::npos || order.find("DESC") != string::npos) && order.find("WHERE") == string::npos)
	{
		// 未加判断

		ans = SELECT_SEQU;
		orderGet = order;
	}


	else if (order.find("SELECT * FROM ") != string::npos && order.find("WHERE ") != string::npos && order.find("TO ") == string::npos && order.find("ORDER BY") == string::npos)
	{
		// 未加判断

		ans = SELECT_WHERE;
		orderGet = order;
	}

	// SELECT * FROM student WHERE Score1 = 90 TO 计算机系学生名单.txt
	else if (order.find("SELECT ") != string::npos && order.find("FROM ") != string::npos && order.find("DISTINCT ") == string::npos
		&& order.find("SELECT * FROM ") != string::npos && order.find("WHERE ") != string::npos && order.find("TO ") != string::npos)
	{
		// 未加判断

		ans = SELECT_TO;
		orderGet = order;
	}

	else if (order.find("SELECT * FROM ") != string::npos && (order.find("ASC") != string::npos || order.find("DESC") != string::npos) && order.find("WHERE") != string::npos)
	{
		ans = SELECT_SEQU_WHERE;
		orderGet = order;
	}

	else if (order.find("VIEW HISTORY WHERE LIKE ") != string::npos)
	{
		ans = SHOW_HIS;
		orderGet = order;
	}

	if (ans == null_mean)
		cout << "error: 输入了无法读取的命令 !" << endl;

	his = orderGet;
	return ans;
}

// 判断一段 首尾空格的string 中间有没有东西
bool CSameFunction::FindSpacingExist(string a)
{
	if (a.length() < 3)
		return false;
	if (a[0] == ' ' && a[a.length() - 1] == ' ')
	{
		for (int i = 0; i < a.length(); ++i)
		{
			if (a[i] != ' ')
				return true;
		}
	}
	return false;
}

// 检测 (    ) 两个括号中间有没有东西 一定要有括号
bool CSameFunction::FindBracketExist(string a)
{
	if (a.length() < 3)
		return false;
	if (a[0] == '(' && a[a.length() - 1] == ')')
	{
		for (int i = 1; i < a.length() - 1; ++i)
		{
			if (a[i] != ' ')
				return true;
		}
	}
	return false;
}


void CSameFunction::EraseSpacing(string &s)
{
	int index = 0;
	if (!s.empty())
	{
		while ((index = s.find(' ', index)) != string::npos)
			s.erase(index, 1);
	}
}

// 传进来必须是严格的 order : (世纪,三角,代收) 可以有空格
void CSameFunction::ReadOrderData(string order, string *data, int &numPro)
{
	EraseSpacing(order);
	for (int bef = 0, end = 0; end < order.length() && order[end] != ')'; bef = end)
	{
		if (order.find(",", end + 1) != string::npos)
			end = order.find(",", end + 1);
		else
			end = order.find(")", end + 1);
		data[numPro++] = order.substr(bef + 1, end - bef - 1);
	}
}

// 作用是把 "(你, 好 , 吗)" 读取出来 放到二维数组(第二个参数里)
void CSameFunction::ReadInsertData(string order, string data[MAX_DATA][MAX_PROPERTY], int beg)
{
	EraseSpacing(order);
	int i_ins = 0;
	bool isEmpty = false;
	for (; ; ++i_ins)
	{
		isEmpty = true;
		for (int i = 0; i < MAX_DATA; ++i)
		{
			if (!data[i_ins][i].empty())
				isEmpty = false;
		}
		if (isEmpty == true)
			break;
	}
	for (int bef = 0, end = 0; end < order.length() && order[end] != ')'; bef = end)
	{
		if (order.find(",", end + 1) != string::npos)
			end = order.find(",", end + 1);
		else
			end = order.find(")", end + 1);

		string t("1");
		string test = order.substr(bef + 1, end - bef - 1);
		data[i_ins][beg++] = order.substr(bef + 1, end - bef - 1);
	}
}

void CSameFunction::ReadSomePro(string rea, string a[], int i_a)
{
	EraseSpacing(rea);
	int beg = 0, end = 0;
	for (int i = 0; i < rea.length(); ++i)
	{
		if (rea[i + 1] == ',' || i + 1 == rea.length())
		{
			end = i + 1;
			a[i_a++] = rea.substr(beg, end - beg);
			beg = end + 1;
		}
	}
}

int CSameFunction::CalcuChinese(string a)
{
	int num = 0;
	for (int i = 0; i < a.length(); ++i)
	{
		if (a[i] < 0 || a[i] > 127)
		{
			++num;
			++i;
		}
	}
	return num / 2;
}

int CSameFunction::CalcuSetw(string a)
{
	int num = 0, numEng = 0;
	for (int i = 0; i < a.length(); ++i)
	{
		if (a[i] < 0 || a[i] > 127)
		{
			++num;
			++i;
		}
		else
			++numEng;
	}
	return num / 2 + numEng;
}

void CSameFunction::CountAllSetw(TableHead *pSetw)
{
	for (int i = 0; !pSetw->_pTable->_property[i].empty(); ++i)
	{
		int t_max = pSetw->_pTable->_property[i].length() + 3;
		for (int k = 0; k < MAX_DATA; ++k)
		{
			pSetw->_pTable->_data[k][i];
			int t_setw = CalcuSetw(pSetw->_pTable->_data[k][i]) + 3;
			t_max = max(t_max, t_setw);
		}
		pSetw->_pTable->_setwPro[i] = t_max;
	}
}

// 优化 每个DATA之间都有分割符

void CSameFunction::DeleteTableHead(Table *&del)
{
	while (del != NULL)
	{
		Table *tDel = del;
		del = del->_next;
		delete tDel;
	}
}


