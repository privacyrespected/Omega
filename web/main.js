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
function callback4(hong_kong_tz){
    document.getElementById("hkt").innerHTML=hong_kong_tz
};
function hong_kong_tz(){
    eel.hktime()(callback4)
};
function callback5(new_york_tz){
    document.getElementById('nyt').innerHTML=new_york_tz
};
function new_york_tz(){
    eel.nytime()(callback5)
};
function callback6(status){
    document.getElementById("openstatus1").innerHTML=status
};
function NYstatus(){
    eel.marketstatus()(callback6)
};
function callback7(status){
    document.getElementById('openstatus2').innerHTML=status
};
function HKstatus(){
    eel.marketstatus1()(callback7)
};
function userconfirm() {
    var username = document.getElementById("username").value
    var usercity = document.getElementById("usercity").value
    var user_gender = document.getElementById("usergender").value
    var userdob = document.getElementById("userdob").value
    eel.usersettingwrite(username, usercity, user_gender, userdob) 
    go_to("home.html")

};

function abortexit(){
    alert("Are you sure you want to exit? Your progress may not be saved.")
    go_to('home.html')
};