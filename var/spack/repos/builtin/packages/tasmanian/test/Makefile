include ./Makefile.in

IADD=-I$(TASMANIAN_ROOT)/include  $(CommonIADD)
LADD=-L$(TASMANIAN_ROOT)/lib  $(CommonLADD)
LIBS=$(TASMANIAN_ROOT)/lib/libtasmaniansparsegrid.a $(CommonLIBS)


GTONJ = gridtest_main.o tasgridTestFunctions.o tasgridExternalTests.o tasgridUnitTests.o tasgridTestInterfaceC.o

WROBJ = dreamtest_main.o tasdreamExternalTests.o

LIBNAME = $(TASMANIAN_ROOT)/lib/libtasmaniandream.a

EXECNAME = dreamtest
TESTNAME = gridtest

%.o: %.cpp $(LHEADERS)
	$(CC) $(OPTC) $(IADD) -c $< -o $@

all: $(EXECNAME) $(TESTNAME)


$(EXECNAME):  $(LIBNAME) $(WROBJ)
	$(CC) $(OPTL) $(LADD) -L. $(WROBJ) -o $(EXECNAME) $(LIBNAME) $(LIBS)

$(TESTNAME):  $(LIBNAME) $(GTONJ)
	$(CC) $(OPTL) $(LADD) -L. $(GTONJ) -o $(TESTNAME) $(LIBNAME) $(LIBS)


clean:
	rm -fr *.o
	rm -fr $(EXECNAME)
	rm -fr $(TESTNAME)
