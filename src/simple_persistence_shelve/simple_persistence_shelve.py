# -*- encoding: utf-8 -*-
# jtuki@foxmail.com

r"""Test the performance of shelve module, a persistence module based on pickle (or cpickle on Python 2.x).
https://docs.python.org/3/library/shelve.html

Note that only since Python 3.4, shelve support "with shelve.open() as db".
http://stackoverflow.com/questions/30444019/shelve-gives-attributeerror-in-python-3-3-for-hello-world-example-using-the-wit
"""
import shelve
from random import randint

db_file = 'db_file.db'

# http://listofrandomwords.com/index.cfm?blist
# 100 different words
words = ["reprobated", "hippophagy", "hovercraft", "chemisette", "coyishness",
         "precommand", "guidwillie", "slavocracy", "underslung", "diorthotic",
         "pronounced", "endostosis", "curability", "humorously", "semiglazed",
         "toothbrush", "metropolis", "cyathiform", "recodified", "undejected",
         "ornithopod", "increscent", "alphameric", "rejuvenize", "bismuthous",
         "fourierite", "mudslinger", "cyclotomic", "overstrode", "diphyletic",
         "protostele", "figuration", "saltarello", "pantaloons", "vitrifying",
         "synclastic", "isocyanine", "coprophagy", "viviparous", "precursory",
         "wickerwork", "displacing", "anorectous", "steriliser", "coercivity",
         "uninflamed", "spoilsport", "thunderbox", "winterthur", "endearment",
         "leptospira", "injunctive", "larentalia", "heptarchal", "outflaming",
         "endoenzyme", "unlionised", "khalkidike", "subspinous", "karyoplasm",
         "duplicatus", "bitterweed", "silverlike", "beaujolais", "pepsinated",
         "enthronise", "eilshemius", "supplicant", "omnivorous", "unfurlable",
         "damselfish", "expurgator", "angulation", "autopsical", "laterality",
         "scandalize", "diffluence", "amianthine", "bootlegged", "initialise",
         "undervalve", "fungitoxic", "decimating", "photodrama", "ungainsaid",
         "unannulled", "lenticular", "marshalsea", "bourbonist", "syndetical",
         "l''etrange", "gethsemane", "quinquefid", "antimerism", "streakedly",
         "supervened", "tristearin", "overgovern", "lichenized", "reradiated",]

gl_keywords_list = list()
gl_unordered_list = list() # no duplicate n sequence range[0, len(gl_keywords_list))
         
def create_keywords(n):
    global gl_keywords_list
    assert n > 0 and n % 10000 == 0 # multiple of 10000 keywords
    
    gl_keywords_list = list()
    j = 0
    for i in range(n):
        gl_keywords_list.append(words[i % 100] + str(j))
        if i % 100 == 99:
            j += 1
            
def create_unordered_list(n):
    global gl_keywords_list
    global gl_unordered_list
    assert len(gl_keywords_list) == n
    
    m_seq = []
    for i in range(n):
        m_seq.append(i)
    
    gl_unordered_list = []
    for i in range(n):
        j = randint(0, len(m_seq)-1)
        gl_unordered_list.append(m_seq[j])
        del m_seq[j]
    
    assert len(gl_unordered_list) == n
    

def test_shelve_insert_new(n):
    global db_file
    global gl_keywords_list
    
    assert len(gl_keywords_list) == n
    
    # https://docs.python.org/3/library/shelve.html#shelve.open
    # always create a new db for reading and writing
    db = shelve.open(db_file, 'n', writeback=True)
    for w in gl_keywords_list:
        db[w] = w*3
    db.close() # automatically sync and close

def test_shelve_random_update(n):
    global db_file
    global words
    global gl_keywords_list
    global gl_unordered_list
    assert len(gl_keywords_list) == n
    assert len(gl_unordered_list) == n
    
    db = shelve.open(db_file, 'w', writeback=True)
    for i in gl_unordered_list:
        w = gl_keywords_list[i]
        db[w] = w*2
    db.close()

def test_shelve_random_read(n):
    global db_file
    global words
    global gl_keywords_list
    assert len(gl_keywords_list) == n
    assert len(gl_unordered_list) == n
    
    db = shelve.open(db_file, 'r')
    for i in gl_unordered_list:
        w = gl_keywords_list[i]
        r = db[w]
    db.close()
    
def test_shelve_random_delete(n):
    global db_file
    global words
    global gl_keywords_list
    assert len(gl_keywords_list) == n
    assert len(gl_unordered_list) == n
    
    db = shelve.open(db_file, 'w', writeback=True)
    for i in gl_unordered_list:
        w = gl_keywords_list[i]
        del db[w]
    db.close()
    
if __name__ == '__main__':
    import timeit
    
    n_keywords = 10000
    
    t = timeit.timeit("create_keywords(%d)" % (n_keywords), "from __main__ import create_keywords", number=1)
    print("create_keywords(%d): %f seconds" % (n_keywords, t))
    
    t = timeit.timeit("create_unordered_list(%d)" % (n_keywords), "from __main__ import create_unordered_list", number=1)
    print("create_unordered_list(%d): %f seconds" % (n_keywords, t))
    
    t = timeit.timeit("test_shelve_insert_new(%d)" % (n_keywords), "from __main__ import test_shelve_insert_new", number=1)
    print("test_shelve_insert_new(%d): %f seconds" % (n_keywords, t))
    
    t = timeit.timeit("test_shelve_random_update(%d)" % (n_keywords), "from __main__ import test_shelve_random_update", number=1)
    print("test_shelve_random_update(%d): %f seconds" % (n_keywords, t))
    
    t = timeit.timeit("test_shelve_random_read(%d)" % (n_keywords), "from __main__ import test_shelve_random_read", number=1)
    print("test_shelve_random_read(%d): %f seconds" % (n_keywords, t))
    
    t = timeit.timeit("test_shelve_random_delete(%d)" % (n_keywords), "from __main__ import test_shelve_random_delete", number=1)
    print("test_shelve_random_delete(%d): %f seconds" % (n_keywords, t))
    
