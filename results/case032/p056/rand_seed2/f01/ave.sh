#!/bin/bash

sl=1000
el=1800

if [ $# -eq 1 ]; then
	sl=$1
elif [ $# -eq 2 ]; then
	sl=$1
	el=$2
fi

cat values.dat | awk "NR==$sl,NR==$el{print}" > tmp1.dat
cat tmp1.dat
cat tmp1.dat | awk '{print $2}' > tmp2.dat
cat tmp1.dat | awk '{print $3}' > tmp3.dat
cat tmp1.dat | awk '{print $4}' > tmp4.dat
cat tmp1.dat | awk '{print $5}' > tmp5.dat
cat tmp1.dat | awk '{print $6}' > tmp6.dat
cat tmp1.dat | awk '{print $7}' > tmp7.dat
cat tmp1.dat | awk '{print $8}' > tmp8.dat
cat tmp1.dat | awk '{print $9}' > tmp9.dat

{
	cat tmp2.dat
} | awk '
	{
		sum += $1
	}
	END{
		printf "%.16e\n", sum / NR
	}
'

{
	cat tmp3.dat
} | awk '
	{
		sum += $1
	}
	END{
		printf "%.16e\n", sum / NR
	}
'

{
	cat tmp4.dat
} | awk '
	{
		sum += $1
	}
	END{
		printf "%.16e\n", sum / NR
	}
'

{
	cat tmp5.dat
} | awk '
	{
		sum += $1
	}
	END{
		printf "%.16e\n", sum / NR
	}
'

{
	cat tmp6.dat
} | awk '
	{
		sum += $1
	}
	END{
		printf "%.16e\n", sum / NR
	}
'

{
	cat tmp7.dat
} | awk '
	{
		sum += $1
	}
	END{
		printf "%.16e\n", sum / NR
	}
'

{
	cat tmp8.dat
} | awk '
	{
		sum += $1
	}
	END{
		printf "%.16e\n", sum / NR
	}
'

{
	cat tmp9.dat
} | awk '
	{
		sum += $1
	}
	END{
		printf "%.16e\n", sum / NR
	}
'

rm tmp*.dat
