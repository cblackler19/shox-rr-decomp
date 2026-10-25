struct func_001208C0_Item { unsigned char pad0[8]; float value; unsigned char pad1[0xC]; };
extern "C" float func_001208C0(const func_001208C0_Item* items, int index)
{
    return items[index].value;
}