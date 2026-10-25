extern "C" void func_00125C28(void* object, unsigned int* index)
{
    unsigned int offset = *index << 2;
    ((int*)((char*)object + offset))[2] = 1;
}
