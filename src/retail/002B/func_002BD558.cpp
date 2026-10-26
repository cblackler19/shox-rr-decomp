struct GlobalBlock {
    unsigned char unused[11904];
    int input;
};
extern "C" GlobalBlock D_00590000;

extern "C" int *func_002BD558(int value)
{
    int **base = (int **)&D_00590000.input;
    *(int *)base = value;
    base[1] = 0;
    base[3] = (int *)(base + 4);
    base[2] = (int *)(base + 4);
    return (int *)base;
}
