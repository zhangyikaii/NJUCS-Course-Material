#include "Admin.h"

int main() {
	Admin adm;
	adm.Read2MdFile();
	printf("Do you need CSS styles? (1: Yes!, 0: No, thanks) :");
	int isSty = 0;
	cin.clear();
	cin >> isSty;
	adm.Md2Html(isSty);


	return 0;
}