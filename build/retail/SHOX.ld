SECTIONS
{
    HIDDEN(__romPos = 0);
    _gp = 0x489C70;
    elf_header_ROM_START = __romPos;
    elf_header_VRAM = ADDR(.elf_header);
    .elf_header : AT(elf_header_ROM_START)
    {
        FILL(0x00000000);
        elf_header_DATA_START = .;
        build/retail/assets/elf_header.bin.o(.data);
        elf_header_DATA_END = .;
        elf_header_DATA_SIZE = ABSOLUTE(elf_header_DATA_END - elf_header_DATA_START);
    }
    __romPos += SIZEOF(.elf_header);
    elf_header_ROM_END = __romPos;
    elf_header_VRAM_END = .;

    main_ROM_START = __romPos;
    main_VRAM = ADDR(.main);
    .main 0x100000 : AT(main_ROM_START)
    {
        FILL(0x00000000);
        main_TEXT_START = .;
        build/retail/asm/retail/text.s.o(.text);
        . = ALIGN(., 16);
        main_TEXT_END = .;
        main_TEXT_SIZE = ABSOLUTE(main_TEXT_END - main_TEXT_START);
        main_DATA_START = .;
        build/retail/asm/retail/text.s.o(.data);
        build/retail/assets/pad_text_vutext.bin.o(.data);
        build/retail/assets/vutext.bin.o(.data);
        build/retail/assets/pad_vutext_data.bin.o(.data);
        build/retail/asm/retail/data/data.data.s.o(.data);
        build/retail/assets/pad_data_rodata.bin.o(.data);
        build/retail/assets/pad_rodata_except.bin.o(.data);
        build/retail/assets/gcc_except_table.bin.o(.data);
        build/retail/assets/pad_except_lit4.bin.o(.data);
        build/retail/assets/lit4.bin.o(.data);
        build/retail/assets/pad_lit4_sdata.bin.o(.data);
        build/retail/asm/retail/data/sdata.data.s.o(.data);
        build/retail/assets/pad_sdata_end.bin.o(.data);
        . = ALIGN(., 16);
        main_DATA_END = .;
        main_DATA_SIZE = ABSOLUTE(main_DATA_END - main_DATA_START);
        main_RODATA_START = .;
        build/retail/asm/retail/text.s.o(.rodata);
        build/retail/asm/retail/data/rodata.rodata.s.o(.rodata);
        . = ALIGN(., 16);
        main_RODATA_END = .;
        main_RODATA_SIZE = ABSOLUTE(main_RODATA_END - main_RODATA_START);
    }
    main_bss_VRAM = ADDR(.main_bss);
    .main_bss (NOLOAD) :
    {
        FILL(0x00000000);
        main_BSS_START = .;
        build/retail/asm/retail/text.s.o(.bss);
        . = ALIGN(., 16);
        main_BSS_END = .;
        main_BSS_SIZE = ABSOLUTE(main_BSS_END - main_BSS_START);
    }
    __romPos += SIZEOF(.main);
    __romPos = ALIGN(__romPos, 16);
    . = ALIGN(., 16);
    main_ROM_END = __romPos;
    main_VRAM_END = .;

    /DISCARD/ :
    {
        *(*);
    }
}
