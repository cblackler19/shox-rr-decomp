extern "C" char D_5983B8[];
extern "C" char D_00447C98[];
extern "C" char D_481EC8[];
extern "C" void *func_0010AA08(void);
extern "C" void func_002671C0(void *object, const char *name, void *type);

extern "C" void *func_0010D870(void) {
    void **instance = (void **)D_5983B8;
    if (*instance == 0) {
        func_0010AA08();
        func_002671C0(instance, D_00447C98, D_481EC8);
    }
    return instance;
}