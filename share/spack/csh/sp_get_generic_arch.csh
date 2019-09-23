#!/bin/csh -f
set target="`spack arch --target`"
set os=`spack arch --operating-system`
set plat=`spack arch --platform`
set archs="`spack arch --known-targets | sed -e 's/^/_/' -e 's/  */:/g'`"
foreach line ( $archs )
    set c=( `echo $line | sed -e 's/:/ /g'` )
    if ( $#c > 1 ) then
        if ( "$c[1]" != "_" ) then
            set generic="$c[3]"
        endif
        if ( "$c[2]" == "$target" ) then
            echo "${plat}-${os}-${generic}"
        endif
    endif
end
