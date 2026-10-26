extern "C" void func_001A8480(void *destination, const void *source) {
    if (source)
        *(int *)((char *)destination + 8) = *(const int *)((const char *)source + 68);
    else
        *(int *)((char *)destination + 8) = 0;
}
