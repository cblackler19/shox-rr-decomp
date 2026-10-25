extern "C" unsigned int* func_00102B58(void* unused, unsigned int** cursor)
{
    unsigned int* current = *cursor;
    unsigned int value = *current;
    *cursor = (unsigned int*)value;
    return (unsigned int*)((char*)current + 8);
}
