#include <iostream>
#include <string>
#include <map>
#include <iomanip>
#include <algorithm>
#include <stdlib.h>
#include <stdio.h>
#define LIN 0
using namespace std;

const int MAX_PROPERTY = 30;   // 最多三十个属性
const int MAX_TABLE = 100;     // 最多一百个表
const int MAX_DATA = 200;      // 最多两百条信息
const int MAX_LINE = 300;      // 每行最多三百
const int MAX_HISTORY = 30;    // 最多三十条历史记录
const char _NameFile_[13] = "NameFile.txt";   // 名字文件名
const int MAX_JUDGE = 30;      // 最多三十个判断条件

enum OrderEnum
{
	null_mean = -1,
	bad_mean,
	end_mean,
	CREATE_TABLE1,
	CREATE_TABLE2,
	DROP_TABLE,
	TABLE_LIST,
	INSERT_INTO1,
	INSERT_INTO2,
	DELETE_FROM,
	DELETE_FROM_ALL,
	UPDATE1,
	UPDATE2,
	SELECT_FROM,
	SELECT_ALL,
	SELECT_DISTINCT,
	SELECT_SEQU,
	SELECT_WHERE,
	SELECT_TO,
	SELECT_SEQU_WHERE,
	SHOW_HIS
};
enum maxflag
{
	AMAX = -1,
	EQUAL,
	BMAX,
	BADMEAN
};

struct Condi
{
	int _pro;
	string _stanData;
	maxflag _how;
	Condi()
	{
		_how = BADMEAN;
		_pro = -1;
	}
};

// 一个TABLE的全部 里面是全部信息(链表)
struct Table
{
	// 一维存属性的
	string _property[MAX_PROPERTY];
	int _num_property;
	int _setwPro[MAX_PROPERTY];
	// 二维数组存数据的
	string _data[MAX_DATA][MAX_PROPERTY];
	Table *_next;
	Table()
	{
		_num_property = 0;
		_next = NULL;
		for (int i = 0; i < MAX_PROPERTY; ++i)
			_setwPro[i] = 0;
	}
};

// 一个TABLE的头 (身体是链表 头结点在这里面)
struct TableHead
{
	string _fileName;
	string _tableName;
	Table *_pTable;
	TableHead()
	{
		_pTable = NULL;
	}
	TableHead(string t, Table *p)
	{
		_tableName = t;
		_pTable = p;
	}
};


class CFile
{
public:
	void ReadFile(TableHead &a);
	void CreateToNameFile(string taNa, string Fina);

};

class CSameFunction
{
public:
	OrderEnum PriReadTable(string &orderGet, string &his);
	void EraseSpacing(string &s);
	void ReadOrderData(string order, string *data, int &numPro);
	bool FindSpacingExist(string a);
	bool FindBracketExist(string a);
	void ReadInsertData(string order, string data[MAX_DATA][MAX_PROPERTY], int beg = 0);
	void DeleteTableHead(Table *&del);
	int CalcuSetw(string a);
	int CalcuChinese(string a);
	void CountAllSetw(TableHead *pSetw);
	void ReadSomePro(string rea, string a[], int i_a = 0);
	void PrintTable(TableHead pri);
};

class CTable
{
public:
	CTable();
	void CreateTableTo(string order);
	void CreateTableFrom(string order);
	TableHead &FindTableHead(string fiName);
	TableHead &FindTableHeadbyTABLEname(string taName);
	void InsertTableTO(string order);
	void InsertTableValue(string order);
	void PriAllTABLEList();
	void DropTable(string order);
	void DropWhere(string order);
	void DropAllRow(string order);
	void UpdateSet(string order);
	void UpdateSetWhere(string order);
	void SelectFrom(string order);
	void SelectDistinct(string order);
	void SelectFromOrder(string order);
	void SelectFromWhere(string order);
	void SelectAll(string order);
	void HistorySearch(string order);
	void TestHis();
	void RefreshFile();
	void InitNameFile();
	void WriteToAllFile();
	void SelectWhereToFile(string order);
	void OneSelectFromOrder(string order);
	int FindProNum(TableHead *p, string pro);
	void SelectFromOrderWhere(string order);
	string &get_historyArr_()
	{
		for (int i = 0; i < MAX_HISTORY; ++i)
		{
			if (history_[i].empty())
				return history_[i];
		}
		
		cout << "error: 历史记录库存不足, 已全部清空 !" << endl;
		for (int i = 0; i < MAX_HISTORY; ++i)
			history_[i].clear();
		return history_[0];
	}

private:
	int num_tablehead_;
	// 一个头一个表
	TableHead TableHead_[MAX_TABLE];
	CSameFunction sameFun_;
	CFile file_;
	string history_[MAX_HISTORY];
};
