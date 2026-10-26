extern "C" int (*D_004302E8)(void) __attribute__((section(".data")));
extern "C" int func_002AAA70(void);
extern "C" int func_002AAA90(const int *left, const int *right)
{
    int difference = *left - *right;
    if (difference == 0)
        D_004302E8 = func_002AAA70;
    return difference;
}
