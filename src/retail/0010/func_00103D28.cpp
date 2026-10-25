extern "C" void* D_597FD0 __attribute__((section(".data")));
extern "C" void* D_481EB8 __attribute__((section(".data")));
extern "C" unsigned char D_00446840[];
extern "C" unsigned char D_00446858[];
extern "C" void func_002671E0(void*, void*);
extern "C" void func_002671C0(void*, void*, void*);
extern "C" void** func_00103D28() {
    if (D_597FD0 == 0) {
        void** instance = &D_481EB8;
        if (*instance == 0)
            func_002671E0(instance, D_00446840);
        func_002671C0(&D_597FD0, D_00446858, instance);
    }
    return &D_597FD0;
}