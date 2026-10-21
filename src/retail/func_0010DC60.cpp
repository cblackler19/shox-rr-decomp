extern "C" char D_00446E60[];
extern "C" void func_001A6050(void*, int);

extern "C" void func_0010DC60(void* object, int flags) {
    void** fields = (void**)object;
    fields[62] = D_00446E60;
    fields[36] = D_00446E60;
    fields[5] = D_00446E60;
    if (flags & 1) {
        func_001A6050(object, flags & 1);
    }
}
