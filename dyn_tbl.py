import Counter as cou
class dyn_tbl_s (object):
	#/// associative array: A(i,j)
	#std::unordered_map<dyn_tbl_key_t, long long, dyn_tbl_key_hash, dyn_tbl_key_eq> array;
         def __init__(self,length,lgn,T):
                  self.array=dict()
	#/// total sum: V(i,j)
                  self.total=0
	#/// maximum length of counters allowed, exceeding this value would trigger expansion: l(i, j)
                  self.max_len=length
	#/// total number of decrement: e(i, j)
                  self.decrement=0
	#/// expansion parameter: T
                  self.T=T
	#/// maximum sum among keys, to speed up detection
                  self.max_value=0
	 #/// length of keys
                  self.lgn=lgn;
   #/// size of the bucket
         @property
         def size(self):
            return len(self.array)
         def dyn_tbl_get_heavy_key(self, thresh,keys,num_key):
                  bias = self.decrement;
                  thresh = thresh - bias;
                  #//for(std::unordered_map<dyn_tbl_key_t, long long>::iterator it = dyn_tbl->array.begin(); it != dyn_tbl->array.end(); ++it) {
                  kvitems = self.array.items()
                  for keyt,value in kvitems:
                           if value >=thresh:
                                    #print(keyt,value)
                                    keys.append(keyt)
                  num_key = len(keys)
                  return keys,num_key
         def dyn_tbl_low_estimate(self, key_str) :
                  key = key_str
                  if key in self.array:
                           return self.array[key]
                  else:
                           return 0

         def dyn_tbl_up_estimate(self, key_str):
                  ret = 0
                  key = key_str
                  if key in self.array:
                           ret = self.array[key]
                  bias = self.decrement
                  return ret + bias
                  
         def dyn_tbl_reset(self):
                  self.array.clear()
                  self.decrement = 0
                  self.total = 0
                  self.max_value = 0
         def dyn_tbl_length(self) :
                  return len(self.array)

         def dyn_tbl_copy(self,dyn_tbl_from, dyn_tbl_to) :
                  dyn_tbl_to.array = dyn_tbl_from.array
                  dyn_tbl_to.decrement = dyn_tbl_from.decrement
                  dyn_tbl_to.total = dyn_tbl_from.total
                  dyn_tbl_to.max_len = dyn_tbl_from.max_len
                  dyn_tbl_to.max_value = dyn_tbl_from.max_value
         def dyn_tbl_print(self):
                  # open a file
                #  file fp = open(output, "w")
                  Len = len(self.array)
                  #fp.write("length: %u max_length:%u\n", len,dyn_tbl->max_len));
                  print("length:{} max_length{}".format(Len,self.max_len))
                  kvitems = self.array.items()
                  for key,value in kvitems:
                           print(key,value)

                  #close(fp)
         def dyn_tbl_fprint(sel,output):
                  # open a file
                  fp = open(output, "a+")
                  Len = len(self.array)
                  temp_str="length: "+str(Len)+" max_length:"+str(self.max_len)+"\n"
                  fp.write(temp_str)
                  #print("length:{} max_length{}".format(Len,dyn_tbl.max_len))
                  kvitems = self.array.items()
                  #for key,value in kvitems:
                    #       print(key,value)
                  for key,value in kvitems:
                           temp_str = key+" "+str(value)+"\n"
                           fp.write(temp_str)
                  fp.close()
                  
         def dyn_tbl_update(self, key_str, val):
                  key=key_str
                  self.total += val
                  if key in self.array:
                           self.array[key] += val
                  else:
                           frac = int(self.total / self.T)
                           if (len(self.array) < self.max_len) :
                                    self.array[key] = val
                           elif (self.max_len < (frac + 1)*(frac + 2) - 1):
                                    self.max_len = (frac + 1)*(frac + 2) - 1
                                    self.array[key] = val
                                   
                           else:
                                    min_key=min( self.array , key=self.array.get)
                                    min_val = self.array[min_key]
                                    
                                    if min_val>val:
                                             min_val = val

                                    self.decrement += min_val
                                    
                                    delkey=list()
                                    existkey=list()
                                    kvitems=self.array.items()
                                    for keyt,value in kvitems:
                                             if value-min_val <= min_val:
                                                      delkey.append(keyt)
                                             else:
                                                      existkey.append(keyt)
                                    for keyt in delkey:
                                             self.array.pop(keyt)
                                    for keyt in existkey:
                                             self.array[keyt]-=min_val
                                    if min_val<val:
                                             if(len(self.array)>=self.max_len):
                                                      print("Warning: maj tbl update error")
                                                      print(key,value,len(self.array),self.max_len)
                                             self.array[key] = val - min_val
                                       

                  value = 0
                  if key in self.array:
                           value = self.array[key] + self.decrement
                  else :
                           value = self.decrement
                  if value > self.max_value:
                           self.max_value = value;
