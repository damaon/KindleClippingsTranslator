import httplib
import urllib2 # pobieranie strony
#konfiguracja
from default_config import *

CONFIG = DEFAULT_CONFIG
SYFY = [".",",","'",'"',"?","!",":",";","\n", "\r\n" ," "]

def wczytaj_linie(path):
	f = open(path, 'r') # r - (read) - odczyt
	linie = f.readlines()
	f.close()
	return linie

def clear_till(slowko, z):
	nowe = ''
	przepisuj = False
	for l in slowko:
		if not l in z: # jesli pojawi sie jakas litera ktorej sie nie chcemy pozbyc, zacznij przepisywac
			przepisuj = True
		if przepisuj:
			nowe += l
	return nowe

def odwrocone(slowko):
	return slowko[::-1]		

def oczysc_slowko(slowko, z):
	czyste = removeNonAscii(slowko)
	czyste = clear_till(czyste, z)
	czyste = clear_till( odwrocone(czyste), z)
	return odwrocone(czyste)

def oczysc_slowka(slowka, z): # zaczyna zczytywac jak sie koncza niechciane znaki, potem obraca i to samo
	czyste_slowka = []
	for s in slowka:
		czyste = oczysc_slowko(s, z)
		czyste_slowka.append( czyste  )
	return czyste_slowka

def wypisz_slowka(slowka):
	for slowo in slowka:
		print "{%s}" % slowo

def removeNonAscii(s): return "".join(filter(lambda x: ord(x) >= 32 and ord(x)<= 126, s))

def remove_formatting(s): return "".join(filter(lambda x: ord(x) >= 32, s))
def kindle_zczytaj(tytul):
	SYFY = [".",",","'",'"',"?","!",":",";","\n", "\r\n" ," "]
	linie = wczytaj_linie("My Clippings.txt")
	#teraz wybranie interesujacych lini
	i = 0
	slowka = []
	tytulowe = tytul.split(' ')
	while( i < len(linie) ):
		if any( [ True for t in tytulowe if t in linie[i] ] ):
			czyste = linie[i+3]
			czyste = oczysc_slowko( czyste, SYFY)
			if czyste and len(czyste) <= CONFIG['MAX_WORD_LENGTH'] :
				slowka.append( czyste ) # omija lokacje i wolna linie
		i += 5
	return slowka


def google_translate(slowko, z, do):
	request = urllib2.Request("http://translate.google.pl/translate_a/t?client=t&sl=%s&tl=%s&hl=%s&sc=2&ie=UTF-8&oe=UTF-8&oc=1&otf=1&ssel=0&tsel=0&q=%s" % (z,do,do,slowko) )
	request.add_header('User-Agent','Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)')
	opener = urllib2.build_opener()
	translacja = opener.open(request).read()
	#uboga extrakcja
	s = translacja.find('"')+1
	e = translacja.find('"',s)	
	return translacja[s:e]

def translate(slowka, z, do):
	translated = []
	for s in slowka:
		translated.append( google_translate(s, z ,do))
	return translated

def save_words(slowka,translacja,plik):
	f = open(plik, 'a')
	for s,t in zip(slowka,translacja):
		f.write(s+'|'+t+'\n')
	f.close()
def read_words(plik):
	linie = wczytaj_linie(plik)
	for l in linie:
		format = l.split("|")
		s = format[0]
		t = remove_formatting(format[1])
		print "{0:10}=>   {1}".format(s,t)




slowka = kindle_zczytaj("Brothers Karamazov")

slowka = ["cat", "dog","elephant","giraffe"]
czyste = oczysc_slowka(slowka, SYFY)
tlumaczenie = translate(czyste,"en", "pl")
for s,t in zip(czyste,tlumaczenie):
	print "{0:15}=>     {1}".format(s,t)

#save_words(czyste,tlumaczenie,"zwierzatka.trans")
read_words("zwierzatka.trans")