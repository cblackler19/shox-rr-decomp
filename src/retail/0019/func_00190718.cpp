extern "C" void func_00190718(void *dst, int index) {
    *(unsigned char *)dst = (unsigned char)(index << 4);
    *(int *)((char *)dst + 8) = 1;
}
