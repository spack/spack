LPORDDIR = $(topdir)/PORD/lib/
IPORD = -I$(topdir)/PORD/include/
LPORD = -L$(LPORDDIR) -lpord

ORDERINGSC = $(ORDERINGSF)
LORDERINGS = $(LMETIS) $(LPORD) $(LSCOTCH)
IORDERINGSF = $(ISCOTCH)
IORDERINGSC = $(IMETIS) $(IPORD) $(ISCOTCH)

PLAT    =
OUTC    = -o
OUTF    = -o
RM = /bin/rm -f

INCSEQ  = -I$(topdir)/libseq
LIBSEQ  = -L$(topdir)/libseq -lmpiseq

INCPAR  =
LIBPAR  = $(SCALAP)

LIBOTHERS = -lpthread

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
