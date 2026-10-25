extern "C" char D_598060[];
extern "C" char D_00446B10[];
extern "C" char D_481EC0[];
extern "C" void *func_00105800(void);
extern "C" void func_002671C0(void *object, const char *name, void *type);

extern "C" void *func_00107F68(void) {
    void **instance = (void **)D_598060;
    if (*instance == 0) {
        func_00105800();
        func_002671C0(instance, D_00446B10, D_481EC0);
    }
    return instance;
}