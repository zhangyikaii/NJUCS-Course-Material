/*
题目二：
我爱记单词系统
我爱记单词是一款帮助大家记忆英文单词的软件，软件功能如下：
（1） 单词库导入
单词信息包括：单词编号、单词英文、单词中文解释等基本信息。
提供文件方式存储的单词列表，从文件读入单词，建立单词库。
（2） 学习计划设置
	① 设置每天需要记忆的单词数，根据总的单词数，计算出计划完成的天数。
	② 设置单词学习的顺序，按照词表顺序或者随机产生每天需学习的单词。
（3） 单词学习
	① 学习新单词
	学习时，每个单词给出中英文对照（或者只给出英文，中文先隐藏起来，给出选择是否给出中文对照），一个一个的浏览，直到当天计划完成。在浏览单词的过程中，如果发现单词没有办法一次记住，添加到生词表中。
	其中涉及到已记忆单词表，未记忆单词表和生词表。将每天已经学习过的单词添加到已记忆单词表中，并从整个单词表中删除，形成未记忆单词表。记忆过程中个人需要重点记忆的单词添加到生词表中。
	② 复习生词表
	按照天或者整个浏览生词表。
	扩展功能：
		（1） 支持单词库的选择。
		（2） 支持系统退出时，将已记忆单词表，未记忆单词表和生词表记录到文件中。
		（3） 显示打卡记录。
*/

#include "Admin.h"
HANDLE hOutput;
COORD coord;
CONSOLE_CURSOR_INFO CursorInfo;

int main() {
	srand(time(NULL));
	hOutput = GetStdHandle(STD_OUTPUT_HANDLE);
	coord = { 0, 0 };
	GetConsoleCursorInfo(hOutput, &CursorInfo);
	CursorInfo.bVisible = false;
	CursorInfo.dwSize = 1;
	SetConsoleCursorInfo(hOutput, &CursorInfo);


	Admin a("word_list_init.txt", "word_display.txt", "start_display.txt");
	a.main();

	return 0;
}