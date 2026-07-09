# Dietista.it – Nuova homepage (versione produzione, no demo)

Versione pulita, pronta per pubblicazione. Tutta la prenotazione è delegata a **Cal.com**, nessun pagamento finto, nessun calendario custom, nessun form demo.

## Cosa è cambiato rispetto alle versioni precedenti

- **Rimossi:** calendario disponibilità custom, form nome/email/telefono, toggle “Paga ora / Paga dopo”, link Stripe placeholder, testi “demo / finto / placeholder / TODO”.
- **Semplificato:** homepage ora è informativa + embed Cal.com. La raccolta dati (nome, email, telefono, consenso privacy) avviene direttamente su Cal.com, che è già GDPR compliant.
- **Foto professionale:** aggiunta `/assets/images/mara-micolucci.jpg` (e `.webp`) estratta dal tuo profilo Instagram e resa più professionale. Usata nell’hero. Sostituibile in qualsiasi momento.
- **Header ovunque:** `_layouts/default.html`, `page.html`, `post.html` includono tutti `{% include header.html %}` quindi la nav con Prenota + WhatsApp appare su Blog, Contatti, Directory e singoli post.
- **Tracking:** GA4 + Meta Pixel supportati insieme. Eventi tracciati: `click_whatsapp`, `click_cal`, `view_booking_calendar`, `Contact`, `InitiateCheckout`.

## Contenuto pacchetto

```
index.html                      → NUOVA homepage definitiva (hero con foto, servizi, embed Cal.com, blog)
_layouts/
  default.html                  → layout globale con header/footer ovunque
  page.html                     → per pagine statiche
  post.html                     → per articoli blog, include CTA
_includes/
  head.html                     → carica CSS vecchi + nuovi, GA4 + Meta Pixel
  header.html                   → nav sticky con WhatsApp https://wa.me/393707021620
  footer.html                   → contatti, socials, podcast, note legali
  cta-prenota.html              → banner CTA
assets/
  css/booking.css
  js/booking.js                 → solo smooth scroll + tracking, nessun calendario/form
  images/mara-micolucci.jpg/.webp
prenota/index.html              → redirect a /#prenota
CONFIG_SNIPPET.yml
README_INSTALL.md
```

## Installazione (macOS / Linux)

```bash
git checkout gh-pages
git pull origin gh-pages
cp index.html index_backup_$(date +%F).html
unzip -o ~/Downloads/dietista-full-package.zip
git add index.html _layouts/ _includes/ assets/ prenota/
git commit -m "feat: homepage produzione con Cal.com embed, rimossi demo/pagamenti, foto professionale, header globale, GA4+Pixel"
git push origin gh-pages
```

## Configurazione tracking

In `_config.yml`:

```yaml
google_analytics: "G-XXXXXXXXXX"
meta_pixel_id: "123456789012345"
whatsapp_number: "393707021620"
```

## Cal.com

Embed iframe in #prenota. Cambia URL cercando `cal.com/dietista/30min` in index.html.

## Foto professionale

File: `/assets/images/mara-micolucci.jpg`. Sostituibile mantenendo stesso nome. Il Reel Facebook linkato non è scaricabile senza login proprietario: se carichi uno screenshot qui, te lo trasformo in ritratto professionale.

## WhatsApp link

Ovunque uso:

```html
<a class="chat_on_whatsapp" aria-label="Chat on WhatsApp" href="https://wa.me/393707021620" target="_blank" rel="noopener">+39 370 702 1620</a>
```

Classe `chat_on_whatsapp` perfetta per CSS/JS tracking, già stilizzata in booking.css.
