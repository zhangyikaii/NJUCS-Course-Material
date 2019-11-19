#include "Shopping.h"
string Chat::SetMessageTime()
{
	time_t time_seconds = time(0);
	struct tm now_time;
	localtime_s(&now_time, &time_seconds);
	char temp[64];
	strftime(temp, sizeof(temp), "%Y-%m-%d %H:%M:%S", &now_time);
	return temp;
}

void Chat::OutputHistory()
{
	cout << endl;
	if (num_message_ == 0)
		return;
	for (int i = 0; i < num_message_; ++i)
	{
		//if (chat_[i].who == w)
		//	cout.setf(ios::left);
		//else
		//	cout.setf(ios::right);

		cout << chat_[i].time << endl;
		cout << chat_[i].who << ": " << chat_[i].content << endl;
		cout << endl;
	}
}

bool Chat::Chatting(who w, string name)
{
	Message *pChat = &chat_[num_message_];
	string chatContent;
	cout << "请输入您要发送给";
	if (w == ADMIN)
		cout << "用户";
	else
		cout << "商家";
	cout << "的内容:";
	cin >> chatContent;
	if (chatContent.compare("*") == 0)
		return false;
	pChat->who = name;
	pChat->content = chatContent;
	pChat->time = SetMessageTime();
	++num_message_;
	return true;
}

void Chat::GodChatting(who w, string name)
{
	system("cls");
	while (true)
	{
		cout << "您已进入聊天界面 ! 任意时刻输入 * 退出";
		OutputHistory();
		if (Chatting(w, name) == false)
		{
			system("cls");
			return;
		}
		system("cls");
	}
}