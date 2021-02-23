#include <iostream>
#include <regex>

using namespace std;

int main()
{
    auto func = [] () { cout << "Hello world from C++11" << endl; };
    func(); // now call the function
 
    std::regex r("st|mt|tr");
    std::cout << "std::regex r(\"st|mt|tr\")" << " match tr? ";
    if (std::regex_match("tr", r) == 0)
       std::cout << "NO!\n  ==> Using pre g++ 4.9.2 libstdc++ which doesn't implement regex properly" << std::endl;
    else
       std::cout << "YES!\n  ==> Correct libstdc++11 implementation of regex (4.9.2 or later)" << std::endl;
}
