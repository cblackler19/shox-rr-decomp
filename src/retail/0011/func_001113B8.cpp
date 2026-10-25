extern "C" void func_001113B8(void* object, void* value) {
    if (value != object) {
        *(void**)((char*)object + 8) = value;
    }
}
