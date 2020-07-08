# AC_SEARCH_GSL(actionIfFound, actionIfNotFound)
AC_DEFUN([AC_SEARCH_GSL],[
  AC_ARG_WITH([gsl], AC_HELP_STRING(--with-gsl, [path to GSL library and header files]))

  ## Use a specified --with-gsl arg to set basic paths, if provided
  GSLCONFIG_PATH=$PATH
  if test -e "$with_gsl"; then
    GSLCONFIG_PATH="$with_gsl/bin:$GSLCONFIG_PATH"
    GSLPATH="$with_gsl"
    GSLINCPATH="$GSLPATH/include"
    GSLLIBPATH="$GSLPATH/lib"
    GSL_CPPFLAGS="-I$GSLINCPATH"
    GSL_CXXFLAGS=""
    GSL_LDFLAGS="-L$GSLPATH/lib -lgsl -lgslcblas -lm"
  fi

  ## Try to do better, using the gsl-config script
  AC_PATH_PROG(GSLCONFIG, gsl-config, [], [$GSLCONFIG_PATH])
  if test -x "$GSLCONFIG"; then
    AC_MSG_NOTICE(Using $GSLCONFIG to find GSL flags)
    GSLPATH=`$GSLCONFIG --prefix`
    GSLINCPATH="$GSLPATH/include"
    GSLLIBPATH="$GSLPATH/lib"
    GSL_CPPFLAGS=`$GSLCONFIG --cflags`
    GSL_CXXFLAGS=`$GSLCONFIG --cflags`
    GSL_LDFLAGS=`$GSLCONFIG --libs`
  fi

  ## If it's worked, propagate the conditionals and execute success arg
  if test -e "$GSLPATH"; then
    AM_CONDITIONAL([WITH_GSL], true)
    AM_CONDITIONAL([WITH_GSLLIB], true)
    AM_CONDITIONAL([WITH_GSLINC], true)
    AM_CONDITIONAL([WITHOUT_GSL], false)
    AM_CONDITIONAL([WITHOUT_GSLLIB], false)
    AM_CONDITIONAL([WITHOUT_GSLINC], false)
    $1
  else
    ## Otherwise execute the fail arg
    AM_CONDITIONAL([WITH_GSL], false)
    AM_CONDITIONAL([WITH_GSLLIB], false)
    AM_CONDITIONAL([WITH_GSLINC], false)
    AM_CONDITIONAL([WITHOUT_GSL], true)
    AM_CONDITIONAL([WITHOUT_GSLLIB], true)
    AM_CONDITIONAL([WITHOUT_GSLINC], true)
    $2
  fi

  ## Propagate path and flag variables
  AC_SUBST([GSLPATH])
  AC_SUBST([GSLINCPATH])
  AC_SUBST([GSLLIBPATH])
  AC_SUBST([GSL_CPPFLAGS])
  AC_SUBST([GSL_CXXFLAGS])
  AC_SUBST([GSL_LDFLAGS])
  AC_MSG_NOTICE([GSL include path is $GSLINCPATH])
  AC_MSG_NOTICE([GSL CPPFLAGS is $GSL_CPPFLAGS])
  AC_MSG_NOTICE([GSL CXXFLAGS is $GSL_CXXFLAGS])
  AC_MSG_NOTICE([GSL LDFLAGS is $GSL_LDFLAGS])
])
