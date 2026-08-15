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

      var ring=document.getElementById('whoop-strain-ring');
      if(ring){
        var circumference=452.39;
        var ratio=strain==null?0:Math.max(0,Math.min(1,strain/21));
        ring.style.strokeDasharray=circumference;
        ring.style.strokeDashoffset=(circumference*(1-ratio)).toFixed(2);
      }

      var activities=document.getElementById('whoop-activities');
      if(activities){
        activities.innerHTML='';
        var list=d.activities||[];
        if(!list.length){
          activities.textContent='No training recorded yet this week';
        }else{
          list.forEach(function(a){
            var chip=document.createElement('span');
            chip.className='whoop-live-chip';
            chip.textContent=(sportIcons[a.sport]||'•')+' '+a.sport;
            activities.appendChild(chip);
          });
        }
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
