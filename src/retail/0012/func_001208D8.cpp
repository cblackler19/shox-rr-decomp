struct func_001208D8_Item { unsigned char pad0[8]; float value; unsigned char pad1[0xC]; };
extern "C" void func_001208D8(func_001208D8_Item* items, int index, float value)
{
    items[index].value = value;
}