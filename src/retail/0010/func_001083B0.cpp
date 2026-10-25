struct func_001083B0_High { int pad[2]; int zero; float one; };
extern "C" void func_001083B0(void *object) {
    *(int *)((char *)object + 0x0C) = 0;
    *(int *)((char *)object + 0x08) = 0;
    *(int *)((char *)object + 0x10) = 0;
    *(int *)((char *)object + 0x34) = 0;
    *(float *)((char *)object + 0x9C) = -1.0f;
    func_001083B0_High *high = (func_001083B0_High *)((char *)object + 0x120);
    high->one = -1.0f;
    high->zero = 0;
}
