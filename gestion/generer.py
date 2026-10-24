# -*- coding: utf-8 -*-
# Générateur des trois maquettes de la console de gestion, (c) Sylvain Caron 2026.
# Trois partis pris de composition sur les mêmes écrans et les mêmes données (base locale du 24/10/2026).
import os, html, shutil

OUT = os.path.dirname(os.path.abspath(__file__))
ASSETS_SITE = '../assets'
e = html.escape

# ---------------------------------------------------------------- Données réelles
# (date iso, début, fin, type, lieu, ville, dép, publiée, affiche)
DATES = [
    ('2026-10-25', '14:30', None, None, 'Théâtre Municipal', 'Abbeville', '80', True, True),
    ('2026-11-01', '14:30', '19:00', None, 'Salle des fêtes', 'St Germain du Bois', '71', True, False),
    ('2026-11-02', '14:30', '19:00', None, 'Zone Commerciale Nationale 7', 'Portes-lès-Valence', '26', True, False),
    ('2026-11-05', None, None, None, 'Avec Christophe Demerson', 'Beffes', '18', True, False),
    ('2026-11-07', '15:00', '18:30', 'Stage', 'Stage de danse en ligne', 'Autun', '71', True, False),
    ('2026-11-08', '14:30', None, None, None, 'Le Looping', '71', True, False),
    ('2026-11-11', '14:30', '19:00', None, 'Centre culturel et de congrès', 'Paray-le-Monial', '71', True, False),
    ('2026-11-12', '14:15', '19:00', None, 'Salle des Fêtes Frédéric Lescure', 'Selongey', '21', True, False),
    ('2026-11-14', '14:30', '19:00', None, 'Salle des fêtes', 'St Just La Pendue', '42', True, False),
    ('2026-11-15', '14:15', '19:00', None, None, 'Labergement-lès-Seurre', '21', False, False),
]
COMPTE = {'dates': 37, 'albums': 11, 'titres': 177, 'commandes': 1187, 'pistes': 211, 'mp3': 0, 'sans_affiche': 35, 'a_expedier': 3}
COMMANDES = [
    ('M31V01189', '17 oct.', 'Clé USB Vol. 23', '20,00 €', 'À expédier'),
    ('RNY301188', '11 oct.', 'Clé USB Vol. 23', '20,00 €', 'À expédier'),
    ('S4NI01187', '9 oct.', 'Clé USB Vol. 23', '20,00 €', 'Terminée'),
    ('EFL401186', '9 oct.', 'CD Vol. 23', '15,00 €', 'Terminée'),
    ('KQ2M01185', '9 oct.', 'CD Vol. 22', '15,00 €', 'À expédier'),
]
ALBUM = {'nom': 'La vie est belle, Chantons l\'amour', 'vol': 23, 'slug': 'vol-23-la-vie-est-belle-chantons-l-amour',
         'formats': [('CD', '10,00 €', 1000, True), ('Clé USB', '15,00 €', 800, True)]}
PISTES = [
    (1, 'Oberlands', 'Marche festive', True, True), (2, 'La vie est belle', 'Marche festive', True, True),
    (3, 'Colomba Bianca', 'Boléro', False, False), (4, 'Trois petites notes en Bavière', 'Valse', False, False),
    (5, 'Blumen aus Holland', 'Valse', False, False), (6, 'Amamé', 'Merengué', False, False),
    (7, 'Être libre', 'Merengué', False, False), (8, 'Couleur menthe à l\'eau', 'Slow', False, False),
    (9, 'España Cañí', 'Paso', False, False), (10, 'Morena de mi Copla', 'Paso', False, False),
    (11, 'La Cumparsita', 'Tango', False, False), (12, 'Noche de Fuego', 'Tango', False, False),
    (13, 'Le Disco', 'Disco', False, False), (14, 'We are the champions', 'Slow-Rock', False, False),
]
ALBUMS = [('Vol. 23', 'La vie est belle, Chantons l\'amour', 'vol-23-la-vie-est-belle-chantons-l-amour', '2 / 14'),
          ('Vol. 22', 'Y\'a pas mieux que la musique', 'vol-22-y-a-pas-mieux-que-la-musique', '0 / 16'),
          ('Vol. 21', 'La vie est faite pour danser', 'vol-21-la-vie-est-faite-pour-danser', '0 / 16')]
JOURS = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
JC = ['Lun.', 'Mar.', 'Mer.', 'Jeu.', 'Ven.', 'Sam.', 'Dim.']

import datetime
def dt(iso): return datetime.date.fromisoformat(iso)
def date_longue(iso):
    d = dt(iso); return '%s %d %s %d' % (JOURS[d.weekday()].capitalize(), d.day, MOIS[d.month - 1], d.year)
def date_courte(iso):
    d = dt(iso); return '%s %d %s' % (JC[d.weekday()], d.day, MOIS[d.month - 1][:4] + '.' if len(MOIS[d.month - 1]) > 5 else MOIS[d.month - 1])
def horaire(deb, fin):
    if not deb: return 'Horaire à préciser'
    if fin: return 'de %s à %s' % (deb.replace(':', 'h'), fin.replace(':', 'h'))
    return 'à partir de %s' % deb.replace(':', 'h')

# ---------------------------------------------------------------- Icônes (SVG, trait 1.8)
def ico(d, vb='0 0 24 24'):
    return '<svg viewBox="%s" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (vb, d)
I = {
    'bord': ico('<rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/>'),
    'cal': ico('<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M16 3v4M8 3v4M3 11h18"/>'),
    'disque': ico('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2.5"/>'),
    'note': ico('<path d="M9 18V6l11-2v12"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/>'),
    'panier': ico('<circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.7 13.4a2 2 0 0 0 2 1.6h9.7a2 2 0 0 0 2-1.6L23 6H6"/>'),
    'page': ico('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>'),
    'seo': ico('<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>'),
    'sauv': ico('<path d="M12 3v12M7 10l5 5 5-5"/><path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"/>'),
    'reglages': ico('<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>'),
    'plus': ico('<path d="M12 5v14M5 12h14"/>'),
    'loupe': ico('<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>'),
    'fleche': ico('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    'retour': ico('<path d="M19 12H5M11 18l-6-6 6-6"/>'),
    'alerte': ico('<path d="M12 9v4M12 17h.01"/><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/>'),
    'ok': ico('<path d="M20 6 9 17l-5-5"/>'),
    'poignee': ico('<circle cx="9" cy="6" r="1.2" fill="currentColor"/><circle cx="15" cy="6" r="1.2" fill="currentColor"/><circle cx="9" cy="12" r="1.2" fill="currentColor"/><circle cx="15" cy="12" r="1.2" fill="currentColor"/><circle cx="9" cy="18" r="1.2" fill="currentColor"/><circle cx="15" cy="18" r="1.2" fill="currentColor"/>'),
    'lecture': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4v16l13-8z"/></svg>',
    'onde': ico('<path d="M3 12h2l2-5 3 10 3-14 3 14 2-5h3"/>'),
    'image': ico('<rect x="3" y="4" width="18" height="16" rx="3"/><circle cx="9" cy="10" r="2"/><path d="m21 16-5-5-8 8"/>'),
    'copie': ico('<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/>'),
    'oeil': ico('<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>'),
    'corbeille': ico('<path d="M3 6h18M8 6V4h8v2M6 6l1 14h10l1-14"/>'),
    'cloche': ico('<path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9M13.7 21a2 2 0 0 1-3.4 0"/>'),
    'sortie': ico('<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/>'),
    'externe': ico('<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14 21 3"/>'),
    'fichier': ico('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/>'),
    'horloge': ico('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
    'chevron': ico('<path d="m9 6 6 6-6 6"/>'),
    'menu': ico('<path d="M4 7h16M4 12h16M4 17h16"/>'),
}

NAV = [('bord', 'Tableau de bord', 'bord'), ('dates', 'Dates', 'cal'), ('album', 'Albums', 'disque'), ('partitions', 'Partitions', 'note'),
       ('commandes', 'Commandes', 'panier'), ('pages', 'Pages et menus', 'page'), ('seo', 'SEO', 'seo'), ('sauvegardes', 'Sauvegardes', 'sauv'), ('reglages', 'Réglages', 'reglages')]

# ---------------------------------------------------------------- CSS commun
BASE_CSS = r'''
:root{--fond:#f7f5f2;--blanc:#fff;--encre:#1d1a17;--gris:#5f5852;--clair:#756e6b;--trait:#e6e0d8;--trait2:#efebe5;--bord:#7b1f2f;--bord-d:#5c1522;--bord-l:#f3e4e7;
--ok:#2e7d4f;--ok-l:#e4f1e7;--att:#9a6700;--att-l:#fbf0d2;--ko:#b42318;--ko-l:#f8e1dd;--ombre:0 1px 2px rgba(29,26,23,.06),0 8px 24px -16px rgba(29,26,23,.25);
--display:'Marcellus',Georgia,serif;--body:'Figtree',system-ui,sans-serif;--r:12px}
*{box-sizing:border-box;margin:0;padding:0}
html{font-size:15px}
body{font-family:var(--body);background:var(--fond);color:var(--encre);line-height:1.5;-webkit-font-smoothing:antialiased;isolation:isolate;min-height:100vh}
a{color:inherit}
img{display:block;max-width:100%}
svg{width:18px;height:18px;flex:none}
button{font:inherit;color:inherit;background:none;border:0;cursor:pointer}
h1,h2{font-family:var(--display);font-weight:400;line-height:1.1}
h1{font-size:30px}h2{font-size:20px}
.sur{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--bord);font-weight:700}
.btn{display:inline-flex;align-items:center;gap:8px;padding:10px 16px;border-radius:999px;font-weight:700;font-size:14px;background:var(--encre);color:#fff;text-decoration:none;cursor:pointer;transition:background .2s,transform .2s;white-space:nowrap}
.btn:hover{background:var(--bord);transform:translateY(-1px)}
.btn.sec{background:var(--blanc);color:var(--encre);box-shadow:inset 0 0 0 1px var(--trait)}
.btn.sec:hover{background:var(--trait2);transform:none}
.btn.prim{background:var(--bord)}.btn.prim:hover{background:var(--bord-d)}
.btn.petit{padding:7px 12px;font-size:13px}
.lien{display:inline-flex;align-items:center;gap:6px;font-weight:700;color:var(--bord);text-decoration:none;font-size:14px;cursor:pointer}
.lien:hover{text-decoration:underline}
.lien svg{width:16px;height:16px}
.badge{display:inline-flex;align-items:center;gap:6px;padding:3px 10px;border-radius:999px;font-size:12px;font-weight:700;background:var(--trait2);color:var(--gris);white-space:nowrap}
.badge.ok{background:var(--ok-l);color:var(--ok)}.badge.att{background:var(--att-l);color:var(--att)}.badge.ko{background:var(--ko-l);color:var(--ko)}.badge.bord{background:var(--bord-l);color:var(--bord)}
.badge svg{width:13px;height:13px}
.carte{background:var(--blanc);border-radius:16px;box-shadow:var(--ombre);padding:22px 24px}
.carte h2{margin-bottom:14px;display:flex;align-items:center;justify-content:space-between;gap:12px}
.carte h2 .lien{font-family:var(--body);font-size:13px}
.champ{display:grid;gap:5px;font-size:13px;color:var(--gris);font-weight:600}
.champ input,.champ select,.champ textarea{font:inherit;font-size:15px;font-weight:400;color:var(--encre);padding:10px 12px;border:1px solid var(--trait);border-radius:10px;background:var(--blanc);width:100%}
.champ input:focus,.champ select:focus,.champ textarea:focus{outline:2px solid var(--bord);outline-offset:1px;border-color:var(--bord)}
.champ .etat{font-weight:400;color:var(--ok);font-size:12px;display:inline-flex;gap:4px;align-items:center}
.champ .etat svg{width:12px;height:12px}
.grille-champs{display:grid;gap:14px 16px;grid-template-columns:repeat(12,1fr)}
.grille-champs>*,.champ input,.champ select,.champ textarea{min-width:0}
.app,.app>*,.page,.page>*,.deux>*,.matin>*,.bord-c>*,.md>*,.album-c>*,.fiche>*,.album-b>*,.carte{min-width:0}
.c2{grid-column:span 2}.c3{grid-column:span 3}.c4{grid-column:span 4}.c6{grid-column:span 6}.c8{grid-column:span 8}.c12{grid-column:span 12}
.interrupteur{display:inline-flex;align-items:center;gap:10px;font-weight:600;font-size:14px;cursor:pointer}
.interrupteur i{width:40px;height:22px;border-radius:999px;background:var(--trait);position:relative;transition:background .2s}
.interrupteur i::after{content:"";position:absolute;top:3px;left:3px;width:16px;height:16px;border-radius:50%;background:#fff;transition:left .2s;box-shadow:0 1px 2px rgba(0,0,0,.2)}
.interrupteur.on i{background:var(--ok)}.interrupteur.on i::after{left:21px}
.tableau{width:100%;border-collapse:collapse;font-size:14px}
.tableau th{text-align:left;font-size:12px;letter-spacing:.04em;text-transform:uppercase;color:var(--clair);font-weight:700;padding:10px 12px;border-bottom:1px solid var(--trait)}
.tableau td{padding:12px;border-bottom:1px solid var(--trait2);vertical-align:middle}
.tableau tr:last-child td{border-bottom:0}
.tableau tr:hover td{background:#fbf9f6}
.tableau td.num,.tableau th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.tableau-enveloppe{overflow-x:auto}
.tableau b{font-weight:700}
.tableau small{display:block;color:var(--clair);font-size:12px}
.cal{display:inline-grid;place-items:center;width:46px;height:50px;border-radius:10px;background:var(--bord-l);color:var(--bord);line-height:1;flex:none}
.cal small{font-size:10px;text-transform:uppercase;letter-spacing:.06em;font-weight:700}
.cal b{font-family:var(--display);font-size:22px;font-weight:400}
.chiffres{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.chiffre{background:var(--blanc);border-radius:16px;box-shadow:var(--ombre);padding:18px 20px;display:grid;gap:4px;text-decoration:none;transition:transform .2s}
.chiffre:hover{transform:translateY(-2px)}
.chiffre small{font-size:13px;color:var(--gris);font-weight:600}
.chiffre b{font-family:var(--display);font-size:34px;font-weight:400;line-height:1}
.chiffre span{font-size:12px;color:var(--clair)}
.chiffre.alerte b{color:var(--bord)}
.afaire{display:grid;gap:10px}
.afaire a{display:flex;align-items:center;gap:14px;padding:12px 14px;border-radius:12px;background:var(--fond);text-decoration:none;transition:background .2s}
.afaire a:hover{background:var(--bord-l)}
.afaire a .p{width:36px;height:36px;border-radius:10px;display:grid;place-items:center;background:var(--blanc);color:var(--bord);flex:none}
.afaire a b{display:block;font-size:14px}.afaire a span{font-size:13px;color:var(--gris)}
.afaire a .fl{margin-left:auto;color:var(--clair)}
.recherche{display:flex;align-items:center;gap:10px;background:var(--blanc);border:1px solid var(--trait);border-radius:999px;padding:8px 14px;color:var(--clair);font-size:14px}
.recherche input{border:0;background:none;font:inherit;width:100%;color:var(--encre)}
.recherche input:focus{outline:0}
.recherche kbd{font:inherit;font-size:11px;padding:2px 6px;border-radius:6px;border:1px solid var(--trait);color:var(--clair)}
.filtres{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.filtres .f{padding:7px 12px;border-radius:999px;background:var(--blanc);border:1px solid var(--trait);font-size:13px;font-weight:600;cursor:pointer;display:inline-flex;gap:6px;align-items:center}
.filtres .f.on{background:var(--encre);color:#fff;border-color:var(--encre)}
.filtres .f svg{width:14px;height:14px}
.depot{border:2px dashed var(--trait);border-radius:14px;padding:22px;text-align:center;color:var(--gris);font-size:14px;display:grid;gap:6px;justify-items:center;cursor:pointer;transition:border-color .2s,background .2s}
.depot:hover{border-color:var(--bord);background:var(--bord-l)}
.depot svg{width:26px;height:26px;color:var(--bord)}
.depot b{color:var(--encre)}
.jaquette{border-radius:12px;box-shadow:0 10px 30px -14px rgba(0,0,0,.5);aspect-ratio:1;object-fit:cover;width:100%}
.piste{display:grid;grid-template-columns:26px 28px 1fr 120px 92px 110px 110px 34px;gap:12px;align-items:center;padding:9px 10px;border-radius:10px;font-size:14px}
.piste:hover{background:var(--fond)}
.piste .n{color:var(--clair);font-variant-numeric:tabular-nums;text-align:right}
.piste .poignee{color:var(--trait);cursor:grab}.piste:hover .poignee{color:var(--clair)}
.piste input{min-width:0;font:inherit;font-size:14px;border:1px solid transparent;border-radius:8px;padding:6px 8px;background:transparent;width:100%}
.piste input:hover{border-color:var(--trait)}.piste input:focus{outline:0;border-color:var(--bord);background:var(--blanc)}
.piste .f{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:700}
.piste .f.oui{color:var(--ok)}.piste .f.non{color:var(--clair)}
.piste .f svg{width:14px;height:14px}
.piste .play{width:30px;height:30px;border-radius:50%;background:var(--encre);color:#fff;display:grid;place-items:center}
.piste .play svg{width:14px;height:14px}
.piste .play.off{background:var(--trait);color:var(--clair);cursor:default}
.piste-tete{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--clair);font-weight:700;padding:4px 10px;display:grid;grid-template-columns:26px 28px 1fr 120px 92px 110px 110px 34px;gap:12px}
.etat-sauv{position:fixed;right:20px;bottom:20px;background:var(--encre);color:#fff;padding:10px 16px;border-radius:999px;font-size:13px;display:flex;align-items:center;gap:8px;box-shadow:var(--ombre);z-index:5}
.etat-sauv svg{width:14px;height:14px;color:#8fd3a8}
.note-maq{font-size:12px;color:var(--clair);font-style:italic}
:focus-visible{outline:3px solid var(--bord);outline-offset:2px}
@media(max-width:1000px){.chiffres{grid-template-columns:repeat(2,1fr)}div[style*='grid-template-columns:1fr 1fr']{grid-template-columns:1fr!important}}
@media(max-width:900px){.tableau{display:block;overflow-x:auto;white-space:nowrap}}
@media(max-width:700px){.piste,.piste-tete{grid-template-columns:26px 1fr 34px 110px!important}.piste>:nth-child(1),.piste>:nth-child(4),.piste>:nth-child(7),.piste>:nth-child(8),.piste-tete>:nth-child(1),.piste-tete>:nth-child(4),.piste-tete>:nth-child(7),.piste-tete>:nth-child(8){display:none}.piste-tete>:nth-child(5){visibility:hidden}.tableau small{white-space:normal}.etat-sauv{right:12px;bottom:12px;font-size:12px}}
@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
'''

# ------------------------------------------------ A, Pupitre : barre latérale sombre, tableaux denses
A_CSS = r'''
.app{display:grid;grid-template-columns:248px 1fr;min-height:100vh}
.lat{background:var(--encre);color:#d9d2ca;padding:22px 16px;display:flex;flex-direction:column;gap:6px;position:sticky;top:0;height:100vh}
.lat .marque{color:#fff;padding:6px 10px 20px;display:grid;gap:2px}
.lat .marque b{font-family:var(--display);font-weight:400;font-size:20px}
.lat .marque span{font-size:12px;color:#a69e95}
.lat a{display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:10px;text-decoration:none;font-weight:600;font-size:14px;transition:background .15s,color .15s}
.lat a:hover{background:rgba(255,255,255,.07);color:#fff}
.lat a.on{background:var(--bord);color:#fff}
.lat a .n{margin-left:auto;font-size:11px;background:rgba(255,255,255,.15);padding:2px 7px;border-radius:999px}
.lat .sep{height:1px;background:rgba(255,255,255,.1);margin:10px 4px}
.lat .bas{margin-top:auto;display:grid;gap:4px}
.lat .bas a{font-size:13px;color:#a69e95}
.haut{display:flex;align-items:center;gap:16px;padding:14px 32px;background:var(--blanc);border-bottom:1px solid var(--trait);position:sticky;top:0;z-index:4}
.haut .recherche{width:380px}
.haut .droite{margin-left:auto;display:flex;align-items:center;gap:10px}
.haut .qui{display:flex;align-items:center;gap:10px;font-size:13px;color:var(--gris)}
.haut .qui i{width:32px;height:32px;border-radius:50%;background:var(--bord);color:#fff;display:grid;place-items:center;font-style:normal;font-weight:700;font-size:13px}
.page{padding:28px 32px 80px;display:grid;gap:22px;max-width:1360px}
.tete{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;flex-wrap:wrap}
.tete h1{margin-top:6px}
.tete .actions{display:flex;gap:8px;flex-wrap:wrap}
.deux{display:grid;grid-template-columns:1.6fr 1fr;gap:22px;align-items:start}
.sommaire{position:sticky;top:90px;display:grid;gap:4px;font-size:14px}
.sommaire a{padding:8px 12px;border-left:2px solid var(--trait);text-decoration:none;color:var(--gris)}
.sommaire a.on{border-color:var(--bord);color:var(--encre);font-weight:700}
.fiche{display:grid;grid-template-columns:1fr 200px;gap:28px;align-items:start}
.fiche .carte{margin-bottom:18px}
.apercu-site{background:var(--fond);border-radius:12px;padding:16px;display:flex;gap:14px;align-items:center;font-size:14px}
.apercu-site em{font-style:normal;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--bord);font-weight:700;display:block}
.album-tete{display:grid;grid-template-columns:180px 1fr;gap:24px;align-items:start}
.album-tete .infos{display:grid;gap:12px}
.formats{display:flex;gap:12px;flex-wrap:wrap}
.formats .fm{display:grid;gap:2px;padding:12px 16px;border-radius:12px;background:var(--fond);min-width:150px}
.formats .fm small{font-size:12px;color:var(--gris);font-weight:600}
.formats .fm b{font-size:18px}
.formats .fm span{font-size:12px;color:var(--clair)}
@media(max-width:1100px){.app{grid-template-columns:1fr}.lat{position:static;height:auto;flex-direction:row;flex-wrap:wrap;padding:12px}.lat .marque{padding:6px 10px}.lat .bas{margin:0}.deux,.fiche{grid-template-columns:1fr}.sommaire{display:none}.haut .recherche{width:auto;flex:1}}
@media(max-width:700px){.lat{flex-wrap:nowrap;overflow-x:auto;gap:2px;padding:10px 8px}.lat .marque{display:none}.lat .sep{display:none}.lat a{white-space:nowrap;padding:8px 10px}.lat .bas{display:contents}.haut{padding:10px 16px;gap:10px}.haut .droite .btn span{display:none}.haut .qui{display:none}.page{padding:18px 16px 80px}.album-tete{grid-template-columns:1fr}.grille-champs > *{grid-column:span 12}}
'''

# ------------------------------------------------ B, Carnet : navigation claire, cartes, panneau latéral
B_CSS = r'''
.app{display:grid;grid-template-columns:200px 1fr;min-height:100vh}
.lat{padding:22px 14px;display:flex;flex-direction:column;gap:4px;position:sticky;top:0;height:100vh;border-right:1px solid var(--trait)}
.lat .marque{padding:4px 10px 18px}
.lat .marque img{height:38px;width:auto}
.lat .marque span{display:block;font-size:12px;color:var(--clair);margin-top:6px}
.lat a{display:flex;align-items:center;gap:10px;padding:9px 10px;border-radius:10px;text-decoration:none;font-weight:600;font-size:14px;color:var(--gris);transition:background .15s,color .15s}
.lat a:hover{background:var(--blanc);color:var(--encre)}
.lat a.on{background:var(--blanc);color:var(--bord);box-shadow:var(--ombre)}
.lat a .n{margin-left:auto;font-size:11px;background:var(--bord-l);color:var(--bord);padding:2px 7px;border-radius:999px}
.lat .groupe{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--clair);font-weight:700;padding:14px 10px 4px}
.lat .bas{margin-top:auto;display:grid;gap:2px}
.page{padding:28px 36px 80px;display:grid;gap:22px;max-width:1180px}
.tete{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}
.tete h1{font-size:34px}
.tete .actions{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.matin{display:grid;grid-template-columns:1.4fr 1fr;gap:22px;align-items:start}
.matin .bonjour{display:grid;gap:18px}
.matin .bonjour h1{font-size:38px}
.matin .bonjour p.lead{font-size:17px;color:var(--gris);max-width:48ch}
.mini-cal{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;text-align:center;font-size:13px}
.mini-cal .j{font-size:11px;color:var(--clair);font-weight:700;text-transform:uppercase;padding:4px 0}
.mini-cal .d{padding:8px 0;border-radius:8px;color:var(--gris)}
.mini-cal .d.ev{background:var(--bord-l);color:var(--bord);font-weight:700}
.mini-cal .d.auj{outline:2px solid var(--encre);color:var(--encre);font-weight:700}
.mini-cal .d.vide{opacity:0}
.mois-titre{display:flex;align-items:baseline;gap:12px;margin:8px 0 4px}
.mois-titre h2{font-size:22px}.mois-titre span{font-size:13px;color:var(--clair)}
.cartes-dates{display:grid;gap:8px}
.cd{display:grid;grid-template-columns:46px 1fr auto auto;gap:16px;align-items:center;background:var(--blanc);border-radius:14px;padding:12px 16px;box-shadow:var(--ombre);text-decoration:none;cursor:pointer;transition:transform .15s,box-shadow .15s;border:2px solid transparent}
.cd:hover{transform:translateY(-1px)}
.cd.on{border-color:var(--bord)}
.cd b{display:block;font-size:15px}.cd span{font-size:13px;color:var(--gris)}
.cd .aff{width:40px;height:54px;border-radius:6px;background:var(--trait2);display:grid;place-items:center;color:var(--clair);overflow:hidden}
.cd .aff img{width:100%;height:100%;object-fit:cover}
.cd.brouillon{opacity:.75;border-style:dashed;border-color:var(--trait)}
.panneau{position:fixed;top:0;right:0;width:min(560px,100%);height:100vh;background:var(--blanc);box-shadow:-20px 0 60px -30px rgba(0,0,0,.35);z-index:6;display:flex;flex-direction:column;animation:glisse .25s ease-out}
@keyframes glisse{from{transform:translateX(30px);opacity:0}to{transform:none;opacity:1}}
.panneau .pt{display:flex;align-items:center;gap:12px;padding:18px 24px;border-bottom:1px solid var(--trait)}
.panneau .pt h2{font-size:22px}
.panneau .pt .x{margin-left:auto;width:34px;height:34px;border-radius:50%;display:grid;place-items:center;background:var(--fond)}
.panneau .pc{padding:22px 24px;overflow:auto;display:grid;gap:20px;align-content:start}
.panneau .pb{margin-top:auto;padding:14px 24px;border-top:1px solid var(--trait);display:flex;gap:10px;align-items:center;font-size:13px;color:var(--gris)}
.panneau .pb .lien.danger{color:var(--ko);margin-left:auto}
.bloc{display:grid;gap:12px}
.bloc h3{font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:var(--clair);font-weight:700}
.voile{position:fixed;inset:0;background:rgba(29,26,23,.25);z-index:5}
.album-b{display:grid;grid-template-columns:260px 1fr;gap:28px;align-items:start}
.album-b .colg{display:grid;gap:14px;position:sticky;top:28px}
.album-b .colg .carte{padding:16px}
.fm-ligne{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--trait2);font-size:14px}
.fm-ligne:last-child{border:0}
.fm-ligne b{font-size:15px}
.fm-ligne small{color:var(--clair);display:block;font-size:12px}
.albums-mini{display:grid;gap:8px}
.albums-mini a{display:grid;grid-template-columns:44px 1fr auto;gap:12px;align-items:center;text-decoration:none;font-size:13px;padding:6px;border-radius:10px}
.albums-mini a:hover{background:var(--fond)}
.albums-mini a.on{background:var(--bord-l)}
.albums-mini img{border-radius:6px}
.albums-mini b{display:block;font-size:13px}.albums-mini span{color:var(--clair);font-size:12px}
@media(max-width:1100px){.album-b{grid-template-columns:1fr}.album-b .colg{position:static}}
@media(max-width:1000px){.app{grid-template-columns:1fr}.lat{position:static;height:auto;flex-direction:row;flex-wrap:nowrap;overflow-x:auto;border:0;border-bottom:1px solid var(--trait);padding:10px;gap:2px;align-items:center}.lat .groupe,.lat .marque span{display:none}.lat .marque{padding:0 8px 0 0}.lat .marque img{height:30px}.lat a{white-space:nowrap}.lat .bas{display:contents}.matin,.album-b{grid-template-columns:1fr}.album-b .colg{position:static}.tete .actions .recherche{width:100%!important}}
@media(max-width:700px){.page{padding:18px 16px 80px}.matin .bonjour h1{font-size:28px}div[style*='grid-template-columns:1fr 1fr']{grid-template-columns:1fr!important}.cd{grid-template-columns:46px 1fr}.cd > :nth-child(n+3){display:none}.chiffres{grid-template-columns:repeat(2,1fr)}.grille-champs > *{grid-column:span 12}}
'''

# ------------------------------------------------ C, Scène : bandeau bordeaux à onglets, maître-détail
C_CSS = r'''
.bandeau{background:var(--bord);color:#fff;padding:0 32px}
.bandeau .h{display:flex;align-items:center;gap:20px;padding:16px 0 10px}
.bandeau .h .marque{font-family:var(--display);font-size:20px;display:flex;align-items:center;gap:12px}
.bandeau .h .marque img{height:34px;filter:brightness(0) invert(1);opacity:.95}
.bandeau .h .recherche{margin-left:auto;background:rgba(255,255,255,.14);border-color:transparent;color:#f3e4e7;width:320px}
.bandeau .h .recherche input{color:#fff}.bandeau .h .recherche input::placeholder{color:#e3c9ce}
.bandeau .h .recherche kbd{border-color:rgba(255,255,255,.3);color:#e3c9ce}
.bandeau .h .qui{display:flex;align-items:center;gap:10px;font-size:13px;color:#f3e4e7}
.bandeau .h .qui a{color:#fff;font-weight:700;text-decoration:none}
.onglets{display:flex;gap:2px;overflow:auto}
.onglets a{display:inline-flex;align-items:center;gap:8px;padding:12px 16px;border-radius:12px 12px 0 0;color:#f3e4e7;text-decoration:none;font-weight:600;font-size:14px;white-space:nowrap;transition:background .15s}
.onglets a:hover{background:rgba(255,255,255,.1);color:#fff}
.onglets a.on{background:var(--fond);color:var(--encre)}
.onglets a .n{font-size:11px;background:rgba(255,255,255,.2);padding:2px 7px;border-radius:999px}
.onglets a.on .n{background:var(--bord-l);color:var(--bord)}
.page{padding:26px 32px 80px;display:grid;gap:22px}
.tete{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;flex-wrap:wrap}
.tete h1{font-size:32px}
.tete .actions{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.md{display:grid;grid-template-columns:minmax(360px,2fr) 3fr;gap:0;background:var(--blanc);border-radius:18px;box-shadow:var(--ombre);overflow:hidden;min-height:620px}
.md .liste{border-right:1px solid var(--trait);display:flex;flex-direction:column}
.md .liste .outils{padding:14px 16px;border-bottom:1px solid var(--trait);display:grid;gap:10px}
.md .liste .outils .recherche{padding:7px 12px}
.md .liste .items{overflow:auto;flex:1}
.md .liste .mois{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--clair);font-weight:700;padding:14px 16px 6px;background:var(--blanc);position:sticky;top:0}
.item{display:grid;grid-template-columns:46px 1fr auto;gap:12px;align-items:center;padding:10px 16px;text-decoration:none;cursor:pointer;border-left:3px solid transparent;transition:background .15s}
.item:hover{background:var(--fond)}
.item.on{background:var(--bord-l);border-left-color:var(--bord)}
.item b{display:block;font-size:14px}.item span{font-size:12px;color:var(--gris)}
.item .etat{display:grid;gap:4px;justify-items:end}
.item.brouillon{opacity:.6}
.md .detail{padding:24px 28px;display:grid;gap:20px;align-content:start}
.md .detail .dt{display:flex;align-items:flex-start;justify-content:space-between;gap:16px}
.md .detail .dt h2{font-size:26px}
.md .detail .dt p{color:var(--gris);font-size:14px;margin-top:4px}
.md .detail .dt .actions{display:flex;gap:6px}
.icone-btn{width:36px;height:36px;border-radius:10px;display:grid;place-items:center;background:var(--fond);color:var(--gris);cursor:pointer;transition:background .15s,color .15s}
.icone-btn:hover{background:var(--bord-l);color:var(--bord)}
.icone-btn.danger:hover{background:var(--ko-l);color:var(--ko)}
.section{display:grid;gap:12px}
.section h3{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--clair);font-weight:700;display:flex;align-items:center;gap:8px}
.section h3::after{content:"";flex:1;height:1px;background:var(--trait)}
.bord-c{display:grid;grid-template-columns:2fr 1fr;gap:22px;align-items:start}
.cal-mois{background:var(--blanc);border-radius:18px;box-shadow:var(--ombre);padding:20px 22px}
.cal-mois .cm{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}
.cal-mois .cm h2{font-size:24px}
.cal-mois .cm .nav{display:flex;gap:4px}
.cal-mois .g{display:grid;grid-template-columns:repeat(7,1fr);gap:4px}
.cal-mois .g .j{font-size:11px;color:var(--clair);text-transform:uppercase;font-weight:700;padding:4px 6px}
.cal-mois .g .d{min-width:0;min-height:74px;border-radius:10px;padding:6px 8px;font-size:13px;background:var(--fond);display:grid;align-content:start;gap:4px}
.cal-mois .g .d.vide{background:transparent}
.cal-mois .g .d.auj>span{font-weight:700;color:var(--bord)}
.cal-mois .g .d .ev{font-size:11px;font-weight:700;background:var(--bord);color:#fff;border-radius:6px;padding:2px 6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.cal-mois .g .d .ev.brouillon{background:var(--att-l);color:var(--att)}
.cal-mois .g .d .ev.stage{background:var(--encre)}
.cote{display:grid;gap:22px}
.album-c{display:grid;grid-template-columns:3fr 2fr;gap:0;background:var(--blanc);border-radius:18px;box-shadow:var(--ombre);overflow:hidden}
.album-c .liste{padding:22px 24px;border-right:1px solid var(--trait)}
.album-c .liste .at{display:grid;grid-template-columns:96px 1fr;gap:18px;align-items:center;margin-bottom:18px}
.album-c .liste .at h2{font-size:24px}
.album-c .liste .at p{color:var(--gris);font-size:14px}
.album-c .detail{padding:22px 24px;display:grid;gap:18px;align-content:start;background:#fcfbf9}
.album-c .detail h2{font-size:24px}
.lecteur{display:grid;gap:10px;background:var(--encre);color:#fff;border-radius:14px;padding:16px}
.lecteur .l{display:flex;align-items:center;gap:12px;font-size:13px}
.lecteur .play{width:40px;height:40px;border-radius:50%;background:#fff;color:var(--encre);display:grid;place-items:center}
.lecteur .play svg{width:16px;height:16px}
.lecteur .onde{display:flex;align-items:end;gap:2px;height:36px;flex:1}
.lecteur .onde i{flex:1;background:#8a7f76;border-radius:2px}
.lecteur .onde i.on{background:#fff}
.piste.on{background:var(--bord-l)}
@media(max-width:1100px){.bord-c{grid-template-columns:1fr}}
@media(max-width:1000px){.md,.album-c{grid-template-columns:1fr}.md .liste,.album-c .liste{border-right:0;border-bottom:1px solid var(--trait)}.md .liste .items{max-height:360px}.bandeau .h .recherche{width:auto;flex:1}}
@media(max-width:700px){.bandeau{padding:0 14px}.bandeau .h{flex-wrap:wrap;gap:10px}.bandeau .h .recherche{width:100%;margin:0}.album-c .liste .at{grid-template-columns:72px 1fr}.md .detail,.album-c .liste,.album-c .detail{padding:16px}.page{padding:18px 14px 80px}.chiffres{grid-template-columns:repeat(2,1fr)}.grille-champs > *{grid-column:span 12}.cal-mois .g .d{min-height:46px}.cal-mois .g .d .ev{display:none}.cal-mois .g .d.ev-oui{background:var(--bord-l)}.bandeau .h .qui{display:none}}
'''

# ---------------------------------------------------------------- Maquettes
MAQ = [
    ('a', 'Pupitre', 'Barre latérale sombre, tableaux denses, fiche sur une page entière avec sommaire.', A_CSS, ['bord', 'dates', 'date', 'album']),
    ('b', 'Carnet', 'Navigation claire, cartes groupées par mois, la fiche s\'ouvre en panneau sur le côté.', B_CSS, ['bord', 'dates', 'album']),
    ('c', 'Scène', 'Bandeau bordeaux à onglets, liste et fiche côte à côte, calendrier au centre du tableau de bord.', C_CSS, ['bord', 'dates', 'album']),
]
LIB = {'bord': 'Tableau de bord', 'dates': 'Dates', 'date': 'Fiche d\'une date', 'album': 'Album'}

def barre(code):
    onglets = ''.join('<a href="%s-bord.html"%s><b>%d</b> <span>%s</span></a>' % (c, ' class="actif"' if c == code else '', i + 1, n) for i, (c, n, _, _, _) in enumerate(MAQ))
    i = [m[0] for m in MAQ].index(code)
    prev = MAQ[(i - 1) % 3][0]; nxt = MAQ[(i + 1) % 3][0]
    return ('<div class="barre-maq" role="navigation" aria-label="Navigation entre les maquettes"><a class="retour" href="index.html">&#8592; <span class="mot">Les 3 consoles</span></a>'
            '<div class="onglets">%s</div><div class="fleches"><a href="%s-bord.html" aria-label="Maquette précédente">&#8249;</a><a href="%s-bord.html" aria-label="Maquette suivante">&#8250;</a></div></div>' % (onglets, prev, nxt))

def doc(code, page, titre, css, corps, extra=''):
    return '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s, console %s</title>
<meta name="robots" content="noindex, nofollow">
<meta name="copyright" content="Maquette (c) Sylvain Caron 2026.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Figtree:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/barre.css">
<style>%s%s%s</style>
</head>
<body>
%s
%s
<script>if(location.search.indexOf('nobar')>-1)document.body.classList.add('barre-cachee');</script>
</body>
</html>
''' % (e(titre), e(dict((m[0], m[1]) for m in MAQ)[code]), BASE_CSS, css, extra, barre(code), corps)

def nav_liens(code, actif):
    out = []
    for cle, lib, ic in NAV:
        href = '%s-%s.html' % (code, cle) if cle in ('bord', 'dates', 'album') else '#'
        n = {'dates': COMPTE['dates'], 'commandes': COMPTE['a_expedier']}.get(cle)
        out.append('<a href="%s"%s>%s<span>%s</span>%s</a>' % (href, ' class="on"' if cle == actif else '', I[ic], e(lib), ('<span class="n">%d</span>' % n) if n else ''))
    return ''.join(out)

ETAT = '<div class="etat-sauv">%s Enregistré à l\'instant</div>' % I['ok']

def afaire():
    return ('<div class="afaire">'
            '<a href="#"><span class="p">%s</span><span><b>%d dates sans affiche</b><span>Les affiches rendent l\'agenda plus vivant</span></span><span class="fl">%s</span></a>'
            '<a href="#"><span class="p">%s</span><span><b>%d pistes sans MP3</b><span>Vol. 23 : 2 chargées sur 14, les autres albums à faire</span></span><span class="fl">%s</span></a>'
            '<a href="#"><span class="p">%s</span><span><b>%d commandes à expédier</b><span>Clés USB et CD payés, à poster</span></span><span class="fl">%s</span></a>'
            '<a href="#"><span class="p">%s</span><span><b>Dernière sauvegarde : cette nuit, 3h00</b><span>Base et fichiers, 1,2 Go, copie hors serveur faite</span></span><span class="fl">%s</span></a>'
            '</div>') % (I['image'], COMPTE['sans_affiche'], I['chevron'], I['onde'], COMPTE['pistes'] - COMPTE['mp3'], I['chevron'], I['panier'], COMPTE['a_expedier'], I['chevron'], I['sauv'], I['chevron'])

def chiffres():
    return ('<div class="chiffres">'
            '<a class="chiffre" href="#"><small>Prochaine date</small><b>Demain</b><span>Abbeville, Théâtre Municipal</span></a>'
            '<a class="chiffre" href="#"><small>Dates à venir</small><b>%d</b><span>jusqu\'en mars 2027</span></a>'
            '<a class="chiffre alerte" href="#"><small>À expédier</small><b>%d</b><span>commandes payées</span></a>'
            '<a class="chiffre" href="#"><small>Ventes d\'octobre</small><b>85 €</b><span>5 commandes</span></a>'
            '</div>') % (COMPTE['dates'], COMPTE['a_expedier'])

def table_dates(n=6, liens=True):
    rows = []
    for d in DATES[:n]:
        iso, deb, fin, typ, lieu, ville, dep, pub, aff = d
        dd = dt(iso)
        rows.append('<tr><td><span class="cal"><small>%s</small><b>%d</b></span></td><td><b>%s</b> (%s)<small>%s</small></td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
            JC[dd.weekday()][:3], dd.day, e(ville), dep, e(lieu or 'Lieu à préciser'), e(horaire(deb, fin)),
            '<span class="badge ok">%s Visible</span>' % I['ok'] if pub else '<span class="badge att">Brouillon</span>',
            '<span class="badge bord">Affiche</span>' if aff else '<span class="badge">Sans affiche</span>'))
    return '<table class="tableau"><thead><tr><th></th><th>Date et lieu</th><th>Horaire</th><th>État</th><th>Affiche</th></tr></thead><tbody>%s</tbody></table>' % ''.join(rows)

def table_commandes():
    rows = ''.join('<tr><td><b>%s</b><small>%s</small></td><td>%s</td><td class="num">%s</td><td>%s</td></tr>' % (
        n, d, e(a), t, '<span class="badge att">%s</span>' % s if s == 'À expédier' else '<span class="badge ok">%s</span>' % s) for n, d, a, t, s in COMMANDES)
    return '<table class="tableau"><thead><tr><th>Commande</th><th>Article</th><th class="num">Total</th><th>État</th></tr></thead><tbody>%s</tbody></table>' % rows

def champs_date(d, mode='large'):
    iso, deb, fin, typ, lieu, ville, dep, pub, aff = d
    MOYEN = {3: 6, 2: 3, 5: 6, 6: 12, 7: 6}
    c = lambda n: 'c%d' % (n if mode == 'large' else MOYEN.get(n, 12) if mode == 'moyen' else 12)
    return ('<div class="grille-champs">'
            '<label class="champ %s">Date <input type="text" value="%s"><span class="etat">%s enregistré</span></label>'
            '<label class="champ %s">Début <input type="text" value="%s" placeholder="14h30"></label>'
            '<label class="champ %s">Fin <input type="text" value="%s" placeholder="19h00"></label>'
            '<label class="champ %s">Type <input type="text" value="%s" placeholder="Thé dansant, repas dansant, concert"></label>'
            '<label class="champ %s">Lieu (salle) <input type="text" value="%s"></label>'
            '<label class="champ %s">Adresse <input type="text" value="" placeholder="Rue et numéro"></label>'
            '<label class="champ %s">Code postal <input type="text" value="80100"></label>'
            '<label class="champ %s">Ville <input type="text" value="%s"></label>'
            '<label class="champ %s">Dép. <input type="text" value="%s"></label>'
            '<label class="champ %s">Téléphones de réservation <input type="text" value="03 22 31 34 89" placeholder="Séparés par des virgules"></label>'
            '<label class="champ %s">Détails (repas, invités) <textarea rows="2">Festival de l\'accordéon</textarea></label>'
            '</div>') % (c(3), date_longue(iso), I['ok'], c(2), (deb or '').replace(':', 'h'), c(2), (fin or '').replace(':', 'h'), c(5), e(typ or ''),
                         c(6), e(lieu or ''), c(6), c(2), c(7), e(ville), c(3), e(dep), c(6), c(6))

def apercu_site(d):
    iso, deb, fin, typ, lieu, ville, dep, pub, aff = d
    dd = dt(iso)
    return ('<div class="apercu-site"><span class="cal"><small>%s</small><b>%d</b></span><div><em>Tel que sur le site</em><b>%s (%s)</b>, %s<br><span style="color:var(--gris)">%s, %s</span></div></div>'
            % (JC[dd.weekday()][:3], dd.day, e(ville), dep, e(horaire(deb, fin)), e(lieu or ''), e(typ or 'Bal')))

def pistes_liste(sel=None, cls=''):
    out = ['<div class="piste-tete"><span></span><span></span><span>Titre</span><span>Danse</span><span>Extrait</span><span>MP3</span><span>Prix</span><span></span></div>']
    for n, t, danse, mp3, ext in PISTES:
        out.append(('<div class="piste%s"><span class="poignee">%s</span><span class="n">%d</span><input type="text" value="%s"><input type="text" value="%s">'
                    '<span class="play%s">%s</span>'
                    '<span class="f %s">%s %s</span><span class="f %s">%s</span><span class="poignee">%s</span></div>') % (
            ' on' if sel == n else '', I['poignee'], n, e(t), e(danse), '' if ext else ' off', I['lecture'],
            'oui' if mp3 else 'non', I['ok'] if mp3 else I['horloge'], 'Chargé, 8,4 Mo' if mp3 else 'À charger',
            'oui' if mp3 else 'non', '1,50 €' if mp3 else 'après le MP3', I['corbeille']))
    return ''.join(out)

def depot_mp3():
    return '<div class="depot">%s<b>Déposez les MP3 de l\'album ici</b><span>Plusieurs fichiers d\'un coup. Le numéro et le titre sont lus dans le fichier, l\'extrait de 30 secondes est fabriqué tout seul.</span></div>' % I['sauv']

JAQ = ASSETS_SITE + '/img/jaquettes/' + ALBUM['slug'] + '.webp'
LOGO = ASSETS_SITE + '/img/live/logo-dp-ligne-fonce.png'

# ================================================================ A
def a_coque(actif, corps, titre_haut=''):
    return ('<div class="app"><aside class="lat"><div class="marque"><b>Damien Poyard</b><span>Console du site</span></div>%s<div class="sep"></div><div class="bas">'
            '<a href="#">%s<span>Voir le site</span></a><a href="#">%s<span>Déconnexion</span></a></div></aside>'
            '<div><header class="haut"><label class="recherche">%s<input type="search" placeholder="Rechercher une date, un titre, une commande"><kbd>⌘K</kbd></label>'
            '<div class="droite"><a class="btn petit prim" href="#">%s<span>Ajouter une date</span></a><span class="qui"><i>DP</i>Damien</span></div></header>'
            '<main class="page">%s</main></div></div>%s') % (nav_liens('a', actif), I['externe'], I['sortie'], I['loupe'], I['plus'], corps, ETAT)

def a_bord():
    corps = ('<div class="tete"><div><span class="sur">Samedi 24 octobre 2026</span><h1>Bonjour Damien</h1></div></div>'
             + chiffres() +
             '<div class="deux"><div class="carte"><h2>Prochaines dates <a class="lien" href="a-dates.html">Toutes les dates %s</a></h2>%s</div>'
             '<div style="display:grid;gap:22px"><div class="carte"><h2>À compléter</h2>%s</div>'
             '<div class="carte"><h2>Dernières commandes <a class="lien" href="#">Toutes %s</a></h2>%s</div></div></div>') % (I['fleche'], table_dates(6), afaire(), I['fleche'], table_commandes())
    return a_coque('bord', corps)

def a_dates():
    filtres = ('<div class="filtres"><span class="f on">À venir <b>%d</b></span><span class="f">Passées</span><span class="f">Brouillons <b>1</b></span><span style="width:12px"></span>'
               '<span class="f">%s Novembre 2026</span><span class="f">Saône-et-Loire (71)</span><span class="f">Sans affiche <b>%d</b></span></div>') % (COMPTE['dates'], I['cal'], COMPTE['sans_affiche'])
    rows = []
    for d in DATES:
        iso, deb, fin, typ, lieu, ville, dep, pub, aff = d
        dd = dt(iso)
        rows.append('<tr><td><span class="cal"><small>%s</small><b>%d</b></span></td><td><b><a href="a-date.html" style="text-decoration:none">%s</a></b> (%s)<small>%s %s</small></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><span style="display:flex;gap:4px"><a class="btn sec petit" href="a-date.html">Modifier</a><a class="btn sec petit" href="#" title="Dupliquer">%s</a></span></td></tr>' % (
            JC[dd.weekday()][:3], dd.day, e(ville), dep, MOIS[dd.month - 1], dd.year, e(lieu or 'Lieu à préciser'), e(horaire(deb, fin)),
            '<span class="badge ok">%s Visible</span>' % I['ok'] if pub else '<span class="badge att">Brouillon</span>',
            '<span class="badge bord">Affiche</span>' if aff else '<span class="badge">Sans affiche</span>', I['copie']))
    table = '<table class="tableau"><thead><tr><th></th><th>Date et ville</th><th>Lieu</th><th>Horaire</th><th>État</th><th>Affiche</th><th></th></tr></thead><tbody>%s</tbody></table>' % ''.join(rows)
    corps = ('<div class="tete"><div><span class="sur">Agenda</span><h1>Dates</h1></div><div class="actions"><a class="btn sec" href="#">%s Calendrier</a><a class="btn prim" href="a-date.html">%s Ajouter une date</a></div></div>'
             '%s<div class="carte" style="padding:8px 10px">%s</div><p class="note-maq">10 dates affichées sur 37, les suivantes se chargent en faisant défiler.</p>') % (I['cal'], I['plus'], filtres, table)
    return a_coque('dates', corps)

def a_date():
    d = DATES[0]
    corps = ('<div class="tete"><div><a class="lien" href="a-dates.html">%s Toutes les dates</a><h1 style="margin-top:8px">%s, Abbeville</h1></div>'
             '<div class="actions"><label class="interrupteur on"><i></i>Visible sur le site</label><a class="btn sec" href="#">%s Dupliquer</a></div></div>'
             '<div class="fiche"><div>'
             '<div class="carte" id="quand"><h2>Quand et où</h2>%s</div>'
             '<div class="carte" id="affiche"><h2>Affiche</h2><div style="display:grid;grid-template-columns:120px 1fr;gap:18px;align-items:center"><img src="%s/img/affiche-abbeville.webp" alt="" style="border-radius:8px;box-shadow:var(--ombre)"><div style="display:grid;gap:10px"><p style="font-size:14px;color:var(--gris)">affiche-abbeville.jpg, 420 Ko, recadrée automatiquement pour la liste.</p><div style="display:flex;gap:8px"><a class="btn sec petit" href="#">Remplacer</a><a class="lien" style="color:var(--ko)" href="#">Retirer</a></div></div></div></div>'
             '<div class="carte" id="site"><h2>Sur le site</h2>%s<p class="note-maq" style="margin-top:10px">Le site affiche cette ligne dans l\'agenda et sur l\'accueil si la date est parmi les six prochaines.</p></div>'
             '<div style="display:flex;justify-content:space-between;align-items:center;padding:0 4px"><span class="note-maq">Créée le 12 septembre 2026, modifiée aujourd\'hui à 10h12.</span><a class="lien" style="color:var(--ko)" href="#">%s Supprimer cette date</a></div>'
             '</div><nav class="sommaire"><a class="on" href="#quand">Quand et où</a><a href="#affiche">Affiche</a><a href="#site">Sur le site</a></nav></div>') % (
        I['retour'], date_longue(d[0]), I['copie'], champs_date(d), ASSETS_SITE, apercu_site(d), I['corbeille'])
    return a_coque('dates', corps)

def a_album():
    corps = ('<div class="tete"><div><a class="lien" href="#">%s Tous les albums</a><h1 style="margin-top:8px">Vol. 23, %s</h1></div>'
             '<div class="actions"><label class="interrupteur on"><i></i>En vente sur le site</label><a class="btn sec" href="#">%s Voir la fiche publique</a></div></div>'
             '<div class="fiche"><div>'
             '<div class="carte" id="album"><div class="album-tete"><div style="display:grid;gap:8px"><img class="jaquette" src="%s" alt=""><a class="lien" href="#">Remplacer la jaquette</a></div>'
             '<div class="infos"><div class="grille-champs"><label class="champ c8">Nom de l\'album <input type="text" value="%s"></label><label class="champ c4">Volume <input type="text" value="23"></label>'
             '<label class="champ c12">Présentation (sur la fiche de l\'album) <textarea rows="2">14 titres pour danser, du paso à la valse, enregistrés en 2026.</textarea></label></div>'
             '<div class="formats"><div class="fm"><small>CD</small><b>10,00 €</b><span>1 000 en stock, 50 g</span></div><div class="fm"><small>Clé USB</small><b>15,00 €</b><span>800 en stock, 50 g</span></div><div class="fm" style="background:var(--bord-l)"><small>Titre à l\'unité</small><b>1,50 €</b><span>réglage commun à tous les albums</span></div></div></div></div></div>'
             '<div class="carte" id="pistes"><h2>Pistes <span class="badge att">%s 2 MP3 sur 14</span></h2>%s<div style="height:14px"></div>%s</div>'
             '</div><nav class="sommaire"><a class="on" href="#album">L\'album</a><a href="#pistes">Pistes</a><a href="#">Formats et stock</a><a href="#">Référencement</a></nav></div>') % (
        I['retour'], e(ALBUM['nom']), I['externe'], JAQ, e(ALBUM['nom']), I['horloge'], pistes_liste(), depot_mp3())
    return a_coque('album', corps)

# ================================================================ B
def b_coque(actif, corps, extra=''):
    liens = []
    groupes = [('Chaque semaine', ['bord', 'dates', 'commandes']), ('Le catalogue', ['album', 'partitions']), ('Le site', ['pages', 'seo', 'sauvegardes', 'reglages'])]
    for g, cles in groupes:
        liens.append('<div class="groupe">%s</div>' % g)
        for cle, lib, ic in NAV:
            if cle in cles:
                href = 'b-%s.html' % cle if cle in ('bord', 'dates', 'album') else '#'
                n = {'dates': COMPTE['dates'], 'commandes': COMPTE['a_expedier']}.get(cle)
                liens.append('<a href="%s"%s>%s<span>%s</span>%s</a>' % (href, ' class="on"' if cle == actif else '', I[ic], e(lib), ('<span class="n">%d</span>' % n) if n else ''))
    return ('<div class="app"><aside class="lat"><div class="marque"><img src="%s" alt="Damien Poyard"><span>Console du site</span></div>%s<div class="bas"><a href="#">%s<span>Voir le site</span></a><a href="#">%s<span>Déconnexion</span></a></div></aside>'
            '<main class="page">%s</main></div>%s%s') % (LOGO, ''.join(liens), I['externe'], I['sortie'], corps, extra, ETAT)

def mini_cal():
    # novembre 2026 : commence un dimanche
    evs = {dt(d[0]).day for d in DATES if d[0].startswith('2026-11')}
    cells = ''.join('<span class="j">%s</span>' % j[0] for j in JC)
    cells += '<span class="d vide"></span>' * 6
    for j in range(1, 31):
        cells += '<span class="d%s">%d</span>' % (' ev' if j in evs else '', j)
    return '<div class="carte"><h2>Novembre 2026 <a class="lien" href="b-dates.html">Agenda %s</a></h2><div class="mini-cal">%s</div></div>' % (I['fleche'], cells)

def b_bord():
    corps = ('<div class="matin"><div class="bonjour"><div><span class="sur">Samedi 24 octobre 2026</span><h1>Bonjour Damien, demain c\'est Abbeville.</h1></div>'
             '<p class="lead">Théâtre Municipal, à partir de 14h30. Il reste 3 commandes à poster et 35 dates sans affiche dans l\'agenda.</p>'
             '<div style="display:flex;gap:8px;flex-wrap:wrap"><a class="btn prim" href="b-dates.html">%s Ajouter une date</a><a class="btn sec" href="#">%s Voir les commandes</a><a class="btn sec" href="b-album.html">%s Charger des MP3</a></div></div>%s</div>'
             '%s'
             '<div style="display:grid;grid-template-columns:1fr 1fr;gap:22px"><div class="carte"><h2>À compléter</h2>%s</div><div class="carte"><h2>Dernières commandes <a class="lien" href="#">Toutes %s</a></h2>%s</div></div>') % (
        I['plus'], I['panier'], I['onde'], mini_cal(), chiffres(), afaire(), I['fleche'], table_commandes())
    return b_coque('bord', corps)

def b_dates(panneau=True):
    mois = {}
    for d in DATES:
        mois.setdefault(dt(d[0]).month, []).append(d)
    blocs = []
    for m, ds in mois.items():
        cartes = []
        for d in ds:
            iso, deb, fin, typ, lieu, ville, dep, pub, aff = d
            dd = dt(iso)
            cartes.append(('<a class="cd%s%s" href="#"><span class="cal"><small>%s</small><b>%d</b></span><span><b>%s (%s)</b><span>%s, %s</span></span>'
                           '<span>%s</span><span class="aff">%s</span></a>') % (
                ' on' if d is DATES[0] else '', '' if pub else ' brouillon', JC[dd.weekday()][:3], dd.day, e(ville), dep, e(lieu or 'Lieu à préciser'), e(horaire(deb, fin)),
                '<span class="badge ok">%s Visible</span>' % I['ok'] if pub else '<span class="badge att">Brouillon</span>',
                '<img src="%s/img/affiche-abbeville.webp" alt="">' % ASSETS_SITE if aff else I['image']))
        blocs.append('<div class="mois-titre"><h2>%s %d</h2><span>%d date%s</span></div><div class="cartes-dates">%s</div>' % (MOIS[m - 1].capitalize(), 2026, len(ds), 's' if len(ds) > 1 else '', ''.join(cartes)))
    corps = ('<div class="tete"><div><span class="sur">Agenda</span><h1>Dates à venir</h1></div><div class="actions"><label class="recherche" style="width:260px">%s<input type="search" placeholder="Ville, salle"></label><a class="btn prim" href="#">%s Ajouter une date</a></div></div>'
             '<div class="filtres"><span class="f on">À venir <b>37</b></span><span class="f">Passées</span><span class="f">Sans affiche <b>35</b></span><span class="f">Brouillons <b>1</b></span></div>%s'
             '<p class="note-maq">Cliquer sur une date ouvre sa fiche sur le côté, sans quitter la liste.</p>') % (I['loupe'], I['plus'], ''.join(blocs))
    d = DATES[0]
    pan = ('<div class="voile"></div><aside class="panneau"><div class="pt"><span class="cal"><small>Dim.</small><b>25</b></span><div><h2>Abbeville (80)</h2><span style="font-size:13px;color:var(--gris)">%s</span></div><span class="x">✕</span></div>'
           '<div class="pc"><label class="interrupteur on"><i></i>Visible sur le site</label>%s'
           '<div class="bloc"><h3>Affiche</h3><div style="display:grid;grid-template-columns:90px 1fr;gap:14px;align-items:center"><img src="%s/img/affiche-abbeville.webp" alt="" style="border-radius:8px"><div style="display:grid;gap:8px;font-size:14px;color:var(--gris)">affiche-abbeville.jpg, 420 Ko<div style="display:flex;gap:10px"><a class="btn sec petit" href="#">Remplacer</a><a class="lien" style="color:var(--ko)" href="#">Retirer</a></div></div></div></div>'
           '<div class="bloc"><h3>Sur le site</h3>%s</div></div>'
           '<div class="pb"><span>%s Enregistré à 10h12</span><a class="lien" href="#">%s Dupliquer</a><a class="lien danger" href="#">%s Supprimer</a></div></aside>') % (
        date_longue(d[0]), champs_date(d, mode='moyen'),
        ASSETS_SITE, apercu_site(d).replace('class="apercu-site"', 'class="apercu-site" style="background:var(--fond)"'), I['ok'], I['copie'], I['corbeille'])
    return b_coque('dates', corps, pan if panneau else '')

def b_album():
    albums = ''.join('<a href="#"%s><img src="%s/img/jaquettes/%s.webp" alt=""><span><b>%s</b><span>%s</span></span><span class="badge%s">%s MP3</span></a>' % (
        ' class="on"' if i == 0 else '', ASSETS_SITE, slug, e(nom), v, ' att' if i == 0 else '', mp3) for i, (v, nom, slug, mp3) in enumerate(ALBUMS))
    corps = ('<div class="tete"><div><span class="sur">Boutique</span><h1>Albums</h1></div><div class="actions"><a class="btn sec" href="#">%s Nouvel album</a></div></div>'
             '<div class="album-b"><div class="colg"><div class="carte"><img class="jaquette" src="%s" alt=""><div style="display:grid;gap:10px;margin-top:14px"><b style="font-family:var(--display);font-weight:400;font-size:18px">Vol. 23, %s</b><label class="interrupteur on"><i></i>En vente</label>'
             '<div><div class="fm-ligne"><span>CD<small>1 000 en stock</small></span><b>10,00 €</b></div><div class="fm-ligne"><span>Clé USB<small>800 en stock</small></span><b>15,00 €</b></div><div class="fm-ligne"><span>Titre à l\'unité<small>réglage commun</small></span><b>1,50 €</b></div></div>'
             '<a class="lien" href="#">Modifier les formats %s</a></div></div><div class="carte"><h2 style="font-size:16px">Les autres albums</h2><div class="albums-mini">%s</div><a class="lien" href="#" style="margin-top:8px">Les 11 albums %s</a></div></div>'
             '<div style="display:grid;gap:18px"><div class="carte"><h2>Pistes <span class="badge att">%s 2 MP3 sur 14</span></h2>%s</div><div class="carte">%s</div>'
             '<div class="carte"><h2>Sur le site</h2><div class="grille-champs"><label class="champ c12">Présentation <textarea rows="2">14 titres pour danser, du paso à la valse, enregistrés en 2026.</textarea></label><label class="champ c6">Adresse de la page <input type="text" value="/boutique/vol-23-la-vie-est-belle-chantons-l-amour"></label><label class="champ c6">Titre pour Google <input type="text" value="Vol. 23 La vie est belle, Damien Poyard"></label></div></div></div></div>') % (
        I['plus'], JAQ, e(ALBUM['nom']), I['fleche'], albums, I['fleche'], I['horloge'], pistes_liste(), depot_mp3())
    return b_coque('album', corps)

# ================================================================ C
def c_coque(actif, corps):
    ong = []
    for cle, lib, ic in NAV:
        href = 'c-%s.html' % cle if cle in ('bord', 'dates', 'album') else '#'
        n = {'dates': COMPTE['dates'], 'commandes': COMPTE['a_expedier']}.get(cle)
        ong.append('<a href="%s"%s>%s<span>%s</span>%s</a>' % (href, ' class="on"' if cle == actif else '', I[ic], e(lib), ('<span class="n">%d</span>' % n) if n else ''))
    return ('<header class="bandeau"><div class="h"><span class="marque"><img src="%s" alt="">Console du site</span><label class="recherche">%s<input type="search" placeholder="Rechercher partout"><kbd>⌘K</kbd></label>'
            '<span class="qui">Damien · <a href="#">Voir le site</a> · <a href="#">Sortir</a></span></div><nav class="onglets">%s</nav></header><main class="page">%s</main>%s') % (LOGO, I['loupe'], ''.join(ong), corps, ETAT)

def cal_mois():
    evs = {}
    for d in DATES:
        if d[0].startswith('2026-11'):
            evs[dt(d[0]).day] = d
    cells = ''.join('<span class="j">%s</span>' % j for j in JC)
    cells += '<span class="d vide"></span>' * 6
    for j in range(1, 31):
        d = evs.get(j)
        ev = ''
        if d:
            cls = 'stage' if d[3] == 'Stage' else ('' if d[7] else 'brouillon')
            ev = '<span class="ev %s">%s</span>' % (cls, e(d[5]))
        cells += '<span class="d%s"><span>%d</span>%s</span>' % (' ev-oui' if d else '', j, ev)
    return ('<div class="cal-mois"><div class="cm"><h2>Novembre 2026</h2><div class="nav"><span class="icone-btn">%s</span><span class="icone-btn" style="transform:scaleX(-1)">%s</span><a class="btn sec petit" href="c-dates.html">Liste</a></div></div><div class="g">%s</div></div>') % (I['retour'], I['retour'], cells)

def c_bord():
    corps = ('<div class="tete"><div><span class="sur">Samedi 24 octobre 2026</span><h1>Bonjour Damien</h1></div><div class="actions"><a class="btn prim" href="c-dates.html">%s Ajouter une date</a></div></div>'
             '%s<div class="bord-c">%s<div class="cote"><div class="carte"><h2>À compléter</h2>%s</div><div class="carte"><h2>Commandes <a class="lien" href="#">Toutes %s</a></h2>%s</div></div></div>') % (
        I['plus'], chiffres(), cal_mois(), afaire(), I['fleche'], table_commandes())
    return c_coque('bord', corps)

def c_dates():
    items = []
    mois_vu = None
    for d in DATES:
        iso, deb, fin, typ, lieu, ville, dep, pub, aff = d
        dd = dt(iso)
        if dd.month != mois_vu:
            mois_vu = dd.month
            items.append('<div class="mois">%s %d</div>' % (MOIS[dd.month - 1], dd.year))
        items.append('<a class="item%s%s" href="#"><span class="cal"><small>%s</small><b>%d</b></span><span><b>%s (%s)</b><span>%s</span></span><span class="etat">%s%s</span></a>' % (
            ' on' if d is DATES[0] else '', '' if pub else ' brouillon', JC[dd.weekday()][:3], dd.day, e(ville), dep, e(lieu or 'Lieu à préciser'),
            '<span class="badge att">Brouillon</span>' if not pub else '', '<span class="badge bord">Affiche</span>' if aff else '<span class="badge">Sans affiche</span>'))
    d = DATES[0]
    detail = ('<div class="dt"><div><h2>%s</h2><p>Abbeville (80), Théâtre Municipal. Visible sur le site depuis le 12 septembre.</p></div><div class="actions"><span class="icone-btn" title="Voir sur le site">%s</span><span class="icone-btn" title="Dupliquer">%s</span><span class="icone-btn danger" title="Supprimer">%s</span></div></div>'
              '<label class="interrupteur on"><i></i>Visible sur le site</label>'
              '<div class="section"><h3>Quand et où</h3>%s</div>'
              '<div class="section"><h3>Affiche</h3><div style="display:grid;grid-template-columns:90px 1fr;gap:14px;align-items:center"><img src="%s/img/affiche-abbeville.webp" alt="" style="border-radius:8px;box-shadow:var(--ombre)"><div style="display:grid;gap:8px;font-size:14px;color:var(--gris)">affiche-abbeville.jpg, 420 Ko<div style="display:flex;gap:10px"><a class="btn sec petit" href="#">Remplacer</a><a class="lien" style="color:var(--ko)" href="#">Retirer</a></div></div></div></div>'
              '<div class="section"><h3>Sur le site</h3>%s</div>') % (date_longue(d[0]), I['oeil'], I['copie'], I['corbeille'], champs_date(d), ASSETS_SITE, apercu_site(d))
    corps = ('<div class="tete"><div><span class="sur">Agenda</span><h1>Dates</h1></div><div class="actions"><a class="btn sec" href="c-bord.html">%s Calendrier</a><a class="btn prim" href="#">%s Ajouter une date</a></div></div>'
             '<div class="md"><div class="liste"><div class="outils"><label class="recherche">%s<input type="search" placeholder="Ville, salle, département"></label><div class="filtres"><span class="f on">À venir <b>37</b></span><span class="f">Passées</span><span class="f">Sans affiche</span></div></div><div class="items">%s</div></div>'
             '<div class="detail">%s</div></div>') % (I['cal'], I['plus'], I['loupe'], ''.join(items), detail)
    return c_coque('dates', corps)

def c_album():
    onde = ''.join('<i style="height:%d%%" class="%s"></i>' % (h, 'on' if i < 14 else '') for i, h in enumerate([30, 55, 70, 45, 80, 60, 35, 75, 90, 50, 40, 65, 85, 55, 30, 60, 70, 45, 35, 65, 80, 50, 40, 75, 55, 30, 60, 45, 70, 35, 50, 65]))
    detail = ('<div><span class="sur">Piste 2 sur 14</span><h2>La vie est belle</h2><p style="color:var(--gris);font-size:14px">Marche festive, 3 min 12, chargée le 24 octobre.</p></div>'
              '<div class="lecteur"><div class="l"><span class="play">%s</span><div class="onde">%s</div><span>0:00 / 0:30</span></div><span style="font-size:12px;color:#c9beb5">Extrait de 30 secondes fabriqué automatiquement à partir du MP3. Déplacez le début si besoin.</span></div>'
              '<div class="grille-champs"><label class="champ c8">Titre <input type="text" value="La vie est belle"></label><label class="champ c4">Danse <input type="text" value="Marche festive"></label>'
              '<label class="champ c6">Auteurs <input type="text" value="Damien Poyard" placeholder="Paroles et musique"></label><label class="champ c6">Lié à la partition <input type="text" value="Aucune" placeholder="Choisir un titre du catalogue"></label></div>'
              '<div class="section"><h3>Fichier</h3><div style="display:flex;gap:14px;align-items:center;font-size:14px"><span class="badge ok">%s MP3 chargé</span><span style="color:var(--gris)">02-la-vie-est-belle.mp3, 8,4 Mo, 320 kb/s</span><a class="lien" href="#" style="margin-left:auto">Remplacer</a></div></div>'
              '<div class="section"><h3>Vente à l\'unité</h3><div style="display:flex;gap:14px;align-items:center;font-size:14px"><label class="interrupteur on"><i></i>En vente</label><span style="color:var(--gris)">1,50 €, prix commun réglé dans Réglages</span></div></div>') % (I['lecture'], onde, I['ok'])
    corps = ('<div class="tete"><div><a class="lien" href="#">%s Tous les albums</a><h1 style="margin-top:8px">Vol. 23, %s</h1></div><div class="actions"><label class="interrupteur on"><i></i>En vente</label><a class="btn sec" href="#">%s Formats et stock</a><a class="btn sec" href="#">%s Fiche publique</a></div></div>'
             '<div class="album-c"><div class="liste"><div class="at"><img class="jaquette" src="%s" alt=""><div><h2>14 pistes</h2><p>2 MP3 chargés, 2 extraits prêts. Glissez les pistes pour changer l\'ordre.</p></div></div>%s<div style="height:14px"></div>%s</div>'
             '<div class="detail">%s</div></div>') % (I['retour'], e(ALBUM['nom']), I['reglages'], I['externe'], JAQ, pistes_liste(sel=2), depot_mp3(), detail)
    return c_coque('album', corps)

# ---------------------------------------------------------------- Index
def index():
    cartes = []
    for i, (code, nom, desc, _, pages) in enumerate(MAQ):
        liens = ''.join('<a href="%s-%s.html">%s</a>' % (code, p, LIB[p]) for p in pages)
        cartes.append(('<article class="maq"><div class="num">%d</div><a class="visuel" href="%s-bord.html"><div class="chrome"><i></i><i></i><i></i></div><img src="apercus/%s-bord.webp" alt="Aperçu de la console %s" width="1000" height="722"></a>'
                       '<div class="texte"><h2>%s</h2><p>%s</p><div class="liens">%s</div><a class="btn" href="%s-bord.html">Ouvrir la console %d %s</a></div></article>') % (
            i + 1, code, code, e(nom), e(nom), e(desc), liens, code, i + 1, I['fleche']))
    return '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Damien Poyard, la console de gestion, 3 visuels</title>
<meta name="robots" content="noindex, nofollow">
<meta name="copyright" content="Maquettes (c) Sylvain Caron 2026.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Figtree:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root{--fond:#f7f5f2;--encre:#1d1a17;--gris:#5f5852;--bord:#7b1f2f;--trait:#e6e0d8;--display:'Marcellus',Georgia,serif;--body:'Figtree',system-ui,sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--body);background:var(--fond);color:var(--encre);line-height:1.55;-webkit-font-smoothing:antialiased}
img{display:block;max-width:100%%;height:auto}
h1,h2{font-family:var(--display);font-weight:400;line-height:1.1}
.wrap{width:min(1180px,100%% - 32px);margin-inline:auto}
.top{background:var(--encre);color:#fff;padding:56px 0 72px;position:relative;overflow:hidden}
.top::before{content:"";position:absolute;width:800px;height:800px;border-radius:50%%;background:radial-gradient(circle,rgba(123,31,47,.55),transparent 60%%);right:-240px;top:-380px}
.top .wrap{position:relative}
.top .sur{font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:#e3c9ce;font-weight:700}
.top h1{font-size:clamp(36px,5vw,60px);margin:12px 0 18px;max-width:18ch}
.top p{font-size:18px;color:#cfc7bf;max-width:60ch}
.top .ecrans{display:flex;gap:10px;flex-wrap:wrap;margin-top:28px}
.top .ecrans span{padding:8px 14px;border-radius:999px;background:rgba(255,255,255,.1);font-size:14px;font-weight:600}
.liste{display:grid;gap:36px;padding:48px 0 80px}
.maq{display:grid;grid-template-columns:1.3fr 1fr;gap:32px;align-items:center;background:#fff;border-radius:24px;padding:28px;box-shadow:0 1px 2px rgba(29,26,23,.06),0 20px 50px -30px rgba(29,26,23,.35);position:relative}
.maq .num{position:absolute;top:-16px;left:28px;width:44px;height:44px;border-radius:50%%;background:var(--bord);color:#fff;display:grid;place-items:center;font-family:var(--display);font-size:22px}
.maq .visuel{display:block;border-radius:14px;overflow:hidden;box-shadow:0 14px 40px -20px rgba(0,0,0,.5);transition:transform .25s}
.maq .visuel:hover{transform:translateY(-4px)}
.maq .chrome{display:flex;gap:6px;padding:8px 12px;background:#ece7e0}
.maq .chrome i{width:10px;height:10px;border-radius:50%%;background:#c9c1b7}
.maq h2{font-size:34px;margin-bottom:10px}
.maq p{color:var(--gris);font-size:17px;margin-bottom:18px}
.maq .liens{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:22px}
.maq .liens a{padding:6px 12px;border-radius:999px;border:1px solid var(--trait);font-size:13px;font-weight:600;text-decoration:none;color:var(--gris)}
.maq .liens a:hover{border-color:var(--bord);color:var(--bord)}
.btn{display:inline-flex;align-items:center;gap:8px;padding:12px 20px;border-radius:999px;font-weight:700;background:var(--encre);color:#fff;text-decoration:none;transition:background .2s}
.btn:hover{background:var(--bord)}
.btn svg{width:18px;height:18px}
.commun{padding:0 0 80px}
.commun h2{font-size:30px;margin-bottom:16px}
.commun ul{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;list-style:none}
.commun li{background:#fff;border-radius:16px;padding:18px 20px;font-size:15px;color:var(--gris)}
.commun li b{display:block;color:var(--encre);margin-bottom:4px;font-size:16px}
footer{padding:24px 0 40px;font-size:13px;color:var(--gris)}
@media(max-width:900px){.maq{grid-template-columns:1fr}.commun ul{grid-template-columns:1fr}}
</style>
</head>
<body>
<header class="top"><div class="wrap"><span class="sur">Damien Poyard, refonte du site</span><h1>La console de gestion, trois visuels</h1>
<p>Même contenu, mêmes données réelles (dates de novembre, Vol. 23, dernières commandes), trois façons de s'organiser. Chaque console montre le tableau de bord, les dates et un album. Le reste (partitions, commandes, pages et menus, SEO, sauvegardes) reprendra la composition choisie.</p>
<div class="ecrans"><span>Tableau de bord</span><span>Dates</span><span>Fiche d'une date</span><span>Album et pistes</span></div></div></header>
<main class="wrap"><div class="liste">%s</div>
<section class="commun"><h2>Dans les trois, d'office</h2><ul>
<li><b>Enregistrement automatique</b>Chaque champ part au serveur quand on le quitte, un signal discret le confirme en bas à droite.</li>
<li><b>Dates et heures en français</b>Dimanche 25 octobre 2026, 14h30. Plus de 10/25/2026 02:30 PM.</li>
<li><b>Ce qu'il reste à faire</b>Affiches manquantes, MP3 à charger, commandes à poster : visibles dès l'ouverture.</li>
<li><b>Aperçu « tel que sur le site »</b>La ligne de l'agenda ou la fiche album telle que le public la verra.</li>
<li><b>MP3 par lot</b>Douze fichiers glissés d'un coup, numéros et titres lus dedans, extraits fabriqués tout seuls.</li>
<li><b>Recherche partout</b>Une date, un titre, une commande, depuis n'importe quel écran.</li>
</ul></section></main>
<footer class="wrap">Maquettes (c) Sylvain Caron 2026. Pages statiques. Les données viennent du site (agenda public, catalogue), aucune donnée personnelle.</footer>
</body>
</html>
''' % ''.join(cartes)

# ---------------------------------------------------------------- Écriture
def main():
    os.makedirs(os.path.join(OUT, 'apercus'), exist_ok=True)
    pages = {
        'a-bord': ('Tableau de bord', A_CSS, a_bord()), 'a-dates': ('Dates', A_CSS, a_dates()), 'a-date': ('Fiche d\'une date', A_CSS, a_date()), 'a-album': ('Album', A_CSS, a_album()),
        'b-bord': ('Tableau de bord', B_CSS, b_bord()), 'b-dates': ('Dates', B_CSS, b_dates()), 'b-album': ('Album', B_CSS, b_album()),
        'c-bord': ('Tableau de bord', C_CSS, c_bord()), 'c-dates': ('Dates', C_CSS, c_dates()), 'c-album': ('Album', C_CSS, c_album()),
    }
    for nom, (titre, css, corps) in pages.items():
        with open(os.path.join(OUT, nom + '.html'), 'w', encoding='utf-8') as f:
            f.write(doc(nom[0], nom, titre, css, corps))
    with open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index())
    print('%d pages écrites dans %s' % (len(pages) + 1, OUT))

if __name__ == '__main__':
    main()
