eel.expose(go_to)
function go_to(url) {window.location.replace(url);};

function callback(done){
    if (done === done) {
        //window.location.href = "home.html";
        go_to('home.html')
    }      
}
function welcome(){
    eel.welcome()
};
function load_modules(){
    eel.load_modules()(callback)
};

function callback(current_ram){
    document.getElementById("ramoutput").innerHTML=current_ram
};
function checkram(){
eel.checkram()(callback)
}


function callback1(current_cpu){
    document.getElementById("cpuoutput").innerHTML=current_cpu
};
function checkcpu(){
eel.checkcpu()(callback1)
}

function callback2(current_network){
    document.getElementById("networkoutput").innerHTML=current_network
};

function checknetwork(){
eel.checknetwork1()(callback2)
};

function callback3(DOJI){
    document.getElementById("DOJIoutput").innerHTML= DOJI
};

function checkDOJI(){
    eel.checkDOJI()(callback3)
};
function userconfirm() {
    var username = document.getElementById("username").value
    var usercity = document.getElementById("usercity").value
    var user_gender = document.getElementById("usergender").value
    var userdob = document.getElementById("userdob").value
    eel.usersettingwrite(username, usercity, user_gender, userdob) 
    go_to("home.html")

}