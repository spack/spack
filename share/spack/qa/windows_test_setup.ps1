Set-Location ../
if (!(test-path scripts)) {
    mkdir scripts
}
Copy-Item "spack\lib\spack\spack\cmd\installer\scripts\*" "scripts"
Copy-Item "spack\lib\spack\spack\cmd\installer\spack_cmd.bat" "."
$env:python_pf_ver="C:\hostedtoolcache\windows\Python\3.9.5\x64\python.exe"
cmd /c "`".\spack_cmd.bat`" print " |
foreach {
    if ($_ -match "=") {
        $v = $_.split("=")
        [Environment]::SetEnvironmentVariable($v[0], $v[1])
    }
}