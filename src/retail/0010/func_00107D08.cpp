extern "C" char D_598040[];
extern "C" char D_00446A48[];
extern "C" char D_481EC0[];
extern "C" void *func_00105800(void);
extern "C" void func_002671C0(void *object, const char *name, void *type);

extern "C" void *func_00107D08(void) {
    void **instance = (void **)D_598040;
    if (*instance == 0) {
        func_00105800();
        func_002671C0(instance, D_00446A48, D_481EC0);
    }
    return instance;
}