extern "C" char D_5980D0[];
extern "C" char D_00446CE8[];
extern "C" char D_481EC0[];
extern "C" void *func_00105800(void);
extern "C" void func_002671C0(void *object, const char *name, void *type);

extern "C" void *func_0010A1F0(void) {
    void **instance = (void **)D_5980D0;
    if (*instance == 0) {
        func_00105800();
        func_002671C0(instance, D_00446CE8, D_481EC0);
    }
    return instance;
}