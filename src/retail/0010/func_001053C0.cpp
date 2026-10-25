extern "C" void *D_598000 __attribute__((section(".data")));
extern "C" unsigned int D_481EC0[3];
extern "C" const char D_00446900[];
extern "C" unsigned int *func_00105800();
extern "C" void func_002671C0(void *, void *, void *);

extern "C" void **func_001053C0() {
    if (D_598000 == 0) {
        func_00105800();
        func_002671C0(&D_598000, (void *)D_00446900, D_481EC0);
    }
    return (void **)&D_598000;
}
