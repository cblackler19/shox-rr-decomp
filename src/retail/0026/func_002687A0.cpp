extern "C" int func_002687A0(int value)
{
    int* base = (int*)0x00420000;
    int previous = base[598];
    base[598] = value;
    return previous;
}
