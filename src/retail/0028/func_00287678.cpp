extern "C" signed char D_00424FF8[] __attribute__((section(".data")));
extern "C" void func_00287678(int value)
{
    int index = D_00424FF8[509];
    *(int *)(D_00424FF8 + 544 + index * 4) = value;
    unsigned char count = ((unsigned char *)D_00424FF8)[509];
    ((unsigned char *)D_00424FF8)[509] = count + 1;
}
