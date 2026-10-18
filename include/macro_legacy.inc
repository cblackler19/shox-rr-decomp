# Compatibility macros for GNU AS 2.9-ee

.macro glabel name
    .globl \name
    .ent \name
\name:
.endm

.macro endlabel name
    .end \name
.endm

.macro nonmatching name, size
.endm

.macro dlabel name
    .globl \name
\name:
.endm

.macro enddlabel name
.endm

.macro jlabel name
    .globl \name
\name:
.endm

.macro alabel name
    .globl \name
\name:
.endm

.macro ehlabel name
    .globl \name
\name:
.endm