extern "C" void func_0026DDA8(unsigned int *object, unsigned int first, unsigned int second) {
    unsigned int flags = object[3] | 0x40000;
    object[15] = first;
    object[13] = second;
    object[3] = flags;
}
