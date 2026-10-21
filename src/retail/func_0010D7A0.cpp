extern "C" char D_598398[];
extern "C" char D_00447C18[];
extern "C" char D_481EC0[];
extern "C" void *func_00105800(void);
extern "C" void func_002671C0(void *object, const char *name, void *type);

extern "C" void *func_0010D7A0(void) {
    void **instance = (void **)D_598398;
    if (*instance == 0) {
        func_00105800();
        func_002671C0(instance, D_00447C18, D_481EC0);
    }
    return instance;
}