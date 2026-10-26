extern "C" int func_00234110()
{
    volatile unsigned long long *status = (volatile unsigned long long *)0x12001000;
    return (int)((*status >> 13) & 1);
}
