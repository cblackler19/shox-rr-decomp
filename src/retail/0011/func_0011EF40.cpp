struct BufferHandle
{
    unsigned char* pointer;
    unsigned int unused[2];
};

extern "C" BufferHandle D_002FFBBC;

extern "C" void func_0011EF40()
{
    if (D_002FFBBC.pointer) {
        D_002FFBBC.pointer[0] = 0;
        D_002FFBBC.pointer[1] = 0;
    }
}
