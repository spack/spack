LPORDDIR = $(topdir)/PORD/lib/
IPORD = -I$(topdir)/PORD/include/
LPORD = -L$(LPORDDIR) -lpord

ORDERINGSC = $(ORDERINGSF)
LORDERINGS = $(LMETIS) $(LPORD) $(LSCOTCH)
IORDERINGSF = $(ISCOTCH)
IORDERINGSC = $(IMETIS) $(IPORD) $(ISCOTCH)

PLAT    =
LIBEXT  = .a
OUTC    = -o 
OUTF    = -o
RM = /bin/rm -f
AR = ar vr 
RANLIB = ranlib

INCSEQ  = -I$(topdir)/libseq
LIBSEQ  = -L$(topdir)/libseq -lmpiseq

INCPAR  =
LIBPAR  = $(SCALAP)

LIBOTHERS = -lpthread

#Preprocessor defs for calling Fortran from C (-DAdd_ or -DAdd__ or -DUPPER)
CDEFS   = -DAdd_

#Sequential:
ifeq ($(MUMPS_TYPE),seq)
INCS = $(INCSEQ)
LIBS = $(LIBSEQ)
LIBSEQNEEDED = libseqneeded
endif

#Parallel:
ifeq ($(MUMPS_TYPE),par)
INCS = $(INCPAR)
LIBS = $(LIBPAR)
LIBSEQNEEDED =
endif
