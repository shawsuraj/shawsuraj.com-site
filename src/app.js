(function(){
  // mobile menu
  var btn=document.querySelector(".menu-btn"), nav=document.querySelector(".nav");
  if(btn&&nav){btn.addEventListener("click",function(){var o=nav.classList.toggle("open");btn.setAttribute("aria-expanded",o?"true":"false");btn.textContent=o?"Close":"Menu";});}

  // copy email
  var copy=document.getElementById("copy"), mail=document.getElementById("mail");
  if(copy&&mail){copy.addEventListener("click",function(){
    var done=function(){copy.textContent="Copied";setTimeout(function(){copy.textContent="Copy";},1800);};
    var fb=function(){var r=document.createRange();r.selectNodeContents(mail);var s=getSelection();s.removeAllRanges();s.addRange(r);copy.textContent="Selected";};
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(mail.textContent.trim()).then(done,fb);}else fb();
  });}

  // story: the sticky stage follows the chapter in view (works without GSAP)
  var stage=document.querySelector(".stage");
  if(stage&&"IntersectionObserver" in window){
    var yr=stage.querySelector(".yr"), w=stage.querySelector(".w"), lesson=stage.querySelector(".lesson"), bar=stage.querySelector(".bar i"), glyph=stage.querySelector(".g");
    var chapters=[].slice.call(document.querySelectorAll(".chapter"));
    var show=function(ch){
      var i=chapters.indexOf(ch);
      stage.style.setProperty("--c",getComputedStyle(ch).getPropertyValue("--c"));
      if(yr.textContent!==ch.dataset.year){yr.animate&&yr.animate([{transform:"translateY(30%)",opacity:0},{transform:"none",opacity:1}],{duration:450,easing:"cubic-bezier(.2,.7,.2,1)"});}
      yr.textContent=ch.dataset.year; w.textContent=ch.dataset.world; lesson.textContent=ch.dataset.lesson;
      bar.style.width=((i+1)/chapters.length*100)+"%";
      var t=document.getElementById("glyph-"+ch.dataset.glyph); glyph.innerHTML=t?t.innerHTML:"";
    };
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)show(e.target);});},{rootMargin:"-45% 0px -45% 0px"});
    chapters.forEach(function(c){io.observe(c);});
    show(chapters[0]);
  }

  var reduce=window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if(!window.gsap||reduce) return;
  gsap.registerPlugin(ScrollTrigger);

  // hero entrance: everything is visible at rest; this only adds a short lift
  gsap.from(".hero h1 .ln",{yPercent:22,opacity:.25,duration:.9,ease:"power3.out",stagger:.08});
  gsap.from(".w-head h1",{y:24,opacity:.25,duration:.8,ease:"power3.out"});

  // gentle reveals for documents
  gsap.utils.toArray(".chapter").forEach(function(ch){gsap.from(ch.querySelectorAll("h3, p, .facts, .go"),{y:18,opacity:.3,duration:.6,stagger:.06,ease:"power2.out",scrollTrigger:{trigger:ch,start:"top 80%"}});});
  gsap.utils.toArray(".report, .feature, .paper, .menu, .paper-ballot, .note-body").forEach(function(el){
    gsap.from(el,{y:30,opacity:.4,duration:.8,ease:"power2.out",scrollTrigger:{trigger:el,start:"top 85%"}});
  });
  gsap.utils.toArray(".findings tbody tr, .log li, .versions li, .roles li").forEach(function(el){
    gsap.from(el,{x:-12,opacity:.3,duration:.45,ease:"power2.out",scrollTrigger:{trigger:el,start:"top 92%"}});
  });
  var X=document.querySelectorAll(".x path");
  X.forEach(function(p){var l=p.getTotalLength();p.style.strokeDasharray=l;gsap.fromTo(p,{strokeDashoffset:l},{strokeDashoffset:0,duration:.5,ease:"power2.out",scrollTrigger:{trigger:p,start:"top 85%"}});});
})();
