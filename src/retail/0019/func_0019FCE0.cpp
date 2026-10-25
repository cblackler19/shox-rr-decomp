extern "C" unsigned short func_0019FCE0(void* object, unsigned int row, unsigned int column) {
    unsigned int offset = column * 2 + (row & 0xFF) * 0x66;
    return *(unsigned short*)((char*)object + offset + 0x838);
}
