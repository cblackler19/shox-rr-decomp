extern "C" float func_00120328(void* object)
{
    char* data = *(char**)((char*)object + 32);
    int index = *(int*)((char*)object + 36);
    return *(float*)(data + index * 32 + 20);
}
