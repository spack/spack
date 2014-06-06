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

    versions = {
        '7.4' : '607e135c559be642f210094ad023dc65',
        '7.3' : '5b9510a17074e2b37d8bb38ae09edbf2',
        '7.2' : 'f0901284b338e448bfd79ccca0041254',
        '7.1' : '44c6b4914f38d6f9aa959640b89da329',
        '7.0' : '4ca69757678272f718b1041c810d82d8',
        '6.4' : '774c14d93ce58674b3b2c880edd12d77',
        '6.3' : '821fda8f14d674346b87e3ef9cb96389',
        '6.2' : 'c49d360bbd069d00e2a57804f2a123d9',
        '6.1.405' : 'd220ff58f2c72ed606e6d0297c2f2a7c',
        '6.1' : '7fd0f915adc7c0dab89772884268b030',
        '6.0' : '9d9ca84d489af6b3f54639dd97af3774',
    }

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
