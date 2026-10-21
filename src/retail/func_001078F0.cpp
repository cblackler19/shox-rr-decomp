extern "C" void func_001A6050(void *object);

extern "C" void func_001078F0(void *object, unsigned flags) {
    if (flags & 1)
        func_001A6050(object);
}
