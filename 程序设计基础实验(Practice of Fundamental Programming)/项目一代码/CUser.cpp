#include "Shopping.h"

CUser::CUser()
{
	num_cart_ = 0;
	cart_[0].idCart = -1;
	balance_ = 0;
	tran_.InitChinaMap();
}

// "D:\\user1.txt"
void CUser::ReadCarttoArr(char *userName)
{
	FILE *pf;
	errno_t err;
	err = fopen_s(&pf, userName, "r");
	if (err != NULL)
	{
		cerr << "Can't open:" << userName << endl;
		exit(-1);
	}

	char readCart[FILE_WORDS] = "";
	fgets(readCart, FILE_WORDS, pf);

	while (!feof(pf))
	{
		int t_id = 0, t_num = 0;
		fgets(readCart, FILE_WORDS, pf);
		get_f_Interface_().SetSpacing(readCart, FILE_WORDS);
		int i = 1;
		for (; readCart[i] <= '9' && readCart[i] >= '0'; ++i)
			t_id = t_id * 10 + readCart[i] - '0';

		bool isNum = false;
		for (; i < FILE_WORDS; ++i)
		{
			if (readCart[i - 1] == '\0' && readCart[i] <= '9' && readCart[i] >= '0')
			{
				if (isNum == false)
				{
					isNum = true;
					continue;
				}
				else
					break;
			}
		}
		while (readCart[i] != '\0')
		{
			t_num = t_num * 10 + readCart[i] - '0';
			++i;
		}
		cart_[num_cart_].idCart = t_id;
		cart_[num_cart_].numCart = t_num;
		++num_cart_;
	}
	cart_[num_cart_].idCart = -1;

	fclose(pf);
}

void CUser::PrintCart(Commodity *allComm)
{
	Commodity *pcom = allComm;
	int i_pri = 0;
	bool isEmpty = true;
	for (int i_empty = 0; cart_[i_empty].idCart != -1; ++i_empty)
	{
		if (cart_[i_empty].numCart != 0)
			isEmpty = false;
	}

	if (isEmpty == true)
	{
		cout << "购物车里空空如也~ 去买一点东西吧~" << endl;
		return;
	}

	cout.setf(std::ios::left);
	cout << setw(10) << "ID" << setw(10) << "名称" << setw(10) << "品牌" << setw(10) << "价格" << setw(10) << "数量" << endl;
	for (; cart_[i_pri].idCart != -1; ++i_pri)
	{
		Commodity *curComm = CInterface::UserFindCommdity(pcom, cart_[i_pri].idCart);
		if (curComm == NULL)
		{
			cout << "没有卖这个诶: " << curComm->id << " " << curComm->brand << "的" << curComm->name << endl;
			continue;
		}
		if (curComm->number == -1)  // 这里如果多线程 还是要看设置一个结账否的库存啊
		{
			cout << "编号:" << curComm->id << curComm->brand << "的" << curComm->name << "被下架咯~" << endl;
			continue;
		}
		if (cart_[i_pri].numCart != 0)
		{
			cout.fill('0');
			cout << right << 'F' << setw(5) << curComm->id << "    ";
			cout.fill(' ');
			cout << left << setw(10) << curComm->name << setw(10) << curComm->brand << setw(10) << curComm->price << setw(10) << cart_[i_pri].numCart << endl;
		}
	}
}

double CUser::PayTran(Commodity *pCo)
{
	double sumTran = 0;
	Commodity *pcomm = pCo;
	string userCity;
	cout << "请输入您所在的城市:";
	cin >> userCity;

	for (int i = 0; cart_[i].idCart != -1; ++i)
	{
		Commodity *commStart = CInterface::UserFindCommdity(pcomm, cart_[i].idCart);
		cout.fill('0');
		cout << right << 'F' << setw(5) << commStart->id << "    ";
		cout.fill(' ');
		cout << left << setw(10) << commStart->name << setw(10) << commStart->brand << setw(10) << commStart->price << setw(10) << commStart->number << "从" << commStart->commCity << "发出" << endl;
		sumTran += round(UNIT_TRAN * tran_.Bfs(commStart->commCity, userCity) * 100) / 100.0;
	}

	cout << "总共要运费:" << sumTran << "元" << endl;
	return sumTran;
}

void CUser::Coupon(bool couponArr[], Commodity *pComm)
{
	static int coupCount = 3;
	if (coupCount <= 0)
	{
		cout << "您已经没有抽奖机会了 !" << endl;
		return;
	}
	bool isHave = false;
	for (int i = 0; cart_[i].idCart != -1; ++i)
	{
		if (cart_[i].numCart > 0)
		{
			isHave = true;
			break;
		}
	}
	if (isHave == false)
	{
		cout << "您的购物车是空的哦, 请选购一些商品在来参加抽奖吧!" << endl;
		return;
	}

	isHave = false;
	for (int i = 0; cart_[i].idCart != -1; ++i)
	{
		if (cart_[i].numCart > 0 && couponArr[cart_[i].idCart] == true)
		{
			Commodity *commStart = CInterface::UserFindCommdity(pComm, cart_[i].idCart);
			cout.fill('0');
			cout << right << 'F' << setw(5) << commStart->id << "    ";
			cout.fill(' ');
			cout << left << setw(10) << commStart->name << setw(10) << commStart->brand << setw(10) << commStart->price << setw(10) << cart_[i].numCart << endl;
			isHave = true;
		}
	}
	if (isHave == true)
		cout << "以上商品参与抽奖 !" << endl;
	else
	{
		cout << "您的购物车中还没有参与抽奖的商品哦~" << endl;
		return;
	}

	--coupCount;
	cout << "您还有" << coupCount << "次抽奖机会" << endl;


	srand((unsigned)time(NULL));
	int numCart = 1, coup = 0;
	for (; cart_[numCart].idCart != -1; ++numCart);
	coup = rand() % (numCart);
	if (coup < numCart && coup >= 0 && couponArr[coup] == true)
	{
		int time = 3;
		while (time--)
		{
			if (time == 2)
				cout << "抽奖中>>>";
			else
				cout << ">>>>>";
			Sleep(1500);
		}
		cout << endl << "您抽中了商品优惠劵\n商品:" << cart_[coup].idCart << "号将被全部打八折 !" << endl;
		cart_[coup].discount = 0.8;
		return;
	}
	cout << "您这次没有抽到奖品哦 !" << endl;
}

void CUser::AddtoCartOrComm(Commodity *pAdd, int who)
{
	bool isOkAdd = false;
	int addid = 0, addSitua = 0;
	int addNum = 0;
	Commodity *padd = NULL;

	while (isOkAdd != true)
	{
		addid = 0;
		cout << "请输入商品ID和数量(输入 * 退出):";
		char addID[NAME_WORDS] = "";
		cin >> addID;
		if (addID[0] == '*')
			return;
		cin >> addNum;

		for (int i = 1; addID[i] != '\0'; ++i)
			addid = addid * 10 + addID[i] - '0';

		padd = CInterface::UserFindCommdity(pAdd, addid);

		if (padd->number <= 0)
		{
			cout << "抱歉这个商品已经卖光或下架咯, 那么现在还加些其他什么?" << endl;
			continue;
		}

		if (padd->number - addNum < 0)
		{
			int isRestart = 0;
			cout << "抱歉这个商品只有" << padd->number << "件, 全部加入购物车请按1, 重新输入请按0:";
			cin >> isRestart;
			if (isRestart == 0)
				continue;
			addNum = padd->number;
		}

		isOkAdd = true;
	}

	for (; addSitua < num_cart_; ++addSitua)
	{
		if (cart_[addSitua].idCart == addid)
			break;
	}

	cart_[addSitua].idCart = addid;
	cart_[addSitua].numCart += addNum;
	if (addSitua == num_cart_)
		cart_[++num_cart_].idCart = -1;
	padd->number -= addNum;

	cout << "已经加入购物车!" << endl;

	char fileName[NAME_WORDS] = "";
	intTostrFileName(fileName, who);

	FILE *pf;
	errno_t err;
	err = fopen_s(&pf, fileName, "w");
	if (err != NULL)
	{
		cerr << "Can't open:" << fileName << endl;
		exit(-1);
	}

	fprintf_s(pf, "ID\t名称\t品牌\t价格\t数量");
	if (cart_[0].idCart != -1)
		fputc('\n', pf);
	for (int i = 0; cart_[i].idCart != -1; ++i)
	{
		Commodity *pcar = NULL;
		pcar = CInterface::UserFindCommdity(pAdd, cart_[i].idCart);
		fprintf_s(pf, "F%04d\t%s\t%s\t%.1f\t%d", pcar->id, pcar->name.c_str(), pcar->brand.c_str(), pcar->price, cart_[i].numCart);
		if (cart_[i + 1].idCart != -1)
			fprintf_s(pf, "\n");
	}
	fclose(pf);

}

// 要是记录商品位置数量的变量有多个不同的初始化等同的量, 就可以用这些来判断是不是够或者有没有
void CUser::DeleteCartOrComm(Commodity *pDel)
{
	int delNum = -1, delSitua = 0, delid = 0;
	bool isMany = true;
	do
	{
		delSitua = 0, delid = 0;
		if (isMany == false)
			cout << "您的购物车中没有那么多东西~ 请重新输入:";
		else
			cout << "请输入需要删除的商品ID和数量:";
		char delID[NAME_WORDS] = "";
		cin >> delID >> delNum;

		for (int i = 1; delID[i] != '\0'; ++i)
			delid = delid * 10 + delID[i] - '0';

		for (; delSitua < num_cart_; ++delSitua)
		{
			if (cart_[delSitua].idCart == delid)
				break;
		}
		if (delSitua == num_cart_)
		{
			cout << "您的购物车中没有这个东西哦~" << endl;
			isMany = true;
		}
		else if (delNum > cart_[delSitua].numCart && delSitua != num_cart_)
			isMany = false;
	} while (delNum > cart_[delSitua].numCart);

	Commodity *pdel = CInterface::UserFindCommdity(pDel, delid);
	pdel->number += delNum;
	cart_[delSitua].numCart -= delNum;

	cout << "删除成功 !" << endl;
}

void CUser::PayCart(CGod *pGod)
{
	Commodity *pPay = pGod->get_pComm_(), *tail = pGod->get_pSell_tail_();
	this->PrintCart(pPay);
	double sumPay = 0;
	int isPay = 0;

	for (int i = 0; cart_[i].idCart != -1; ++i)
	{
		Commodity *t_pay = CInterface::UserFindCommdity(pPay, cart_[i].idCart);
		if (t_pay->number < cart_[i].numCart)
		{
			cout << "编号:" << t_pay->id << t_pay->brand << "的" << t_pay->name << "不够了~" << endl;
			cout << "此商品不被计入总价格~" << endl;
			continue;
		}
		if (t_pay->number < 0)
		{
			cout << "编号:" << t_pay->id << t_pay->brand << "的" << t_pay->name << "下架咯~" << endl;
			cout << "此商品不被计入总价格~" << endl;
			continue;
		}
		//t_pay->number -= cart_[i].numCart;
		if (cart_[i].numCart > 0)
			sumPay += t_pay->price * cart_[i].numCart;
	}

	sumPay += PayTran(pPay);

	while (sumPay > get_balance_())
	{
		bool isPay = false;
		cout << "一共需要付款:" << setiosflags(ios::fixed) << setprecision(2) << sumPay << "元~" << endl;
		cout << "您的余额只有:" << get_balance_() << "元 !\n充值请按 1 , 退出请按 0 :";
		cin >> isPay;
		if (isPay == 0)
			return;
		AddBalance();
	}

	cout << "一共需要付款:" << setiosflags(ios::fixed) << setprecision(2) << sumPay << "元~ 确认付款请按 1 , 取消请按 0 :";
	cin >> isPay;

	if (isPay == 1)
	{
		for (int i = 0; cart_[i].idCart != -1; ++i)
		{
			Commodity *t_pay = CInterface::UserFindCommdity(pPay, cart_[i].idCart);
			if (t_pay->number < 0)
				continue;
			if (t_pay->number < cart_[i].numCart)
				continue;

			Commodity *p = new Commodity;
			*p = *t_pay;
			p->number = cart_[i].numCart;

			if (pGod->get_pSell_() == NULL)
			{
				pGod->get_pSell_() = p;
				tail = pGod->get_pSell_();
			}
			else
			{
				tail->next = p;
				p->pre = tail;
				tail = p;
			}
			cart_[i].numCart = 0;
		}
		pGod->get_pSell_tail_() = tail;
		this->add_balance_(-sumPay);

		cout << "付款成功 !" << endl;

		char fileName[NAME_WORDS] = "";
		intTostrFileName(fileName, pGod->get_cur_who_());

		FILE *pf;
		errno_t err;
		err = fopen_s(&pf, fileName, "w");
		if (err != NULL)
		{
			cerr << "Can't open:" << fileName << endl;
			exit(-1);
		}

		fprintf_s(pf, "ID\t名称\t品牌\t价格\t数量");
		if (cart_[0].idCart != -1)
			fputc('\n', pf);
		for (int i = 0; cart_[i].idCart != -1; ++i)
		{
			Commodity *pcar = NULL;
			pcar = CInterface::UserFindCommdity(pPay, cart_[i].idCart);
			fprintf_s(pf, "F%04d\t%s\t%s\t%.1f\t%d", pcar->id, pcar->name.c_str(), pcar->brand.c_str(), pcar->price, cart_[i].numCart);
			if (cart_[i + 1].idCart != -1)
				fprintf_s(pf, "\n");
		}
		fclose(pf);
	}
}

bool CUser::AddBalance()
{
	double addMoney;
	cout << "请输入需要充值的金额:";
	cin >> addMoney;
	add_balance_(addMoney);
	cout << "充值成功 !" << endl;

	return true;
}

void CUser::PrintBalance()
{
	cout << "当前余额:" << get_balance_() << endl;
}

void CUser::InitCart(int who, void(*pintTostr)(char str[], int a))
{
	char filename[NAME_WORDS] = "";
	char cart[FILE_WORDS] = "";
	pintTostr(filename, who);
	FILE *pf;
	errno_t err;
	err = fopen_s(&pf, filename, "r");
	if (err != NULL)
	{
		cerr << "Can't open:" << filename << endl;
		exit(-1);
	}

	fgets(cart, FILE_WORDS, pf);
	while (!feof(pf))
	{
		fgets(cart, FILE_WORDS, pf);

		int idcart = 0, i = 1, bef_i = 0, numcart = 0;
		for (; cart[i] != '\t'; ++i)
			idcart = idcart * 10 + cart[i] - '0';

		while (cart[i] != '\0')
		{
			if (cart[i] == '\t')
				bef_i = i;
			++i;
		}
		++bef_i;

		for (; cart[bef_i] <= '9' && cart[bef_i] >= '0'; ++bef_i)
			numcart += cart[bef_i] - '0';

		cart_[num_cart_].idCart = idcart;
		cart_[num_cart_].numCart = numcart;
		++num_cart_;
	}
	int a = num_cart_;
	cart_[num_cart_].idCart = -1;

	fclose(pf);
}

void CUser::intTostrUsername(char name[], int who)
{
	int c_a = 0, t_a = who;
	name[0] = 'u';
	name[1] = 's';
	name[2] = 'e';
	name[3] = 'r';

	while (t_a != 0)
	{
		++c_a;
		t_a /= 10;
	}

	for (int i = 0; i < c_a; ++i)
		name[4 + c_a - i - 1] = (int)(who / pow(10, i)) % 10 + '0';

	name[4 + c_a] = '\0';
}

void CUser::InitBalance(int who)
{
	char name[NAME_WORDS] = "";
	bool isEnro = true;
	intTostrUsername(name, who);

	char fileName[NAME_WORDS] = "D:\\用户资产.txt", read[NAME_WORDS] = "";
	FILE *pf;
	errno_t err;
	err = fopen_s(&pf, fileName, "r");
	if (err != NULL)
	{
		cerr << "Can't open:" << fileName << endl;
		exit(-1);
	}

	fgets(read, NAME_WORDS, pf);
	while (!feof(pf))
	{
		fgets(read, NAME_WORDS, pf);
		char *r = read, *n = name;
		for (; *r != '\t' && *r == *n; ++r, ++n);
		if (*r == '\t')
		{
			isEnro = false;
			double balance = 0;
			++r;

			bool isPoint = false;
			int point = 1;
			for (; *r != '\0'; ++r)
			{
				if (isPoint == false && *r <= '9' && *r >= '0')
					balance = balance * 10 + *r - '0';
				else if (*r == '.')
					isPoint = true;
				else if (isPoint == true && *r <= '9' && *r >= '0')
				{
					balance += (*r - '0') / pow(10, point);
					++point;
				}
			}
			this->balance_ = balance;
			break;
		}
	}
	fclose(pf);

	if (isEnro == true)
	{
		FILE *pf;
		errno_t err;
		err = fopen_s(&pf, fileName, "a");
		if (err != NULL)
		{
			cerr << "Can't open:" << fileName << endl;
			exit(-1);
		}

		fputc('\n', pf);
		fprintf(pf, "%s\t%c", name, '0');

		fclose(pf);
	}
}

void CUser::Init()
{
	num_cart_ = 0;
	cart_[0].idCart = -1;
	balance_ = 0;
}
