.PHONY : git pull fetch prune sync

git :
	git pull origin
	git push origin

pull :
	git pull upstream develop

fetch :
	git fetch upstream

prune :
	git remote prune origin
	git remote prune upstream

sync :
	rsync -ar --progress --exclude=cudnn var/spack/cache/ root@lb://var/lib/www/spack.pi.sjtu.edu.cn/mirror/
