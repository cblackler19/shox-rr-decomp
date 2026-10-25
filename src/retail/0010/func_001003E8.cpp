extern "C" void* D_002D96C0 __attribute__((section(".data")));
extern "C" unsigned char D_00445EA0[];
extern "C" void* func_001A5F10(unsigned int);
struct Instance;
extern "C" Instance* func_00102628(Instance*);
extern "C" void func_00100448(void*);
struct Instance { unsigned char padding[0x258]; void* descriptor; };
extern "C" Instance* func_001003E8() {
    if (D_002D96C0 == 0) {
        Instance* instance = (Instance*)func_001A5F10(0x25C);
        func_00102628(instance);
        instance->descriptor = D_00445EA0;
        func_00100448(instance);
        D_002D96C0 = instance;
    }
    return (Instance*)D_002D96C0;
}