extern "C" unsigned short pendingUpdate_00356FB0 __attribute__((section(".data")));

extern "C" int func_00237100()
{
    if (pendingUpdate_00356FB0 != 0) {
        pendingUpdate_00356FB0 = 0;
    }
    return 0;
}
