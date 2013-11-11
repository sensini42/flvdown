#!/bin/sh

for fic in $(find . -name "*.flv" -o -name "*.avi" -o -name "*.mp4")
do
  fic=${fic#./*}
  if [ $1 ]
  then
    echo $fic
  fi
  sub=${fic%.*}".srt"
  if [ -e $sub ]
  then
    if [ $1 ]
    then
      echo "sous-titres deja present"
    fi
  else
    if [ $1 ]
    then
      echo "telechargement"
    fi
    /home/fred/monbin/flvdown/util/subdown.py $fic $* #1 verbeux, 2 pour encore plus, i pour interactif
		if [ -e $sub ]
		then	
			if [ $1 ]
			then
				echo "telechargement reussi"
			fi	
		else
			echo "$sub : telechargement echoue"
		fi	
  fi
done
