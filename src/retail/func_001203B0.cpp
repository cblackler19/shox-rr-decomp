extern "C" float func_001203B0(void* object)
{
    char* data = *(char**)((char*)object + 32);
    int index = *(int*)((char*)object + 36);
    *(float*)((char*)object + 44) = *(float*)(data + index * 32 + 20);
    return *(float*)(data + index * 32 + 20);
}
