#include <octave/oct.h>

DEFUN_DLD (helloworld, args, nargout,
           "Hello World Help String")
{
  octave_stdout << "Hello World has "
                << args.length () << " input arguments and "
                << nargout << " output arguments.\n";

  return octave_value_list ();
}
