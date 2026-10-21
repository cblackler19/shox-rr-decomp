extern "C" void func_00111840(char** cursor, char* destination) {
    __builtin_memcpy(destination, *cursor, 4);
    *cursor += 4;
}
