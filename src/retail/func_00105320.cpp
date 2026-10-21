extern "C" void *D_597FE0 __attribute__((section(".data")));
extern "C" unsigned char D_004468C0[];
extern "C" unsigned char D_481EC0[];
extern "C" void func_00105800();
extern "C" void func_002671C0(void *target, const void *first, const void *second);
extern "C" void **func_00105320() {
    if (D_597FE0 == 0) {
        func_00105800();
        func_002671C0(&D_597FE0, D_004468C0, D_481EC0);
    }
    return &D_597FE0;
}
