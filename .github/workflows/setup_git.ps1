# (c) 2021 Lawrence Livermore National Laboratory

Set-Location spack

git config --global user.email "spack@example.com"
git config --global user.name "Test User"
git config --global core.longpaths true

if ($(git branch --show-current) -ne "develop")
{
    git branch develop origin/develop
    git branch releases/v0.18 origin/releases/v0.18
}
