var mailPattern = /\S+@\S+\.\S+/;
var specialPattern = /[ `!#$%^&*()_+\-=\[\]{};':"\\|,<>\/?~]/;
var stringPattern = /\S/;

function ValidateFormSignIn() {

    usrid = document.forms["loginForm"]["userid"].value;
    pwd = document.forms["loginForm"]["password"].value;
    $.ajax({
        url:'/validateUser/'+usrid+'-_-'+pwd,
        type:'POST',
        success: function(data){
          
          if(data == "No Data"){ 
            console.log("No Data Found");
            document.getElementById('error').innerHTML = "Invalid Credentials:)"
            
          }
          else{
            window.location.replace("/dashboard");
          }
        }
    })
  
    

}


function ValidatePWD(pwd) {
    check = {
        'special': 0,
        'number': 0,
        'lower': 0,
        'upper': 0
    }
    if (pwd.length >= 8 && pwd.length <= 25) {
        for (i = 0; i < pwd.length; i++) {
            ascii = pwd.charCodeAt(i);
            if (ascii >= 65 && ascii <= 91) check['upper']++;
            else if (ascii >= 97 && ascii <= 122) check['lower']++;
            else if (ascii >= 48 && ascii <= 57) check['number']++;
            else check['special']++;
        }
        if (check['number'] >= 1 && check['special'] >= 1 && check['upper'] >= 1 && check['lower'] >= 1) return true;
    }
    return false;
}

function ValidateMAIL(mail) {
    return !specialPattern.test(mail) && mailPattern.test(mail);
}

function ValidateUSERNAME(usr) {
    for (i = 0; i < usr.length; i++) {
        ascii = usr.charCodeAt(i);
        if ((ascii >= 65 && ascii <= 91) || (ascii >= 97 && ascii <= 122));
        else return false;
    }
    return true;
}

function CheckUSERNAME(usrid) {
    flag = true;
    $.ajax({
        url: '/checkUser/' + usrid,
        type: 'POST',
        success: function(data) {
            if (parseInt(data) == 1) flag = false;
        }
    })
    return flag;
}
function CheckMAIL(mailid){
    flag = true;
    $.ajax({
      url:'/checkMail/'+mailid,
      type:'POST',
      success: function(data){
        
        if(parseInt(data) == 1) flag = false;
      }
    })
  
  return flag;
}
function ValidateFormSignUp() {
  
            usrid = document.forms["signUPForm"]["usrid"].value;
            usr = document.forms["signUPForm"]["usr"].value;
            mail = document.forms["signUPForm"]["mailId"].value;
            pwd = document.forms["signUPForm"]["password"].value;
                if (!ValidateUSERNAME(usr)) {
                    document.getElementById('error1').innerHTML = "Invalid USERNAME Format-_-";
                } else {

                    if (!ValidateMAIL(mail)) {
                        document.getElementById('error1').innerHTML = "Invalid Email Format-_-";
                    } else {
                        if (!CheckUSERNAME(usrid) || !CheckMAIL(mail)) {         
                     document.getElementById('error1').innerHTML = "User or Mail Already Exists -_-";
                        } else {
                            if (ValidatePWD(pwd)) {
                                var form_data = new FormData($('#signUPForm')[0]);
                                  $.ajax({
                                    url: '/addUser/' + usr + '-_-' + mail + '-_-' + pwd + '-_-' + usrid,
                                    data: form_data,
                                    type: 'POST',
                                    contentType: false,
                                    cache: false,
                                    processData: false,
                                    success: function(){
                                       window.location.replace("/"); console.log('Success!');
                                    }
                                });
                                
                              
                            } else {
                                document.getElementById('error1').innerHTML = "Incorrect Password Format-_-)"
                                alert("Password Must contain\n at least one number and one uppercase and lowercase letter, and at least 8 or more characters")

                            }
                        }


                    }
                }

    
}
var loadFile = function(event) {
    var image = document.getElementById('output');
    image.src = URL.createObjectURL(event.target.files[0]);
};