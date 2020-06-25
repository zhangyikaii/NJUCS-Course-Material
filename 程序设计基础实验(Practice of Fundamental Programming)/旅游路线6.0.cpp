#include <iostream>
#include <iomanip>
#include <string>

using namespace std;

const int CITY_NUMBER = 100;
const int CITY_WORDS = 30;

struct CityNode
{
	string city_type;
	double price;
};

struct Route
{
	CityNode *pcity;
	Route *next;
};

char PrintMenu();
CityNode *InitializeCityList();
CityNode *InitializeCityListFile();
void PrintPriceList(CityNode *head);
Route *BuildRoute(CityNode *curcityhead);
CityNode *SearchCity(string citytype, CityNode *curcityhead);
void SetSpacing(char *arr, int num);
void PrintRoute(Route *proute, bool isbuild);
void PrintSumPrice(Route *proute);
Route *ChangeCity(Route *proute, CityNode *cityhead);
Route *InsertCity(Route *proute, CityNode *cityhead);
Route *DeleteCity(Route *proute);
void ChangeCityPrice(CityNode *cityhead);
void Finish(Route *proute, CityNode *cityhead);



int main()
{
	CityNode *city_head = InitializeCityListFile();
	Route *route_head = NULL;
	bool isinitial = false;

	char input;
	while ((input = PrintMenu()) != '*')
	{
		if (isinitial == false && input != '2' && input != '1')
			continue;
		switch (input)
		{
		case '1':
			PrintPriceList(city_head);
			break;

		case '2':
			isinitial = true;
			route_head = BuildRoute(city_head);
			PrintRoute(route_head, true);
			PrintSumPrice(route_head);
			break;

		case '3':
			PrintRoute(ChangeCity(route_head, city_head), false);
			PrintSumPrice(route_head);
			break;

		case '4':
			PrintRoute(InsertCity(route_head, city_head), false);
			PrintSumPrice(route_head);
			break;

		case '5':
			PrintRoute(DeleteCity(route_head), false);
			PrintSumPrice(route_head);
			break;

		case '6':
			ChangeCityPrice(city_head);
			PrintPriceList(city_head);
			PrintRoute(route_head, true);
			PrintSumPrice(route_head);
			break;

			default:
				break;
		}
	}

	Finish(route_head, city_head);

	return 0;
}

char PrintMenu()
{
	puts("****************************************************************");
	cout << setw(33) << "菜单" << endl;
	cout << "           " << "1. 打印旅游城市价格表" << endl;
	cout << "           " << "2. 创建旅游路线" << endl;
	cout << "           " << "3. 将旅游路线中的某个城市替换为其他的城市" << endl;
	cout << "           " << "4. 在旅游路线中的两个城市之间, 插入新的城市" << endl;
	cout << "           " << "5. 删除旅游路线中的某个城市" << endl;
	cout << "           " << "6. 调整旅游城市价格表中某个城市的价格" << endl;
	cout << "           " << "*. 退出程序" << endl;
	puts("****************************************************************\n");

	char input;
	cout << "请输入您的操作:";
	(cin >> input).get();

	return input;
}

void PrintPriceList(CityNode *head)
{
	int num = 0;
	for (; head->price != -1; ++head)
		cout << num++ << "    " << head->city_type << "   " << head->price << endl;

}

CityNode *InitializeCityList()
{
	CityNode *head = new CityNode[CITY_NUMBER];
	CityNode *write = head;

	write->city_type = "北京";
	write->price = 3000;
	++write;

	write->city_type = "南京";
	write->price = 2500;
	++write;

	write->city_type = "扬州";
	write->price = 2400;
	++write;

	write->city_type = "无锡";
	write->price = 2000;
	++write;

	write->city_type = "苏州";
	write->price = 2200;
	++write;

	write->city_type = "拉萨";
	write->price = 3500;
	++write;

	write->price = -1;

	return head;
}

CityNode *InitializeCityListFile()
{
	CityNode *head = new CityNode[CITY_NUMBER];
	CityNode *write = head;

	FILE *pf;
	errno_t err;
	err = fopen_s(&pf, "D:\\pricelist.txt", "r");
	if (err != NULL)
	{
		cerr << "Initial file can't open !" << endl;
		exit(-1);
	}

	char filecity[CITY_WORDS];
	fgets(filecity, CITY_WORDS, pf);

	while (!feof(pf))
	{
		SetSpacing(filecity, CITY_WORDS);

		bool iscity = true;
		for (int i = 1; i < CITY_WORDS; ++i)
		{
			if (iscity && filecity[i] != '\0')
			{
				iscity = false;
				char *p = &filecity[i];
				string temp = p;
				write->city_type = temp;
			}
			else if (!iscity && filecity[i] <= '9' && filecity[i] >= '0')
			{
				double sum_price = 0;
				while (filecity[i] <= '9' && filecity[i] >= '0')
				{
					sum_price = sum_price * 10 + double(filecity[i] - '0');
					++i;
				}
				write->price = sum_price;
				break;
			}
		}
		++write;

		fgets(filecity, CITY_WORDS, pf);
	}
	write->price = -1;

	return head;
}

// only add existed city
Route *BuildRoute(CityNode *curcityhead)
{
	// input
	char city_array[CITY_NUMBER * 3];
	cout << "请输入城市, 以空格分割, 换行结束:";
	gets_s(city_array);

	// trun spacing into \0 for copying to 'string' type
	int cityarrnum = 0;
	for (; city_array[cityarrnum] != '\0'; ++cityarrnum);
	SetSpacing(city_array, cityarrnum);

	// read and build
	char *strhead = city_array;
	bool isfirst = true;
	Route *head = NULL, *tail = NULL;
	for (int i_city_array = 0; i_city_array < cityarrnum; ++i_city_array)
	{
		if (i_city_array == 0 || (i_city_array != cityarrnum - 1 && city_array[i_city_array] == '\0'))
		{
			if (i_city_array == 0)
				strhead = &city_array[i_city_array];
			else
				strhead = &city_array[i_city_array + 1];
			string inputcity = strhead;
			if (isfirst)
			{
				isfirst = false;
				head = new Route;
				head->next = NULL;
				head->pcity = SearchCity(inputcity, curcityhead);
				tail = head;
			}
			else
			{
				Route *p = new Route;
				p->next = NULL;
				p->pcity = SearchCity(inputcity, curcityhead);
				tail->next = p;
				tail = p;
			}
		}
	}
	

	//cout << head->pcity->city_type << endl;
	//head = head->next;
	//cout << head->pcity->city_type << endl;

	cout << "创建成功!" << endl;
	return head;
}

CityNode *SearchCity(string citytype, CityNode *curcityhead)
{
	for (; curcityhead->price != -1; ++curcityhead)
	{
		if (curcityhead->city_type.compare(citytype) == 0)
			return curcityhead;
	}
}

void SetSpacing(char *arr, int num)
{
	for (int i = 0; i < num; ++i)
	{
		if (arr[i] == ' ' || arr[i] == '\t' || arr[i] == '\n')
			arr[i] = '\0';
	}
}

// use it after " cout << "旅游线路为:" ... "
void PrintRoute(Route *proute, bool isbuild)
{
	/*static int isfirst = 0;
	if (isfirst == 0)
	{
		cout << "旅游线路为:";
		++isfirst;
	}
	else
	{
		cout << "旅游线路更改为:";
	}*/

	if (isbuild)
		cout << "旅游线路为:";
	else
		cout << "旅游线路更改为:";

	cout << proute->pcity->city_type;
	proute = proute->next;

	while (proute != NULL)
	{
		cout << "->" << proute->pcity->city_type;
		proute = proute->next;
	}

	cout << endl;
}

void PrintSumPrice(Route *proute)
{
	double sum_price = 0;
	while (proute != NULL)
	{
		sum_price += proute->pcity->price;
		proute = proute->next;
	}

	cout << "总价格:" << setiosflags(ios::fixed) << setprecision(1) << sum_price << endl;
}

Route *ChangeCity(Route *proute, CityNode *cityhead)
{
	string change_city, input_city;
	cout << "请输入被替换的城市:";
	cin >> change_city;
	cout << "请输入替换城市:";
	cin >> input_city;

	Route *pchange = proute;
	while (pchange->pcity->city_type != change_city)
		pchange = pchange->next;

	pchange->pcity = SearchCity(input_city, cityhead);

	return proute;
}

Route *InsertCity(Route *proute, CityNode *cityhead)
{
	string city1, city2, insertcity;
	cout << "请输入两个在路线中连续的城市:";
	cin >> city1 >> city2;
	cout << "请输入需要插入的城市:";
	cin >> insertcity;

	// find the location to insert
	Route *ins = proute;
	for (; ins != NULL && ins->pcity->city_type != city1; ins = ins->next);
	
	Route *p = new Route;
	p->pcity = SearchCity(insertcity, cityhead);

	if (ins->next != NULL)
		p->next = ins->next;
	else
		p->next = NULL;

	ins->next = p;

	return proute;
}

Route *DeleteCity(Route *proute)
{
	string delcity;
	Route *pfind = proute;
	cout << "请输入需要删除的城市:";
	cin >> delcity;

	// find the location to delete
	for (; pfind->next != NULL && pfind->next->pcity->city_type != delcity; pfind = pfind->next);

	if (pfind->next == NULL)
	{
		cout << "城市不在旅游线路中!" << endl;
		return proute;
	}

	Route *tdel = pfind->next;

	if (pfind->next->next != NULL)
		pfind->next = pfind->next->next;
	else
		pfind->next = NULL;

	delete tdel;

	return proute;
}

void ChangeCityPrice(CityNode *cityhead)
{
	string changecity;
	CityNode *pcity;
	double changeprice = 0;

	cout << "请输入需要调整价格的城市:";
	cin >> changecity;
	pcity = SearchCity(changecity, cityhead);

	cout << changecity << "原来的价格为" << pcity->price << ", 请输入调整后的价格:";
	cin >> changeprice;

	pcity->price = changeprice;
}

void Finish(Route *proute, CityNode *cityhead)
{
	delete[]cityhead;
	while (proute != NULL)
	{
		Route *del = proute;
		proute = proute->next;
		delete del;
	}
}