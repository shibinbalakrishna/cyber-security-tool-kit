// Like Function Starts
function like(val){
  ls = ['like.png','likeFull.png']

  source = document.getElementById(val).src.split('/');
  console.log(source[source.length-1]);
  key = ls.indexOf(source[source.length-1]);
  key = (key==0)?1:0;
  
  if(key==1){
    $.ajax({
          url:'/addLike/'+val.slice(1),
          type:'POST',
          success: function(data){
          document.getElementById(val).src = '/static/./images/'+ls[key];
          doc = parseInt(document.getElementById('m'+val.slice(1)).innerHTML)+1;
            document.getElementById('m'+val.slice(1)).innerHTML= doc.toString();
          }
    })
  }
  else{
    $.ajax({
      url:'/deleteLike/'+val.slice(1),
      type:'POST',
      success: function(data){
         document.getElementById(val).src = '/static/./images/'+ls[key];
        doc = parseInt(document.getElementById('m'+val.slice(1)).innerHTML)-1;
            document.getElementById('m'+val.slice(1)).innerHTML= doc.toString();
       
      }
    })
  }
}
// Like Function Ends
// Post Comment Function Starts
function postComment(msgid){
  msg = document.getElementById('cmp'+msgid.slice(2)).value;
  id = 'cos'+msgid.slice(2)
  $.ajax({
    url:'/addComments/'+msgid.slice(2)+'-_-'+msg,
    type:'POST',
    success:function(data){
      if(data['data'][5]==1){
        console.log(document.getElementById('co'+msgid.slice(2)));
        document.getElementById('co'+msgid.slice(2)).style.height="350px";
        document.getElementById('cos'+msgid.slice(2)).style.height="200px";
      }
      comment = document.getElementById(id);
      console.log(data);
      comment.insertBefore(addClass(data['data']),comment.firstChild);
      doc = parseInt(document.getElementById('cc'+msgid.slice(2)).innerHTML)+1;
      document.getElementById('cc'+msgid.slice(2)).innerHTML= doc.toString();
    }
  })
}
// Post Comment Function ends 
// Add div to comments starts
function addClass(data){
   const div = document.createElement('div');
   div.className = 'container mt-2 border py-2';
   div.style.cssText = 'border-radius:25px;';
   div.innerHTML = `
        <div class="row">
           <div class="col-md-1">
              <img src="${data[4]}" style="border-radius:100px;"width="43" id="cmsg${data[0]}"/>
           </div>
           <div class="col-md-9 ">
              <strong>
                 <p style="display:inline" class="ml-1">${data[2]}</p>
              </strong>
              <p class="ml-1" style="font-size:15px;">${data[3]}</p>
           </div>
          
        </div>
        <div class="row">
           <div class="col-md-1"></div>
           <div class="col-md-9" style="word-wrap: break-word;">
              ${data[1]}
           </div>
           
        </div>
     `
  return div;
}
// Add div to comments ends
// Comments functions starts
function comments(val,url){
  ls = ['comment.png','commentFull.png']
  source = document.getElementById(val).src.split('/');
  key = ls.indexOf(source[source.length-1]);
  key = (key==0)?1:0;
  
  if(key==1){
    $.ajax({
      url:'/getComments/'+val.slice(2),
      type:'POST',
      success: function(data){
        size = data['data'].length;
        if(size>0){
          commentTab = document.getElementById('co'+val.slice(2))
          commentTab.style.height = "300px";
          crsTab = document.getElementById('crs'+val.slice(2))
          crsTab.classList.add('border-bottom');
          crsTab.classList.add('border-white');
          commentTab.innerHTML=`
          <br>
          <h4>Comments</h4>
          <div class="container" id="cos${val.slice(2)}" style="max-height: 200px;">
          </div>
          `
          comment = document.getElementById('cos'+val.slice(2));
          comment.classList.add('scrollView');
          for(i=0;i<size;i++){
            comment.appendChild(addClass(data['data'][i]));
          }
         
          commentTab.innerHTML+=`
            <img src="${url}" style="border-radius:100px;"width="40"/><input class="comment bg-dark text-white" placeholder="Add a comment" id="cmp${val.slice(2)}"/><img src="/static/./images/send.png" style="margin-top:-10px; margin-left:10px" width="40" onclick="postComment('cp${val.slice(2)}')"/>
          `
        }
        else{
          commentTab = document.getElementById('co'+val.slice(2))
          commentTab.style.height = "150px";
          crsTab = document.getElementById('crs'+val.slice(2))
          crsTab.classList.add('border-bottom');
          crsTab.classList.add('border-white');
          commentTab.innerHTML=`
          <br>
          <h4>Comments</h4>
          <div class="container" id="cos${val.slice(2)}" style="height: 10px;">
          </div>
          `
          comment = document.getElementById('cos'+val.slice(2));
          comment.classList.add('scrollView');
          commentTab.innerHTML+=`
            <br>
            <img src="${url}" style="border-radius:100px;"width="40"/><input class="comment bg-dark text-white" placeholder="Be the First To Comment.." id="cmp${val.slice(2)}"/><img src="/static/./images/send.png" style="margin-top:-10px; margin-left:10px" width="40" onclick="postComment('cp${val.slice(2)}')"/>
          `
        }
      }
    })
    
    document.getElementById(val).src = '/static/./images/'+ls[key];
  }
  else{
    commentTab = document.getElementById('co'+val.slice(2))
    commentTab.style.height = "0px";
    commentTab.classList.remove("scrollView");
    crsTab = document.getElementById('crs'+val.slice(2))
    crsTab.classList.remove('border-bottom');
    crsTab.classList.remove('border-white');
    commentTab.innerHTML=""
    document.getElementById(val).src = '/static/./images/'+ls[key];
  }
}
// Comments function ends

function retweet(val){
  ls = ['retweet.png','retweetFull.png']
  console.log(val);
  source = document.getElementById(val).src.split('/');
  console.log(source[source.length-1]);
  key = ls.indexOf(source[source.length-1]);
  key = (key==0)?1:0;
  
  if(key==1){
    $.ajax({
      url:'/addRetweet/'+val.slice(2),
      type:'POST',
      success: function(data){
      document.getElementById(val).src = '/static/./images/'+ls[key];
    doc = parseInt(document.getElementById('rc'+val.slice(2)).innerHTML)+1;
    document.getElementById('rc'+val.slice(2)).innerHTML= doc.toString();
      }
    })
  }
  else{
    $.ajax({
      url:'/deleteRetweet/'+val.slice(2),
      type:'POST',
      success: function(data){
        document.getElementById(val).src = '/static/./images/'+ls[key];
        doc = parseInt(document.getElementById('rc'+val.slice(2)).innerHTML)-1;
        document.getElementById('rc'+val.slice(2)).innerHTML= doc.toString();
      }
    })
  }
}

