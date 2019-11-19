#include "DataBase.h"
using namespace std;

// INSert 2 识别还有问题
int main()
{
	//string a("CREATE TABLE student (学号 ,姓名, 年级) TO student.txt");
	//string b("INSERT INTO student VALUES (12345 , 马好好, 哈 )");
	//string c("DROP TABLE student");
	//string d("INSERT INTO student (姓名 , 年级) VALUES (misdjflskfjngzi名字 , 空间)");
	//string d1("INSERT INTO student (Names, studentID, Score1) VALUES (12346 , df, dskfj)");
	//string d2("INSERT INTO student (姓名 , 年级) VALUES (12346 , gy)");
	//string d3("INSERT INTO student (学号, 年级) VALUES (1 , hd)");

	//string e("DELETE FROM student WHERE Score1 = 90");
	//string f("DELETE * FROM student");
	//string g("CREATE TABLE name FROM lecture.txt");
	//string h("UPDATE student SET Score1 = value1, Score2 = value2");
	//string i("UPDATE student SET 姓名 = hahaha, 年级 = 99 WHERE 学号 = 12345");
	//string j("SELECT studentID,Score1 FROM student");
	//string k("SELECT DISTINCT studentID,Score1 FROM student");
	//string l("SELECT * FROM student ORDER BY 学号 ASC");
	//string m("SELECT * FROM student WHERE 姓名 = 12346");
	//string n("VIEW HISTORY WHERE LIKE 故事,一个");
	//string o("SELECT * FROM student WHERE Score1 = 90 TO 计算机系学生名单.txt");
	//CTable c_table;
	//CSameFunction c_sameFun;

	//// c_sameFun.PriReadTable();
	//c_table.CreateTableTo(a);
	//c_sameFun.PrintTable(c_table.FindTableHead("student.txt"));

	//c_table.InsertTableTO(b);
	//c_sameFun.PrintTable(c_table.FindTableHead("student.txt"));

	//c_table.InsertTableValue(d3);
	//c_table.InsertTableValue(d1);
	//c_table.InsertTableValue(d2);
	//c_table.InsertTableValue(d);

	////c_table.DropTable(c);
	////c_sameFun.PrintTable(c_table.FindTableHead("student.txt"));

	///*c_table.DropWhere(e);
	//c_sameFun.PrintTable(c_table.FindTableHead("student.txt"));
	//
	//c_table.DropAllRow(f);
	//c_sameFun.PrintTable(c_table.FindTableHead("student.txt"));*/

	///*c_table.CreateTableFrom(g);
	//c_sameFun.PrintTable(c_table.FindTableHead("lecture.txt"));*/

	///*c_table.UpdateSet(h);
	//c_sameFun.PrintTable(c_table.FindTableHead("student.txt"));*/

	///*c_table.UpdateSetWhere(i);
	//c_sameFun.PrintTable(c_table.FindTableHead("student.txt"));*/

	///*c_table.SelectFrom(j);

	//c_table.SelectDistinct(k);

	//c_table.PriAllTABLEList();*/

	//c_sameFun.PrintTable(c_table.FindTableHead("student.txt"));
	//c_table.SelectFromWhere(m);
	////c_table.SelectFromOrder(l);

	//c_table.TestHis();
	//c_table.HistorySearch(n);

	CTable c_table;
	CSameFunction c_sameFun;
	//c_table.InitNameFile();

	//////
	/*string a("CREATE TABLE student FROM student.txt");
	string l("SELECT * FROM student ORDER BY Score2, Score3 ASC WHERE TotalScore = 346, Score4 < 90");
	string r("DELETE FROM student WHERE Score1 = 90");
	string h("SELECT DISTINCT studentID,Score1 FROM student");
	
	c_table.CreateTableFrom(a);
	c_sameFun.PrintTable(c_table.FindTableHead("student.txt"));
	c_table.SelectDistinct(h);*/
	//c_table.UpdateSetWhere(h);
	//c_table.SelectFromOrderWhere(l);
	/*string o("SELECT * FROM student WHERE Score1 = 90 TO 计算机系名单.txt");
	c_table.SelectWhereToFile(o);*/
	////////

	/*CREATE TABLE student FROM student.txt
~$ CREATE TABLE student FROM lecture.txt
~$ TABLE LIST*/

	string order;
	OrderEnum input = null_mean;
	do
	{
		input = c_sameFun.PriReadTable(order, c_table.get_historyArr_());
		//c_sameFun.PrintTable(c_table.FindTableHead("student.txt"));
		switch (input)
		{
		case CREATE_TABLE1:
			c_table.CreateTableTo(order);
			break;

		case CREATE_TABLE2:
			c_table.CreateTableFrom(order);
			break;

		case DROP_TABLE:
			c_table.DropTable(order);
			break;

		case TABLE_LIST:
			c_table.PriAllTABLEList();
			break;

		case INSERT_INTO1:
			c_table.InsertTableTO(order);
			break;

		case INSERT_INTO2:
			c_table.InsertTableValue(order);
			break;

		case DELETE_FROM:
			c_table.DropWhere(order);
			break;

		case DELETE_FROM_ALL:
			c_table.DropAllRow(order);
			break;

		case UPDATE1:
			c_table.UpdateSet(order);
			break;

		case UPDATE2:
			c_table.UpdateSetWhere(order);
			break;

		case SELECT_FROM:
			c_table.SelectFrom(order);
			break;

		case SELECT_ALL:
			c_table.SelectAll(order);
			break;

		case SELECT_DISTINCT:
			c_table.SelectDistinct(order);
			break;

		case SELECT_SEQU:
			c_table.SelectFromOrder(order);
			break;

		case SELECT_WHERE:
			c_table.SelectFromWhere(order);
			break;

		case SELECT_TO:
			c_table.SelectWhereToFile(order);
			break;

		case SELECT_SEQU_WHERE:
			c_table.SelectFromOrderWhere(order);
			break;

		case SHOW_HIS:
			c_table.HistorySearch(order);
			break;
		
		case end_mean:
			c_table.WriteToAllFile();
			break;

		default:
			break;
		}
	} while (input != end_mean);

	return 0;
}





