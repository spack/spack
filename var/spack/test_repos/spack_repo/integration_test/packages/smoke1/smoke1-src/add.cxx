#include <iostream>

int main(int argc, char ** argv){
    if(argc != 3) {
        std::cerr << "Improper number of arguments (" << argc-1 << "), 2 were expected\n";
        return 1;
    }
    int a = atoi(argv[1]);
    int b = atoi(argv[2]);
    std::cout << "Result: " << a + b << "\n";
    return 0;
}