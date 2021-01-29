int main()
{
    switch(sizeof(long int)) {
        case sizeof(long int):
            return 1;
        case sizeof(long long int):
            return 2;
        default:
            return 0;
    }
}
