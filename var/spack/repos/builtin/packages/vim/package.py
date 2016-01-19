from spack import *

class Vim(Package):
    """Vim is a highly configurable text editor built to enable efficient text
    editing. It is an improved version of the vi editor distributed with most
    UNIX systems.  Vim is often called a "programmer's editor," and so useful
    for programming that many consider it an entire IDE. It's not just for
    programmers, though. Vim is perfect for all kinds of text editing, from
    composing email to editing configuration files.
    """

    homepage = "http://www.vim.org"
    url      = "ftp://ftp.vim.org/pub/vim/unix/vim-7.4.tar.bz2"
    list_url = "http://ftp.vim.org/pub/vim/unix/"

    version('7.4',     '607e135c559be642f210094ad023dc65')
    version('7.3',     '5b9510a17074e2b37d8bb38ae09edbf2')
    version('7.2',     'f0901284b338e448bfd79ccca0041254')
    version('7.1',     '44c6b4914f38d6f9aa959640b89da329')
    version('7.0',     '4ca69757678272f718b1041c810d82d8')
    version('6.4',     '774c14d93ce58674b3b2c880edd12d77')
    version('6.3',     '821fda8f14d674346b87e3ef9cb96389')
    version('6.2',     'c49d360bbd069d00e2a57804f2a123d9')
    version('6.1.405', 'd220ff58f2c72ed606e6d0297c2f2a7c')
    version('6.1',     '7fd0f915adc7c0dab89772884268b030')
    version('6.0',     '9d9ca84d489af6b3f54639dd97af3774')

    feature_sets = ('huge', 'big', 'normal', 'small', 'tiny')
    for fs in feature_sets:
      variant(fs, default=False, description="Use '%s' feature set" % fs)

    variant('python', default=False, description="build with Python")
    depends_on('python', when='+python')

    variant('ruby', default=False, description="build with Ruby")
    depends_on('ruby', when='+ruby')

    variant('cscope', default=False, description="build with cscope support")
    depends_on('cscope', when='+cscope')

    variant('gui', default=False, description="build with gui (gvim)")
    # virtual dependency?

    def install(self, spec, prefix):
      feature_set = None
      for fs in self.feature_sets:
        if "+" + fs in spec:
          if feature_set is not None:
            tty.error("Only one feature set allowed, both %s and %s specified"
                      % (feature_set, fs))
          feature_set = fs
      if '+gui' in spec:
        if feature_set is not None:
          if feature_set is not 'huge':
            tty.error("+gui variant requires 'huge' feature set, %s was specified"
                      % feature_set)
        feature_set = 'huge'
      if feature_set is None:
        feature_set = 'normal'

      configure_args = []
      configure_args.append("--with-features=" + feature_set)

      if '+python' in spec:
        configure_args.append("--enable-pythoninterp=yes")
      else:
        configure_args.append("--enable-pythoninterp=dynamic")

      if '+ruby' in spec:
        configure_args.append("--enable-rubyinterp=yes")
      else:
        configure_args.append("--enable-rubyinterp=dynamic")

      if '+gui' in spec:
        configure_args.append("--enable-gui=auto")

      if '+cscope' in spec:
        configure_args.append("--enable-cscope")

      configure("--prefix=%s" % prefix, *configure_args)

      make()
      make("install")
