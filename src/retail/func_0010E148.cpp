extern "C" float* func_0010E148(float* value, float first, float second) {
    float current = *value;
    if (second < current) {
        *value = second;
        return value;
    }
    if (current < first) {
        *value = first;
    }
    return value;
}
