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

  function set(id,value){
    var el=document.getElementById(id);
    if(el)el.textContent=value;
  }

  fetch('assets/data/whoop-week.json?v='+Date.now(),{cache:'no-store'})
    .then(function(r){
      if(!r.ok)throw new Error('WHOOP data unavailable');
      return r.json();
    })
    .then(function(d){
      var strain=d.average_strain==null?null:Number(d.average_strain);
      set('whoop-time',d.training_time||'—');
      set('whoop-strain',strain==null?'—':strain.toFixed(1));
      set('whoop-peak',d.peak_hr==null?'—':d.peak_hr);

      var fill=document.getElementById('whoop-strain-fill');
      if(fill){
        var pct=strain==null?0:Math.max(0,Math.min(100,(strain/21)*100));
        fill.style.width=pct+'%';
      }

      var activities=document.getElementById('whoop-activities');
      if(activities){
        var names=(d.activities||[]).map(function(a){
          return (sportIcons[a.sport]||'•')+' '+a.sport;
        });
        activities.textContent=names.length?names.join('  ·  '):'No training recorded yet this week';
      }

      var updated=document.getElementById('whoop-updated');
      if(updated&&d.updated_at){
        var date=new Date(d.updated_at);
        updated.textContent='updated '+date.toLocaleString([],{
          month:'short',day:'numeric',hour:'numeric',minute:'2-digit'
        });
      }
    })
    .catch(function(){
      set('whoop-updated','waiting for WHOOP sync');
    });
})();
