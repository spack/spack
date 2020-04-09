/* Simple libsigsegv include test 
 *
 * Inspired by libsigsegv's test cases.
 */

#include "sigsegv.h"
#include <stdio.h>
#include <stdlib.h>   /* for exit */
# include <stddef.h>  /* for NULL on SunOS4 */
#include <setjmp.h>   /* for controlling handler-related flow */


jmp_buf mainbuf;

char *message = "Hello, World!";

volatile int handler_called = 0;

static void
handler_continuation(void *arg1, void *arg2, void *arg3)
{
     /* Go back to where we started */
    longjmp(mainbuf, handler_called);
}

int
handler(void *fault_address, int serious)
{
    handler_called++;
    if (handler_called > 2)
        abort();
    printf("Caught sigsegv #%d\n", handler_called);

    return sigsegv_leave_handler(handler_continuation, NULL, NULL, NULL);
}

void printit(char *m)
{
    if (handler_called <= 0)
        /* Force SIGSEGV */
        printf("%s\n", *m);
    else
        /* Print it correctly. */
        printf("%s\n", m);
}

int
main(void)
{
    /* Install the sigsegv handler */
    sigsegv_install_handler(&handler);

    char *msg = "Hello, World!";
    int calls = setjmp(mainbuf);

    /* This will be called multiple times thanks to the handler. */
    printit(msg);

    /* Stop the cycle after the first two calls. */
    if (calls > 1)
        exit(0);

    exit(0);
}
