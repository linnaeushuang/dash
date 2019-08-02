#include <fstream>
#include<iostream>
using namespace std;
int main()
{
	char a[100];
	char b[100];
	ifstream permission;
    permission.open("./data/predict0");
    while(!permission.eof())
    {
    	permission >> a;
    }
    cout << a;
    return 0;
}
    