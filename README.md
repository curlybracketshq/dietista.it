# dietista.it v5 – aggiornamento richiesto

Questa versione risolve i 7 punti richiesti:

### 1. Immagine non più prominente
- Rimosso hero con foto grande.
- Foto usata solo come **avatar 40px** nel logo top-left (`header.html`) e 48px nel footer.
- Al posto della foto, in hero a destra c'è la **checklist "Perché prenotare con me"** – card sticky con 6 motivi, come nella versione precedente che ti piaceva.

### 2. WhatsApp fix
- Nuovo stile `.btn-whatsapp` con verde ufficiale `#25D366` e hover `#1FB356`.
- Icona SVG ufficiale inclusa nel bottone.
- Classe `chat_on_whatsapp` mantenuta ovunque per tracking GA4/Pixel.
- Link unificato: `https://wa.me/393707021620`

### 3. Directory rimosso
- Rimosso link a `/directory/` da `header.html` e `footer.html`.
- Nessun entry point visibile. La cartella può restare sul repo ma non è linkata.

### 4. Blog boxes overlap fix
- Vecchio CSS causava `position:absolute` o grid rotta da `stylesheets/main.css`.
- Nuovo `.blog-grid` = `display:grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap:20px; align-items:stretch`
- `.post-preview` è `display:flex; flex-direction:column; min-height:180px; position:relative` – niente più sovrapposizione.

### 5. Link color default fix
- **Rimosso completamente** il vecchio `stylesheets/main.css` dal caricamento.
- `head.html` ora carica **solo** `/assets/css/main.css?v=5`.
- Tutti i link usano `var(--green-700)` con hover coerente, niente blu di default.

### 6. Nuova palette green professionale
- Primary: `#2F7D6B` (verde salvia scuro, non quasi-nero)
- Hover: `#224F44`
- Accent light: `#E6F4F0`, `#F4FAF8`
- Bottoni primary: verde, non nero. Ombre soft.
- WhatsApp separato con suo verde.
- Font: Fraunces per titoli, Inter per corpo – più professionale e leggibile.

### 7. Pagine interne coerenti
- `_layouts/default.html` → base pulita con header/footer + booking.js
- `_layouts/page.html` → `container narrow + page-header + card page-card + cta-prenota`
- `_layouts/post.html` → breadcrumbs + `card post-card` + meta + cta
- `blog/index.html` e `contatti/index.html` usano `layout: page` e quindi ereditano stesso stile, stessa palette, stesso header.
- `prenota/index.html` rimane redirect a `/#prenota`.

### Installazione
```bash
git checkout gh-pages
git pull origin gh-pages
# backup
cp index.html index_backup_$(date +%F).html

# scompatta questo zip nella root
unzip -o ~/Downloads/dietista-v5.zip

# IMPORTANTE: mantieni la tua foto esistente
# Se hai già assets/images/mara-micolucci.jpg non sovrascriverla
# Questo pacchetto NON include la foto per non sostituirla

git add index.html _layouts/ _includes/ assets/ blog/ contatti/ prenota/ CONFIG_SNIPPET.yml
git rm -r stylesheets || true  # rimuove vecchio CSS legacy come richiesto
git commit -m "feat v5: green palette, checklist hero, whatsapp fix, remove directory link, fix blog overlap, unify internal pages, remove legacy css"
git push origin gh-pages
```

### Cosa NON è stato toccato
- La tua foto `assets/images/mara-micolucci.jpg` – mantieni quella che hai già.
- Cal.com embed URL – puoi cambiarlo cercando `cal.com/dietista/30min` in `index.html`.
- GA4 / Meta Pixel – config in `_config.yml` come prima.

Fatto.
