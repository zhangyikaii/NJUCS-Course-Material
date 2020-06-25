#include "DataBase.h"

void CFile::ReadFile(TableHead &table)
{
	string openFile;
	openFile += table._fileName;

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


	// 读属性
	char proChar[MAX_LINE] = "", onePro[MAX_LINE] = "";
	int i_onePro = 0, i_realPro = 0;
	fgets(proChar, MAX_LINE, pf);
	for (int i_pro = 0; proChar[i_pro] != '\0'; ++i_pro)
	{
		onePro[i_onePro++] = proChar[i_pro];
		if (proChar[i_pro + 1] == ' ' || proChar[i_pro + 1] == '\0' || proChar[i_pro + 1] == '\n' || proChar[i_pro + 1] == '\t')
		{
			table._pTable->_property[i_realPro++] = onePro;
			for (int i = 0; i < MAX_LINE; ++i)
				onePro[i] = '\0';
			i_onePro = 0;
			++table._pTable->_num_property;
			if (proChar[i_pro + 1] != '\0')
				++i_pro;
		}
	}

	// 读data
	for (int num_realData = 0; !feof(pf); ++num_realData)
	{
		char dataChar[MAX_LINE] = "", oneData[MAX_LINE] = "";
		int i_oneData = 0, i_realData = 0;
		fgets(dataChar, MAX_LINE, pf);
		for (int i_data = 0; dataChar[i_data] != '\0'; ++i_data)
		{
			oneData[i_oneData++] = dataChar[i_data];
			if (dataChar[i_data + 1] == ' ' || dataChar[i_data + 1] == '\0' || dataChar[i_data + 1] == '\n' || dataChar[i_data + 1] == '\t')
			{
				if (oneData[0] != ' ' && oneData[0] != '\n')
					table._pTable->_data[num_realData][i_realData++] = oneData;
				for (int i = 0; i < MAX_LINE; ++i)
					oneData[i] = '\0';
				i_oneData = 0;
				if (dataChar[i_data + 1] != '\0')
					++i_data;
			}
		}
	}
	fclose(pf);
}

void CFile::CreateToNameFile(string taNa, string Fina)
{
	string openFile, newFile;
	openFile += _NameFile_;
	newFile += Fina;


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
	FILE *f;
	pf = fopen(newFile.c_str(), "w");
	if (f == NULL)
	{
		cerr << "Can't open:" << newFile << endl;
		return;
	}
#endif


	fprintf(pf, "%s\t%s\n", taNa.c_str(), Fina.c_str());
	
	fclose(pf);
}
