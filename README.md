# dietista.it

Sito Jekyll su `gh-pages` — `https://dietista.it` — repo `curlybracketshq/dietista.it`

## Come funziona — convenzioni complete (aggiornato 2026-08-15)

### 0) Lingua + CTA policy (IMPORTANTE - DO NOT VIOLATE)
- Italiano per Mara, English con Giovanni.
- CTA SEMPRE: `scrivimi su Instagram @dietista.it in DM, oppure via email a info@dietista.it` + disclaimer "è informazione generale, per il tuo caso costruiamo insieme".
- MAI usare "studio a Musile / ne parliamo in studio / Ti aspetto in studio" (policy 2026-07-20).
- `_includes/cta-prenota.html` FREEZED, `/prenota/` keep as-is, non toccare.
- Banner finale auto-incluso da layout, non duplicare CTA nel markdown.

### 1. Spotify embed è già nel layout del post
- Non aggiungere `iframe` o link `> **Ascolta...**` nel contenuto del post.
- Basta mettere `episode_id: XXXXX` nel frontmatter del post (es. `5TzC3fIv3G9Ni7zXP3Q4Y5`).
- `_layouts/post.html` include già:
  ```liquid
  {% if page.episode_id %}
    {% include embed.html episode_id=page.episode_id %}
  {% endif %}
  ```
  che carica `_includes/embed.html` (iframe 152px).
- Se lo aggiungi anche nel markdown, appare due volte (bug visto il 2026-08-09).
- JSON-LD `PodcastEpisode` auto-generato da layout con `contentUrl: https://open.spotify.com/episode/{{ page.episode_id }}`.

### 2. Ricette citate — sorgente diretta da `/_recipes`
- Non scrivere link manuali `> 📋 [Nome](/ricette/nome/)` nel post.
- Metti nel frontmatter del post:
  ```yaml
  recipes:
    - acqua-sale-limone-idratazione
    - ciotola-estiva-yogurt-pesca-mandorle
    - panzanella-veloce
  ```
  Gli slug sono i nomi file in `_recipes` senza `.md`. Solo 7 ricette LIVE.
- `_layouts/post.html` include già `{% include related_recipes.html %}` dopo `{{ content }}`.
- `_includes/related_recipes.html` fa:
  - se `page.recipes` esiste → cerca ogni slug in `site.recipes` (`rec.path contains slug`) e renderizza card con immagine, titolo, tempo.
  - altrimenti fallback: `site.recipes | where: "source_post_url", page.url` (auto-link via `source_post_url` nelle ricette).
- Risultato: aggiorni la ricetta in `_recipes/*.md` e si aggiorna ovunque è citata.
- Esempio vivo: posts estate 2026 (`2026-07-18`, `2026-07-24`, `2026-08-02`, `2026-08-09`, `2026-08-14`) già migrati a questo sistema.

### 3. Frontmatter obbligatorio post
```yaml
---
layout: post
title: "Titolo episodio identico Spotify"
seo_title: "Titolo SEO con keyword Ferragosto/estate/..."
description: "1 frase dall'episodio, max 160 caratteri"
image: /assets/images/recipes/<food-only>.jpg  # esiste in /assets/images/recipes/
image_alt: "Descrizione piatto - contesto Ferragosto/estate"
episode_id: SPOTIFY_ID_22CHARS
date: YYYY-MM-DD 09:00:00 +0200
author: Mara Micolucci
keywords: "keyword1, keyword2, dietista Musile di Piave, ..."
tags: [Ferragosto, estate, convivialità, stagionalità, idratazione] # max 5
last_modified_at: YYYY-MM-DD 09:00:00 +0200 # = date
recipes:
  - slug1
  - slug2
  - slug3
faq:
  - q: "Domanda paziente stile colloquio?"
    a: "Risposta breve, fisiologia, niente diagnosi."
  - q: "..."
    a: "..."
  - q: "..."
    a: "..."
---
```

### 4. Struttura corpo post (Mara tone lock)
- Saluto: "Buongiorno a tutti, buongiorno a tutte. Sono Mara Micolucci, dietista, farmacista, dottoressa in Scienze e Tecniche Psicologiche. Benvenuti su dietista.it."
- Intro meteo: "Oggi registriamo da Musile di Piave, XX gradi, ..." (usa meteo reale Musile)
- Domanda paziente in bold quote: **"Dottoressa, ..."**
- Validazione empatica: "Se ti è successo anche una volta..."
- > Collegato: link interni agli ultimi 2-3 post con slug corretti.
- ## 1. Primo meccanismo (fisiologia / contesto)
- ## 2. Secondo meccanismo (testa / comportamento / perfezionismo)
- ---
- ## Cosa fare oggi, in meno di due minuti
  - ### Azione alimentare – ... (1 piatto salato freddo obbligatorio, 3 esempi veneti, sale/proteine/fresco)
  - Idra: "bottiglia 1L vicino, acqua con presa di sale e limone se sudi"
  - ### Azione comportamentale – rituale 3 respiri / 5 min prima / sedia / senza telefono
  - ### Cosa evitare – lista 3-4 bullet (no digiuno compensatorio, no peso con caldo, no vaschetta TV, no "da lunedì")
- Chiusura empatica + domanda aperta: "Anche a te capita? / Ti ritrovi?"
- CTA doppia + disclaimer.

### 5. Immagini + layout lock
- `mara-micolucci.jpg` SOLO header 40×40 + footer 48×48, mai in post.
- Blog covers: food-only, no persone, no AI slop. Preferibilmente foto reali da `/assets/images/recipes/`, o acquerello acqua se manca ma sempre food-only.
- Container.lock: `.container.narrow` = 20px desktop / 16px mobile, `post-card`/`page-card` padding 0. Margini identici in `/blog/`, post, ricette, 404.
- No `<iframe>` manuale, no `<h2>Errore 404` fuori container, no card padding.

### 6. Tone + formato contenuti (weekly)
- Reel breve: 145-180 parole
- Reel lungo: 380-560 parole
- Podcast: 1050-1250 parole
- Ordine: hook empatico → 2 meccanismi → azione <2min → comportamentale → cosa evitare / FAQ → CTA doppia + disclaimer generale, no diagnosi.
- Pilastro rotation (W1 sazietà, W2 bimbi estate, W3 carboidrati sera, W4 fame emotiva originally ma W6 Ferragosto = stagionalità+idratazione NOT fame emotiva)
- Humanization: no em-dashes —, CTA varied, spoken intercalari "guarda, senti, ecco", Italian natural.
- Hashtag IG/Threads: max 4, empatia + azione.

### 7. Pubblicazione post (ricorda)
1. Mara registra podcast → ottieni `episode_id` Spotify (22 char)
2. Crea file `_posts/YYYY-MM-DD-slug.markdown` con frontmatter completo + `recipes:` se serve
3. Assicurati che ogni ricetta in `recipes:` esista in `_recipes/` con `image` esistente in `/assets/images/recipes/`
4. Body senza embed, senza link manuali ricette, con CTA clean
5. `git add`, `commit -m "post: Titolo - EPISODE_ID"`, `push` su `gh-pages` — Pages ricostruisce in ~1 min
6. Verifica live: `https://dietista.it/YYYY/MM/DD/slug.html` — controlla embed singolo, immagini, related_recipes cards, footer.

### 8. Sicurezza / repo
- PAT GitHub Classic con scope `repo` → `git push` via `https://oauth:TOKEN@github.com/curlybracketshq/dietista.it.git` o credential helper store. Se 401 "Bad credentials", rigenera PAT (quello del 2026-08-09 leak è invalido).
- Non committare PAT nel repo, `.git/config` deve restare `https://github.com/curlybracketshq/dietista.it.git` senza token.

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
