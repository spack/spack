# (c) 2021 Lawrence Livermore National Laboratory

Set-Location spack

git config --global user.email "spack@example.com"
git config --global user.name "Test User"

if ($(git branch --show-current) -ne "develop")
{
    git branch develop origin/develop
}
