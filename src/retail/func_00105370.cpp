extern "C" void *D_597FF0 __attribute__((section(".data")));
extern "C" unsigned int D_481EC0[3];
extern "C" const char D_004468E0[];
extern "C" unsigned int *func_00105800();
extern "C" void func_002671C0(void *, void *, void *);

extern "C" void **func_00105370() {
    if (D_597FF0 == 0) {
        func_00105800();
        func_002671C0(&D_597FF0, (void *)D_004468E0, D_481EC0);
    }
    return (void **)&D_597FF0;
}
