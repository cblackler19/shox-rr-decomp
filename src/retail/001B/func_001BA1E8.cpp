struct Object
{
    unsigned int unused[7];
    unsigned int* table;
};

extern "C" void func_001BA1E8(Object* object)
{
    unsigned int* table = object->table;
    unsigned int index = table[0] - 1;
    unsigned char* address = (unsigned char*)table + index * 4;
    unsigned int target = *(unsigned int*)(address + 4);
    *(unsigned char*)target = 1;
}
