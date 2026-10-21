extern char D_002E02A0[];
extern "C" int func_00130918(int index) {
    char* record = D_002E02A0 + index * 432;
    return *(int*)(record + 4828) + 1;
}
