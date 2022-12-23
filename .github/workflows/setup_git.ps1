# (c) 2022 Lawrence Livermore National Laboratory

git config --global user.email "spack@example.com"
git config --global user.name "Test User"
git config --global core.longpaths true

# See https://github.com/git/git/security/advisories/GHSA-3wp6-j8xr-qw85 (CVE-2022-39253)
# This is needed to let some fixture in our unit-test suite run
git config --global protocol.file.allow always

if ($(git branch --show-current) -ne "develop")
{
    git branch develop origin/develop
}
