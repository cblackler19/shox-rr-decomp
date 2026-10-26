extern "C" void func_00213770(void *first, void *second);
extern "C" void func_00213EE8(void *first, const void *object) {
    func_00213770(first, *(void *const *)((const char *)object + 1624));
}
