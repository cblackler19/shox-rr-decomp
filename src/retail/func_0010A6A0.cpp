extern "C" int func_0010A6A0(void* self, void* target)
{
    typedef void (*Callback)(void*);
    void* previous = 0;
    void* current = *(void**)((char*)self + 4);

    while (current) {
        if (current == target) {
            if (previous == 0) {
                *(void**)((char*)self + 4) = 0;
            } else {
                *(void**)((char*)previous + 8) = *(void**)((char*)current + 8);
            }

            *(int*)((char*)target + 0x0C) = 0;
            *(int*)((char*)target + 0x08) = 0;
            char* table = *(char**)((char*)target + 0x14);
            short offset = *(short*)(table + 0x38);
            Callback callback = *(Callback*)(table + 0x3C);
            callback((char*)target + offset);
            return 1;
        }
        previous = current;
        current = *(void**)((char*)current + 8);
    }
    return 0;
}