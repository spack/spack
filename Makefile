.PHONY : git pull

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
