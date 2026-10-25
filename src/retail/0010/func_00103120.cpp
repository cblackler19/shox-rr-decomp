struct InitState {
    unsigned int initialized;
    unsigned int reserved[3];
};

extern "C" InitState D_481EB0;
extern "C" char D_004467C0[];
extern "C" void func_002671E0(void*, void*);

extern "C" void* func_00103120() {
    if (D_481EB0.initialized == 0) {
        func_002671E0(&D_481EB0, D_004467C0);
    }
    return &D_481EB0;
}
