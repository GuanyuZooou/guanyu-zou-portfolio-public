const SITE_CONFIG = window.PORTFOLIO_CONFIG || {};
(() => {
 const work=document.querySelector('#work'), toolkit=document.querySelector('#skills'), tools=document.querySelector('#tools');
 if(work && toolkit){
  const mobile=matchMedia('(max-width:820px)');
  const order=()=>{const p=work.parentElement;if(mobile.matches){p.insertBefore(work,toolkit);p.insertBefore(tools,toolkit);}else{p.insertBefore(toolkit,work);p.insertBefore(tools,document.querySelector('#approach'));}};
  order();mobile.addEventListener('change',order);
 }
 const menu=document.querySelector('.menu-button'), nav=document.querySelector('.nav-links');
 const close=()=>{nav.classList.remove('open');menu.setAttribute('aria-expanded','false');menu.textContent='☰';};
 if(menu&&nav){menu.addEventListener('click',()=>{const open=nav.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));menu.textContent=open?'✕':'☰';});nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',close));document.addEventListener('keydown',e=>{if(e.key==='Escape'){close();}});}
 document.querySelectorAll('.filter-button').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('.filter-button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));document.querySelectorAll('.project-card').forEach(c=>c.classList.toggle('is-hidden',b.dataset.filter!=='all'&&c.dataset.category!==b.dataset.filter));}));
 const links=document.querySelector('.contact-links');
 if(links&&SITE_CONFIG.contactApproved){for(const key of ['email','linkedin','github']){const value=SITE_CONFIG[key];if(!value)continue;let url=value;if(key==='email'){if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value))continue;url='mailto:'+value;}else{try{if(new URL(value).protocol!=='https:')continue;}catch{continue;}}const a=document.createElement('a');a.href=url;a.textContent=key==='email'?'Email ↗':key==='linkedin'?'LinkedIn ↗':'GitHub ↗';if(key!=='email'){a.target='_blank';a.rel='noopener noreferrer';}links.appendChild(a);}}
 const copier=document.querySelector('[data-copy-intro]');
 if(copier)copier.addEventListener('click',async()=>{const text='Guanyu Zou | Research & Engineering Portfolio\nMaterials researcher working with COMSOL multiphysics simulation, Python scientific machine learning, 3D image analysis and scientific software workflows.';const status=document.querySelector('[data-copy-status]');try{await navigator.clipboard.writeText(text);status.textContent='Introduction copied.';}catch{status.textContent=text;}});
})();
