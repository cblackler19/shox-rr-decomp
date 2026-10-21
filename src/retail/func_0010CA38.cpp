extern "C" char D_598378[];
extern "C" char D_00447968[];
extern "C" char D_481EC0[];
extern "C" void *func_00105800(void);
extern "C" void func_002671C0(void *object, const char *name, void *type);

extern "C" void *func_0010CA38(void) {
    void **instance = (void **)D_598378;
    if (*instance == 0) {
        func_00105800();
        func_002671C0(instance, D_00447968, D_481EC0);
    }
    return instance;
}