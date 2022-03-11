# NERSC fork+branch of spack develop branch:

This branch aims to track the 'develop' branch of Spack upstream, but to incorporate
package updates implemented at/for NERSC even before they are available upstream.

This repo includes a patch to support having a central Spack instance, this is in
`nersc-patch` and has been applied here. To apply the patch to a new branch from 
upstream develop, use:

```
patch --dry-run -t -p1 < nersc-patch || echo "error!"
patch -t -p1 < nersc-patch || echo "error!"
```

The workflow for package development at NERSC is:

- clone this repo
- checkout a new branch from `nersc-develop`
- edit and test the package
- commit and push the changes, and make an MR to `nersc-develop`
- once merged, make another MR from `nersc-develop` to the upstream Spack `develop`.
  This MR should have only the changes from your branch, so you might need to 
  cherry-pick 

