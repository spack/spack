Set-Location ../

$env:python_pf_ver="C:\hostedtoolcache\windows\Python\3.9.5\x64\python.exe"

cmd /c "`"spack\bin\spack_cmd.bat`" print " |
foreach {
    if ($_ -match "=") {
        $v = $_.split("=")
        [Environment]::SetEnvironmentVariable($v[0], $v[1])
    }
}
