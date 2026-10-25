extern "C" char D_598070[];
extern "C" char D_00446B28[];
extern "C" char D_481EC0[];
extern "C" void *func_00105800(void);
extern "C" void func_002671C0(void *object, const char *name, void *type);

extern "C" void *func_00107FB8(void) {
    void **instance = (void **)D_598070;
    if (*instance == 0) {
        func_00105800();
        func_002671C0(instance, D_00446B28, D_481EC0);
    }
    return instance;
}