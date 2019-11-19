// 余额 搜索记录
// 登录状态
// 查看已购商品



#include <iostream>
#include <string>
#include <stdlib.h>
#include <cmath>
#include <iomanip>
#include <io.h>
#include <stdio.h>
#include <queue>
#include <ctime>
#include <Windows.h>
using namespace std;

const int MESSAGE_MAX = 200;
const int NAME_WORDS = 31;
const int FILE_WORDS = 101;
const int ALL_LIST = 2001;
const int MAX_USERS_NUM = 10;
const int MAX_ADMIN_NUM = 10;
const int NUM_TRY_INPUT_PASSWORD = 3;
const int MAX_COMM_LINE = 100;
const int MAX_MAP = 10;
const double UNIT_TRAN = 0.8;
const int MAX_COMMENT = 20;


class CFile;
class CGod;
class CAdmin;
class CUser;
class CInterface;
class Hash;
class Tran;
class Chat;


enum What
{
	MOUN = -1,
	ROAD = 0,
	CITY = 1
};

struct Map
{
	string city;
	What w;
	int dis;
	Map()
	{
		w = ROAD;
		dis = 0;
	}
};


enum haveread
{
	NULLMES = 0,
	UNREAD,
	READMES
};

enum who
{
	ADMIN = 0,
	USER
};

struct Message
{
	string content, time;
	string who;
	Message()
	{
		who = USER;
	}
};

// 一件商品的评论
struct Comment
{
	bool is_have;
	string comment[MAX_COMMENT];
	string name[MAX_COMMENT];
	int num_com;
	Comment()
	{
		num_com = 0;
		is_have = false;
	}
};



struct Commodity
{
	int id;
	string name;
	string brand;
	string commCity;
	double price;
	int number;
	Commodity *next;
	Commodity *pre;
	int likes;
	Commodity()
	{
		id = -1;
		price = 0;
		number = 0;
		next = NULL;
		pre = NULL;
		likes = 0;
	}
	Commodity& operator =(Commodity t)
	{
		this->id = t.id;
		this->name = t.name;
		this->brand = t.brand;
		this->price = t.price;
		this->number = t.number;
		this->commCity = t.commCity;
		this->likes = t.likes;

		return *this;
	}
	// 如果还没加的左边的对象还没有被赋值 就是右边的对象被赋值过去
	Commodity& operator +(Commodity t)
	{
		if (this->id == -1)
			*this = t;
		else
			this->number += t.number;

		return *this;
	}
	Commodity(int _id, string _name, string _brand, double _price, int _number)
	{
		id = _id;
		name = _name;
		brand = _brand;
		price = _price;
		number = _number;
		next = NULL;
		pre = NULL;
		likes = 0;
	}
};

struct Cart
{
	int idCart;
	int numCart;
	double discount;
	bool isIncluTran;
	Cart()
	{
		idCart = 0;
		numCart = 0;
		discount = 1;
		isIncluTran = false;
	}
	Cart(int _idCart, int _numCart, double _disc)
	{
		idCart = _idCart;
		numCart = _numCart;
		discount = _disc;
		isIncluTran = false;
	}
};



void DeleteList(Commodity *del);
class CFile
{
public:
	CFile()
	{
	}
	void SetSpacing(char *arr, int num);
	int FindName(char *name, char *file);
	int ReadCommodity(char(&comm_arr)[FILE_WORDS][FILE_WORDS], char *fileName);                // 查看商品
};

// 有'或'的都是前一个是管理员类的功能 后一个是用户类的功能
// 在 CUser 和 CAdmin 中都会用这些函数 他们还有各自独有的函数
class CInterface
{
public:
	int LoginAdminOrUser(int &cur, string &loginname);            // 登录:管理员或用户
	Commodity *UserFindCommdity(Commodity *pComm, int findID);
	int ThisIsWho(char userName[], int &cur);

	CFile get_f_Interface_()
	{
		return f_Interface_;
	}
	virtual void DeleteCartOrComm(Commodity *pDel) = 0;
	virtual void AddtoCartOrComm(Commodity *pAdd, int who) = 0;                   // 加入商品:到购物车或库存


private:
	CFile f_Interface_;
	
};
class Tran
{
public:
	Tran()
	{
		row_ = MAX_MAP;
		line_ = MAX_MAP;
		xWays[0] = -1, xWays[1] = 1, xWays[2] = 0, xWays[3] = 0;
		yWays[0] = 0, yWays[1] = 0, yWays[2] = -1, yWays[3] = 1;
	}
	void set_map_city(int x, int y, string _city)
	{
		map_[x * row_ + y].city = _city;
		map_[x * row_ + y].w = CITY;
	}
	void InitChinaMap();
	int Bfs(string start, string end);
	int WhereCity(string findCity);
	void clear(queue<int>& q);

private:
	int row_, line_;
	int xWays[4], yWays[4];
	queue<int> que_;
	Map map_[MAX_MAP * MAX_MAP];

};

class CUser : public CInterface
{
public:
	CUser();
	void Init();
	double get_balance_()
	{
		return balance_;
	}
	void add_balance_(double b)
	{
		balance_ += b;
	}
	bool AddBalance();
	void ReadCarttoArr(char *userName);
	void PrintCart(Commodity *allComm);
	void AddtoCartOrComm(Commodity *pAdd, int who);
	void DeleteCartOrComm(Commodity *pDel);
	void PayCart(CGod *pGod);
	void PrintBalance();
	void InitCart(int who, void (*pintTostr)(char str[], int a));
	void intTostrUsername(char name[], int who);
	void InitBalance(int who);
	void CartFile();
	void Coupon(bool couponArr[], Commodity *pComm);
	double PayTran(Commodity *pCo);

private:
	Cart cart_[MAX_COMM_LINE];
	int num_cart_;
	double balance_;
	Tran tran_;
};

class CAdmin :public CInterface
{
public:
	void DeleteCartOrComm(Commodity *pDel);
	void AddtoCartOrComm(Commodity *pAdd, int who);
	void ChangeCommNum(Commodity *pCha);
	void ChangeCommPrice(Commodity *pCha);
private:

};

class Chat
{
public:
	Chat()
	{
		num_message_ = 0;
		for (int i = 0; i < MESSAGE_MAX; ++i)
			newnum_message_[i] = NULLMES;
	}
	string SetMessageTime();
	bool Chatting(who w, string name);
	void OutputHistory();
	void GodChatting(who w, string name);
private:
	Message chat_[MESSAGE_MAX];
	int num_message_;
	haveread newnum_message_[MESSAGE_MAX];
};


// 管理类
class CGod
{
public:
	CGod();
	void GodAllInit();
	char PrintMenu();
	char PrintAdminMenu();
	char PrintUserMenu();
	char PrintTouristMenu();
	int GodEnroll(string &loginname);
	int GodLogin();
	void GodReadCommodity(int who);
	void GodPrintCommodity(int who, Commodity *ppri);
	void SumList(Commodity *&phead);
	void SumListComm(Commodity *&phead);
	friend void intTostrFileName(char str[], int a);
	void UpdataCommFile(char *fileName);
	void UpdataSellFile(char *fileName);
	void SetCouponComm();
	void UserComment();
	void UserLike();
	CInterface *get_puser(int num)
	{
		if (num < MAX_USERS_NUM)
			return pRun[num];
		return NULL;
	}
	void set_puser(int num, CInterface *who)
	{
		if (num < MAX_USERS_NUM)
			pRun[num] = who;
	}
	void tran_arr_pComm_(Commodity *&To, bool flag);
	static bool Cmp_ID(Commodity *a, Commodity *b);
	bool isPartSame(string a, string b);
	void QuickSort(Commodity *beg, Commodity *end, bool(*Cmp)(Commodity *, Commodity *), bool flag);
	string &get_login_user_name_()
	{
		return login_user_name_;
	}
	Commodity *&get_pComm_()
	{
		return pComm_;
	}
	Commodity *&get_pComm_tail_()
	{
		return pComm_tail_;
	}
	bool p_Cmp(Commodity *a, Commodity *b);
	void FindCommodity(int who);
	void GodSetCommCity();
	void InitCommCity(string cityDeliver);
	Commodity *&get_pSell_()
	{
		return pSell_;
	}
	Commodity *&get_pSell_tail_()
	{
		return pSell_tail_;
	}
	int &get_num_user()    // 已经注册了多少人
	{
		return num_user_;
	}
	bool *get_arr_coupon_()
	{
		return arr_coupon_;
	}
	// 现在登录的是哪位(跟着购物车文件名走)
	int &get_cur_who_()
	{
		return cur_who_;
	}
	Chat &get_chat_()
	{
		return chat_obj_;
	}

private:
	CFile f_;
	CInterface *pRun[MAX_USERS_NUM];
	int num_user_;         
	int cur_who_;
	Commodity *pComm_, *pComm_tail_;
	Commodity *pSell_, *pSell_tail_;
	char comm_arr_[FILE_WORDS][FILE_WORDS];
	char sell_arr[FILE_WORDS][FILE_WORDS];
	int line_comm_arr_;
	int line_sell_arr;
	string login_user_name_;
	Chat chat_obj_;
	bool arr_coupon_[MAX_COMM_LINE];
	Comment arr_comment_[MAX_COMM_LINE];
};

class Hash
{
public:
	Hash()
	{
		for (int i = 0; i < FILE_WORDS; ++i)
			commo[i] = NULL;
	}
	Commodity *&get_commo_(double price)
	{
		int i = 0;
		for (; commo[i] != NULL; ++i)
		{
			if (commo[i]->price == price)
				return commo[i];
		}
		return commo[i];
	}
	Commodity *&getRealComm(int i)
	{
		return commo[i];
	}

private:
	Commodity *commo[FILE_WORDS];
};


