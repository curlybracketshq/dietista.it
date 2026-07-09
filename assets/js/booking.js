// booking.js - simplified for Cal.com delegation (no custom calendar/form)
// Mobile nav toggle already inline, this adds smooth scroll + analytics

document.addEventListener('DOMContentLoaded', () => {
  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(a=>{
    a.addEventListener('click', e=>{
      const id = a.getAttribute('href');
      if(id.length>1){
        const el = document.querySelector(id);
        if(el){ e.preventDefault(); el.scrollIntoView({behavior:'smooth', block:'start'}); }
      }
    });
  });

  // Track WhatsApp clicks in GA4 + Meta
  document.querySelectorAll('.chat_on_whatsapp').forEach(link=>{
    link.addEventListener('click', ()=>{
      if(window.gtag) gtag('event','click_whatsapp',{method:'whatsapp'});
      if(window.fbq) fbq('track','Contact');
    });
  });

  // Track Cal.com CTA clicks
  document.querySelectorAll('a[href*="cal.com"]').forEach(link=>{
    link.addEventListener('click', ()=>{
      if(window.gtag) gtag('event','click_cal',{link:link.href});
      if(window.fbq) fbq('track','InitiateCheckout');
    });
  });

  // Track when Cal iframe loads (user viewed booking)
  const calFrame = document.querySelector('iframe[src*="cal.com"]');
  if(calFrame){
    calFrame.addEventListener('load', ()=>{
      if(window.gtag) gtag('event','view_booking_calendar');
      if(window.fbq) fbq('track','ViewContent',{content_name:'cal_booking'});
    });
  }
});

// Legacy stubs - kept so old inline onclick don't error if cached
window.selectService = ()=>{};
window.setChannel = ()=>{};
window.setPay = ()=>{};
window.confirmBooking = ()=>{ window.location.href='#prenota'; };
