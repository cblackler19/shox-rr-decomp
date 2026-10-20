struct func_001208F0_Item { unsigned char pad0[0xC]; float value; unsigned char pad1[8]; };
extern "C" float func_001208F0(const func_001208F0_Item* items, int index)
{
    return items[index].value;
}