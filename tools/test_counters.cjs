const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(require.resolve('../public/assets/site.js'), 'utf8');
const marker = '// Metric counters';
assert(source.includes(marker), 'Metric counter component is present');

function fixture(reduced = false) {
  const project = {dataset:{count:'1500', countSuffix:'+'}, textContent:'1,500+', hasAttribute:()=>false};
  const age = {dataset:{count:''}, textContent:'17', hasAttribute:name=>name==='data-company-age'};
  const events = {}, frames = new Map();
  let observer, id = 0, preference;
  const context = {
    Intl, Number, Math,
    document:{hidden:false, querySelectorAll:()=>[project, age], addEventListener:(name, fn)=>events[name]=fn},
    window:{matchMedia:()=>preference={matches:reduced, addEventListener:(_, fn)=>events.motion=fn}},
    IntersectionObserver:class {
      constructor(fn) { observer = fn; }
      observe() {} unobserve() {}
    },
    requestAnimationFrame:fn=>{frames.set(++id, fn);return id;},
    cancelAnimationFrame:id=>frames.delete(id),
  };
  context.window.IntersectionObserver = context.IntersectionObserver;
  vm.runInNewContext(source.slice(source.indexOf(marker)), context);
  const tick = time => { const current=[...frames.values()];frames.clear();current.forEach(fn=>fn(time)); };
  return {project, age, events, frames, preference, context, tick,
    enter:target=>observer([{isIntersecting:true,target}])};
}

let f = fixture();
assert.equal(f.project.textContent, '1,500+', 'Final number is usable before observation');
f.enter(f.project); f.tick(0);
const samples = [300, 600, 900, 1200, 1500, 1800].map(time => {
  f.tick(time);
  return Number(f.project.textContent.replace(/[^0-9]/g, ''));
});
assert(samples[0] > 0 && samples.at(-1) < 1500, 'Large counter is still moving at 1.8 seconds');
const gains = samples.map((value, i) => value - (samples[i - 1] || 0));
assert(Math.abs(gains[0] - gains[1]) <= 1, 'Large counter starts at a steady rate');
for (let i = 2; i < gains.length; i++) {
  assert(gains[i] > 0 && gains[i] < gains[i - 1], 'Large counter progressively slows');
}
f.tick(2000);
assert.equal(f.project.textContent,'1,500+');
assert.equal(f.frames.size,0,'No perpetual counter loop');
f.enter(f.project);
assert.equal(f.frames.size,0,'A second observation does not restart a finished counter');
f.enter(f.age); f.tick(2100); f.tick(2200);
f.age.textContent='18';
f.events['company-date-updated']({detail:{age:18}});
f.tick(3100);
assert.equal(f.age.textContent,'18','New Year update cannot be overwritten by an old animation');

f = fixture(true);
assert.equal(f.frames.size,0,'Reduced motion is static');
assert.equal(f.project.textContent,'1,500+');
f = fixture(); f.enter(f.project); f.tick(0);
f.preference.matches=true; f.events.motion();
assert.equal(f.project.textContent,'1,500+');
assert.equal(f.frames.size,0);
console.log('PASS: counting, exact final totals, finite frames, New Year race and reduced motion.');
