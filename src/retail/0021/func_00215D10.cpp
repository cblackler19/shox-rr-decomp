extern "C" void func_00215D30(void *object);
extern "C" void func_00215D10(void *object, int value) {
    *(int *)((char *)object + 64) = value;
    func_00215D30(object);
}
