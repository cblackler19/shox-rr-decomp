extern "C" void func_0026DD68(unsigned int *object, unsigned int first, unsigned int second) {
    unsigned int flags = object[3] | 0x10000;
    object[15] = first;
    object[10] = second;
    object[3] = flags;
}
