import random

WORDLIST = ['time','year','people','way','day','man','thing','woman','life','child','world','school','state','family','student','group','country','problem','hand','part','place','case','week','company','system','program','question','work','government','number','night','point','home','water','room','mother','area','money','story','fact','month','lot','right','study','book','eye','job','word','business','issue','side','kind','head','house','service','friend','father','power','hour','game','line','end','member','law','car','city','community','name','president','team','minute','idea','kid','body','information','back','parent','face','others','level','office','door','health','person','art','war','history','party','result','change','morning','reason','research','girl','guy','moment','air','teacher','force','education']


def human_hash(seed=None):
    '''Hash a string and return a human readable string
    
    Not crytographically secure, uses a library of 100 nouns
    '''
    if seed is not None:
        random.seed(seed)
    return u"{}-{}-{}".format(random.choice(WORDLIST), random.choice(WORDLIST), random.choice(WORDLIST))

def handler(request, match):
    from dbops_mysql import DB
    db = DB()

    iid = match.group(1)
    name = human_hash(iid)

    db.createInstance(iid, name)
    response = {
        'attributes' : {},
        'display_name': name,
        'owner': '25721053-ebe8-59f1-95b3-de39bc253c7f'
    }
    return (200, response, {})