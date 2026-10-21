extern "C" void func_00244008(const char *path);
extern "C" void *func_00242C90(const char *name, int flags);
extern "C" void *func_00243128(const char *name, int flags);
extern "C" int func_0023FBA8(void *object, int group, int resource, int mode, int flags);
extern "C" void func_00240858(short object, int value);
extern "C" void func_00241060(short object, int value);
extern "C" void func_00240A20(short object, int value);
extern "C" void func_00240BF8(short object, int value);
extern "C" void func_00241220(short object, int value);
extern "C" void func_00240EB0(short object, int value);
extern "C" void func_0020CE98(void *object);
extern "C" void func_0020CEE8(void *object);
extern "C" void func_0020CC70(void *object);
extern "C" void func_0020CD60(void *object);
extern "C" int func_00205AB8();
extern "C" void func_00205AA8(int value);
extern "C" const char gfxOSD[9];
extern "C" const char neutralBeacon[11];
extern "C" const char gfxMisc[10];
extern "C" const char shockWaveBand[13];
extern "C" const char spikeName[9];
extern "C" const char atariFalcon[12];
extern "C" unsigned short soundGroup __attribute__((section(".data")));
extern "C" unsigned short alternateSoundGroup __attribute__((section(".data")));
extern "C" unsigned short bandSoundGroup __attribute__((section(".data")));
extern "C" unsigned short carSoundGroup __attribute__((section(".data")));
extern "C" void *audioContext __attribute__((section(".data")));

extern "C" void func_0020B408(void *object)
{
    char *base = (char *)object;
    func_00244008(gfxOSD);
    void *sample = func_00242C90(neutralBeacon, 0x000C0000);
    unsigned short group = soundGroup;
    int sound = func_0023FBA8(sample, group, 0xA311, 0, 0);
    *(short *)(base + 0x40) = sound;
    func_00240858(*(short *)(base + 0x40), 7);
    func_00241060(*(short *)(base + 0x40), 0);
    func_00240A20(*(short *)(base + 0x40), 0);

    func_00244008(gfxMisc);
    unsigned short alternateGroup = alternateSoundGroup;
    sound = func_0023FBA8(audioContext, alternateGroup, 0xACA1, 0, 0);
    *(short *)(base + 0x28) = sound;
    func_00240858(*(short *)(base + 0x28), 7);
    func_00240A20(*(short *)(base + 0x28), 0);

    sound = func_0023FBA8(audioContext, group, 0x3947, 0, 0);
    *(short *)(base + 0x32) = sound;
    func_00240858(*(short *)(base + 0x32), 7);
    func_00240A20(*(short *)(base + 0x32), 0);
    func_00240BF8(*(short *)(base + 0x32), 0);

    sound = func_0023FBA8(audioContext, group, 0x3941, 0, 0);
    *(short *)(base + 0x36) = sound;
    func_00240858(*(short *)(base + 0x36), 7);
    func_00240A20(*(short *)(base + 0x36), 0);

    sound = func_0023FBA8(audioContext, group, 0xB247, 0, 0);
    *(short *)(base + 0x34) = sound;
    func_00240858(*(short *)(base + 0x34), 7);
    func_00240A20(*(short *)(base + 0x34), 0);

    --alternateGroup;
    sound = func_0023FBA8(audioContext, alternateGroup, 0xB247, 0, 0);
    *(short *)(base + 0x3E) = sound;
    func_00240858(*(short *)(base + 0x3E), 7);
    func_00240A20(*(short *)(base + 0x3E), 0);

    int wasEnabled = func_00205AB8();
    func_00205AA8(0);
    void *waveSample = func_00242C90(shockWaveBand, 0x000C0000);
    int wave = func_0023FBA8(waveSample, bandSoundGroup, 0x7247, 0, 0);
    *(short *)(base + 0x38) = wave;
    func_00240858(*(short *)(base + 0x38), 3);
    func_00241060(*(short *)(base + 0x38), 0);
    func_00240A20(*(short *)(base + 0x38), 0);
    func_00205AA8(wasEnabled);

    void *spikeSample = func_00242C90(spikeName, 0x000C0000);
    int spike = func_0023FBA8(spikeSample, group, 0x7247, 0, 0);
    *(short *)(base + 0x3A) = spike;
    func_00240858(*(short *)(base + 0x3A), 7);
    func_00241060(*(short *)(base + 0x3A), 0);
    func_00240A20(*(short *)(base + 0x3A), 0);

    void *bandSample = func_00242C90(shockWaveBand, 0x000C0000);
    int band = func_0023FBA8(bandSample, group, 0x8158, 0, 0);
    *(short *)(base + 0x3C) = band;
    func_00240858(*(short *)(base + 0x3C), 3);
    func_00241060(*(short *)(base + 0x3C), 0);
    func_00240A20(*(short *)(base + 0x3C), 0);

    void *car = func_00243128(atariFalcon, 1);
    unsigned short carIndex = carSoundGroup - 1;
    *(void **)(base + 0x2C) = car;
    int carEvent = func_0023FBA8(car, carIndex, 0xABA1, 0, 0);
    *(short *)(base + 0x30) = carEvent;
    func_00240A20(*(short *)(base + 0x30), 0);
    func_00240858(*(short *)(base + 0x30), 3);
    func_00241060(*(short *)(base + 0x30), 0);
    func_00241220(*(short *)(base + 0x30), 0);
    func_00240EB0(*(short *)(base + 0x30), 0);

    unsigned short i = 0;
    for (; i < 8; ++i) {
        func_0020CE98(base + 0x2B0 + i * 32);
    }

    i = 0;
    for (; i < 256; ++i) {
        func_0020CEE8(base + 0x3B0 + i * 40);
    }

    func_0020CC70(object);
    func_0020CD60(object);
}
