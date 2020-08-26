/* Simple "Hello World" test set up to handle a single page fault
 *
 * Inspired by libsigsegv's test cases with argument names for handlers
 * taken from the header files.
 */

#include "sigsegv.h"
#include <stdio.h>
#include <stdlib.h>   /* for exit */
# include <stddef.h>  /* for NULL on SunOS4 (per libsigsegv examples) */
#include <setjmp.h>   /* for controlling handler-related flow */


/* Calling environment */
jmp_buf calling_env;

char *message = "Hello, World!";

/* Track the number of times the handler is called */
volatile int times_called = 0;


/* Continuation function, which relies on the latest libsigsegv API */
static void
resume(void *cont_arg1, void *cont_arg2, void *cont_arg3)
{
     /* Go to calling environment and restore state. */
    longjmp(calling_env, times_called);
}

/* sigsegv handler */
int
handle_sigsegv(void *fault_address, int serious)
{
    times_called++;

    /* Generate handler output for the test. */
    printf("Caught sigsegv #%d\n", times_called);

    return sigsegv_leave_handler(resume, NULL, NULL, NULL);
}

/* "Buggy" function used to demonstrate non-local goto */
void printit(char *m)
{
  if (times_called < 1) {
    /* Force SIGSEGV only on the first call. */
    volatile int *fail_ptr = 0;
    int failure = *fail_ptr;
    printf("%s\n", m);
  } else {
    /* Print it correctly. */
    printf("%s\n", m);
  }
}

int
main(void)
{
    /* Install the global SIGSEGV handler */
    sigsegv_install_handler(&handle_sigsegv);

    char *msg = "Hello World!";
    int calls = setjmp(calling_env);  /* Resume here after detecting sigsegv */

    /* Call the function that will trigger the page fault. */
    printit(msg);

    return 0;
}
