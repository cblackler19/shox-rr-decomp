extern "C" char D_00446E60[];
extern "C" void func_001A6050(void *, int);

extern "C" void func_001129A0(void *object, int flags) {
    void **fields = (void **)object;
    fields[69] = D_00446E60;
    fields[43] = D_00446E60;
    fields[12] = D_00446E60;
    fields[5] = D_00446E60;
    if (flags & 1) {
        func_001A6050(object, flags & 1);
    }
}
