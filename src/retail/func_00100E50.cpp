extern "C" const char D_00445F70[];
extern "C" const char D_00445F78[];
extern "C" void func_00100DE0();
extern "C" void func_00100E30();
extern "C" void func_001A56D8(const char*, int, int, void (*)(), int);

extern "C" void func_00100E50() {
    func_001A56D8(D_00445F70, 0, 0, func_00100DE0, 0);
    func_001A56D8(D_00445F78, 0, 0, func_00100E30, 0);
}
