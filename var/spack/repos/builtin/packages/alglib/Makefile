CC = $(SPACK_CXX)
CFLAGS = -fPIC -Wall -O2 -g
LDFLAGS = -shared
RM = rm -f
TARGET_LIB = libalglib.so

SRCS = $(wildcard *.cpp)
OBJS = $(SRCS:.cpp=.o)

%.o: %.cpp
	$(CC) -c ${CFLAGS} $<

.PHONY: all
all: $(OBJS)
	$(CC) ${LDFLAGS} -o ${TARGET_LIB} $^

# do not look for "clean", consider it always as missing
.phony: clean
clean:
	${RM} *.o
