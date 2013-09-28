# max length of 5
N = 'n'
V = 'v'
ADJ = 'a'
ADV = 'r'
IDIOM = 'idiom'
PREP = 'prep'
AUXV = 'auxv'
IDFA = 'idfa'
CC = 'cc'
ABRV = 'abrv'
PN = 'pn'
NPS = 'nps'
INTRJ = 'intrj'
AFF = 'aff'
AT = 'at'
DFA = 'dfa'
FN = 'fn'
GN = 'gn'
IMPR = 'impr'
NP = 'np'
PP = 'pp'
PHRP = 'phrp'
PPN = 'ppn'
PPNPL = 'ppnpl'
PPNPS = 'ppnps'
SFF = 'sff'
VIT = 'vit'
VT = 'vt'
PHRV = 'phrv'
PREDP = 'predp'

POS = (
    N,
    V,
    ADJ,
    ADV,
)

POS_CHOICES = (
    (ABRV, 'Abbreviation'),
    (ADJ, 'Adjective'),
    (ADV, 'Adverb'),
    (AFF, 'Affix'),
    (AT, 'Article'),
    (AUXV, 'Auxiliary-Verb'),
    (CC, 'Conjunction'),
    (DFA, 'Definite-Article'),
    (FN, 'Family-Name'),
    (GN, 'Given-Name'),
    (IDIOM, 'Idiom'),
    (IDFA, 'Indefinite-Article'),
    (INTRJ, 'Interjection'),
    (IMPR, 'Imperative'),
    (N, 'Noun'),
    (NP, 'Noun-Plural'),
    (NPS, 'Noun-Possessive'),
    (PP, 'Past-Participle'),
    (PHRP, 'Phrasal-Prefix'),
    (PHRV, 'Phrasal-Verb'),
    (PREP, 'Preposition'),
    (PN, 'Pronoun'),
    (PPN, 'Proper-Noun'),
    (PPNPL, 'Proper-Noun-Plural'),
    (PPNPS, 'Proper-Noun-Posessive'),
    (SFF, 'Suffix'),
    (V, 'Verb'),
    (VIT, 'Verb-Intransitive'),
    (VT, 'Verb-Transitive'),
    (PREDP, 'Predicate Phrase'),
)

POS_NAME_TO_TAG = dict((name.lower(), tag) for tag,name in POS_CHOICES)

WN_POS_TO_LOCAL_POS = {
    'n':N,
    'v':V,
    'a':ADJ,
    'r':ADV,
    's':ADJ, # correct? http://wordnet.princeton.edu/wordnet/man/wngloss.7WN.html 
}

YES = 1.0
NO = 0.0
MAYBE = 0.5
RARELY = 0.1
VOTE_CHOICES = (
    (YES, 1.0),
    (NO, 0.0),
    (MAYBE, 0.5),
    (RARELY, 0.1),
)

OPEN = 'open'
CLOSED = 'closed'
ASSUMPTION_CHOICES = (
    (OPEN, 'Open - missing triples are assumed to have some specified truth value.'),
    (CLOSED, 'Closed - missing triples are assumed to be false'),
)

IRREGULAR_NOUNS = dict(
    foot='feet',
    child='children',
    person='people',
    tooth='teeth',
    mouse='mice',
    man='men',
    woman='women',
    louse='lice',
    cactus='cacti',
    appendix='appendices',
    ox='oxen',
    #TODO:expand
)

PLURALE_TANTUMS = (
    'fish', 'deer', 'moose', 'aircraft', 'offspring', 'sheep', 'shrimp', 'glasses', 'scissors', 'pants',
    #TODO:expand
)

SAMEAS = 'is same as'
ISOPPOSITEOF = 'is opposite of'
ISA = 'is a'
HASA = 'has a'
HAS_PLURAL = 'has plural'
HAS_SINGULAR = 'has singular'
ISPARTOF = 'is part of'

RULE_ISA = 'ISA'
RULE_CHOICES = (
    (RULE_ISA, 'ISA'),
)
