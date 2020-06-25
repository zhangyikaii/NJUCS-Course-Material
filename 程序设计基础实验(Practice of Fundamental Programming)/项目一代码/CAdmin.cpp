#include "Shopping.h"
void CAdmin::AddtoCartOrComm(Commodity *pAdd, int who)
{
	Commodity *padd = 0;
	char addID[NAME_WORDS] = "";
	int addid = 0;
	string addName, addBrand;
	double addPrice = 0;
	int addNum = 0;

	cout << "请输入需要加入的商品编号(输入 * 退出):";
	cin >> addID;
	if (addID[0] == '*')
		return;


	for (int i = 1; addID[i] != '\0'; ++i)
		addid = addid * 10 + addID[i] - '0';

	padd = CInterface::UserFindCommdity(pAdd, addid);

	if (padd == NULL)
	{
		cout << "这个商品不在已有商品中, 请输入商品名称, 品牌, 价格, 数量(以空格隔开):";
		cin >> addName >> addBrand >> addPrice >> addNum;
		Commodity *p = new Commodity(addid, addName, addBrand, addPrice, addNum);
		if (pAdd == NULL)
			pAdd = p;
		else
		{
			Commodity *tail = pAdd;
			for (; tail->next != NULL; tail = tail->next);
			tail->next = p;
		}
		cout << "添加成功 !" << endl;
	}
	else if (padd->number >= 0)
	{
		cout << "商品已经存在, 请输入要添加的数量:";
		cin >> addNum;
		padd->number += addNum;
		cout << "添加成功 !" << endl;
	}
	else if (padd->number == -1)
	{
		bool isRestart = false;
		cout << "商品曾经被下架过, 请问要恢复它吗, 恢复请按 1 , 放弃请按 0 :";
		cin >> isRestart;
		if (isRestart == 0)
			return;
		else if (isRestart == 1)
		{
			cout << "请输入要加入的数量:";
			cin >> addNum;
			padd->number = addNum;
			cout << "添加成功 !" << endl;
		}
	}
}

void CAdmin::ChangeCommNum(Commodity *pCha)
{
	Commodity *pcha = NULL;
	char chaID[NAME_WORDS] = "";
	int chaid = 0;
	int chaPrice = 0;

	cout << "请输入需要修改数量的商品编号:";
	cin >> chaID;

	for (int i = 1; chaID[i] != '\0'; ++i)
		chaid = chaid * 10 + chaID[i] - '0';

	pcha = CInterface::UserFindCommdity(pCha, chaid);

	if (pcha == NULL)
	{
		cout << "这个商品不在已有商品中 !" << endl;
		return;
	}

	cout << "现有数量为:" << pcha->number << endl << "请输入修改后的数量:";
	cin >> chaPrice;

	while (chaPrice <= 0)
	{
		cout << "非法输入 !" << endl;
		cin >> chaPrice;
	}

	pcha->number = chaPrice;
	cout << "修改成功 !" << endl;
}

void CAdmin::ChangeCommPrice(Commodity *pCha)
{
	Commodity *pcha = NULL;
	char chaID[NAME_WORDS] = "";
	int chaid = 0;
	double chaPrice = 0;

	cout << "请输入需要修改价格的商品编号:";
	cin >> chaID;

	for (int i = 1; chaID[i] != '\0'; ++i)
		chaid = chaid * 10 + chaID[i] - '0';

	pcha = CInterface::UserFindCommdity(pCha, chaid);

	if (pcha == NULL)
	{
		cout << "这个商品不在已有商品中 !" << endl;
		return;
	}

	cout << "现有价格为:" << pcha->price << endl << "请输入修改后的价格:";
	cin >> chaPrice;

	while (chaPrice <= 0)
	{
		cout << "非法输入 !" << endl;
		cin >> chaPrice;
	}

	pcha->price = chaPrice;
	cout << "修改成功 !" << endl;
}

void CAdmin::DeleteCartOrComm(Commodity *pDel)
{
	int delSitua = 0, delid = 0;
	bool isMany = true;
	do
	{
		delid = 0;
		cout << "请输入需要删除的商品ID:";
		char delID[NAME_WORDS] = "";
		cin >> delID;

		for (int i = 1; delID[i] != '\0'; ++i)
			delid = delid * 10 + delID[i] - '0';

		Commodity *ppDel = pDel;
		for (; ppDel != NULL && ppDel->id != delid; ppDel = ppDel->next);

		if (ppDel == NULL || ppDel->number < 0)
		{
			bool isConti = false;
			cout << "您要删除的商品早就被下架啦~\n继续删除请按 1 , 退出请按 0 :";
			cin >> isConti;
			if (isConti == 0)
				return;
			else if (isConti == 1)
				continue;

			return;
		}

		if (ppDel->number != 0)
		{
			bool isAllDel;
			cout << "您要下架的商品是:" << ppDel->brand << "的" << ppDel->name << "  价格:" << ppDel->price << "\n确定下架请按 1 , 重新输入请按 0 :";
			cin >> isAllDel;
			if (isAllDel == 0)
				continue;
		}

		ppDel->number = -1;
		cout << "此商品被成功下架 !" << endl;
		return;
	} while (true);

	return;
}
