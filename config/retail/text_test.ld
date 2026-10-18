INCLUDE "build/retail/undefined_syms_auto.txt"
INCLUDE "build/retail/undefined_funcs_auto.txt"

SECTIONS
{
    . = 0x00100000;

    .text :
    {
        build/retail/asm/retail/text.s.o(.text)
    }

    /DISCARD/ :
    {
        *(.mdebug)
        *(.comment)
    }
}
