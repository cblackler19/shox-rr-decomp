extern "C" void func_00113530(void*);
extern "C" void func_001134A0(void*, int, int);
extern "C" void func_00112E70(void*);

extern "C" void func_0010F7D8(void* object, int first, int second) {
    void* component = static_cast<unsigned char*>(object) + 0x6C;
    func_00113530(component);
    func_001134A0(component, first, second);
    func_00112E70(component);
}
