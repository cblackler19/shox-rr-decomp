extern "C" void func_0026D460(int, int);
extern "C" int func_0026F288(void *first, void *second)
{
    int firstValue = *(int *)((char *)first + 4);
    int secondValue = *(int *)((char *)second + 200);
    func_0026D460(secondValue, firstValue);
    return 1;
}
