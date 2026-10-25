extern "C" void func_001FA220(void *destination, const void *source) {
    *(int *)((char *)destination + 8) = *(const int *)source;
}
