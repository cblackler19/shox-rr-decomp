struct Entry16 { int value; int padding[3]; };
extern "C" int func_00123330(unsigned char* base, int index) {
    Entry16* entry = (Entry16*)(base + 0x1ECD0);
    entry += index;
    return entry->value < 1;
}
