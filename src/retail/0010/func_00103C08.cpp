extern "C" void *D_481EB8 __attribute__((section(".data")));
extern "C" unsigned char D_00446840[];
extern "C" void func_002671E0(void *target, void *source);
extern "C" void **func_00103C08() {
    if (D_481EB8 == 0)
        func_002671E0(&D_481EB8, D_00446840);
    return &D_481EB8;
}
