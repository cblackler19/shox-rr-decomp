extern "C" int func_001F0850(void *object)
{
    int result = 0;
    void *first = *(void **)((char *)object + 76);
    if (first)
    {
        void *second = *(void **)((char *)first + 8);
        if (second)
            result = *(int *)((char *)second + 96);
    }
    return result;
}
