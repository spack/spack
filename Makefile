.PHONY : git pull

git :
	git pull origin
	git push origin

pull :
	git pull upstream develop
