#!/bin/sh

for dossier in $(find ./ -type d)
do 
 echo "going to $dossier"
 cd $dossier

 for fic in $(ls *.flv *.avi *.mp4)
 do
    echo $fic
    sub=${fic%.*}".srt"
    if [ -e $sub ]
    then
	echo "sous-titres deja present"
    else
	echo "telechargement"
	subdown.py $fic $* #1 verbeux, 2 pour encore plus, i pour interactif
    fi
 done
 echo "going back"
 cd -
done