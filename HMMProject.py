import math
import numpy


input1 = "315116246446644245321131631164152133625144543631656626566666"
input2 = "651166453132651245636664631636663162326455235266666625151631"
input3 = "222555441666566563564324364131513465146353411126414626253356"
input4 = "366163666466232534413661661163252562462255265252266435353336"
input5 = "233121625364414432335163243633665562466662632666612355245242"

A = {"FF":0.95, "FL":0.05, "LF": 0.10, "LL":0.90}
B = {"F1":1.0/6, "F2":1.0/6, "F3":1.0/6, "F4":1.0/6, "F5":1.0/6, "F6":1.0/6, "L1":0.1, "L2":0.1, "L3":0.1, "L4":0.1, "L5":0.1, "L6":0.5}
I = {"F":0.5, "L":0.5}

Q,S = set(),set()
for x, y in A.items():
	x_src = x[0]
	x_dst = x[1]
	Q.add(x_src)
	Q.add(x_dst)

for x,y in B.items():
	eq= x[0]
	es = x[1]
	Q.add(eq)
	S.add(es)

Q = sorted(list(Q))
S = sorted(list(S))

qmap = {}
smap = {}

for i in range(len(Q)):
	qmap[Q[i]] = i
for i in range(len(S)):	
	smap[S[i]] = i

len_Q = len(Q);

Anpy = numpy.zeros(shape=(len_Q,len_Q), dtype = float)
for x,y in A.items():
	x_src,x_dst = x[0],x[1]
	Anpy[qmap[x_src],qmap[x_dst]] = y

Anpy /= Anpy.sum(axis=1)[:, numpy.newaxis]

Bnpy = numpy.zeros(shape=(len_Q,len(S)), dtype = float)
for x,y in B.items():
	eq = x[0]
	es = x[1]
	Bnpy[qmap[eq], smap[es]] = y

Bnpy /= Bnpy.sum(axis=1)[:, numpy.newaxis]

Inpy = [0.0] * len(Q)
for x,y in I.items():
	Inpy[qmap[x]] = y

Inpy = numpy.divide(Inpy,sum(Inpy))

Alog = numpy.log2(Anpy)
Blog = numpy.log2(Bnpy)
Ilog = numpy.log2(Inpy)

# SELECT FIRST INPUT AS X
x = input5
x = list(map(smap.get,x))
num_row = len(Q)
num_col = len(x)

prob_mat = numpy.zeros(shape=(num_row,num_col), dtype = float)
back_mat = numpy.zeros(shape =(num_row,num_col), dtype = int)

for i in range(0,num_row):
	prob_mat[i,0] = Blog[i,x[0]] + Ilog[i]

for j in range(1, num_col):
	for i in range(0, num_row):
		ep = Blog[i,x[j]]
		mx = prob_mat[0,j-1] + Alog[0,i] + ep
		mxi = 0
		for k in range(1, num_row):
			pr = prob_mat[k,j-1] + Alog[k,i] + ep
			if pr > mx:
				mx = pr
				mxi = k
		prob_mat[i,j] = mx
		back_mat[i,j] = mxi

omx = prob_mat[0,num_col-1]
omxi = 0

for i in range(1,num_row):
	if prob_mat[i,num_col-1] > omx:
		omx = prob_mat[i,num_col-1]
		omxi = i

i = omxi
p = [omxi]
for j in range(num_col-1,0,-1):
	i = back_mat[i,j]
	p.append(i)
p = ''.join(map(lambda x: Q[x],p[::-1]))

print p
