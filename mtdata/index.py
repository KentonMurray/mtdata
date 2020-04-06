#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/4/20

from typing import Tuple, List, Optional
from dataclasses import dataclass
from mtdata.parser import detect_extension


@dataclass
class Entry:
    langs: Tuple[str, str]
    name: str
    url: str
    filename: Optional[str] = None  # optional local file name; tries to auto-decide iff missing
    ext: Optional[str] = None  # extension name; tries to auto-decide iff missing
    in_paths: Optional[List[str]] = None  # if URL is a tar or zip, specify inside paths
    cite: Optional[str] = None

    def __post_init__(self):
        assert len(self.langs) == 2
        assert isinstance(self.langs, tuple)
        for ch in '.-/* ':
            assert ch not in self.name, f"Character '{ch}' not supported in dataset name"

        orig_name = self.url.split('/')[-1]
        self.ext = self.ext or detect_extension(self.filename or orig_name)
        langs = '_'.join(self.langs)
        self.filename = self.filename or f'{self.name}-{langs}.{self.ext}'
        self.is_archive = self.ext in ['zip', 'tar', 'tar.gz', 'tgz']
        if self.is_archive:
            assert self.in_paths and len(self.in_paths) > 0, 'Archive entries must have in_paths'

    def is_swap(self, langs):
        return tuple(reversed(langs)) == tuple(self.langs)

    def __str__(self):
        self.format(delim=' ')

    def format(self, delim: str = ' '):
        msg = f'{self.name}{delim}{"-".join(self.langs)}{delim}{self.url}{delim}' \
              f'{",".join(self.in_paths or [])}'
        return msg


entries: List[Entry] = []


def get_entries(langs=None, names=None):
    select = entries

    if names:
        if not isinstance(names, set):
            names = set(names)
        select = [e for e in select if e.name in names]
    if langs:
        assert len(langs) == 2
        select = [e for e in select if sorted(langs) == sorted(e.langs)]
    return select


# === Europarl V9 corpus
EUROPARL_v9 = 'http://www.statmt.org/europarl/v9/training/europarl-v9.%s-%s.tsv.gz'
cite = r"""@inproceedings{koehn2005europarl,
  title={Europarl: A parallel corpus for statistical machine translation},
  author={Koehn, Philipp},
  booktitle={MT summit},
  volume={5},
  pages={79--86},
  year={2005},
  organization={Citeseer}
}"""
for pair in ['de en', 'cs en', 'cs pl', 'es pt', 'fi en', 'lt en']:
    l1, l2 = pair.split()
    entries.append(Entry(langs=(l1, l2), name='europarl_v9', url=EUROPARL_v9 % (l1, l2), cite=cite))

# === Para crawl corpus
PARACRAWL_v3 = 'https://s3.amazonaws.com/web-language-models/paracrawl/release3/%s-%s.bicleaner07.tmx.gz'
cite = r"""@inproceedings{espla-etal-2019-paracrawl,
    title = "{P}ara{C}rawl: Web-scale parallel corpora for the languages of the {EU}",
    author = "Espl{\`a}, Miquel  and
      Forcada, Mikel  and
      Ram{\'\i}rez-S{\'a}nchez, Gema  and
      Hoang, Hieu",
    booktitle = "Proceedings of Machine Translation Summit XVII Volume 2: Translator, Project and User Tracks",
    month = aug,
    year = "2019",
    address = "Dublin, Ireland",
    publisher = "European Association for Machine Translation",
    url = "https://www.aclweb.org/anthology/W19-6721",
    pages = "118--119",
}"""
for pair in ['en cs', 'en de', 'en fi', 'en lt']:
    l1, l2 = pair.split()
    entries.append(
        Entry(langs=(l1, l2), name='paracrawl_v3', url=PARACRAWL_v3 % (l1, l2), cite=cite))

# === News Commentary v14
NEWSCOM_v14 = "http://data.statmt.org/news-commentary/v14/training/news-commentary-v14.%s-%s.tsv.gz"
cite = r"""@inproceedings{bojar-etal-2018-findings,
    title = "Findings of the 2018 Conference on Machine Translation ({WMT}18)",
    author = "Bojar, Ond{\v{r}}ej  and
      Federmann, Christian  and
      Fishel, Mark  and
      Graham, Yvette  and
      Haddow, Barry  and
      Koehn, Philipp  and
      Monz, Christof",
    booktitle = "Proceedings of the Third Conference on Machine Translation: Shared Task Papers",
    month = oct,
    year = "2018",
    address = "Belgium, Brussels",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W18-6401",
    doi = "10.18653/v1/W18-6401",
    pages = "272--303"
}"""
for pair in ['en kk', 'ar cs', 'ar de', 'ar en', 'ar es', 'ar fr', 'ar hi', 'ar id', 'ar it',
             'ar ja', 'ar kk', 'ar nl', 'ar pt', 'ar ru', 'ar zh', 'cs de', 'cs en', 'cs es',
             'cs fr', 'cs hi', 'cs id', 'cs it', 'cs ja', 'cs kk', 'cs nl', 'cs pt', 'cs ru',
             'cs zh', 'de en', 'de es', 'de fr', 'de hi', 'de id', 'de it', 'de ja', 'de kk',
             'de nl', 'de pt', 'de ru', 'de zh', 'en es', 'en fr', 'en hi', 'en id', 'en it',
             'en ja', 'en kk', 'en nl', 'en pt', 'en ru', 'en zh', 'es fr', 'es hi', 'es id',
             'es it', 'es ja', 'es kk', 'es nl', 'es pt', 'es ru', 'es zh', 'fr hi', 'fr id',
             'fr it', 'fr ja', 'fr kk', 'fr nl', 'fr pt', 'fr ru', 'fr zh', 'hi id', 'hi it',
             'hi nl', 'hi pt', 'hi ru', 'hi zh', 'id it', 'id kk', 'id nl', 'id pt', 'id ru',
             'id zh', 'it kk', 'it nl', 'it pt', 'it ru', 'it zh', 'ja ru', 'ja zh', 'kk nl',
             'kk pt', 'kk ru', 'kk zh', 'nl pt', 'nl ru', 'nl zh', 'pt ru', 'pt zh', 'ru zh']:
    l1, l2 = pair.split()
    entries.append(Entry(langs=(l1, l2), name='news_commentary_v14', url=NEWSCOM_v14 % (l1, l2),
                         cite=cite))

# ===== Wiki Titles V1
WIKI_TITLES_v1 = 'http://data.statmt.org/wikititles/v1/wikititles-v1.%s-%s.tsv.gz'
cite = r"""@inproceedings{barrault-etal-2019-findings,
    title = "Findings of the 2019 Conference on Machine Translation ({WMT}19)",
    author = {Barrault, Lo{\"\i}c  and
      Bojar, Ond{\v{r}}ej  and
      Costa-juss{\`a}, Marta R.  and
      Federmann, Christian  and
      Fishel, Mark  and
      Graham, Yvette  and
      Haddow, Barry  and
      Huck, Matthias  and
      Koehn, Philipp  and
      Malmasi, Shervin  and
      Monz, Christof  and
      M{\"u}ller, Mathias  and
      Pal, Santanu  and
      Post, Matt  and
      Zampieri, Marcos},
    booktitle = "Proceedings of the Fourth Conference on Machine Translation (Volume 2: Shared Task Papers, Day 1)",
    month = aug,
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W19-5301",
    doi = "10.18653/v1/W19-5301",
    pages = "1--61"
}"""
for pair in ['cs en', 'cs pl', 'de en', 'es pt', 'fi en', 'gu en', 'hi ne', 'kk en', 'lt en',
             'ru en', 'zh en']:
    l1, l2 = pair.split()
    entries.append(Entry(langs=(l1, l2), name='wiki_titles_v1', url=WIKI_TITLES_v1 % (l1, l2),
                         cite=cite))

# ===== Wiki Titles V2
WIKI_TITLES_v2 = 'http://data.statmt.org/wikititles/v2/wikititles-v2.%s-%s.tsv.gz'
for pair in ['ca es', 'cs en', 'de en', 'de fr', 'es pt', 'iu en', 'ja en', 'pl en', 'ps en',
             'ru en', 'ta en', 'zh en']:
    l1, l2 = pair.split()
    entries.append(Entry(langs=(l1, l2), name='wiki_titles_v2', url=WIKI_TITLES_v2 % (l1, l2),
                         cite=cite))

# ==== WMT  Dev and Tests
wmt_sets = {
    'newstest2014': [('de', 'en'), ('cs', 'en'), ('fr', 'en'), ('ru', 'en'), ('hi', 'en')],
    'newsdev2015': [('fi', 'en'), ('en', 'fi')],
    'newstest2015': [('fi', 'en'), ('en', 'cs'), ('cs', 'en'), ('en', 'ru'), ('en', 'de'),
                     ('de', 'en'), ('ru', 'en'), ('en', 'fi')],
    'newsdev2016': [('en', 'ro'), ('ro', 'en'), ('tr', 'en'), ('en', 'tr')],
    'newstest2016': [('de', 'en'), ('en', 'de'), ('en', 'ro'), ('en', 'fi'), ('ro', 'en'),
                     ('ru', 'en'), ('fi', 'en'), ('en', 'ru'), ('tr', 'en'), ('cs', 'en'),
                     ('en', 'tr'), ('en', 'cs')],
    'newsdev2017': [('zh', 'en'), ('lv', 'en'), ('en', 'zh'), ('en', 'lv')],
    'newstest2017': [('zh', 'en'), ('ru', 'en'), ('en', 'fi'), ('lv', 'en'), ('en', 'de'),
                     ('de', 'en'), ('cs', 'en'), ('en', 'cs'), ('en', 'tr'), ('en', 'ru'),
                     ('tr', 'en'), ('fi', 'en'), ('en', 'zh'), ('en', 'lv')],
    'newsdev2018': [('et', 'en'), ('en', 'et')],
    'newstest2018': [('ru', 'en'), ('zh', 'en'), ('et', 'en'), ('en', 'fi'), ('en', 'de'),
                     ('de', 'en'), ('en', 'cs'), ('en', 'tr'), ('cs', 'en'), ('tr', 'en'),
                     ('en', 'ru'), ('en', 'et'), ('fi', 'en'), ('en', 'zh')],
    'newsdev2019': [('gu', 'en'), ('kk', 'en'), ('en', 'lt'), ('en', 'kk'), ('lt', 'en'),
                    ('en', 'gu')],
    'newstest2019': [('de', 'en'), ('de', 'fr'), ('kk', 'en'), ('en', 'de'), ('en', 'fi'),
                     ('ru', 'en'), ('zh', 'en'), ('gu', 'en'), ('en', 'kk'), ('en', 'zh'),
                     ('cs', 'de'), ('fi', 'en'), ('en', 'gu'), ('lt', 'en'), ('de', 'cs'),
                     ('en', 'lt'), ('en', 'ru'), ('en', 'cs'), ('fr', 'de')],
    'newsdev2020': [('iu', 'en'), ('en', 'ta'), ('ta', 'en'), ('pl', 'en'), ('en', 'iu'),
                    ('en', 'ja'), ('ja', 'en'), ('en', 'pl')]
}

for set_name, pairs in wmt_sets.items():
    for l1, l2 in pairs:
        src = f'dev/{set_name}-{l1}{l2}-src.{l1}.sgm'
        ref = f'dev/{set_name}-{l1}{l2}-ref.{l2}.sgm'
        name = f'{set_name}_{l1}{l2}'
        entries.append(Entry((l1, l2), name=name, filename='wmt20dev.tgz', in_paths=[src, ref],
                             url='http://data.statmt.org/wmt20/translation-task/dev.tgz'))