// dietista.it v5 – tracking only, no custom calendar/form
(function(){
  function track(name, params){
    try{ if(window.gtag) gtag('event', name, params||{}); }catch(e){}
    try{ if(window.fbq) fbq('trackCustom', name, params||{}); }catch(e){}
  }
  document.addEventListener('click', function(e){
    var a = e.target.closest('a');
    if(!a) return;
    var href = a.getAttribute('href')||'';
    if(a.classList.contains('chat_on_whatsapp') || href.includes('wa.me') || href.includes('whatsapp')){
      track('click_whatsapp', {link: href});
      try{ if(window.fbq) fbq('track','Contact'); }catch(_){}
    }
    if(href.includes('cal.com')){
      track('click_cal', {link: href});
      try{ if(window.fbq) fbq('track','InitiateCheckout'); }catch(_){}
    }
  });
  window.addEventListener('load', function(){
    var cal = document.querySelector('iframe[src*=\"cal.com\"]');
    if(cal){ track('view_booking_calendar'); }
  });
  // smooth scroll for hash links
  document.addEventListener('click', function(e){
    var a = e.target.closest('a[href^=\"#\"]');
    if(!a) return;
    var id = a.getAttribute('href');
    if(id.length>1){
      var el = document.querySelector(id);
      if(el){ e.preventDefault(); el.scrollIntoView({behavior:'smooth', block:'start'}); history.pushState(null,'',id); }
    }
  });
  // legacy stubs so old posts don't error
  window.selectService = function(){};
})();
