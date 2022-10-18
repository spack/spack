$ErrorActionPreference = "SilentlyContinue"
Write-Output F|xcopy .\share\spack\qa\configuration\windows_config.yaml $env:USERPROFILE\.spack\windows\config.yaml
(Get-Item '.\lib\spack\docs\_spack_root').Delete()
./share/spack/setup-env.ps1