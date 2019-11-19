#include "DataBase.h"

CTable::CTable()
{
	num_tablehead_ = 0;
}

// 根据TABLE名找CTable 类里面的数据(所有表格)
TableHead &CTable::FindTableHeadbyTABLEname(string taName)
{
	for (int i = 0; i < MAX_TABLE; ++i)
	{
		if (TableHead_[i]._tableName == taName)
			return TableHead_[i];
	}

	// 没有找到就返回最后一个空的
	for (int i = 0; i < MAX_TABLE; ++i)
	{
		if (TableHead_[i]._fileName.empty() && TableHead_[i]._tableName.empty())
			return TableHead_[i];
	}

	cout << "error: FindTableHeadbyTABLEname 找不到目标表格且所有表格已满, 返回第一个表格 !" << endl;

	return TableHead_[0];
}


// 根据文件名找CTable 类里面的数据(所有表格)
TableHead &CTable::FindTableHead(string fiName)
{
	for (int i = 0; i < MAX_TABLE; ++i)
	{
		if (TableHead_[i]._fileName == fiName)
			return TableHead_[i];
	}

	// 没有找到就返回最后一个空的
	for (int i = 0; i < MAX_TABLE; ++i)
	{
		if (TableHead_[i]._fileName.empty() && TableHead_[i]._tableName.empty())
			return TableHead_[i];
	}

	cout << "error: FindTableHeadbyTABLEname 找不到目标表格且所有表格已满, 返回第一个表格 !" << endl;

	return TableHead_[0];
}

void CTable::CreateTableFrom(string order)
{
	size_t TABLEpos = order.find("TABLE "), FROMpos = order.find("FROM ");
	string tableName = order.substr(TABLEpos + 6, FROMpos - 1 - TABLEpos - 6), fileName = order.substr(FROMpos + 5, order.length() - FROMpos - 5);

	// 找TABLE
	TableHead *pTa = &FindTableHeadbyTABLEname(tableName);

	if (pTa->_fileName.empty())
	{
		pTa->_fileName = fileName;
		pTa->_tableName = tableName;
		pTa->_pTable = new Table;

		file_.ReadFile(*pTa);
		++num_tablehead_;
	}
	else
		cout << "error: " << order << " TABLE 已经存在 !" << endl;
}


// 进来之前必须有 CREATE TABLE 和 TO 之前要写一个判断+识别代码的函数
void CTable::CreateTableTo(string order)
{
	string prop, tableName, fileName;
	size_t start, end, taNam, fileNa;
	Table *t_head = NULL;

	// 找属性
	start = order.find("("), end = order.find(")");
	prop = order.substr(start, end - start + 1);

	// 找TABLE名
	taNam = order.rfind(" ", start - 2);
	tableName = order.substr(taNam + 1, start - taNam - 2);

	// 找文件名
	fileNa = order.find("TO", end);
	fileName = order.substr(fileNa + 2, order.length() - fileNa);
	sameFun_.EraseSpacing(fileName);

	TableHead *newTable = &FindTableHead(fileName);
	if (!(*newTable)._fileName.empty())
	{
		cout << "error: function CREATE TABLE TO 文件名已存在 !" << endl;
		return;
	}
	
	if ((*newTable)._pTable != NULL)
	{
		cout << "error: function CREATE TABLE TO 表格已存在 !" << endl;
		return;
	}
	else
	{
		(*newTable)._pTable = new Table;
		this->num_tablehead_++;
	}

	(*newTable)._fileName = fileName;
	(*newTable)._tableName = tableName;
	// 建立表格链表
	sameFun_.ReadOrderData(prop, (*newTable)._pTable->_property, (*newTable)._pTable->_num_property);

#if LIN == 1
	string newFile;
	newFile += fileName;
	FILE *f;
	errno_t err1;
	err1 = fopen_s(&f, newFile.c_str(), "w");
	if (err1 != NULL)
	{
		cerr << "Can't open:" << newFile << endl;
		exit(-1);
	}
#endif


#if LIN == 0

	string newFile;
	newFile += fileName;
	FILE *f;
	f = fopen(newFile.c_str(), "w");
	if (f == NULL)
	{
		cerr << "Can't open:" << newFile << endl;
		return;
	}
#endif

	TableHead pri = FindTableHeadbyTABLEname(tableName);
	for (int i_pro = 0; !pri._pTable->_property[i_pro].empty(); ++i_pro)
	{
		if (pri._pTable->_property[i_pro + 1].empty())
			fprintf(f, "%s\n", pri._pTable->_property[i_pro].c_str());
		else
			fprintf(f, "%s ", pri._pTable->_property[i_pro].c_str());
	}
	fclose(f);

	file_.CreateToNameFile(tableName, fileName); // 写入数据库文件
}

void CTable::InsertTableValue(string order)
{
	size_t VALUEpos = order.find("VALUES "), LBracketpos1 = order.find_first_of("("), RBracketpos1 = order.find_first_of(")"), LBracketpos2 = order.find_last_of("("), RBracketpos2 = order.find_last_of(")");
	string TABLEname = order.substr(12, LBracketpos1 - 12 - 1), insData = order.substr(LBracketpos2, RBracketpos2 + 1 - LBracketpos2);
	int i_TABLEna = 0;
	for (; i_TABLEna < MAX_TABLE; ++i_TABLEna)
	{
		if (TableHead_[i_TABLEna]._tableName == TABLEname)
			break;
	}
	if (TableHead_[i_TABLEna]._pTable != NULL)
	{
		size_t test = order.find(",", LBracketpos1 + 1);
		string firPro = order.substr(LBracketpos1 + 1,order.find(",", LBracketpos1 + 1) - LBracketpos1 - 1);
		sameFun_.EraseSpacing(firPro);
		int i_pro = 0;
		for (; !TableHead_[i_TABLEna]._pTable->_property[i_pro].empty(); ++i_pro)
		{
			if (TableHead_[i_TABLEna]._pTable->_property[i_pro] == firPro)
			{
				sameFun_.ReadInsertData(insData, TableHead_[i_TABLEna]._pTable->_data, i_pro);
				break;
			}
		}
	}
	else
		cout << "error: function INSERT INTO (2) TABLE不存在 !" << endl;
}



void CTable::InsertTableTO(string order)
{
	size_t VALUEpos = order.find("VALUES "), LBracketpos = order.find("("), RBracketpos = order.find(")");
	string TABLEname = order.substr(12, VALUEpos - 12 - 1), ProAll = order.substr(LBracketpos, RBracketpos + 1 - LBracketpos);
	int i_TABLEna = 0;
	for (; TableHead_[i_TABLEna]._pTable != NULL; ++i_TABLEna)
	{
		if (TableHead_[i_TABLEna]._tableName == TABLEname)
			break;
	}
	if (TableHead_[i_TABLEna]._pTable != NULL)
		sameFun_.ReadInsertData(ProAll, TableHead_[i_TABLEna]._pTable->_data);
	else
		cout << "error: function INSERT INTO (1) TABLE不存在 !" << endl;
}

void CTable::PriAllTABLEList()
{
	cout << "  total:" << num_tablehead_ << endl;
	for (int i_table = 0; i_table < MAX_TABLE; ++i_table)
	{
		if (TableHead_[i_table]._pTable == NULL)
			continue;

		int row = 0;
		cout << "    " << TableHead_[i_table]._tableName << ": (" << TableHead_[i_table]._pTable->_num_property << ", ";

		// 算列数
		for (; !TableHead_[i_table]._pTable->_data[row][0].empty(); ++row);
		cout << row << ") [";

		cout << TableHead_[i_table]._pTable->_property[0];
		for (int priPro = 1; priPro < TableHead_[i_table]._pTable->_num_property; ++priPro)
			cout << "," << TableHead_[i_table]._pTable->_property[priPro];
		cout << "]" << endl;
	}

}

void CTable::DropTable(string order)
{
	string dropName = order.substr(11, order.length() - 11);
	int i_drop = 0;
	for (; i_drop < MAX_TABLE && TableHead_[i_drop]._tableName != dropName; ++i_drop);
	
	if (i_drop != MAX_TABLE)
	{
		TableHead_[i_drop]._tableName.clear();
		TableHead_[i_drop]._fileName.clear();
		this->sameFun_.DeleteTableHead(TableHead_[i_drop]._pTable);
		--num_tablehead_;
	}
	RefreshFile();
}

// 空的返回 true
bool isArrOneDimen(string *p, int n)
{
	if (p == NULL)
		return true;

	for (int i = 0; i < n; ++i)
	{
		if (!p[i].empty())
			return false;
	}
	return true;
}

// 亮点: 对各种有缺省值的数据也可以处理
void MoveArrTwoDimen(string **arr, int i_row)
{
	while (isArrOneDimen(arr[i_row + 1], MAX_PROPERTY) != true)
	{
		for (int i_line = 0; i_line < MAX_PROPERTY; ++i_line)
			arr[i_row][i_line] = arr[i_row + 1][i_line];
		++i_row;
	}
	for (int i = 0; i < MAX_PROPERTY; ++i)
		arr[i_row][i].clear();
}

void CTable::DropAllRow(string order)
{
	size_t FROMpos = order.find("FROM ");
	string tableName = order.substr(FROMpos + 5, order.length() - FROMpos - 5);
	for (int i_findTable = 0; !TableHead_[i_findTable]._tableName.empty(); ++i_findTable)
	{
		if (TableHead_[i_findTable]._tableName == tableName)
		{
			for (int i_row = 0; isArrOneDimen(TableHead_[i_findTable]._pTable->_data[i_row], MAX_PROPERTY) == false; ++i_row)
			{
				for (int i_line = 0; i_line < MAX_PROPERTY; ++i_line)
					TableHead_[i_findTable]._pTable->_data[i_row][i_line].clear();
			}
		}
	}
}

void CTable::DropWhere(string order)
{
	size_t FROMpos = order.find("FROM "), WHEREpos = order.find("WHERE "), EQUALpos = order.find("=");
	string tableName = order.substr(FROMpos + 5, WHEREpos - 1 - FROMpos - 5), findPro = order.substr(WHEREpos + 6, EQUALpos - 1 - WHEREpos - 6), findData = order.substr(EQUALpos + 2, order.length() - EQUALpos - 2);
	int i_findTable = 0;
	for (; !TableHead_[i_findTable]._tableName.empty(); ++i_findTable)
	{
		if (TableHead_[i_findTable]._tableName == tableName)
		{
			bool isHave = false;
			for (int i = 0; i < MAX_PROPERTY; ++i)
			{
				if (!TableHead_[i_findTable]._pTable->_data[0][i].empty())
				{
					isHave = true;
					break;
				}
			}
			if (isHave == false)
			{
				cout << "error: Drop Where 当前TABLE为空 !" << endl;
				return;
			}

			int i_pro = 0;
			while (i_pro < MAX_PROPERTY && TableHead_[i_findTable]._pTable->_property[i_pro] != findPro)
				++i_pro;
			if (i_pro == MAX_PROPERTY)
			{
				cout << "error: Drop Where 找不到命令中的属性 !" << endl;
				return;
			}
			for (int i_delRow = 0; i_delRow < MAX_DATA; ++i_delRow)
			{
				if (TableHead_[i_findTable]._pTable->_data[i_delRow][i_pro] == findData)
				{
					string *p[MAX_DATA] = { NULL };
					for (int i_arr = 0; isArrOneDimen(TableHead_[i_findTable]._pTable->_data[i_arr], MAX_PROPERTY) == false; ++i_arr)
						p[i_arr] = TableHead_[i_findTable]._pTable->_data[i_arr];
					MoveArrTwoDimen(p, i_delRow);
				}
			}
		}
	}
	if (!TableHead_[i_findTable]._tableName.empty())
		cout << "error: Drop Where 找不到这个TABLE !" << endl;
}

void CTable::UpdateSet(string order)
{
	size_t UPDATEpos = order.find("UPDATE "), SETpos = order.find("SET ");
	string tableNa = order.substr(UPDATEpos + 7, SETpos - 1 - UPDATEpos - 7);
	TableHead *pTa = &FindTableHeadbyTABLEname(tableNa);

	size_t i_deal = SETpos;
	while (i_deal != order.length())
	{
		size_t nextPunc = order.find(',', i_deal + 1);
		if (nextPunc == string::npos)
			nextPunc = order.length();

		string equalAll, pro, data;
		if (i_deal == SETpos)
		{
			equalAll = order.substr(SETpos + 4, nextPunc - SETpos - 4);
			size_t equalPunc = equalAll.find("= ");
			pro = equalAll.substr(0, equalPunc - 1);
			data = equalAll.substr(equalPunc + 2, nextPunc - equalPunc - 2);
		}

		else
		{
			equalAll = order.substr(i_deal + 2, nextPunc - i_deal - 2);
			size_t equalPunc = equalAll.find("= ");
			pro = equalAll.substr(0, equalPunc - 1);
			data = equalAll.substr(equalPunc + 2, nextPunc - equalPunc - 2);
		}

		i_deal = nextPunc;

		// 更新数据
		for (int i = 0; !pTa->_pTable->_property[i].empty(); ++i)
		{
			if (pTa->_pTable->_property[i] == pro)
			{
				for (int k = 0; isArrOneDimen(pTa->_pTable->_data[k], pTa->_pTable->_num_property) != true; ++k)
				{
					pTa->_pTable->_data[k][i] = data;
				}
			}
		}
	}
}

// UPDATE student SET 学号 = value1, 年级 = value2
// UPDATE student SET 姓名 = hahaha, 年级 = 99 WHERE 学号 = 221dsfsfsdfsfsf626
void CTable::UpdateSetWhere(string order)
{
	size_t UPDATEpos = order.find("UPDATE "), SETpos = order.find("SET "), WHEREpos = order.find("WHERE ");
	string tableNa = order.substr(UPDATEpos + 7, SETpos - 1 - UPDATEpos - 7);
	TableHead *pTa = &FindTableHeadbyTABLEname(tableNa);

	size_t desEqual = order.find("=", WHEREpos + 1);
	string desPro = order.substr(WHEREpos + 6, desEqual - 1 - WHEREpos - 6), desData = order.substr(desEqual + 2, order.length() - desEqual - 2);
	int desRow[MAX_DATA] = { 0 }, i_desRow = 0;
	for (int i = 0; i < MAX_DATA; ++i)
		desRow[i] = -1;

	for (int i = 0; !pTa->_pTable->_property[i].empty(); ++i)
	{
		if (pTa->_pTable->_property[i] == desPro)
		{
			for (int k = 0; k < MAX_DATA; ++k)
			{
				if (pTa->_pTable->_data[k][i] == desData)
					desRow[i_desRow++] = k;
			}
		}
	}
	if (desRow[0] == -1)
	{
		cout << "error: " << order << " 条件不能成立 !" << endl;
		return;
	}

	size_t i_deal = SETpos;
	while (i_deal != WHEREpos - 1)
	{
		size_t nextPunc = order.find(',', i_deal + 1);
		if (nextPunc == string::npos)
			nextPunc = WHEREpos - 1;

		string equalAll, pro, data;
		if (i_deal == SETpos)
		{
			equalAll = order.substr(SETpos + 4, nextPunc - SETpos - 4);
			size_t equalPunc = equalAll.find("= ");
			pro = equalAll.substr(0, equalPunc - 1);
			data = equalAll.substr(equalPunc + 2, nextPunc - equalPunc - 2);
		}

		else
		{
			equalAll = order.substr(i_deal + 2, nextPunc - i_deal - 2);
			size_t equalPunc = equalAll.find("= ");
			pro = equalAll.substr(0, equalPunc - 1);
			data = equalAll.substr(equalPunc + 2, nextPunc - equalPunc - 2);
		}

		i_deal = nextPunc;

		// 更新数据
		for (int i = 0; !pTa->_pTable->_property[i].empty(); ++i)
		{
			if (pTa->_pTable->_property[i] == pro)
			{
				for (int k = 0; desRow[k] != -1; ++k)
					pTa->_pTable->_data[desRow[k]][i] = data;
			}
		}
	}
}


void CTable::SelectFrom(string order)
{
	size_t FROMpos = order.find("FROM "), SELECTpos = order.find("SELECT "), prePos;
	string tableNa = order.substr(FROMpos + 5, order.length() - FROMpos - 5);
	TableHead pri = FindTableHeadbyTABLEname(tableNa);

	// 读取条件: 哪一列要展示
	prePos = SELECTpos + 7;
	int outPro[MAX_PROPERTY] = { 0 }, i_outPro = 0;
	for (int i = 0; i < MAX_PROPERTY; ++i)
		outPro[i] = -1;

	while (prePos != FROMpos)
	{
		size_t nextPunc = order.find(',', prePos + 1);
		string show;
		if (nextPunc == string::npos)
			nextPunc = FROMpos - 1;

		show = order.substr(prePos, nextPunc - prePos);
		prePos = nextPunc + 1;

		for (int i = 0; !pri._pTable->_property[i].empty(); ++i)
		{
			if (pri._pTable->_property[i] == show)
				outPro[i_outPro++] = i;
		}
	}
	if (outPro[0] == -1)
	{
		cout << "error: " << order << " 找不到要展示的条件属性 !" << endl;
		return;
	}
	
	// 开始输出
	sameFun_.CountAllSetw(&pri);
	if (pri._pTable == NULL)
	{
		cout << "error: PrintTable(const TableHead pri) 当前TABLE为空 !" << endl;
		return;
	}
	int priID = -1;
	bool isFirst = true, isEnd = false;



	////// 以下是一行一行输出
	// ID 的边框
	cout << "+----+";
	// 属性的边框
	for (int i = 0; outPro[i] != -1; ++i)
	{
		cout.fill('-');
		cout << setw(pri._pTable->_setwPro[outPro[i]]) << "-";
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
			for (int i = 0; outPro[i] != -1; ++i)
				cout << setw(pri._pTable->_setwPro[outPro[i]]) << pri._pTable->_property[outPro[i]] << '|';
			cout << endl;
		}
		else
		{
			cout << "| " << setw(2) << priID + 1 << " |";
			for (int i = 0; outPro[i] != -1; ++i)
				cout << setw(pri._pTable->_setwPro[outPro[i]]) << pri._pTable->_data[priID][outPro[i]] << '|';
			cout << endl;
		}

		// ID 的边框
		cout << "+----+";
		// 属性的边框
		for (int i = 0; outPro[i] != -1; ++i)
		{
			cout.fill('-');
			cout << setw(pri._pTable->_setwPro[outPro[i]]) << "-";
			cout << "+";
		}
		cout << endl;
		cout.fill(' ');

		++priID;

		isEnd = true;
		for (int i = 0; outPro[i] != -1; ++i)
		{
			if (!pri._pTable->_data[priID][outPro[i]].empty())
			{
				isEnd = false;
				break;
			}
		}
	}
}

void CTable::SelectDistinct(string order)
{
	int i_pri = 0;   // 要输出的那一列
	bool isFirstIn = true;
	size_t DISTINCTpos = order.find("DISTINCT "), FROMpos = order.find("FROM "), nextPos = 0;
	string tableNa = order.substr(FROMpos + 5, order.length() - FROMpos - 5), pro;

	TableHead pri = FindTableHeadbyTABLEname(tableNa);

	while (nextPos != FROMpos - 1)
	{
		i_pri = 0;
		if (isFirstIn == true)
		{
			isFirstIn = false;
			nextPos = order.find(",", DISTINCTpos);
			if (nextPos == string::npos)
				nextPos = FROMpos - 1;
			pro = order.substr(DISTINCTpos + 9, nextPos - DISTINCTpos - 9);
		}
		else
		{
			DISTINCTpos = nextPos + 1;
			nextPos = order.find(",", DISTINCTpos);
			if (nextPos == string::npos)
				nextPos = FROMpos - 1;
			pro = order.substr(DISTINCTpos, nextPos - DISTINCTpos);
		}


		// 找到输出的那个属性
		for (; !pri._pTable->_property[i_pri].empty() && pri._pTable->_property[i_pri] != pro; ++i_pri);

		int dataOut[MAX_DATA] = { 0 }, i_dataOut = 0;
		for (int i = 0; i < MAX_DATA; ++i)
			dataOut[i] = -1;

		string cmp[MAX_DATA];
		int i_cmp = 0;
		for (int i = 0; isArrOneDimen(&pri._pTable->_data[i][0], MAX_DATA) != true; ++i)
		{
			bool isHave = false;
			if (i_cmp == 0)
			{
				cmp[i_cmp++] = pri._pTable->_data[i][i_pri];
				dataOut[i_dataOut++] = i;
				continue;
			}
			for (int k = 0; !cmp[k].empty(); ++k)
			{
				if (cmp[k] == pri._pTable->_data[i][i_pri])
				{
					isHave = true;
					break;
				}
			}
			if (isHave == false)
			{
				cmp[i_cmp++] = pri._pTable->_data[i][i_pri];
				dataOut[i_dataOut++] = i;
			}
		}
		// 开始输出
		sameFun_.CountAllSetw(&pri);
		if (pri._pTable == NULL)
		{
			cout << "error: PrintTable(const TableHead pri) 当前TABLE为空 !" << endl;
			return;
		}
		int priID = -1, i_priLine = -1;
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
					cout << setw(pri._pTable->_setwPro[i]) << pri._pTable->_data[dataOut[i_priLine]][i] << '|';
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
			++i_priLine;

			isEnd = true;
			if (dataOut[i_priLine] != -1)
				isEnd = false;
		}
	}
}

maxflag cmpAscend(const char *a, const char *b)
{
	int i = 0;
	for (; a[i] != '\0' && b[i] != '\0'; ++i)
	{
		if (a[i] > b[i])
			return AMAX;
		else if (b[i] > a[i])
			return BMAX;
	}
	if (a[i] != '\0')
		return AMAX;
	else if (b[i] != '\0')
		return BMAX;

	return EQUAL;
}

maxflag cmpDescend(const char *a, const char *b)
{
	int i = 0;
	for (; a[i] != '\0' && b[i] != '\0'; ++i)
	{
		if (a[i] > b[i])
			return BMAX;
		else if (b[i] > a[i])
			return AMAX;
	}
	if (a[i] != '\0')
		return BMAX;
	else if (b[i] != '\0')
		return AMAX;

	return EQUAL;
}

maxflag cmpDescend(string data[][MAX_PROPERTY], int a, int b, int find[])
{
	for (int i = 0; find[i] != -1; ++i)
	{
		if (data[a][find[i]].compare(data[b][find[i]]) < 0)
			return AMAX;
		else if (data[a][find[i]].compare(data[b][find[i]]) > 0)
			return BMAX;
	}

	return EQUAL;

}

maxflag cmpAscend(string data[][MAX_PROPERTY], int a, int b, int find[])
{
	if (a == b)
		return EQUAL;

	for (int i = 0; find[i] != -1; ++i)
	{
		if (data[a][find[i]].compare(data[b][find[i]]) < 0)
			return BMAX;
		else if (data[a][find[i]].compare(data[b][find[i]]) > 0)
			return AMAX;
	}

	return EQUAL;

}


// SELECT * FROM student ORDER BY 学号 DESC
void CTable::OneSelectFromOrder(string order)
{
	int numData = 0;
	bool isFirstIn = true;
	maxflag isASC = BMAX;
	maxflag (*pCmp)(const char *a, const char *b) = NULL;
	size_t DESCpos = order.find("DESC"), ASCpos = order.find("ASC"), nextPos = 0;
	if (DESCpos != string::npos)
		pCmp = cmpDescend;
	else if (ASCpos != string::npos)
	{
		isASC = AMAX;
		pCmp = cmpAscend;
	}
	else
	{
		cout << "error: " << order << " 不能识别到排序顺序 !" << endl;
		return;
	}

	int i_pro = 0;
	size_t FROMpos = order.find("FROM "), BYpos = order.find("BY "), ORDERpos = order.find("ORDER ");
	string tableNa = order.substr(FROMpos + 5, ORDERpos - 1 - FROMpos - 5), pro;

	TableHead pri = FindTableHeadbyTABLEname(tableNa);
	for (numData = 0; isArrOneDimen(&pri._pTable->_data[numData][0], MAX_DATA) != true; ++numData);


	int dataOut[MAX_DATA] = { 0 }, i_dataOut = 0;
	for (int i = 0; i < MAX_DATA; ++i)
		dataOut[i] = -1;
	bool isUsed[MAX_DATA] = { false };

	if (isFirstIn == true)
	{
		isFirstIn = false;
		nextPos = order.find(",", BYpos);
		if (nextPos == string::npos && isASC == BMAX)
			nextPos = DESCpos - 1;
		else if (nextPos == string::npos && isASC == AMAX)
			nextPos = ASCpos - 1;

		pro = order.substr(BYpos + 3, nextPos - BYpos - 3);
	}
	else
	{
		BYpos = nextPos + 1;
		nextPos = order.find(",", BYpos);
		if (nextPos == string::npos && isASC == BMAX)
			nextPos = DESCpos - 1;
		else if (nextPos == string::npos && isASC == AMAX)
			nextPos = ASCpos - 1;
		
		pro = order.substr(BYpos, nextPos - BYpos);
	}

	for (i_pro = 0; !pri._pTable->_property[i_pro].empty(); ++i_pro)
	{
		if (pri._pTable->_property[i_pro] == pro)
			break;
	}
	if (pri._pTable->_property[i_pro].empty())
	{
		cout << "error: " << order << " 找不到属性 !" << endl;
		return;
	}
	
	for (int i = 0; i < numData; ++i)
	{
		int max = 0;
		for (max = 0; max < numData; ++max)
		{
			if (isUsed[max] == false && !pri._pTable->_data[max][i_pro].empty())
				break;
		}

		if (max == numData)
			break;

		for (int k = 1; k < numData; ++k)
		{
			if (isUsed[k] == false && !pri._pTable->_data[k][i_pro].empty()
				&& pCmp(pri._pTable->_data[k][i_pro].c_str(), pri._pTable->_data[max][i_pro].c_str()) == BMAX)
				max = k;

		}
		dataOut[i_dataOut++] = max;
		isUsed[max] = true;
	}

	for (int i = 0; i < numData; ++i)
	{
		if (pri._pTable->_data[i][i_pro].empty())
			dataOut[i_dataOut++] = i;
	}

	// 开始输出
	sameFun_.CountAllSetw(&pri);
	if (pri._pTable == NULL)
	{
		cout << "error: PrintTable(const TableHead pri) 当前TABLE为空 !" << endl;
		return;
	}
	int priID = -1, i_priLine = -1;
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
				cout << setw(pri._pTable->_setwPro[i]) << pri._pTable->_data[dataOut[i_priLine]][i] << '|';
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
		++i_priLine;

		isEnd = true;
		if (dataOut[i_priLine] != -1)
			isEnd = false;
	}
}

bool isCondiOK(Condi a[], string da[][MAX_PROPERTY], int whe)
{
	int okNum = 0, i = 0;
	for (i = 0; i < MAX_JUDGE && a[i]._pro != -1; ++i)
	{
		if (a[i]._how == EQUAL && a[i]._stanData.compare(da[whe][a[i]._pro]) == 0)
			++okNum;

		if (a[i]._stanData.compare(da[whe][a[i]._pro]) * (int)a[i]._how > 0)
			++okNum;
	}
	if (okNum == i)
		return true;

	return false;
}

int ReadWhereMax(string a, maxflag &f)
{
	if (a.find("<") != string::npos)
	{
		f = BMAX;
		return a.find("<");
	}
	if (a.find(">") != string::npos)
	{
		f = AMAX;
		return a.find(">");
	}
	if (a.find("=") != string::npos)
	{
		f = EQUAL;
		return a.find("=");
	}

	return -1;
}

int CTable::FindProNum(TableHead *p, string pro)
{
	for (int i = 0; i < MAX_PROPERTY && !p->_pTable->_property[i].empty(); ++i)
	{
		if (p->_pTable->_property[i] == pro)
			return i;
	}

	return -1;
}

// SELECT * FROM student ORDER BY Score2, Score3 ASC WHERE Score1 > 90
void CTable::SelectFromOrderWhere(string order)
{
	Condi conDi[MAX_JUDGE];
	int i_conDi = 0;
	int numData = 0;
	bool isFirstIn = true;
	maxflag isASC = BMAX;
	maxflag(*pCmp)(string data[][MAX_PROPERTY], int a, int b, int find[]) = NULL;
	size_t DESCpos = order.find("DESC"), ASCpos = order.find("ASC"), nextPos = 0, SEQUpos = 0, WHEREpos = order.find("WHERE ");

	if (DESCpos != string::npos)
	{
		SEQUpos = DESCpos;
		pCmp = cmpDescend;
	}
	else if (ASCpos != string::npos)
	{
		SEQUpos = ASCpos;
		isASC = AMAX;
		pCmp = cmpAscend;
	}
	else
	{
		cout << "error: " << order << " 不能识别到排序顺序 !" << endl;
		return;
	}


	int i_pro = 0;
	size_t FROMpos = order.find("FROM "), BYpos = order.find("BY "), ORDERpos = order.find("ORDER ");
	string tableNa = order.substr(FROMpos + 5, ORDERpos - 1 - FROMpos - 5), pro[MAX_PROPERTY];
	int arrPro = 0;

	string proArr[MAX_PROPERTY];
	int findOrd[MAX_PROPERTY] = { 0 }, i_findOrd = 0;
	for (int i = 0; i < MAX_PROPERTY; ++i)
		findOrd[i] = -1;

	sameFun_.ReadSomePro(order.substr(BYpos + 2, SEQUpos - BYpos - 2), proArr);

	TableHead pri = FindTableHeadbyTABLEname(tableNa);
	for (numData = 0; isArrOneDimen(&pri._pTable->_data[numData][0], MAX_DATA) != true; ++numData);  // 计算data行数
	
	// 找到排序的属性位置
	for (int i = 0; !proArr[i].empty(); ++i)
	{
		for (int k = 0; !pri._pTable->_property[k].empty(); ++k)
		{
			if (pri._pTable->_property[k] == proArr[i])
				findOrd[i_findOrd++] = k;
		}
	}

	// 找到不能输出的条件设置
	string how = order.substr(WHEREpos + 5, order.length() - WHEREpos - 5);
	size_t hbeg = 0, hend = 0;
	sameFun_.EraseSpacing(how);
	for (int i = 0; i < how.length(); ++i)
	{
		if (how[i + 1] == ',' || i + 1 == how.length())
		{
			hend = i + 1;
			string oneHow = how.substr(hbeg, hend - hbeg), pr, da;
			int maxPos = ReadWhereMax(oneHow, conDi[i_conDi]._how);

			if (maxPos == -1 || conDi[i_conDi]._how == BADMEAN)
			{
				cout << "error: " << order << " 识别不到条件 !" << endl;
				return;
			}

			pr = oneHow.substr(0, maxPos);
			if (FindProNum(&pri, pr) == -1)
			{
				cout << "error: " << order << " 找不到条件中的属性 !" << endl;
				return;
			}
			da = oneHow.substr(maxPos + 1, oneHow.length());
			conDi[i_conDi]._pro = FindProNum(&pri, pr);
			conDi[i_conDi]._stanData = da;
			++i_conDi;
			hbeg = hend + 1;
		}
	}

	// 排序
	int dataOut[MAX_DATA] = { 0 }, i_dataOut = 0;
	for (int i = 0; i < MAX_DATA; ++i)
		dataOut[i] = -1;
	bool isUsed[MAX_DATA] = { false };

	for (int i = 0; i < numData; ++i)
	{
		int max = 0;
		for (max = 0; max < numData; ++max)
		{
			if (isUsed[max] == false && !pri._pTable->_data[max][i_pro].empty())
				break;
		}

		if (max == numData)
			break;

		for (int k = 0; k < numData; ++k)
		{
			if (isUsed[k] == false && !pri._pTable->_data[k][i_pro].empty()
				&& pCmp(pri._pTable->_data, k, max, findOrd) == BMAX)
				max = k;
		}
		if (isCondiOK(conDi, pri._pTable->_data, max))
			dataOut[i_dataOut++] = max;
		isUsed[max] = true;
	}

	// 加入空的数据
	for (int i = 0; i < numData; ++i)
	{
		if (pri._pTable->_data[i][i_pro].empty())
			dataOut[i_dataOut++] = i;
	}

	
	

	// 开始输出
	sameFun_.CountAllSetw(&pri);
	if (pri._pTable == NULL)
	{
		cout << "error: PrintTable(const TableHead pri) 当前TABLE为空 !" << endl;
		return;
	}
	int priID = -1, i_priLine = -1;
	bool isFirst = true, isEnd = false;

	//// 以下是一行一行输出
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
				cout << setw(pri._pTable->_setwPro[i]) << pri._pTable->_data[dataOut[i_priLine]][i] << '|';
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
		++i_priLine;

		isEnd = true;
		if (dataOut[i_priLine] != -1)
			isEnd = false;
	}
}




//SELECT * FROM student ORDER BY Score2, Score3 ASC
void CTable::SelectFromOrder(string order)
{
	int numData = 0;
	bool isFirstIn = true;
	maxflag isASC = BMAX;
	maxflag(*pCmp)(string data[][MAX_PROPERTY], int a, int b, int find[]) = NULL;
	size_t DESCpos = order.find("DESC"), ASCpos = order.find("ASC"), nextPos = 0, SEQUpos = 0;
	if (DESCpos != string::npos)
	{
		SEQUpos = DESCpos;
		pCmp = cmpDescend;
	}
	else if (ASCpos != string::npos)
	{
		SEQUpos = ASCpos;
		isASC = AMAX;
		pCmp = cmpAscend;
	}
	else
	{
		cout << "error: " << order << " 不能识别到排序顺序 !" << endl;
		return;
	}


	int i_pro = 0;
	size_t FROMpos = order.find("FROM "), BYpos = order.find("BY "), ORDERpos = order.find("ORDER ");
	string tableNa = order.substr(FROMpos + 5, ORDERpos - 1 - FROMpos - 5), pro[MAX_PROPERTY];
	int arrPro = 0;

	string proArr[MAX_PROPERTY];
	int findOrd[MAX_PROPERTY] = { 0 }, i_findOrd = 0;
	for (int i = 0; i < MAX_PROPERTY; ++i)
		findOrd[i] = -1;

	sameFun_.ReadSomePro(order.substr(BYpos + 2, SEQUpos - BYpos - 2), proArr);

	TableHead pri = FindTableHeadbyTABLEname(tableNa);
	for (numData = 0; isArrOneDimen(&pri._pTable->_data[numData][0], MAX_DATA) != true; ++numData);  // 计算data行数
	// 找到排序的属性位置
	for (int i = 0; !proArr[i].empty(); ++i)
	{
		for (int k = 0; !pri._pTable->_property[k].empty(); ++k)
		{
			if (pri._pTable->_property[k] == proArr[i])
				findOrd[i_findOrd++] = k;
		}
	}

	int dataOut[MAX_DATA] = { 0 }, i_dataOut = 0;
	for (int i = 0; i < MAX_DATA; ++i)
		dataOut[i] = -1;
	bool isUsed[MAX_DATA] = { false };

	// 排序
	for (int i = 0; i < numData; ++i)
	{
		int max = 0;
		for (max = 0; max < numData; ++max)
		{
			if (isUsed[max] == false && !pri._pTable->_data[max][i_pro].empty())
				break;
		}

		if (max == numData)
			break;

		for (int k = 0; k < numData; ++k)
		{
			if (isUsed[k] == false && !pri._pTable->_data[k][i_pro].empty()
				&& pCmp(pri._pTable->_data, k, max, findOrd) == BMAX)
				max = k;
		}
		dataOut[i_dataOut++] = max;
		isUsed[max] = true;
	}

	for (int i = 0; i < numData; ++i)
	{
		if (pri._pTable->_data[i][i_pro].empty())
			dataOut[i_dataOut++] = i;
	}

	// 开始输出
	sameFun_.CountAllSetw(&pri);
	if (pri._pTable == NULL)
	{
		cout << "error: PrintTable(const TableHead pri) 当前TABLE为空 !" << endl;
		return;
	}
	int priID = -1, i_priLine = -1;
	bool isFirst = true, isEnd = false;

	//// 以下是一行一行输出
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
				cout << setw(pri._pTable->_setwPro[i]) << pri._pTable->_data[dataOut[i_priLine]][i] << '|';
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
		++i_priLine;

		isEnd = true;
		if (dataOut[i_priLine] != -1)
			isEnd = false;
	}
}

// SELECT * FROM student WHERE 姓名 = 12346
void CTable::SelectFromWhere(string order)
{
	size_t FROMpos = order.find("FROM "), WHEREpos = order.find("WHERE "), EQUALpos = order.find("= ");
	string tableNa = order.substr(FROMpos + 5, WHEREpos - 1 - FROMpos - 5), pro = order.substr(WHEREpos + 6, EQUALpos - 1 - WHEREpos - 6), data = order.substr(EQUALpos + 2, order.length() - EQUALpos - 2);
	TableHead pri = FindTableHeadbyTABLEname(tableNa);

	int i_pri = 0, dataOut[MAX_DATA] = { 0 }, i_dataOut = 0, numData = 0;
	for (numData = 0; isArrOneDimen(&pri._pTable->_data[numData][0], MAX_DATA) != true; ++numData);
	for (int i = 0; i < MAX_DATA; ++i)
		dataOut[i] = -1;

	for (i_pri = 0; !pri._pTable->_property[i_pri].empty(); ++i_pri)
	{
		if (pri._pTable->_property[i_pri] == pro)
		{
			for (int i = 0; i < numData; ++i)
			{
				if (pri._pTable->_data[i][i_pri] == data)
					dataOut[i_dataOut++] = i;
			}
			break;
		}
	}

	// 开始输出
	sameFun_.CountAllSetw(&pri);
	if (pri._pTable == NULL)
	{
		cout << "error: PrintTable(const TableHead pri) 当前TABLE为空 !" << endl;
		return;
	}
	int priID = -1, i_priLine = -1;
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
				cout << setw(pri._pTable->_setwPro[i]) << pri._pTable->_data[dataOut[i_priLine]][i] << '|';
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
		++i_priLine;

		isEnd = true;
		if (dataOut[i_priLine] != -1)
			isEnd = false;
	}
}

// a中有没有出现b
bool cmpString(string a, string b)
{
	size_t bLen = b.length(), aLen = a.length();
	if (aLen < bLen)
		return false;
	if (aLen < bLen)
		return false;

	for (size_t i = 0; i < aLen - bLen + 1; ++i)
	{
		if (a.compare(i, bLen, b) == 0)
			return true;
	}
	return false;
}

void CTable::TestHis()
{
	this->history_[0] = "我知道我是一个";
	history_[1] = "这是一个故事";
	history_[2] = "故事就是这一个";
}

// VIEW HISTORY WHERE LIKE
void CTable::HistorySearch(string order)
{
	size_t LIKEpos = order.find("LIKE");
	size_t nextPos = 0;
	string key;
	bool isFir = true;

	while (nextPos != order.length())
	{
		nextPos = order.find(",", LIKEpos);
		if (nextPos == string::npos)
			nextPos = order.length();
		
		if (isFir == true)
		{
			isFir = false;
			key = order.substr(LIKEpos + 5, nextPos - LIKEpos - 5);
		}
		else
			key = order.substr(LIKEpos, nextPos - LIKEpos);

		for (int i = 0; !history_[i].empty(); ++i)
		{
			if (cmpString(history_[i], key) == true)
				cout << "\"" << history_[i] << "\"" << endl;
		}
		cout << endl;
		LIKEpos = nextPos + 1;
	}
}

void CTable::RefreshFile()
{
	string openFile;
	openFile += _NameFile_;


#if LIN == 1
	FILE *pf;
	errno_t err;
	err = fopen_s(&pf, openFile.c_str(), "w");
	if (err != NULL)
	{
		cerr << "Can't open:" << openFile << endl;
		exit(-1);
	}
#endif

#if LIN == 0
	FILE *pf;
	pf = fopen(openFile.c_str(), "w");
	if (pf == NULL)
	{
		cerr << "Can't open:" << openFile << endl;
		return;
	}
#endif


	for (int fpri = 0; fpri < MAX_TABLE; ++fpri)
	{
		if (TableHead_[fpri]._tableName.empty() || TableHead_[fpri]._fileName.empty())
			continue;
		fprintf(pf, "%s\t%s\n", TableHead_[fpri]._tableName.c_str(), TableHead_[fpri]._fileName.c_str());
	}

	fclose(pf);
}

/*void CTable::InitNameFile()
{
	string openFile;
	openFile += _NameFile_;

	if ((_access(openFile.c_str(), 0)) != -1)
	{
#if LIN == 1
		FILE *pf;
		errno_t err;
		err = fopen_s(&pf, openFile.c_str(), "r");
		if (err != NULL)
		{
			cerr << "Can't open:" << openFile << endl;
			exit(-1);
		}
#endif

#if LIN == 0
		FILE *pf;
		pf = fopen(openFile.c_str(), "r");
		if (pf == NULL)
		{
			cerr << "Can't open:" << openFile << endl;
			return;
		}
#endif


		char arrNameData[MAX_LINE] = "";
		fgets(arrNameData, MAX_LINE, pf);
		while (!feof(pf))
		{
			string temp, tabNa;
			bool isTaNa = true;
			for (int i = 0; i < MAX_LINE; ++i)
			{
				temp += arrNameData[i];
				if (arrNameData[i + 1] == '\t' || arrNameData[i + 1] == '\n')
				{
					if (isTaNa == true)
					{
						isTaNa = false;
						FindTableHeadbyTABLEname(temp)._tableName = temp;
						tabNa = temp;
					}
					else
						FindTableHeadbyTABLEname(tabNa)._fileName = temp;

					if (arrNameData[i + 1] == '\n')
						break;
					++i;
				}
			}
			fgets(arrNameData, MAX_LINE, pf);
		}
		fclose(pf);
	}
	else
		//cout << "error: InitNameFile 找不到初始化文件, 将建立一个空的文件 !" << endl;
		RefreshFile();
}*/

void CTable::WriteToAllFile()
{
	/*for (int i = 0; i < MAX_TABLE; ++i)
	{
		if (TableHead_[i]._fileName.empty() || TableHead_[i]._tableName.empty())
			continue;

		string openFile;
		//openFile += TableHead_[i]._fileName;   ////// 确定要更新全部的时候解除这个注释 !!!!!!!


#if LIN == 1
		FILE *pf;
		errno_t err;
		err = fopen_s(&pf, openFile.c_str(), "w");
		if (err != NULL)
		{
			cerr << "Can't open:" << openFile << endl;
			exit(-1);
		}
#endif

#if LIN == 0
		FILE *pf;
		pf = fopen(openFile.c_str(), "w");
		if (pf == NULL)
		{
			cerr << "Can't open:" << openFile << endl;
			return;
		}
#endif

		if (TableHead_[i]._pTable != NULL)
		{
			for (int i_pro = 0; !TableHead_[i]._pTable->_property[i_pro].empty(); ++i_pro)
			{
				if (TableHead_[i]._pTable->_property[i_pro + 1].empty())
					fprintf(pf, "%s\n", TableHead_[i]._pTable->_property[i_pro].c_str());
				else
					fprintf(pf, "%s ", TableHead_[i]._pTable->_property[i_pro].c_str());
			}

			for (int row_data = 0; isArrOneDimen(TableHead_[i]._pTable->_data[row_data], MAX_PROPERTY) != true; ++row_data)
			{
				for (int line_data = 0; line_data < MAX_PROPERTY; ++line_data)
				{
					if (line_data + 1 == MAX_PROPERTY)
						fprintf(pf, "%s\n", TableHead_[i]._pTable->_data[row_data][line_data].c_str());
					else
						fprintf(pf, "%s ", TableHead_[i]._pTable->_data[row_data][line_data].c_str());
				}
			}
		}

		fclose(pf);
	}*/
}

// SELECT * FROM student WHERE Score1 = 90 TO 计算机系学生名单.txt
void CTable::SelectWhereToFile(string order)
{
	size_t FROMpos = order.find("FROM "), WHEREpos = order.find("WHERE "), TOpos = order.find("TO "), EQUpos = order.find("=");
	string taNa = order.substr(FROMpos + 5, WHEREpos - 1 - FROMpos - 5), fiNa = order.substr(TOpos + 3, order.length() - TOpos - 3);
	string pro = order.substr(WHEREpos + 6, EQUpos - 1 - WHEREpos - 6), data = order.substr(EQUpos + 2, TOpos - 1 - EQUpos - 2);
	int numPro = 0;
	
	string openFile;
	openFile += fiNa;
	//openFile += TableHead_[i]._fileName;


#if LIN == 1
	FILE *pf;
	errno_t err;
	err = fopen_s(&pf, openFile.c_str(), "a");
	if (err != NULL)
	{
		cerr << "Can't open:" << openFile << endl;
		exit(-1);
	}
#endif

#if LIN == 0
	FILE *pf;
	pf = fopen(openFile.c_str(), "a");
	if (pf == NULL)
	{
		cerr << "Can't open:" << openFile << endl;
		return;
	}
#endif


	TableHead pri = FindTableHeadbyTABLEname(taNa);
	for (numPro = 0; numPro < MAX_PROPERTY; ++numPro)
	{
		if (pri._pTable->_property[numPro] == pro)
			break;
	}
	if (numPro == MAX_PROPERTY)
	{
		cout << "error: " << order << " 找不到属性 !" << endl;
		return;
	}	
	
	if (!pri._fileName.empty() && !pri._tableName.empty())
	{
		// 写属性
		for (int i_pro = 0; !pri._pTable->_property[i_pro].empty(); ++i_pro)
		{
			if (pri._pTable->_property[i_pro + 1].empty())
				fprintf(pf, "%s\n", pri._pTable->_property[i_pro].c_str());
			else
				fprintf(pf, "%s ", pri._pTable->_property[i_pro].c_str());
		}

		for (int row_data = 0; isArrOneDimen(pri._pTable->_data[row_data], MAX_PROPERTY) != true; ++row_data)
		{
			if (pri._pTable->_data[row_data][numPro].compare(data) == 0)
			{
				// 写入一行的
				for (int line_data = 0; line_data < MAX_PROPERTY; ++line_data)
				{
					if (line_data + 1 == MAX_PROPERTY)
						fprintf(pf, "%s\n", pri._pTable->_data[row_data][line_data].c_str());
					else
						fprintf(pf, "%s ", pri._pTable->_data[row_data][line_data].c_str());
				}
			}
		}
	}
	fclose(pf);	
}

void CTable::SelectAll(string order)
{
	size_t FROMpos = order.find("FROM ");
	string taNa = order.substr(FROMpos + 5, order.length() - FROMpos - 5);
	TableHead pri = FindTableHeadbyTABLEname(taNa);
	sameFun_.PrintTable(pri);
}

