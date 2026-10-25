typedef unsigned int uint128 __attribute__((mode(TI)));
extern "C" void func_001C1448(void *destination, const void *source) {
    *(uint128 *)((char *)destination + 384) = *(const uint128 *)source;
}
