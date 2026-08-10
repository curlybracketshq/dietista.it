# dietista.it

Sito Jekyll su `gh-pages` — `https://dietista.it` — repo `curlybracketshq/dietista.it`

## Come funziona — note veloci (aggiunto 2026-08-10)

### 1. Spotify embed è già nel layout del post
- Non aggiungere `iframe` o link `> **Ascolta...**` nel contenuto del post.
- Basta mettere `episode_id: XXXXX` nel frontmatter del post.
- `_layouts/post.html` include già:
  ```liquid
  {% if page.episode_id %}
    {% include embed.html episode_id=page.episode_id %}
  {% endif %}
  ```
  che carica `_includes/embed.html`.
- Se lo aggiungi anche nel markdown, appare due volte (bug visto il 2026-08-09).

### 2. Ricette citate — sorgente diretta da `/_recipes`
- Non scrivere link manuali `> 📋 [Nome](/ricette/nome/)` nel post.
- Metti nel frontmatter del post:
  ```yaml
  recipes:
    - acqua-sale-limone-idratazione
    - ciotola-estiva-yogurt-pesca-mandorle
    - panzanella-veloce
  ```
  Gli slug sono i nomi file in `_recipes` senza `.md`.
- `_layouts/post.html` include già `{% include related_recipes.html %}` dopo `{{ content }}`.
- `_includes/related_recipes.html` fa:
  - se `page.recipes` esiste → cerca ogni slug in `site.recipes` (`rec.path contains slug`) e renderizza card con immagine, titolo, tempo.
  - altrimenti fallback: `site.recipes | where: "source_post_url", page.url` (auto-link via `source_post_url` nelle ricette).
- Risultato: aggiorni la ricetta in `_recipes/*.md` e si aggiorna ovunque è citata.
- Esempio vivo: posts estate 2026 (`2026-07-18`, `2026-07-24`, `2026-08-02`, `2026-08-09`) già migrati a questo sistema.

### Pubblicazione post (ricorda)
1. Mara registra podcast → ottieni `episode_id` Spotify
2. Crea file `_posts/YYYY-MM-DD-slug.markdown` con frontmatter completo + `recipes:` se serve
3. Assicurati che ogni ricetta in `recipes:` esista in `_recipes/` con `image` esistente in `/assets/images/recipes/`
4. `git add`, `commit`, `push` su `gh-pages` — Pages ricostruisce in ~1 min

---

## v5 – aggiornamento (storico)

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
