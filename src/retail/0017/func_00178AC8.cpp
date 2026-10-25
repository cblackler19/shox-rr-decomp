extern "C" void func_00178AC8(void* object) {
    char* base = (char*)object;
    unsigned int ptr4 = (unsigned int)(base + 4);
    unsigned int ptr1C = (unsigned int)(base + 0x1C);
    unsigned int ptr34 = (unsigned int)(base + 0x34);

    *(unsigned int*)(base + 0x4C) = ptr4;
    *(unsigned int*)(base + 0x54) = ptr34;
    *(unsigned int*)(base + 0x50) = ptr1C;
    *(unsigned int*)(base + 0x190) = 0;
}
