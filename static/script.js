var view = 12;
var msg = 12;
prevtop =0;
prevbottom =0;
flagtop = 0;
flagbottom=0;
try{
  var tweet = document.getElementById("tweet");
  tweet.addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
      document.getElementById("post").click();
    }
  });
}
catch(e){
  console.log("");
}
// Post a new message
function postMessage(){
  dt = new Date();
  $.ajax({
      url: '/addData/'+tweet.value+'-_-'+dt.getDate()+"-"+(dt.getMonth()+1)+"-"+dt.getFullYear(),
      type: 'POST',
      success: function () {
                  location.reload();
      },
  });
}
// Delete existing message
function deleteEntry(val){
  $.ajax({
      url: '/deleteData/'+val,
      type: 'POST',
      success: function () {
                  location.reload();
      },
  });
}
// Bookmark or Remove boomarked element
function bookmarkEntry(usrid,val,key,from){
  console.log(usrid,val,key,from);
  val = val.toString()
  if(key==1){
    $.ajax({
        url: '/bookmarkData/'+usrid+'-'+val,
        type: 'POST',
        success: function () {
          document.getElementById(val).src = "/static/./images/bookmarksFull.png";
           var clickfun = document.getElementById(val).getAttribute("onclick");
  var funname = clickfun.substring(0,clickfun.indexOf("("));
  document.getElementById(val).setAttribute("onclick",funname+"('"+usrid+"',"+val+","+0+","+"'"+from+"')");
          if(from=="bookmarks"){
            document.getElementById('A'+val).remove();
          }
        },
    });
  }
  else if(key==0){
    $.ajax({
        url: '/removebookmark/'+usrid+'-'+val,
        type: 'POST',
        success: function () {
          document.getElementById(val).src = "/static/./images/bookmarks.png";
          var clickfun = document.getElementById(val).getAttribute("onclick");
          var funname = clickfun.substring(0,clickfun.indexOf("("));
          document.getElementById(val).setAttribute("onclick",funname+"('"+usrid+"',"+val+","+1+","+"'"+from+"')");
          if(from=="bookmarks"){
            document.getElementById('A'+val).remove();
          }
        },
    });
  }
  
}


// try{
// const myMsgScroller = document.getElementById('scrollerMsg') ;
// myMsgScroller.addEventListener('scroll', () => {  
//   if (myMsgScroller.offsetHeight + myMsgScroller.scrollTop >= myMsgScroller.scrollHeight) {   
//     $.ajax({
//         url: '/loaddata/'+msg+'-_-msg',
//         type: 'POST',
//         success: function (data) {
//           size = data['data'].length
//           if(size>0){
             

//              for(i=0;i<size;i++){
//              const div = document.createElement('div');
//              div.className = 'container mt-2 border py-2';
//              div.style.cssText = 'border-radius:25px;';
//              div.innerHTML = `
//                   <div class="row">
//                      <div class="col-md-1">
//                         <img src="${data['data'][i][6]}" style="border-radius:100px;"width="43" id="i${data['data'][i][0]}"/>
//                      </div>
//                      <div class="col-md-9 ">
//                         <strong>
//                            <p style="display:inline" class="ml-1">${data['data'][i][5]}</p>
//                         </strong>
//                         <p class="ml-1 text-dark" style="font-size:15px;">${data['data'][i][1]}</p>
//                      </div>
//                      <div class="col-md-2 text-dark" style="font-size:15px;">
//                         ${data['data'][i][3]} 
//                      </div>
//                   </div>
//                   <div class="row">
//                      <div class="col-md-1"></div>
//                      <div class="col-md-9" style="word-wrap: break-word;">
//                         ${data['data'][i][2]}
//                      </div>
//                      <div class="col-md-2 ">    
//                          <img src="/static/./images/bin.png" style="margin-left:10px; padding:10px 10px 10px 10px;" width="33" onclick="deleteEntry(${data['data'][i][0]})" class="deleteBtn "/>
                       
//                      </div>
//                   </div>
//                `
//              document.getElementById('scrollerMsg').appendChild(div);  
//            }
//           }
//         },
//     });
//     msg+=6;
//   }  
// })
// }
// catch(e){
//   console.log("No Msg");
// }

// try{
// const myScroller = document.getElementById('scroller') ;
// myScroller.addEventListener('scroll', () => {  
//   if(myScroller.scrollTop==0){
//     if(flagbottom==1){
//       if(view-prevbottom>0){
//         view-=prevbottom;
//         flagbottom=0;
//       }
//     }
  
//     flagtop=1;
//     // if(view-6>0) 
//     if(view-6>0)
//      view-=6;
//     prevtop=view;
    
      
//     console.log(view+'top');
    
//        $.ajax({
//         url: '/loaddata/'+view+'-_-main',
//         type: 'POST',
//         success: function (data) {
//           size = data['data'].length
//           val = 6;
//           ls=[]
//           parent  = document.getElementById('scroller')
//           length = parent.children.length;
//           for(i=length-1;i>=length-val;i--)
//            document.getElementById(parent.children[i].id).remove();
             
//           if(size==6){
              
//            for(i=size-1;i>=0;i--){
//              const div = document.createElement('div');
//              div.className = 'container mt-2 border py-2';
//              div.style.cssText = 'border-radius:25px;';
//              flag = data['data'][i][4];
//              flag = !flag;
//              if(flag){
//                src = "/static/./images/bookmarks.png"
//              }
//              else{
//                src = "/static/./images/bookmarksFull.png"
//              }
//              div.setAttribute("id", 'a'+data['data'][i][0]);
//              div.innerHTML = `
//                   <div class="row">
//                      <div class="col-md-1">
//                         <img src="${data['data'][i][6]}" style="border-radius:100px;"width="43" id="i${data['data'][i][0]}"/>
//                      </div>
//                      <div class="col-md-9 ">
//                         <strong>
//                            <p style="display:inline" class="ml-1">${data['data'][i][5]}</p>
//                         </strong>
//                         <p class="ml-1 text-dark" style="font-size:15px;">${data['data'][i][1]}</p>
//                      </div>
//                      <div class="col-md-2 text-dark" style="font-size:15px;">
//                         ${data['data'][i][3]} 
//                      </div>
//                   </div>
//                   <div class="row">
//                      <div class="col-md-1"></div>
//                      <div class="col-md-9" style="word-wrap: break-word;">
//                         ${data['data'][i][2]}
//                      </div>

//                      <div class="col-md-2 ">    
//                           <img class="invert" src="${src}" style="margin-left:10px; padding:10px 10px 10px 10px;" width="33" onclick="bookmarkEntry('${data['data'][i][1]}','${data['data'][i][0]}',${flag},'main')" class="deleteBtn" id="${data['data'][i][0]}"/>
                       
//                      </div>
//                   </div>
//                `
//           parent = document.getElementById('scroller')
//           parent.insertBefore(div,parent.firstChild);  
           
//            }
//           myScroller.scrollTop -= 20;
//           }
//         },
//     });
//   }
//   if (myScroller.offsetHeight + myScroller.scrollTop >= myScroller.scrollHeight) {
//     console.log(view+'bottom');
    
//     if(flagtop==1){
//       view+=prevtop;
//       flagtop=0;
//     }
//     flagbottom=1;
//     $.ajax({
//         url: '/loaddata/'+view+'-_-main',
//         type: 'POST',
//         success: function (data) {
//           console.log(data)
//           size = data['data'].length
          
//           if(size==6){
            
//            for(i=0;i<size;i++){
//              const div = document.createElement('div');
//              div.className = 'container mt-2 border py-2';
//              div.style.cssText = 'border-radius:25px;';
//              flag = data['data'][i][4];
//              flag = !flag;
//              if(flag){
//                src = "/static/./images/bookmarks.png"
//              }
//              else{
//                src = "/static/./images/bookmarksFull.png"
//              }
//              div.setAttribute("id", 'a'+data['data'][i][0]);
//              div.innerHTML = `
//                   <div class="row">
//                      <div class="col-md-1">
//                         <img src="${data['data'][i][6]}" style="border-radius:100px;"width="43" id="i${data['data'][i][0]}"/>
//                      </div>
//                      <div class="col-md-9 ">
//                         <strong>
//                            <p style="display:inline" class="ml-1">${data['data'][i][5]}</p>
//                         </strong>
//                         <p class="ml-1 text-dark" style="font-size:15px;">${data['data'][i][1]}</p>
//                      </div>
//                      <div class="col-md-2 text-dark" style="font-size:15px;">
//                         ${data['data'][i][3]} 
//                      </div>
//                   </div>
//                   <div class="row">
//                      <div class="col-md-1"></div>
//                      <div class="col-md-9" style="word-wrap: break-word;">
//                         ${data['data'][i][2]}
//                      </div>
//                      <div class="col-md-2 ">    
//                           <img class="invert" src="${src}" style="margin-left:10px; padding:10px 10px 10px 10px;" width="33" onclick="bookmarkEntry('${data['data'][i][1]}','${data['data'][i][0]}',${flag},'main')" class="deleteBtn" id="${data['data'][i][0]}"/>
                       
//                      </div>
//                   </div>
//                `
//              document.getElementById('scroller').appendChild(div);  
//            }
           
//               val = 6;
//               parent  = document.getElementById('scroller')
//               var ls = []
//               for(i=0;i<val;i++){
//                 ls.push(parent.children[i].id)
//               }
//              for(i=0;i<val;i++)document.getElementById(ls[i]).remove();
//               myScroller.scrollTop = 10;
            
          
//           prevbottom = size;
//           check = parseInt(data['msgid'].toString().slice(5))
//           // if(check<=view+size)
//             view+=size;
//           }
//         },
//     });
  
//   }  
// })
// }
// catch(e){
//   console.log("No main");
// }