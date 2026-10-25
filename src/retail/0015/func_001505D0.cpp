extern "C" int settingsGlobal_00481F20 __attribute__((section(".data")));

extern "C" void func_001505D0(void *owner, const int *value)
{
    if (value != 0) {
        settingsGlobal_00481F20 = *value;
    }
}
