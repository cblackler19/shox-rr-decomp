extern "C" char D_00446560[];
extern "C" void func_001024E0(void *object, unsigned flags);
extern "C" void func_001A6050(void *object);

extern "C" void func_00102B70(void *object, unsigned flags) {
    *(char **)((char *)object + 0xC) = D_00446560;
    func_001024E0(object, flags);
    if (flags & 1)
        func_001A6050(object);
}