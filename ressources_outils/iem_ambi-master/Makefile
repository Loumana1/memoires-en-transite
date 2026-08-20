#!/usr/bin/make -f
# Makefile to the 'iem_ambi' library for Pure Data.
# Needs Makefile.pdlibbuilder as helper makefile for platform-dependent build
# settings and rules (https://github.com/pure-data/pd-lib-builder).

lib.name = iem_ambi

## iemlib.h lives in include/
cflags  = -Iinclude

# special file that does not provide a class
lib.setup.sources = src/$(lib.name).c

# all other C and C++ files in subdirs are source files per class
# (alternatively, enumerate them by hand)
# class.sources = $(filter-out $(lib.setup.sources),$(wildcard src/*.c))

class.sources = \
	src/ambi_decode.c \
	src/ambi_decode2.c \
	src/ambi_decode3.c \
	src/ambi_decode_cube.c \
	src/ambi_encode.c \
	src/ambi_rot.c \
	src/bin_ambi_calc_HRTF.c \
	src/bin_ambi_reduced_decode.c \
	src/bin_ambi_reduced_decode_fft.c \
	src/bin_ambi_reduced_decode_fft2.c \
	src/bin_ambi_reduced_decode_fir.c \
	src/bin_ambi_reduced_decode_fir2.c \
	src/bin_ambi_reduced_decode2.c \
	src/matrix_mul_line~.c \
	src/matrix_mul_line8~.c \
	src/matrix_mul_stat~.c \
	src/matrix_diag_mul_line~.c \
	src/matrix_diag_mul_line8~.c \
	src/matrix_diag_mul_stat~.c \
	src/matrix_bundle_line~.c \
	src/matrix_bundle_line8~.c \
	src/matrix_bundle_stat~.c \
	$(empty)

datafiles = \
	$(wildcard *.txt) \
	$(wildcard *.pdf) \
	$(wildcard *.pd) \
	$(wildcard *.gif) \
	$(wildcard *.bat) \
	$(wildcard *.sh) \
	$(wildcard *.wav) \
	$(empty)


#cflags = -DVERSION=$(shell cat VERSION.txt)

## build a multi-object library
make-lib-executable=yes

## suppress "unused" warnings
#suppress-wunused=yes

################################################################################
### pdlibbuilder ###############################################################
################################################################################

# This Makefile is based on the Makefile from pd-lib-builder written by
# Katja Vetter. You can get it from:
# https://github.com/pure-data/pd-lib-builder
PDLIBBUILDER_DIR=pd-lib-builder/
include $(firstword $(wildcard $(PDLIBBUILDER_DIR)/Makefile.pdlibbuilder Makefile.pdlibbuilder))
