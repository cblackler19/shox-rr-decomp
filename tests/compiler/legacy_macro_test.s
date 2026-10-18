.include "macro_legacy.inc"

.set noreorder
.text

nonmatching test_function, 0x8

glabel test_function
    jr $ra
    nop
endlabel test_function