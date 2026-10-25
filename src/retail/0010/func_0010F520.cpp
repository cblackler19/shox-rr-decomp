extern "C" char D_00446E60[];
extern "C" void func_001A6050(void*, int);

extern "C" void func_0010F520(void* object, int flags) {
    void** fields = (void**)object;
    fields[58] = D_00446E60;
    fields[32] = D_00446E60;
    fields[5] = D_00446E60;
    if (flags & 1) {
        func_001A6050(object, flags & 1);
    }
}
