extern "C" char D_598428[];
extern "C" char D_00448550[];
extern "C" char D_598100[];
extern "C" void *func_001132B8(void);
extern "C" void func_002671C0(void *object, const char *name, void *type);

extern "C" void *func_0010FAB0(void) {
    void **instance = (void **)D_598428;
    if (*instance == 0) {
        func_001132B8();
        func_002671C0(instance, D_00448550, D_598100);
    }
    return instance;
}