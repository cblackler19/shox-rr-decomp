struct func_00120910_Item { unsigned char pad0[0x10]; float value; unsigned char pad1[4]; };
extern "C" float func_00120910(const func_00120910_Item* items, int index)
{
    return items[index].value;
}