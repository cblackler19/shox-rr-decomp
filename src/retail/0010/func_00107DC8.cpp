extern "C" char D_0032B550[];
extern "C" void func_001A1B10(void *manager, int id, void *object, int flags);
extern "C" void func_00107E08(void *object);

extern "C" void func_00107DC8(void *object) {
    func_001A1B10(*(void **)D_0032B550, 0x1C, object, 0);
    func_00107E08(object);
}