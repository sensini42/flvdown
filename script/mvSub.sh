delay=$1
fic=$2
tmpfile=tempfile
exec 3>&1
exec 1>>$tmpfile
awk -F'[:, ]' '/-->/{
   h1 = $1;
   m1 = $2;
   s1 = $3;
   ms1 = $4;
   
   h2 = $6;
   m2 = $7;
   s2 = $8;
   ms2 = $9;
   
   nt1 = h1*3600 + m1*60 + s1 + ms1/1000 + '$delay';
   nt2 = h2*3600 + m2*60 + s2 + ms2/1000 + '$delay';
   h1 = int(nt1/3600);
   m1 = int((nt1-(3600*h1))/60);
   s1 = int(nt1 - (3600*h1) - (60*m1));
   ms1 = int(1000*(nt1 - (3600*h1) - (60*m1) - s1));

   h2 = int(nt2/3600);
   m2 = int((nt2-(3600*h2))/60);
   s2 = int(nt2 - (3600*h2) - (60*m2));
   ms2 = int(1000*(nt2 - (3600*h2) - (60*m2) - s2));
   
   
   new = sprintf("%02d:%02d:%02d,%03d --> %02d:%02d:%02d,%03d", h1, m1, s1, 
	 			ms1, h2, m2, s2, ms2)
   }
{if(new){print new;new=""}else{print}}
' $fic
exec 1>&3
mv -f $tmpfile $fic
rm -f $tmpfile
