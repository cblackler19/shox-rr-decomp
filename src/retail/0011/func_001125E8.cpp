extern "C" int D_002DED28 __attribute__((section(".data")));
extern "C" unsigned char D_00448EE0[];
extern "C" unsigned char D_00448EF0[];
extern "C" void func_001A4D60(void *argument);
extern "C" void func_001125E8() {
    if (D_002DED28 == 0) {
        D_002DED28 = 1;
        func_001A4D60(D_00448EE0);
    } else {
        D_002DED28 = 0;
        func_001A4D60(D_00448EF0);
    }
}
