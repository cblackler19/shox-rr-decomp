extern "C" char D_598030[];
extern "C" char D_004469F8[];
extern "C" char D_481EC0[];
extern "C" void *func_00105800(void);
extern "C" void func_002671C0(void *object, const char *name, void *type);

extern "C" void *func_00107AD8(void) {
    void **instance = (void **)D_598030;
    if (*instance == 0) {
        func_00105800();
        func_002671C0(instance, D_004469F8, D_481EC0);
    }
    return instance;
}