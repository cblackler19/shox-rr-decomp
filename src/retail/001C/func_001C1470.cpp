typedef unsigned int uint128 __attribute__((mode(TI)));
extern "C" void func_001C1470(void *destination, const void *source) {
    *(uint128 *)((char *)destination + 400) = *(const uint128 *)source;
}
