/* Headless simulation harness for Municipality Tycoon.
   Load the game page, then evaluate this file in the page. It replaces all UI with no-ops,
   plays whole games with a simple policy, and collects stats for balance and pacing checks.
   Usage:  const r = await SIM.batch(12, 30, 'sensible');  console.log(r.summary) */
(function(){
 const S0=JSON.parse(JSON.stringify(S));
 const stats={lines:0,chars:0,asks:0,errors:[]};
 let last=null;
 const noop=async()=>{};
 MUTE=true;SPD=1e9;
 window.say=async(sp,text)=>{stats.lines++;stats.chars+=(text||'').length};
 window.showSpeaker=noop;window.hideSpeaker=noop;window.showCrowd=()=>{};window.hideCrowd=noop;
 window.gavel=noop;window.heckle=()=>{};window.banner=()=>{};window.showTag=()=>{};window.clearTags=()=>{};
 window.audMood=()=>{};window.autosave=()=>{};window.toast=()=>{};window.flash=()=>{};
 window.openOverlay=()=>{};window.closeOverlay=()=>{};window.showElectionResults=noop;
 window.ending=code=>{last=code};
 let policy='sensible';
 const pickR=a=>a[Math.floor(Math.random()*a.length)];
 window.ask=async(title,opts)=>{
  stats.asks++;
  if(/Your response\?/.test(title)&&policy==='sensible'){const f=opts.find(o=>o.k==='extra')||opts.find(o=>o.k==='fine');if(f)return f.k}
  if(/summary/.test(title))return opts[0].k;
  return pickR(opts).k;
 };
 window.chooseDecision=async p=>{
  stats.asks++;
  if(policy==='random'){return{action:pickR(['approve','deny','table']),conds:{}}}
  const order=['fireplan','buffer','monitor','noise','hire','recycle','fund','bond','road','park'];
  const conds={...p.free};const mx=maxBurden(p)-.2;
  for(const k of order){if(p.nocond)break;if(conds[k])continue;const t={...conds,[k]:true};if(burden(t,p)<=mx)conds[k]=true}
  const yes=COUNCIL.filter(m=>score(m,p,conds,{pub:0,mayor:.15,bribe:0})>0).length;
  if(yes>=3)return{action:'approve',conds};
  if(!p.tabled&&yes===2)return{action:'table',conds:{}};
  return{action:'deny',conds};
 };
 if(typeof budgetPanel==='function')window.budgetPanel=async()=>{
  stats.asks++;
  if(policy==='random'){const f={};DEPTS.forEach(d=>f[d.k]=pickR([-1,0,1]));return{rate:pickR([.8,1,1.2,1.4]),fund:f,bond:Math.random()<.2}}
  const f=finCalc();const fund={...S.fund};
  let rate=S.rate;
  if(f.net<-3000)rate=Math.min(1.4,rate+.1);else if(f.net>12000&&rate>.8)rate=Math.max(.8,rate-.1);
  return{rate,fund,bond:S.budget<0&&S.debt<1e6};
 };
 const snapshotState=()=>({week:S.week,trust:S.trust,env:S.env,dev:S.dev,corrupt:S.corrupt,budget:S.budget,approved:S.stats.approved,denied:S.stats.denied,incidents:S.stats.incidents,projects:S.projects.length,pop:S.pop,debt:S.debt});
 async function runOne(maxWeeks,pol,init){
  policy=pol||'sensible';
  Object.assign(S,JSON.parse(JSON.stringify(S0)));
  if(init)Object.assign(S,init);
  S.maxWeeks=maxWeeks;stats.lines=0;stats.chars=0;stats.asks=0;last=null;
  const t0=performance.now();
  try{await runGame()}catch(e){stats.errors.push(String(e&&e.stack||e));}
  const out={...snapshotState(),end:last,lines:stats.lines,chars:stats.chars,asks:stats.asks,ms:Math.round(performance.now()-t0)};
  out.estMinutes=+((stats.chars/16+stats.lines*1.0+stats.asks*8)/60).toFixed(1);
  return out;
 }
 async function batch(maxWeeks,n,pol,init){
  const runs=[];
  for(let i=0;i<n;i++)runs.push(await runOne(maxWeeks,pol,init));
  const avg=k=>+(runs.reduce((a,r)=>a+(r[k]||0),0)/runs.length).toFixed(1);
  const ends={};runs.forEach(r=>{const e=(r.end||'none').split('|')[0];ends[e]=(ends[e]||0)+1});
  return{runs,summary:{n,maxWeeks,policy:pol||'sensible',ends,avgWeek:avg('week'),trust:avg('trust'),env:avg('env'),dev:avg('dev'),corrupt:avg('corrupt'),budget:avg('budget'),approved:avg('approved'),denied:avg('denied'),incidents:avg('incidents'),projects:avg('projects'),pop:avg('pop'),lines:avg('lines'),chars:avg('chars'),asks:avg('asks'),estMinutes:avg('estMinutes'),errors:stats.errors.slice(0,3)}};
 }
 window.SIM={runOne,batch,stats};
})();
