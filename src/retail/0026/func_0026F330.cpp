extern "C" int func_0026F330(void *first, void *second) {
    int *source = *(int **)((char *)second + 196);
    int *destination = *(int **)((char *)first + 4);
    *destination = *source;
    return 1;
}
