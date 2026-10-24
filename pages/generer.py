# -*- coding: utf-8 -*-
# Générateur des pages maquettées (visuel Portrait révisé), (c) Sylvain Caron 2026.
import os, html

OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)

PAGES = [
    ('accueil.html', 'Accueil'),
    ('agenda.html', 'Agenda'),
    ('boutique.html', 'Boutique'),
    ('album.html', 'Album'),
    ('partitions.html', 'Partitions'),
    ('famille.html', 'Valses'),
    ('titre.html', 'Titre'),
]

SACEM = "Dans le cas d'une diffusion publique de ces oeuvres, Merci de bien vouloir mentionner les titres et compositeurs sur votre programme SACEM."

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
DL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M12 3v12M7 10l5 5 5-5M5 21h14"/></svg>'
TEL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2Z"/></svg>'
YT = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12 31 31 0 0 0 1 16.8a3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .5-4.8 31 31 0 0 0-.5-4.8ZM9.7 15.1V8.9L15.5 12l-5.8 3.1Z"/></svg>'
PLAY = '<button class="play" data-play aria-pressed="false" aria-label="Écouter un extrait"><svg class="lect" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4v16l13-8z"/></svg><svg class="pause" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg></button>'
CART = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.7 13.4a2 2 0 0 0 2 1.6h9.7a2 2 0 0 0 2-1.6L23 6H6"/></svg>'
ICO_CAL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="3"/><path d="M16 3v4M8 3v4M3 11h18M8 15h.01M12 15h.01M16 15h.01"/></svg>'
ICO_DISC = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2.5"/><path d="M12 3a9 9 0 0 1 9 9" stroke-width="2.4"/></svg>'
ICO_NOTE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M9 18V6l11-2v12"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/></svg>'
ICO_FILE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/></svg>'
ICO_WAVE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M3 12h2l2-5 3 10 3-14 3 14 2-5h3"/></svg>'

# ---------- Données reprises de la base locale (import du site actuel) ----------
JOURS = ['Lun.', 'Mar.', 'Mer.', 'Jeu.', 'Ven.', 'Sam.', 'Dim.']
JOURS_LONG = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
MOIS_C = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.']

# (date, debut, fin, titre, lieu, ville, dep, type, [tels], details, affiche)
AGENDA = [
    ('2026-10-25', '14:30', None, 'Abbeville', 'Théâtre Municipal', 'Abbeville', '80', None, ['0322313489'], 'Festival de l\'accordéon', '../assets/img/affiche-abbeville.webp'),
    ('2026-11-01', '14:30', '19:00', 'Saint-Germain-du-Bois', 'Salle des fêtes', 'Saint-Germain-du-Bois', '71', None, ['0682974705'], None, None),
    ('2026-11-02', '14:30', '19:00', 'Le Broadway', 'Zone commerciale Nationale 7', 'Portes-lès-Valence', '26', None, ['0767016735'], None, None),
    ('2026-11-05', None, None, 'Beffes', 'Salle des fêtes', 'Beffes', '18', None, ['0651514484'], 'Avec Christophe Demerson', None),
    ('2026-11-07', '15:00', '18:30', 'Autun', 'Salle de l\'Hexagone', 'Autun', '71', 'Stage', ['0607261210'], 'Stage de danse en ligne', None),
    ('2026-11-08', '14:30', None, 'Le Looping', 'Saint-Désert', 'Saint-Désert', '71', None, ['0385479018'], None, None),
    ('2026-11-11', '14:30', '19:00', 'Paray-le-Monial', 'Centre culturel et de congrès', 'Paray-le-Monial', '71', None, ['0385811797', '0676997853'], None, None),
    ('2026-11-12', '14:15', '19:00', 'Selongey', 'Salle des fêtes Frédéric Lescure', 'Selongey', '21', None, ['0771080954', '0671521359'], None, None),
    ('2026-11-14', '14:30', '19:00', 'Saint-Just-la-Pendue', 'Salle des fêtes', 'Saint-Just-la-Pendue', '42', None, ['0772294891'], None, None),
    ('2026-11-15', '14:15', '19:00', 'Le Palatino', None, 'Labergement-lès-Seurre', '21', None, ['0623765900'], None, None),
    ('2026-11-19', None, None, 'O\'Complexe', 'Repas le midi', 'Francourt', '70', None, ['0384926984'], None, None),
    ('2026-11-22', '14:30', '19:30', 'Le Rétro 60', 'Le Champ Monte', 'Lamenay-sur-Loire', '58', None, ['0386507492'], None, None),
    ('2026-11-26', '14:30', '19:30', 'Bourg-de-Thizy', None, 'Bourg-de-Thizy', '69', None, ['0667650796'], None, None),
    ('2026-11-28', '14:30', '19:00', 'Ouroux-sur-Saône', 'Salle des fêtes', 'Ouroux-sur-Saône', '71', None, ['0617421462'], None, None),
    ('2026-11-29', '14:30', '19:00', 'L\'Isle-sur-Serein', 'Salle des fêtes', 'L\'Isle-sur-Serein', '89', None, ['0789851878', '0780002116'], None, None),
    ('2026-12-01', '14:30', '19:00', 'Saint-Didier-sur-Chalaronne', 'Salle de la Lyre, place Georges Agniel', 'Saint-Didier-sur-Chalaronne', '01', None, ['0623029472'], 'Avec Olivier Boulard', None),
    ('2026-12-03', '14:30', '19:00', 'La Bamba', '476 avenue Saint-Martin', 'Magneux-Haute-Rive', '42', None, ['0477761127'], None, None),
    ('2026-12-05', '14:30', '19:30', 'Sevrey', 'Salle des fêtes', 'Sevrey', '71', 'Thé dansant', ['0676290666'], 'Thé dansant du club de danse « À pas comptés »', '../assets/img/affiche-sevrey.webp'),
    ('2026-12-06', '14:30', '19:30', 'Autun', 'Salle de l\'Hexagone', 'Autun', '71', None, ['0607261210'], None, None),
    ('2026-12-08', None, None, 'La Belle Époque', 'La Combe aux Jardinets, repas le midi', 'Pouilley-Français', '25', None, ['0381810817'], 'Avec Olivier Boulard', None),
    ('2026-12-10', '14:30', None, 'La Croisette d\'Hérival', None, 'Girmont-Val-d\'Ajol', '88', None, ['0689959847'], 'Avec Cyril Blanchard', None),
    ('2026-12-12', '14:30', '19:00', 'La Pacaudière', 'Salle des fêtes', 'La Pacaudière', '42', None, ['0679448399'], None, None),
    ('2026-12-13', '14:30', None, 'Les Arcades de Barjavelle', None, 'Courpière', '63', None, ['0473536118'], None, None),
    ('2026-12-16', '14:00', '18:00', 'La Ficelle', 'Salle de la Ficelle', 'Lyon', '69', None, [], None, None),
    ('2026-12-17', None, None, 'Le Looping', 'Repas de Noël', 'Saint-Désert', '71', None, ['0385479018'], None, None),
    ('2026-12-20', '14:30', None, 'La Belle Époque', 'La Combe aux Jardinets', 'Pouilley-Français', '25', None, ['0381810817'], None, None),
    ('2027-01-03', '14:30', '19:30', 'La Bamba', '476 avenue Saint-Martin', 'Magneux-Haute-Rive', '42', None, ['0477761127'], None, None),
    ('2027-01-07', '14:30', '19:00', 'Baudemont', 'Salle des fêtes', 'Baudemont', '71', None, ['0629955967', '0681744287'], None, None),
    ('2027-01-09', '15:00', '18:00', 'Espace culturel de Bioux', 'Centre culturel et de loisirs', 'Mâcon', '71', None, ['0613355086'], None, None),
    ('2027-01-10', '14:00', '18:30', 'Le Mic Mac', 'Salle à côté du stade', 'Saint-Maur', '39', None, ['0633206635'], None, None),
    ('2027-01-14', '15:00', '19:30', 'Champs-sur-Yonne', 'Salle Podium, 5 min au sud d\'Auxerre', 'Champs-sur-Yonne', '89', None, ['0764694135'], None, None),
    ('2027-01-16', '14:30', '19:00', 'Laiz', 'Salle des fêtes, ouverture des portes à 13h30', 'Laiz', '01', None, ['0681702996', '0685655821'], 'Avec Olivier Boulard', None),
    ('2027-01-17', '14:30', '19:00', 'Le Crystal', 'Quartier Tine Rodet', 'Saint-Désirat', '07', None, ['0650351747'], None, None),
    ('2027-01-21', '14:30', '19:00', 'Perrex', 'Salle des fêtes', 'Perrex', '01', None, ['0695563869'], None, None),
    ('2027-01-24', '14:15', '19:00', 'Le Palatino', None, 'Labergement-lès-Seurre', '21', None, ['0623765900'], None, None),
    ('2027-01-28', '14:30', '19:30', 'Bourg-de-Thizy', 'Espace culturel et musical', 'Thizy-les-Bourgs', '69', None, [], 'Assiette gourmande en fin d\'après-midi', None),
    ('2027-01-31', '14:30', '19:00', 'La Belle Époque', 'La Combe aux Jardinets', 'Pouilley-Français', '25', None, ['0381810817'], None, None),
]

ALBUMS = [  # (vol, nom, slug, cd, usb, pistes)
    (23, 'La vie est belle, chantons l\'amour', 'vol-23-la-vie-est-belle-chantons-l-amour', 10, 15, 19),
    (22, 'Y\'a pas mieux que la musique', 'vol-22-y-a-pas-mieux-que-la-musique', 10, 15, 18),
    (21, 'La vie est faite pour danser', 'vol-21-la-vie-est-faite-pour-danser', 10, 15, 18),
    (20, 'Olé Ola pour la musique', 'vol-20-ole-ola-pour-la-musique', 10, 15, 18),
    (19, 'Du bonheur et rien d\'autre', 'vol-19-du-bonheur-et-rien-d-autre', 10, 15, 18),
    (18, 'Le bal des retrouvailles', 'vol-18-le-bal-des-retrouvailles', 10, 15, 20),
    (17, 'Mille étoiles dans le ciel', 'vol-17-mille-etoiles-dans-le-ciel', 10, 15, 21),
    (16, 'La Casa de Luisa', 'vol-16-la-casa-de-luisa', 10, 15, 21),
    (15, 'Le Kadansé', 'vol-15-le-kadanse', None, None, 21),
    (11, 'Tant qu\'il y aura l\'amour', 'vol-11-tant-qu-il-y-aura-l-amour', None, None, 25),
    (None, 'Avec le temps', 'avec-le-temps', None, None, 12),
]

PISTES_23 = [
    (1, 'Oberlands', 'Marche festive'), (2, 'La vie est belle', 'Marche festive'), (3, 'Colomba Bianca', 'Boléro'),
    (4, 'Trois petites notes en Bavière', 'Valse'), (5, 'Blumen aus Holland', 'Valse'), (6, 'Amamé', 'Merengué'),
    (7, 'Être libre', 'Merengué'), (8, 'Couleur menthe à l\'eau', 'Slow'), (9, 'España Cañí', 'Paso'),
    (10, 'Morena de mi Copla', 'Paso'), (11, 'La Cumparsita', 'Tango'), (12, 'Noche de Fuego', 'Tango'),
    (13, 'Le Disco', 'Disco'), (14, 'We are the champions', 'Slow rock'), (15, 'La java des bals de France', 'Java'),
    (16, 'Kizomba', 'Kizomba'), (17, 'C\'est quand le bonheur', 'Foxtrot'), (18, 'Le bonheur en musique', 'Foxtrot'),
    (19, 'Au plus près de nos cœurs', 'Ballade'),
]

FAMILLES = [  # (nom, slug, nb)
    ('Valse viennoise', 'valse-viennoise', 1), ('Valse', 'valse', 25), ('Tarentelle', 'tarentelle', 5), ('Tango', 'tango', 11),
    ('Boléro', 'bolero', 14), ('Boston', 'boston', 2), ('Bourrée', 'bourree', 1), ('Chacha', 'chacha', 5), ('Charleston', 'charleston', 1),
    ('Country', 'country', 2), ('Cumbia', 'cumbia', 2), ('Foxtrot', 'foxtrot', 12), ('Gigue', 'gigue', 1), ('Java', 'java', 6),
    ('Madison', 'madison', 4), ('Mambo', 'mambo', 2), ('Marche', 'marche', 5), ('Marche festive', 'marche-festive', 12), ('Paso', 'paso', 13),
    ('Polka', 'polka', 9), ('Rock & Roll', 'rock-and-roll', 3), ('Rumba', 'rumba', 1), ('Salsa', 'salsa', 1), ('Samba', 'samba', 3),
    ('Sirtaki', 'sirtaki', 1), ('Slowfox', 'slowfox', 3), ('Ambiance', 'ambiance', 5), ('Bachata', 'bachata', 1), ('Baïon', 'baion', 8),
    ('Ballade', 'ballade', 2), ('Danse en ligne et nouvelle danse', 'danse-en-ligne-et-nouvelle-danse', 12), ('Slow rock', 'slowrock', 3), ('Scottish', 'scottish', 1),
]

VALSES = [  # (nom, nb versions)
    ('Au rendez-vous des copains', 2), ('Autrefois à Vienne', 2), ('Bouquet de romances', 2), ('C\'est la fête des voisins', 2),
    ('Cette valse mexicaine', 2), ('Devinez la danse', 1), ('En chantant l\'amour', 2), ('Escapade mexicaine', 2), ('Et si on tournait', 2),
    ('Et tu tournes', 2), ('J\'écoute l\'accordéon', 1), ('L\'accordéon dans les bruyères', 2), ('La plus belle valse du monde', 2),
    ('Le temps d\'une romance', 2), ('Merci, merci', 2), ('Ne laissons pas filer les étoiles', 2), ('Nos mamies', 2), ('On sort l\'accordéon', 1),
    ('Pour une valse avec toi', 2), ('P\'tit bouquet de jeunesse', 2), ('P\'tite fleur d\'Alsace', 1), ('Quand reviendront les airs d\'accordéon', 2),
    ('Refrain charmeur', 2), ('Sur un air tyrolien', 2), ('Sur un vent de liberté', 2), ('Valsons sur les souvenirs', 1),
]

DERNIERS = [('Foxtrot', 'Adieu l\'Amour, adieu ma Terre', 2), ('Foxtrot', 'Je t\'aime en bleu et blanc', 2), ('Tango', 'Noche de Fuego', 2), ('Samba', 'Être libre', 3)]


def e(s):
    return html.escape(s, quote=True)


def tel_fmt(t):
    return ' '.join(t[i:i + 2] for i in range(0, 10, 2))


def tel_href(t):
    return 'tel:+33' + t[1:]


def date_parts(d):
    import datetime
    dt = datetime.date.fromisoformat(d)
    return dt, JOURS[dt.weekday()], JOURS_LONG[dt.weekday()], dt.day, MOIS[dt.month - 1], MOIS_C[dt.month - 1]


def horaire(deb, fin):
    if deb and fin:
        return 'de %s à %s' % (deb.replace(':', 'h'), fin.replace(':', 'h'))
    if deb:
        return 'à partir de %s' % deb.replace(':', 'h')
    return None


# ---------- Enveloppe commune ----------
def barre(actif):
    i = [p[0] for p in PAGES].index(actif)
    prev = PAGES[i - 1][0]
    nxt = PAGES[(i + 1) % len(PAGES)][0]
    tabs = ''.join('<a href="%s"%s><b>%d</b><span>%s</span></a>' % (f, ' class="actif" aria-current="page"' if f == actif else '', n + 1, lbl) for n, (f, lbl) in enumerate(PAGES))
    return ('<div class="barre-maq" role="navigation" aria-label="Navigation entre les pages maquettées"><a class="retour" href="index.html">&#8592; <span class="mot">Les pages du site,</span> 7 pages</a>'
            '<div class="onglets">%s</div><div class="fleches"><a href="%s" title="Page précédente" aria-label="Page précédente">&#8249;</a><a href="%s" title="Page suivante" aria-label="Page suivante">&#8250;</a></div></div>' % (tabs, prev, nxt))


def entete(actif):
    def nav(f, lbl):
        cur = ' aria-current="page"' if f == actif else ''
        return '<a href="%s"%s>%s</a>' % (f, cur, lbl)
    return '''<header class="entete">
  <div class="wrap">
    <div class="pilule">
      <a class="logo-img" href="accueil.html"><img src="../assets/img/live/logo-dp-ligne-fonce.png" alt="Damien Poyard, auteur compositeur interprète" width="1363" height="245"></a>
      <button class="burger" data-menu aria-controls="menu" aria-expanded="false">Menu</button>
      <nav class="nav" id="menu" aria-label="Menu principal">
        %s
        %s
        %s
        <a class="yt" href="#">%sYouTube</a>
      </nav>
    </div>
  </div>
</header>
''' % (nav('agenda.html', 'Agenda'), nav('boutique.html', 'Boutique'), nav('partitions.html', 'Partitions et bandes orchestre'), YT)


PIED = '''<footer>
  <div class="wrap">
    <span class="logo-img logo-pied"><img src="../assets/img/live/logo-dp-fonce.png" alt="Damien Poyard, auteur compositeur interprète" width="1028" height="750"></span>
    <nav aria-label="Pied de page"><a href="agenda.html">Agenda</a><a href="boutique.html">Boutique</a><a href="partitions.html">Partitions et bandes orchestre</a><a href="#">Biographie</a><a href="#">Contact</a><a href="#">YouTube</a><a href="#">Mentions légales</a><a href="#">Confidentialité</a><a href="#">Conditions de vente</a><a href="#">Gérer mes cookies</a></nav>
    <p class="bas">Maquette © Sylvain Caron 2026. Textes, dates, pochettes et photos repris du site actuel et des envois de Damien Poyard.</p>
  </div>
</footer>
'''


def page(fichier, titre, corps, extra_css=''):
    doc = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s | Damien Poyard, maquette</title>
<meta name="robots" content="noindex, nofollow">
<meta name="copyright" content="Maquette (c) Sylvain Caron 2026.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Bodoni+Moda:wght@600;700&family=Figtree:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/barre.css">
<link rel="stylesheet" href="pages.css">
%s</head>
<body>
%s
%s
<main>
%s</main>
%s<script src="../assets/commun.js"></script>
</body>
</html>
''' % (e(titre), ('<style>%s</style>\n' % extra_css) if extra_css else '', barre(fichier), entete(fichier), corps, PIED)
    with open(os.path.join(OUT, fichier), 'w', encoding='utf-8') as f:
        f.write(doc)


def tete_page(sur, h1, intro=None, fil=None):
    out = '<section class="wrap tete-page arrive">'
    if fil:
        out += '<nav class="fil" aria-label="Fil d\'Ariane">%s</nav>' % ' <i>›</i> '.join(fil)
    out += '<span class="sur2">%s</span><h1>%s</h1>' % (sur, h1)
    if intro:
        out += '<p class="intro">%s</p>' % intro
    return out + '</section>\n'


def ligne_date(row, compact=False):
    d, deb, fin, titre, lieu, ville, dep, typ, tels, details, affiche = row
    dt, jc, jl, jour, mois, moisc = date_parts(d)
    h = horaire(deb, fin)
    titre_aff = titre if titre.lower() == ville.lower() else '%s, %s' % (titre, ville)
    out = '<li class="rdv"><div class="cal"><small>%s</small><b>%d</b><span>%s</span></div><div class="corps"><h3>%s <span class="dep">(%s)</span></h3>' % (jc, jour, moisc, e(titre_aff), dep)
    sub = [x for x in [lieu, h] if x]
    if sub:
        out += '<p>%s</p>' % e('. '.join(sub).replace('.. ', '. '))
    if details and not compact:
        out += '<p class="det">%s</p>' % e(details)
    if typ:
        out += '<span class="badge">%s</span>' % e(typ)
    out += '</div><div class="actions">'
    for t in tels:
        out += '<a class="tel" href="%s">%s%s</a>' % (tel_href(t), TEL, tel_fmt(t))
    if affiche and not compact:
        out += '<a class="aff" href="%s" target="_blank" rel="noopener"><img src="%s" alt="Affiche" width="120" height="160"><span>Voir l\'affiche</span></a>' % (affiche, affiche)
    out += '</div></li>'
    return out


# ---------- 1. Accueil ----------
def accueil():
    rub = lambda href, ico, b, s: '<li><a class="rub" href="%s"><span class="picto">%s</span><span><b>%s</b><span>%s</span></span><span class="fl">%s</span></a></li>' % (href, ico, b, s, ARROW)
    prochaine = AGENDA[0]
    dt, jc, jl, jour, mois, moisc = date_parts(prochaine[0])
    corps = '''<section class="wrap">
  <div class="hero">
    <div class="portrait arrive">
      <img src="../assets/img/live/damien-2027.webp" alt="Damien Poyard et son accordéon, sur fond clair" width="1800" height="1279">
      <a class="prochaine" href="agenda.html"><span class="cal"><small>%s</small><b>%d</b></span><span><em>Prochain rendez-vous</em>%s (%s), %s</span></a>
    </div>
    <div class="panneau arrive d1">
      <div>
        <small class="sur">Auteur compositeur interprète</small>
        <h1 class="nom">Damien Poyard</h1>
        <p class="lead">Chanteur accordéoniste</p>
      </div>
      <ul class="rubs" aria-label="Les trois rubriques">
        %s
        %s
        %s
      </ul>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="tete"><div><span class="sur2">Agenda</span><h2>Nos prochains rendez-vous</h2></div><a class="lien" href="agenda.html">Tout l'agenda %s</a></div>
    <ul class="rdvs deux">
%s
    </ul>
  </div>
</section>

<section class="wrap">
  <div class="bandeau"><img src="../assets/img/damien-concert-1.webp" alt="Damien Poyard face à une salle comble" width="1024" height="678"><div class="t"><span class="contour">En bal</span><p>Repas dansants, thés dansants, spectacles et concerts.</p></div></div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="album">
      <div class="pochette"><a href="album.html"><img src="../assets/img/jaquettes/vol-23-la-vie-est-belle-chantons-l-amour.webp" alt="Jaquette du volume 23, La vie est belle, chantons l'amour" width="900" height="900"></a></div>
      <div>
        <span class="sur2">Le nouvel album · Vol. 23</span>
        <h2>La vie est belle, chantons l'amour</h2>
        <p>19 titres à écouter sur la fiche de l'album, en CD, en clé USB ou titre par titre.</p>
        <div class="formats"><a href="album.html"><small>En CD</small><b>10 €</b></a><a href="album.html"><small>En clé USB</small><b>15 €</b></a></div>
        <p class="cheque">Vous préférez le chèque ? <a href="#">Imprimer le bon de commande</a></p>
      </div>
    </div>
    <div class="disco">
%s
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="part">
      <div>
        <span class="sur2">Partitions et bandes orchestre</span>
        <h2>Derniers ajouts</h2>
        <p class="intro">Sans créer de compte. Écoutez un extrait, puis téléchargez la partition ou la bande orchestre.</p>
        <a class="lien" href="partitions.html">Tout le catalogue %s</a>
        <q>%s</q>
      </div>
      <ol class="pistes">
%s
      </ol>
    </div>
  </div>
</section>

<section class="lettre">
  <div class="wrap">
    <div class="boite">
      <div class="txt">
        <h2>Toutes les nouveautés par mail</h2>
        <p>Inscrivez-vous pour recevoir les infos, les dates, les albums, les partitions et les bandes orchestre.</p>
        <form><label for="mail" class="cache">Votre adresse e-mail</label><input id="mail" type="email" placeholder="Votre adresse e-mail" required><button type="submit">Je m'inscris</button></form>
        <small>Désinscription en un clic, dans chaque lettre.</small>
      </div>
      <figure><img src="../assets/img/live/live-02.webp" alt="Damien Poyard en concert dans une église, lumière rouge" width="1814" height="1020" style="object-position:55%% 40%%"></figure>
    </div>
  </div>
</section>
''' % (
        jc, jour, e(prochaine[3]), prochaine[6], e(horaire(prochaine[1], prochaine[2]) or ''),
        rub('agenda.html', ICO_CAL, 'Agenda', 'Nos prochains rendez-vous'),
        rub('boutique.html', ICO_DISC, 'Boutique', 'Albums en CD et en clé USB'),
        rub('partitions.html', ICO_NOTE, 'Partitions et bandes orchestre', 'À télécharger tout de suite'),
        ARROW,
        '\n'.join(ligne_date(r, compact=True) for r in AGENDA[:6]),
        '\n'.join('      <a href="%s"><img src="../assets/img/jaquettes/%s.webp" alt="" width="900" height="900"><b>%s</b><span>Vol. %d</span></a>' % ('album.html' if v == 23 else 'boutique.html', s, e(n), v) for v, n, s, cd, usb, np in ALBUMS[1:5]),
        ARROW, e(SACEM),
        '\n'.join('        <li class="piste" data-piste>%s<div><small>%s</small><h3>%s</h3><div class="ligne-son"><i></i></div></div><a class="dl" href="%s">%s%d versions</a></li>' % (PLAY, e(f), e(t), 'titre.html' if t.startswith('Être') else '#', DL, n) for f, t, n in DERNIERS),
    )
    page('accueil.html', 'Accueil, Damien Poyard, auteur compositeur interprète', corps)


# ---------- 2. Agenda ----------
def agenda():
    groupes = {}
    ordre = []
    for r in AGENDA:
        dt = date_parts(r[0])[0]
        k = (dt.year, dt.month)
        if k not in groupes:
            groupes[k] = []
            ordre.append(k)
        groupes[k].append(r)
    blocs = ''
    for k in ordre:
        y, m = k
        blocs += '<section class="mois"><h2 id="m-%d-%02d">%s %d <span>%d date%s</span></h2><ul class="rdvs">%s</ul></section>\n' % (
            y, m, MOIS[m - 1].capitalize(), y, len(groupes[k]), 's' if len(groupes[k]) > 1 else '', '\n'.join(ligne_date(r) for r in groupes[k]))
    sommaire = ''.join('<a href="#m-%d-%02d">%s %d</a>' % (y, m, MOIS[m - 1].capitalize(), y) for y, m in ordre)
    corps = tete_page('Agenda', 'Nos prochains rendez-vous', 'Repas dansants, thés dansants, stages et concerts. Pour réserver, appelez directement l\'organisateur, le numéro est sur chaque date.')
    corps += '''<section class="wrap agenda-page">
  <nav class="sommaire-mois" aria-label="Aller à un mois">%s</nav>
  <div class="colonnes">
    <div>
%s
    </div>
    <aside class="cote">
      <div class="carte-cote">
        <img src="../assets/img/live/live-09.webp" alt="Damien Poyard sur scène" width="2048" height="1563" style="object-position:30%% 25%%">
        <h2>Vous organisez un bal ?</h2>
        <p>Repas dansant, thé dansant, spectacle, animation de club : parlons de votre date.</p>
        <a class="bouton" href="#">Demander une date %s</a>
      </div>
      <div class="carte-cote lettre-cote">
        <h2>Les dates par mail</h2>
        <p>Recevez les nouvelles dates, les albums et les partitions.</p>
        <form><label for="mail2" class="cache">Votre adresse e-mail</label><input id="mail2" type="email" placeholder="Votre adresse e-mail" required><button type="submit">Je m'inscris</button></form>
      </div>
    </aside>
  </div>
</section>
''' % (sommaire, blocs, ARROW)
    page('agenda.html', 'Agenda, les prochains rendez-vous', corps)


# ---------- 3. Boutique ----------
def boutique():
    cartes = ''
    for v, n, s, cd, usb, np in ALBUMS:
        prix = '<span class="prix"><b>CD %d €</b><b>Clé USB %d €</b></span>' % (cd, usb) if cd else '<span class="prix epuise">Extraits à écouter</span>'
        vol = 'Vol. %d · %d titres' % (v, np) if v else '%d titres' % np
        cartes += '      <a class="carte-album" href="%s"><span class="visuel"><img src="../assets/img/jaquettes/%s.webp" alt="" width="900" height="900"></span><b>%s</b><span class="vol">%s</span>%s</a>\n' % ('album.html' if v == 23 else '#', s, e(n), vol, prix)
    corps = tete_page('Boutique', 'Les albums', 'Chaque album existe en CD et en clé USB, et chaque titre peut aussi s\'acheter à l\'unité, en téléchargement. Paiement par carte, ou par chèque avec le bon de commande.')
    corps += '''<section class="wrap">
  <div class="vedette">
    <div class="pochette"><img src="../assets/img/jaquettes/vol-23-la-vie-est-belle-chantons-l-amour.webp" alt="Jaquette du volume 23" width="900" height="900"></div>
    <div class="texte">
      <span class="sur2">Nouveauté · Vol. 23</span>
      <h2>La vie est belle, chantons l'amour</h2>
      <p>19 titres, de la marche festive à la ballade, avec España Cañí, La Cumparsita, Kizomba et Être libre.</p>
      <div class="formats"><a href="album.html"><small>En CD</small><b>10 €</b></a><a href="album.html"><small>En clé USB</small><b>15 €</b></a></div>
      <a class="lien" href="album.html">Écouter les extraits et voir les titres %s</a>
    </div>
  </div>
  <div class="tete"><div><span class="sur2">Tous les albums</span><h2>La discographie</h2></div><p class="cheque">Vous préférez le chèque ? <a href="#">Imprimer le bon de commande</a></p></div>
  <div class="grille-albums">
%s
  </div>
  <div class="reassurance">
    <div>%s<b>Envoi par La Poste</b><span>Les CD et clés USB partent de l'Ain, frais de port calculés au panier.</span></div>
    <div>%s<b>Titre à l'unité</b><span>Chaque chanson s'achète aussi seule, en téléchargement immédiat.</span></div>
    <div>%s<b>Carte ou chèque</b><span>Paiement sécurisé par carte, ou bon de commande à imprimer pour le chèque.</span></div>
  </div>
</section>
''' % (ARROW, cartes, ICO_DISC, ICO_WAVE, ICO_FILE)
    page('boutique.html', 'Boutique, les albums en CD et en clé USB', corps)


# ---------- 4. Album ----------
def album():
    pistes = ''
    for n, t, d in PISTES_23:
        lien = 'titre.html' if t == 'Être libre' else '#'
        pistes += '      <li class="piste piste-album" data-piste><span class="num">%02d</span>%s<div><small>%s</small><h3><a href="%s">%s</a></h3><div class="ligne-son"><i></i></div></div><a class="achat" href="#">%sAcheter ce titre</a></li>\n' % (n, PLAY, e(d), lien, e(t), CART)
    autres = '\n'.join('      <a href="#"><img src="../assets/img/jaquettes/%s.webp" alt="" width="900" height="900"><b>%s</b><span>Vol. %d</span></a>' % (s, e(n), v) for v, n, s, cd, usb, np in ALBUMS[1:5])
    corps = tete_page('Album · Vol. 23', 'La vie est belle, chantons l\'amour', None, ['<a href="boutique.html">Boutique</a>', 'Vol. 23'])
    corps += '''<section class="wrap fiche-album">
  <div class="colonne-pochette">
    <div class="pochette"><img src="../assets/img/jaquettes/vol-23-la-vie-est-belle-chantons-l-amour.webp" alt="Jaquette du volume 23" width="900" height="900"></div>
    <div class="achat-album">
      <h2>Commander l'album</h2>
      <div class="formats colonne"><a href="#"><small>En CD</small><b>10 €</b><i>%sAjouter</i></a><a href="#"><small>En clé USB</small><b>15 €</b><i>%sAjouter</i></a></div>
      <p class="cheque">Vous préférez le chèque ? <a href="#">Imprimer le bon de commande</a></p>
      <p class="note">19 titres. Les extraits s'écoutent ici, chaque titre s'achète aussi à l'unité.</p>
    </div>
  </div>
  <div class="colonne-pistes">
    <div class="tete"><div><span class="sur2">Les titres</span><h2>19 titres à écouter</h2></div><a class="lien" href="#">Tout écouter %s</a></div>
    <ol class="pistes">
%s
    </ol>
    <p class="sacem">%s</p>
  </div>
</section>
<section class="sec" style="padding-top:40px">
  <div class="wrap">
    <div class="tete"><div><span class="sur2">Boutique</span><h2>Les autres albums</h2></div><a class="lien" href="boutique.html">Toute la discographie %s</a></div>
    <div class="disco">
%s
    </div>
  </div>
</section>
''' % (CART, CART, '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4v16l13-8z"/></svg>', pistes, e(SACEM), ARROW, autres)
    page('album.html', 'Album vol. 23, La vie est belle, chantons l\'amour', corps)


# ---------- 5. Partitions (catégories) ----------
def partitions():
    tuiles = ''
    for nom, slug, nb in FAMILLES:
        tuiles += '      <a class="tuile" href="%s"><span class="lettre-init" aria-hidden="true">%s</span><b>%s</b><span>%d titre%s</span><span class="fl">%s</span></a>\n' % ('famille.html' if slug == 'valse' else '#', e(nom[0]), e(nom), nb, 's' if nb > 1 else '', ARROW)
    corps = tete_page('Partitions et bandes orchestre', 'Choisissez votre danse', 'Chaque titre est rangé par danse, avec sa partition et sa bande orchestre, avec ou sans chœurs. Écoutez l\'extrait, puis téléchargez. Sans créer de compte.')
    corps += '''<section class="wrap">
  <form class="recherche" role="search"><label for="q" class="cache">Rechercher un titre ou une danse</label><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input id="q" type="search" placeholder="Un titre ou une danse : valse, java, Être libre"><button type="submit">Chercher</button></form>
  <div class="grille-tuiles">
%s
  </div>
  <div class="part" style="margin-top:72px">
    <div>
      <span class="sur2">Nouveautés</span>
      <h2>Derniers ajouts</h2>
      <p class="intro">Les derniers titres mis en ligne, toutes danses confondues.</p>
      <q>%s</q>
    </div>
    <ol class="pistes">
%s
    </ol>
  </div>
</section>
''' % (tuiles, e(SACEM), '\n'.join('      <li class="piste" data-piste>%s<div><small>%s</small><h3>%s</h3><div class="ligne-son"><i></i></div></div><a class="dl" href="%s">%s%d versions</a></li>' % (PLAY, e(f), e(t), 'titre.html' if t.startswith('Être') else '#', DL, n) for f, t, n in DERNIERS))
    page('partitions.html', 'Partitions et bandes orchestre, par danse', corps)


# ---------- 6. Famille (Valse) ----------
def famille():
    cartes = ''
    for nom, nb in VALSES:
        chips = '<span class="chips"><i>Partition</i>%s</span>' % ('<i>Bande orchestre</i>' if nb > 1 else '')
        cartes += '      <article class="carte-titre" data-piste>%s<div><h3><a href="#">%s</a></h3>%s<div class="ligne-son"><i></i></div></div><a class="fl" href="#" aria-label="Voir %s">%s</a></article>\n' % (PLAY, e(nom), chips, e(nom), ARROW)
    corps = tete_page('Valse · 25 titres', 'Les valses', 'Écoutez l\'extrait d\'un clic, puis ouvrez le titre pour télécharger la partition ou la bande orchestre.', ['<a href="partitions.html">Partitions et bandes orchestre</a>', 'Valse'])
    corps += '''<section class="wrap">
  <div class="filtres"><span>Trier :</span><a class="actif" href="#">A à Z</a><a href="#">Les plus récents</a><a href="#">Avec chœurs</a></div>
  <div class="grille-titres">
%s
  </div>
  <p class="sacem">%s</p>
  <div class="autres-danses"><span class="sur2">Changer de danse</span><div>%s</div></div>
</section>
''' % (cartes, e(SACEM), ''.join('<a href="%s">%s <small>%d</small></a>' % ('famille.html' if s == 'valse' else '#', e(n), nb) for n, s, nb in FAMILLES if s in ('valse-viennoise', 'tango', 'paso', 'java', 'foxtrot', 'polka', 'bolero', 'marche-festive')))
    page('famille.html', 'Valse, 25 titres', corps)


# ---------- 7. Titre ----------
def titre():
    def variation(ico, libelle, meta, extrait, bouton):
        ext = ('<div class="extrait">%s<span>Extrait, 30 secondes</span><div class="ligne-son"><i></i></div></div>' % PLAY) if extrait else '<div class="extrait apercu">%s<span>Aperçu de la première page</span></div>' % ICO_FILE
        return '<li class="variation" data-piste><div class="v-tete"><span class="v-ico">%s</span><div><h2>%s</h2><small>%s</small></div></div>%s<a class="bouton" href="#">%s%s</a></li>' % (ico, libelle, meta, ext, DL, bouton)
    corps = tete_page('Samba', 'Être libre', 'Samba de Damien Poyard, extraite du volume 23. Trois versions à télécharger : la partition, la bande orchestre avec chœurs et la bande orchestre sans chœurs.', ['<a href="partitions.html">Partitions et bandes orchestre</a>', '<a href="#">Samba</a>', 'Être libre'])
    corps += '''<section class="wrap fiche-titre">
  <ul class="variations">
    %s
    %s
    %s
  </ul>
  <aside class="cote-titre">
    <a class="sur-album" href="album.html"><img src="../assets/img/jaquettes/vol-23-la-vie-est-belle-chantons-l-amour.webp" alt="" width="900" height="900"><span><small>Sur l'album</small><b>La vie est belle, chantons l'amour</b><span>Vol. 23, piste 7</span></span>%s</a>
    <div class="encart">
      <h2>Comment ça marche</h2>
      <ol>
        <li>Écoutez l'extrait.</li>
        <li>Cliquez sur « Télécharger », le fichier arrive tout de suite.</li>
        <li>Partition en PDF, bande orchestre en MP3.</li>
      </ol>
    </div>
    <p class="sacem">%s</p>
  </aside>
</section>
<section class="wrap" style="padding-bottom:96px">
  <div class="tete"><div><span class="sur2">Samba</span><h2>Dans la même danse</h2></div><a class="lien" href="#">Toutes les sambas %s</a></div>
  <div class="grille-titres">
%s
  </div>
</section>
''' % (
        variation(ICO_FILE, 'Partition', 'PDF, 88 Ko', False, 'Télécharger la partition'),
        variation(ICO_WAVE, 'Bande orchestre avec chœurs', 'MP3, 7,4 Mo', True, 'Télécharger'),
        variation(ICO_WAVE, 'Bande orchestre sans chœurs', 'MP3, 7,5 Mo', True, 'Télécharger'),
        ARROW, e(SACEM), ARROW,
        '\n'.join('      <article class="carte-titre" data-piste>%s<div><h3><a href="#">%s</a></h3><span class="chips"><i>Partition</i><i>Bande orchestre</i></span><div class="ligne-son"><i></i></div></div><a class="fl" href="#" aria-label="Voir %s">%s</a></article>' % (PLAY, e(n), e(n), ARROW) for n in ['Rosita', 'Une jolie tahitienne']),
    )
    page('titre.html', 'Être libre, samba : partition et bande orchestre', corps)


accueil(); agenda(); boutique(); album(); partitions(); famille(); titre()
print('ok', sorted(os.listdir(OUT)))
