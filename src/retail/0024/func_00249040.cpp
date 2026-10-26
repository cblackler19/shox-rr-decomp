extern "C" int func_00249040(void *buffer, int row, int column, int flags)
{
    unsigned char *value = (unsigned char *)buffer + 125;
    int index = row * 6 + column;
    value += index;
    int updated = *value | flags;
    *value = (unsigned char)updated;
    return updated;
}
