extern "C" char D_5983C8[];
extern "C" char D_00447E30[];
extern "C" char D_598100[];
extern "C" void *func_001132B8(void);
extern "C" void func_002671C0(void *object, const char *name, void *type);

extern "C" void *func_0010DC98(void) {
    void **instance = (void **)D_5983C8;
    if (*instance == 0) {
        func_001132B8();
        func_002671C0(instance, D_00447E30, D_598100);
    }
    return instance;
}