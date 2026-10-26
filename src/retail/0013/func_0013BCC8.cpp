struct Entry_0013BCC8 { unsigned int index; int value; };
extern "C" void func_0013BCC8(int *base, const Entry_0013BCC8 *entry)
{
    if (entry && entry->index < 6) {
        int *location = base;
        location += entry->index;
        location += 2;
        *location = entry->value;
    }
}
