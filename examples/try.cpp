#include <fstream>
#include<iostream>
using namespace std;
int
main(int argc, char const *argv[])
{
	ifstream bwfile;
	double data;
	double data2;
	streampos position;
	bwfile.open("tracefile");
	
	position = bwfile.tellg();
	
	bwfile>>data>>data2;
	cout<<data<<" "<<data2<<endl;
	
	bwfile>>data>>data2;
	cout<<data<<" "<<data2<<endl;
	
	bwfile.seekg(position);
	
	bwfile>>data;
	cout<<data<<endl;	
	return 0;
}