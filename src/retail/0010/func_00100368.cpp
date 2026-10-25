extern "C" unsigned int D_597BC0[3];
extern "C" const char D_00445ED0[];
extern "C" unsigned int D_481EA0[3];
extern "C" void func_001025E0();
extern "C" void func_002671C0(void*, const char*, void*);

extern "C" unsigned int* func_00100368() {
    if (D_597BC0[0] == 0) {
        func_001025E0();
        func_002671C0(D_597BC0, D_00445ED0, D_481EA0);
    }
    return D_597BC0;
}
