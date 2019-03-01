import dyn_tbl as dyn_tbl
import hashes as hashes 
class LDSketch_t(object):
	def __init__(self,w,h,l,thresh_abs,tbl_id):
		self.tbl = []
		self.w = int(w)
		self.h = int(h)
		self.l = int(l)
		#self.lgn=int()
		self.thresh_abs = thresh_abs
		self.tbl_id = int(tbl_id)
		
		for i in range(h*w):
			self.tbl.append(dyn_tbl.dyn_tbl_s(1,64,thresh_abs))

	def LDSketch_find(self,key,row_no):
		return int(hashes.AwareHash(key,row_no),16)%self.w

	def LDSketch_update(self, key, val):
		j = 0
		for j in range(self.h):
			k = self.LDSketch_find(key,j)
			self.tbl[j*self.w+k].dyn_tbl_update(key, val) 

	def LDSketch_write_plaintext(self, output):
		fp = open(output,"w")
		fp.write("of hash row: "+str(self.h)+"\n")
		fp.write("of hash buckets: "+str(self.w)+"\n")
		i = 0
		j = 0
		for i in range(self.h):
			for j in range(self.w):
				index = self.w*i + j
				fp.write(str(self.tbl[index].total)+" "+str(self.tbl[index].size)+" ")
			fp.write("\n")
	def LDSketch_get_heavy_keys(self, thresh, keys, vals, num_key):
		max_array_len = 0
		i = 0
		for i in range (self.w*self.h):
			if self.tbl[i].max_value >= thresh:
				len = self.tbl[i].size
				if len > max_array_len:
					max_array_len = len
		i = 0
		j = 0
		tmp_keys = list()
		tmp_n = 0
		n = 0
		for i in range(self.w*self.h):
			if self.tbl[i].max_value>= thresh:
				tmp_keys = list()
				tmp_keys ,tmp_n= self.tbl[i].dyn_tbl_get_heavy_key(thresh,tmp_keys,tmp_n)
				j=0
				for j in range(tmp_n):
					if tmp_keys[j] in keys:continue
					
					v = self.LDSketch_up_estimate(tmp_keys[j])
					if v >= thresh:
						keys.append(tmp_keys[j])
						vals.append(v)
						n+=1
		num_key = n

	def LDSketch_low_estimate(self, key):
		ret = 0
		for i in range(self.h):
			k = self.LDSketch_find(key, 0)
			index = i*self.w+k
			ret = max(ret, self.tbl[index].dyn_tbl_low_estimate(key))
			return ret
	def LDSketch_up_estimate(self, key):
		k = self.LDSketch_find(key, 0)
		ret = self.tbl[k].dyn_tbl_up_estimate(key)
		i=0
		for i in range(self.h-1):
			k = self.LDSketch_find(key, i+1)
			index = (i+1)*self.w+k
			ret = min(ret, self.tbl[index].dyn_tbl_up_estimate(key))
		return ret#def LDSketch_copy(self, from,to)#def LDSketch_reset(self):
def GetRequest(contain):
	c=contain.split("\n")
	request = c[0].split(" ")
	return c
def ParserRequest(request):
	req = request.split(" ")
	key = req[0]
	value = eval(req[1])
	return key,value

lds = LDSketch_t(10000,4,1,1024,0)
filename = "/home/sdn/rlsketch/dotraffic2000000.txt"
fp = open(filename,"r")
pkt_index = 0

while True:
	if pkt_index >= 1000:break
	contain = fp.readline()
	if not contain:
		continue
	else:
		key,value = ParserRequest(contain)
		if value == 0:
			continue
		else:
			lds.LDSketch_update(key,value)
			pkt_index += 1
