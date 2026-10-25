struct Interface_0010F668 {
    char pad[80];
    short adjust;
    short pad82;
    void (*invoke)(void *);
};

struct Object_0010F668 {
    char pad[20];
    Interface_0010F668 *interface;
    char middle[80];
    int value104;
};

extern "C" void func_0010F668(Object_0010F668 *self) {
    self->interface->invoke((char *)self + self->interface->adjust);
    self->value104 = 0;
}
