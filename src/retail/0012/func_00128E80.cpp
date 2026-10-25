struct func_00120910_Item { unsigned char pad0[0x10]; float value; unsigned char pad1[4]; };
extern "C" float func_00120910(const func_00120910_Item* items, int index);

extern "C" float func_00128E80(const func_00120910_Item* items, int index) {
    const func_00120910_Item* adjusted = (const func_00120910_Item*)((const char*)items + 12);
    return func_00120910(adjusted, index);
}
