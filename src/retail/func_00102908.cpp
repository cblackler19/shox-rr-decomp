extern "C" void func_001A6050();

extern "C" void func_00102908(void*, int flags) {
    if (flags & 1) {
        func_001A6050();
    }
}
