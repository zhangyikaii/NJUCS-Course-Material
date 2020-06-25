#include "Shopping.h"

// isLogin -2:随便逛逛  1:登录用户 2:登录管理员
int main()
{
	bool a = false;
	CGod *p;
	CAdmin *pAdmin = NULL;
	CUser *pUser = NULL;
	p = &CGod();
	p->GodReadCommodity(ADMIN);   // 这里的ADMIN 没有什么用 要不要删除?
	p->tran_arr_pComm_(p->get_pComm_(), true);
	p->QuickSort(p->get_pComm_(), p->get_pComm_tail_(), p->Cmp_ID, true);  // 排序
	p->GodAllInit();

	
	int isLogin = -2;
	char input = '#';

	while (input != '*')
	{
		if (a == false)
			a = true;
		else
		{
			p->GodReadCommodity(ADMIN);   // 这里的ADMIN 没有什么用 要不要删除?
			p->tran_arr_pComm_(p->get_pComm_(), true);
			p->QuickSort(p->get_pComm_(), p->get_pComm_tail_(), p->Cmp_ID, true);  // 排序
		}

		isLogin = -2;
		while ((input = p->PrintMenu()) != '*')
		{
			bool isInput = true;
			switch (input)
			{
			case '0':
				isLogin = p->GodLogin();
				if (isLogin == -1 && isLogin == 0)
					return 0;
				break;

			case '1':
				isLogin = p->GodEnroll(p->get_login_user_name_());
				if (isLogin == -1)
					return 0;
				break;

			case '2':
				isLogin = 3;
				break;

			case '3':
				return 0;

			default:
				isInput = false;
				break;
			}
			if (isInput != false)
				break;
		}

		if (isLogin == 1)
		{
			char adminInput;
			while ((adminInput = p->PrintAdminMenu()) != '0')
			{
				switch (adminInput)
				{
				case '1':
					p->GodPrintCommodity(ADMIN, p->get_pComm_());
					break;

				case '2':
					p->get_puser(p->get_cur_who_())->AddtoCartOrComm(p->get_pComm_(), p->get_cur_who_());
					break;

				case '3':
					p->get_puser(p->get_cur_who_())->DeleteCartOrComm(p->get_pComm_());
					break;

				case '4':
					pAdmin = dynamic_cast<CAdmin *>(p->get_puser(p->get_cur_who_()));
					pAdmin->ChangeCommPrice(p->get_pComm_());
					break;

				case '5':
					pAdmin = dynamic_cast<CAdmin *>(p->get_puser(p->get_cur_who_()));
					pAdmin->ChangeCommNum(p->get_pComm_());
					break;

				case '6':
					p->FindCommodity(ADMIN);
					break;

				case '7':
					p->GodPrintCommodity(ADMIN, p->get_pSell_());
					break;

				case '8':
					p->GodSetCommCity();
					break;

				case '9':
					p->SetCouponComm();
					break;

				case '@':
					p->get_chat_().GodChatting(ADMIN, p->get_login_user_name_());
					break;

				default:
					break;
				}
			}
		}

		else if (isLogin == 2)
		{
			char userInput;
			pUser = dynamic_cast<CUser *>(p->get_puser(p->get_cur_who_()));

			pUser->InitCart(p->get_cur_who_(), intTostrFileName);
			pUser->InitBalance(p->get_cur_who_());
			while ((userInput = p->PrintUserMenu()) != '0')
			{
				switch (userInput)
				{
				case '1':
					p->GodPrintCommodity(USER, p->get_pComm_());
					break;

				case '2':
					p->FindCommodity(USER);
					break;

				case '3':
					p->get_puser(p->get_cur_who_())->AddtoCartOrComm(p->get_pComm_(), p->get_cur_who_());
					break;

				case '4':
					p->get_puser(p->get_cur_who_())->DeleteCartOrComm(p->get_pComm_());
					break;

				case '5':
					pUser->PrintCart(p->get_pComm_());
					break;

				case '6':
					pUser->PayCart(p);
					p->UserComment();
					break;

				case '7':
					pUser->AddBalance();
					break;

				case '8':
					pUser->PrintBalance();
					break;

				case '9':
					pUser->Coupon(p->get_arr_coupon_(), p->get_pComm_());
					break;

				case '@':
					p->get_chat_().GodChatting(USER, p->get_login_user_name_());
					break;

				case '&':
					p->UserComment();
					break;

				case '%':
					p->UserLike();
					break;

				default:
					break;
				}
			}
		}

		else if (isLogin == 3)
		{
			char touristInput;
			while ((touristInput = p->PrintTouristMenu()) != '0')
			{
				switch (touristInput)
				{
				case '1':
					p->GodPrintCommodity(USER, p->get_pComm_());
					break;

				case '2':
					p->FindCommodity(USER);
					break;

				default:
					break;
				}
			}
		}



		if (isLogin == 1 || isLogin == 2)
		{
			p->UpdataCommFile("D:\\库存.txt");
			p->UpdataSellFile("D:\\已售清单.txt");
		}

	}

	/*p->GodReadCommodity(0);
	p->tran_arr_pComm_();
	p->GodPrintCommodity(pRun, p->get_pComm_());

	p->QuickSort(p->get_pComm_(), p->get_pComm_tail_(), p->Cmp_ID);
	p->GodPrintCommodity(pRun, p->get_pComm_());*/


	////p->FindCommodity(pRun);

	//CAdmin u;
	//
	///*u.AddtoCartOrComm(p->get_pComm_());
	//u.PrintCart(p->get_pComm_());*/
	//u.DeleteCartOrComm(p->get_pComm_());
	////u.PrintCart(p->get_pComm_());
	//p->GodPrintCommodity(pRun, p->get_pComm_());
	/*p->GodPrintCommodity(pRun, p->get_pComm_());
	u.PayCart(p);*/

	/*CAdmin test;
	test.DeleteCartOrComm(p->get_pComm_());
	test.AddtoCartOrComm(p->get_pComm_());
	p->GodPrintCommodity(pRun, p->get_pComm_());*/

	/*CUser c;
	c.AddtoCartOrComm(p->get_pComm_());
	c.PayCart(p);
	p->GodPrintCommodity(ADMIN, p->get_pSell_());*/

	return 0;
}


