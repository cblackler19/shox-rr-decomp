extern "C" char D_0032B550[];
extern "C" void func_001A1CA0(void *manager, int id, void *object);

extern "C" void func_001079D8(void *object) {
    func_001A1CA0(*(void **)D_0032B550, 3, object);
    func_001A1CA0(*(void **)D_0032B550, 0x2F, (char *)object + 0x6870);
}