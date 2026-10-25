extern "C" int func_002CB170();
extern "C" void func_002C8F68(void*);
extern "C" void func_00100C98();

extern "C" void func_00100DE0(void* object) {
    if (object && func_002CB170()) {
        func_002C8F68(object);
    } else {
        func_00100C98();
    }
}
