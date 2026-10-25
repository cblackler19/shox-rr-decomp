extern "C" void func_00120930(void *object, int first, int second) {
    *(int *)object = first;
    *(int *)((char *)object + 4) = second;
}
