$erroractionpreference = "stop"

$VCVARSALL="C:\\Program Files (x86)\\MicroSoft Visual Studio\\2019\\Enterprise\\VC\\Auxiliary\\Build\\vcvars64.bat"
$VCVARSPLATFORM="x64"
$VCVARSVERSION="14.29.30038"


cmd /c "`"$VCVARSALL`" $VCVARSPLATFORM -vcvars_ver=$VCVARSVERSION & set" |
foreach {
    if ($_ -match "=") {
        $v = $_.split("=")
        [Environment]::SetEnvironmentVariable($v[0], $v[1])
    }
}
