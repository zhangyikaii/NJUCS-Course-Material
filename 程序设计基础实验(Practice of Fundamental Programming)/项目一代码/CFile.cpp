#include "Shopping.h"
int CFile::ReadCommodity(char(&comm_arr)[FILE_WORDS][FILE_WORDS], char *fileName)
{
	FILE *pf;
	errno_t err;
	err = fopen_s(&pf, fileName, "r");
	if (err != NULL)
	{
		cerr << "Can't open:" << fileName << endl;
		exit(-1);
	}


	int i_re = 0;

	while (!feof(pf))
	{
		fgets(comm_arr[i_re++], sizeof(comm_arr[0]), pf);
		comm_arr[i_re][0] = '\0';
	}

	fclose(pf);

	return i_re;
}

// return -1 没有找到   >= 0表示找到了的编号
int CFile::FindName(char *name, char *file)
{
	int whonum = 0;
	FILE *pf;
	errno_t err;
	err = fopen_s(&pf, file, "r");
	if (err != NULL)
	{
		cerr << "Can't open:" << file << endl;
		exit(-1);
	}

	while (!feof(pf))
	{
		++whonum;
		char realNamPas[NAME_WORDS];
		fgets(realNamPas, NAME_WORDS, pf);
		SetSpacing(realNamPas, NAME_WORDS);
		if (strcmp(realNamPas, name) == 0)
		{
			fclose(pf);
			return whonum;
		}
	}

	fclose(pf);
	return -1;
}

void CFile::SetSpacing(char *arr, int num)
{
	for (int i = 0; i < num; ++i)
	{
		if (arr[i] == ' ' || arr[i] == '\t' || arr[i] == '\n')
			arr[i] = '\0';
	}
}
