struct Entry { char reserved[4]; float value; int count; };
extern "C" int func_00113788(void* object)
{
    Entry* first = (Entry*)((char*)object + 0x74);
    Entry* second = (Entry*)((char*)object + 0xdc);
    first->count = 28;
    first->value = -1.0f;
    second->count = 28;
    second->value = -1.0f;
    return 1;
}