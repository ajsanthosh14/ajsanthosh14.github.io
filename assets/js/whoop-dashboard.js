(function(){
  var root=document.getElementById('whoop-week');
  if(!root)return;
  var sportIcons={
    'Muay Thai':'🥊',
    'Martial Arts':'🥋',
    'Weightlifting':'🏋️',
    'Hiking':'⛰️',
    'Running':'🏃',
    'Cycling':'🚴',
    'Activity':'⚡'
  };
  function set(id,value){var el=document.getElementById(id);if(el)el.textContent=value;}
  fetch('assets/data/whoop-week.json?v='+Date.now(),{cache:'no-store'})
    .then(function(r){if(!r.ok)throw new Error('WHOOP data unavailable');return r.json();})
    .then(function(d){
      set('whoop-workouts',d.workouts==null?'—':d.workouts);
      set('whoop-time',d.training_time||'—');
      set('whoop-strain',d.average_strain==null?'—':d.average_strain);
      set('whoop-peak',d.peak_hr==null?'—':d.peak_hr);
      var list=document.getElementById('whoop-activities');
      if(list){
        list.innerHTML='';
        (d.activities||[]).forEach(function(a){
          var row=document.createElement('div');
          row.style.cssText='display:flex;align-items:center;justify-content:space-between;gap:12px;padding:8px 0;border-bottom:1px solid var(--line);font-size:13px';
          var icon=sportIcons[a.sport]||'•';
          row.innerHTML='<span>'+icon+' '+a.sport+'</span><strong style="font-family:var(--mono);font-size:11px">'+a.count+'</strong>';
          list.appendChild(row);
        });
        if(!(d.activities||[]).length){list.innerHTML='<span style="font-size:13px;color:var(--dim)">No workouts recorded yet this week.</span>';}
      }
      var updated=document.getElementById('whoop-updated');
      if(updated&&d.updated_at){
        var date=new Date(d.updated_at);
        updated.textContent='updated '+date.toLocaleString([], {month:'short',day:'numeric',hour:'numeric',minute:'2-digit'});
      }
    })
    .catch(function(){
      set('whoop-updated','waiting for WHOOP sync');
    });
})();
