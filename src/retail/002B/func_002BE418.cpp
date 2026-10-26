extern "C" void func_002BE418(int *source, void *destination) {
    int *base = *(int **)((char *)destination + 28);
    base[source[4]] = source[5];
}
