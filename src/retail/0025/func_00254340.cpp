struct Global_254340 {
    unsigned char unused[12];
    unsigned char first;
    unsigned char second;
    unsigned char gap15;
    int field16;
    unsigned char gap20[4];
    int field24;
    unsigned char field28;
};
extern "C" Global_254340 D_00587638 __attribute__((section(".data")));
extern "C" int func_00254340(void)
{
    D_00587638.first = 0;
    D_00587638.second = 0;
    D_00587638.field16 = 0;
    D_00587638.field24 = 0;
    D_00587638.gap20[0] = 0;
    D_00587638.field28 = 0;
    return 1;
}
