extern "C" void func_00119838(int unused, int* object) {
    int current = object[12];
    int target = object[11];
    if (current < target) {
        int difference = target - current;
        object[12] = target;
        object[10] += difference;
    }
}
