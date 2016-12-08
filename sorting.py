# (IF969) Algoritmos e Estruturas de Dados
# 3o projeto de implementacao - analise experimental de algoritmos
# Autor: Vinicius Giles Costa (vgcp@cin.ufpe.br)

import time
import random
import numpy as np
from ggplot import *
from pandas import DataFrame

class Sorting:
	def insertionSort(self, v, n):
		startTime = time.time()
		for i in range(1,n):
			element = v[i]
			j = i-1
			while j >= 0 and v[j] > element:
				v[j+1] = v[j]
				j -= 1
			v[j+1] = element
		return time.time() - startTime

	def quickSort(self, v, n):
		startTime = time.time()
		self.__qs(v,0,n)
		return time.time() - startTime

	def __qs(self,v,f,l):
		if f < l:
			j = self.__qsPart(v, f, l)
			self.__qs(v,f, j-1)
			self.__qs(v,j+1,l)

	def __qsPart(self, v, esq, dir):
		'''Funcao de particao'''
		# pivo aleatorio
		self.__swap(v, esq, random.randint(esq,dir))
		p = v[esq]; i = esq+1; j = dir
		while i <= j:
			if v[i] <= p: i+=1
			elif p < v[j]: j-=1
			else:
				self.__swap(v, i, j)
				i+=1; j-=1
		v[esq] = v[j]
		v[j] = p
		return j

	def __swap(self, v, e1, e2):
		aux = v[e1]
		v[e1] = v[e2]
		v[e2] = aux

	def radixSort(self, v, n, d=8):
		startTime = time.time()
		buckets = [[] for i in range(10)]
		for digit in range(1,d+1):
			for element in v:
				ld = self.__digit(element, digit)
				buckets[ld].append(element)
			i = 0
			for l in buckets:
				for element in l: v[i] = element; i+=1
			buckets = [[] for i in range(10)]
		return time.time() - startTime

	def __digit(self, n, d):
		'''Retorna d-esimo digito do numero n'''
		return (n % 10**d) // 10**(d-1)

class Experiment:
	def __init__(self):
		self.qdata, self.rdata, self.idata = list(), list(), list()
		self.tipoVetores = {-1: 'decrescentes', 0: 'aleatórios', 1: 'crescentes'}
		self.__startTime, self.__endTime = None, None

	def reset(self):
		'''Limpa os dados obtidos'''
		self.qdata, self.rdata, self.idata = list(), list(), list()

	def getCurrentTime(self):
		'''Retorna dia e hora para formatacao no nome dos arquivos gerados'''
		return '{0} {1}'.format(time.strftime("%d-%m-%Y"), time.strftime("%H:%M:%S"))

	def generate(self, size, x):
		'''Gera um vetor com tamanho solicitado em size. 
			x = 1: vetor em ordem crescente.
			x = 0: vetor aleatorio
			x = -1: vetor em ordem decrescente '''
		if x > 0: # crescente
			return list(range(size))
		elif x < 0: # decrescente
			return list(range(size-1,-1,-1))
		else: # aleatorio
			return random.sample(range(size), size)

	def __getSortingTime(self, sort, v, n, name, i=False):
		'''Ordena 10 vezes e tira o tempo medio e desvio padrao. 
			- sort: 	funcao de ordenacao
			- v: 		vetor
			- n: 		tamanho do vetor
			- name:		string com nome do algoritimo'''
		print('Ordenando vetor de {0} com {1}... xxxx'.format(n+1, name), end='', flush=True)
		total = list()
		vec = v[:] # copia do vetor
		for i in range(1,11):
			print('\b\b\b\b'+str(i*10)+'% ',end='', flush=True)
			total.append(sort(vec, n))
			vec = v[:]
		print('[OK]')
		return np.mean(total), np.std(total)

	def __saveToTxt(self, dList, desc):
		'''Salva dados em arquivo txt'''
		filetime = '[{0}]'.format(self.__startTime)
		#### dataframes para txt ####
		with open('DataFrames '+filetime+'.txt', 'a') as f:
			f.write('####### {0} #######\n'.format(desc))
			f.write(str(dList) + '\n\n')
		
	def __saveToHtml(self, dframe, desc):
		'''Salva dados em tabelas de HTML para melhor visualizacao'''
		filetime = '[{0}]'.format(self.__startTime)
		### tabelas para html ###
		with open('Experimento '+filetime+'.html', 'a') as f:
			gpath = '{0}[{1}].png'.format(desc,self.__startTime)
			f.write("<h3>{title}</h3><br/><a href='{path}'><img src='{path}' width='500'/></a>".format(title=desc, path=gpath))
			f.write(dframe.to_html(col_space=120,index=False,float_format=lambda x: '{:.10f}s'.format(x)))

	def __plot(self, dframe, desc):
		'''Plota o grafico do data frame'''
		plt = ggplot(dframe, aes('Tamanho', 'Tempo')) + geom_point(size=45) + stat_smooth(color='dodgerblue') + \
		ggtitle(desc) + xlab("Nº de elementos no vetor") + ylab("Tempo (segundos)")
		plt.save(filename=desc+'[{0}].png'.format(self.__startTime), dpi=500)

	def totalTime(self):
		return self.__startTime, self.__endTime

	def test(self, s):
		self.__startTime = self.getCurrentTime()
		for t in self.tipoVetores: # -1 decrescente, 0 aleatorio, 1 crescente
			for size in range(5000, 100001, 5000):
				vetor = self.generate(size, t) # novo vetor
				# Quick sort
				quickTime, stdev = self.__getSortingTime(s.quickSort, vetor, size-1, 'quicksort')
				self.qdata.append({'Tamanho': size, 'Tempo': quickTime, 'desvio padrão': stdev})
				# Radix sort
				radixTime, stdev = self.__getSortingTime(s.radixSort, vetor, size-1, 'radix sort')
				self.rdata.append({'Tamanho': size, 'Tempo': radixTime, 'desvio padrão': stdev})
				# Insertion sort
				inserTime, stdev = self.__getSortingTime(s.insertionSort, vetor, size-1, 'insertion sort', True)
				self.idata.append({'Tamanho': size, 'Tempo': inserTime, 'desvio padrão': stdev})
				
			# Salva os dataframes em arquivos texto e html. plota os graficos
			quickData = DataFrame(self.qdata)
			self.__plot(quickData, 'Quick sort - vetores {0}'.format(self.tipoVetores[t]))
			self.__saveToTxt(self.qdata, 'Quick sort - vetores {0}'.format(self.tipoVetores[t]))
			self.__saveToHtml(quickData, 'Quick sort - vetores {0}'.format(self.tipoVetores[t]))

			radixData = DataFrame(self.rdata)
			self.__plot(radixData, 'Radix sort - vetores {0}'.format(self.tipoVetores[t]))
			self.__saveToTxt(self.rdata, 'Radix sort - vetores {0}'.format(self.tipoVetores[t]))
			self.__saveToHtml(radixData, 'Radix sort - vetores {0}'.format(self.tipoVetores[t]))

			inserData = DataFrame(self.idata)
			self.__plot(inserData, 'Insertion sort - vetores {0}'.format(self.tipoVetores[t]))
			self.__saveToTxt(self.idata, 'Insertion sort - vetores {0}'.format(self.tipoVetores[t]))
			self.__saveToHtml(inserData, 'Insertion sort - vetores {0}'.format(self.tipoVetores[t]))

			self.reset() # apaga os dados
		self.__endTime = self.getCurrentTime()

######## EXPERIMENTOS ########
if __name__ == '__main__':
	s = Sorting()
	exp = Experiment()
	exp.test(s) # executar testes
	print('Inicio do teste: {0}\nFim do teste: {1}'.format(exp.totalTime()[0], exp.totalTime()[1]))