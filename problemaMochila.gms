option optcr=0.0001;
Set
i /1 *20/;

Parameters
p(i)/
1 107
2 105
3 81
4 112
5 72
6 115
7 66
8 67
9 70
10 114
11 60
12 111
13 87
14 107
15 98
16 95
17 65
18 104
19 79
20 74
/;

Parameters
b(i)/
1 1967
2 1841
3 1259
4 1347
5 1645
6 1538
7 1812
8 1325
9 1906
10 1782
11 1429
12 1769
13 1053
14 1131
15 1384
16 1461
17 1996
18 82
19 80
20 107
/;

Variable
z;

binary Variable
x(i);

Equations
obj
r1;

obj.. z=E= sum(i, b(i)* x(i));
r1.. sum(i,p(i) * x(i)) =L= 700;

model problemaMochila /all/;
solve problemaMochila using MIP max z;
