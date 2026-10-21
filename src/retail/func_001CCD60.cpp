extern "C" int *D_0034FD00 __attribute__((section(".data")));

extern "C" int func_001CCD60(int index) {
    int *table = D_0034FD00;
    table += index;
    return table[0x124C];
}
