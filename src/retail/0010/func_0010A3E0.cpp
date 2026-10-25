extern "C" void func_001A6050(void *object);

extern "C" void func_0010A3E0(void *object, unsigned flags) {
    if (flags & 1)
        func_001A6050(object);
}
