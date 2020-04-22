/*
@file chatbot.js
@description ...
*/

eel.expose(py_to_js);

const chatBtn = document.getElementById('r2');
const chatForm = document.getElementById('chatForm');
const chatInput = document.getElementById('chatInput');
const loginForm = document.getElementById("login");
const chatLog = document.getElementById("chatlog");
const successBtn = document.getElementById("yesResponseBtn");
const failBtn = document.getElementById("noResponseBtn");
const scaler = document.getElementById("scaler");
const profileImg = document.getElementById("profileImg");
const chatWindow = document.getElementsByClassName("chatbot")[0];
const responseButtons = document.getElementById("responseButtons");
const muteBtn = document.getElementById("mute").getElementsByTagName("a")[0];

const CONFIDENCE_LOWER_BOUND = 50;
const CONFIDENCE_UPPER_BOUND = 80;

chatForm.addEventListener('submit', onSubmit);
loginForm.addEventListener('submit', loginSubmit);
chatBtn.addEventListener('click', toggleWindow);
scaler.addEventListener("mousedown", scalerClick);
document.addEventListener("mouseup", function(){
    document.removeEventListener("mousemove", scaleWindow);
    scale_base = scale_val;
    document.body.style.cursor = "default";
});
profileImg.addEventListener('click', function(){
    profileImg.style.backgroundColor = 'rgb(' + Math.random()*230 + ', ' + Math.random()*230 + ', ' + Math.random()*230 + ')';
});

let open = false;
let name = "";
let email = "";
let identity = "";
let xPos;
let yPos;
let scale_base = 1;
let scale_val = 1;
var isReady = true;
let muted = false;
let userQueryCount = 0;

const STT_Button = document.getElementById('sttButton');

const isChrome = !!window.chrome && (!!window.chrome.webstore || !!window.chrome.runtime);
chatBtn.addEventListener('click', () => {
  if (!isChrome) {
    // clock is visible. hide it
    STT_Button.style.display = 'none';
  }
});

$('.dropdown-content').click(function(e) {
    e.stopPropagation();
});

const send_sound = new Audio("sounds/blop2.mp3");
const recieved_sound = new Audio("sounds/blop.mp3");
let prev_question = "";

const fiveMinutes = 60 * 5;
let resetIdleTimer = false;
let loading_response = false;

/* picks the color for the bot's profile image */
profileImg.style.backgroundColor = 'rgb(' + Math.random()*230 + ', ' + Math.random()*230 + ', ' + Math.random()*230 + ')';

/* takes text that's in the input box and displays it
   in the messaging window */
function onSubmit(e){
    e.preventDefault();
    const question = (chatInput.value).trim();
    tempString = question.toString().replace('(', '');
    updatedQuestion = tempString.replace(')', '');

    if (isReady == true && question != "" && question != prev_question) {
        /* adds user's question */
        chatInput.value = '';
        const user_message = document.createElement("li");
        user_message.id = "usertext";
        user_message.textContent = question;
        chatLog.appendChild(user_message);
        chatLog.appendChild(document.createElement("lb"));
        chatLog.scrollTop = chatLog.scrollHeight - chatLog.clientHeight;
        
        if(!muted) {
            send_sound.play();
        }

        if (userQueryCount > 0) {
            userQueryCount--;
        }
        if (responseButtons.style.display === "block") {
            responseButtons.style.display = "none";
            userQueryCount = 5;
        }

        isReady = false;

        /* shows a "..." to indicate the bot is processing */
        const dots = document.createElement("li");
        dots.id = "chattext";
        // dots.textContent = "...";
        dots.insertAdjacentHTML("afterbegin", "<span class='spinner-grow spinner-grow-sm'></span>");
        dots.insertAdjacentHTML("afterbegin", "<span class='spinner-grow spinner-grow-sm'></span>");
        dots.insertAdjacentHTML("afterbegin", "<span class='spinner-grow spinner-grow-sm'></span>");        
        chatLog.appendChild(dots);
        chatLog.scrollTop = chatLog.scrollHeight - chatLog.clientHeight;

        prev_question = question;

        eel.get_name_email(name, email, identity)
        eel.js_to_py(updatedQuestion);

        var child_nodes = document.getElementById("dropdownMenu").childNodes;
        child_nodes[1].style.pointerEvents = "none";
    } else {
        chatInput.style.color = "red";
        setTimeout(() => {
            chatInput.style.color = "initial";
        }, 1000);
    }

    loading_response = true;
    resetIdleTimer = true;
}

/* shows and hides chatbot. */
function toggleWindow(){
    if (open){
        chatWindow.classList.remove("toggleShow");
        chatWindow.classList.add("toggleHide");
        chatBtn.classList.remove("r2Open");
        chatBtn.classList.add("r2Close");
        setTimeout(() => {chatWindow.style.transform = "scale(0)";}, 190);
        open = false;
    } else {
        chatWindow.classList.remove("toggleHide");
        chatWindow.classList.add("toggleShow");
        chatBtn.classList.remove("r2Close");
        chatBtn.classList.add("r2Open");
        chatWindow.style.transform = "scale(" + scale_val + ")";
        open = true;
    }
}

/* displays responce from chatbot in the messaging window */
function py_to_js(ret_string, response_confidence, user_identity)
{
    if(user_identity ==  identity)
    {
        chatLog.removeChild(chatLog.lastChild);
        isReady = true;

        const bot_message = document.createElement("li");
        bot_message.id = "chattext";
        bot_message.textContent = ret_string;
        chatLog.appendChild(bot_message);
        chatLog.appendChild(document.createElement("lb"));
        chatLog.scrollTop = chatLog.scrollHeight - chatLog.clientHeight;

        if (response_confidence < CONFIDENCE_UPPER_BOUND && userQueryCount <= 0 && response_confidence > 0) {
            getUserSatisfaction();
        }        

        if(!muted){
            recieved_sound.play();
        }

        var child_nodes = document.getElementById("dropdownMenu").childNodes;
        child_nodes[1].style.pointerEvents = "auto";

    }

    loading_response = false;
}

/* takes name and email from user at the start of the interaction
    also sends the intro message after submitting */
function loginSubmit(e) {
    e.preventDefault();
    const name_input = document.getElementById("name");
    const email_input = document.getElementById("email");
    name = name_input.value;
    email = email_input.value;
    if (name != "" && validateName(name) && email != ""){
        name_input.value = "";
        email_input.value = "";
        document.getElementById("login_window").style.visibility = "hidden";

        setTimeout(() => {
            const bot_message = document.createElement("li");
            bot_message.id = "chattext";
            bot_message.textContent = "Hello, I am Russ Rufus the Russ College of Engineering Recruitment Chatbot. I am here to help answer any questions you have about appying to the college. E.g. How will my credits from HS transfer? or What is your approach to interships? For more information on how I work type help.";
            chatLog.appendChild(bot_message);
            chatLog.appendChild(document.createElement("lb"));
            chatLog.scrollTop = chatLog.scrollHeight - chatLog.clientHeight;
            if(!muted){
                recieved_sound.play();
            }
        }, 500);
    }
    identity = makeid(4)
    identity = email.concat(identity);
    startIdleTimer(fiveMinutes);
}

/* checks if name  is valid  */
function validateName(name)
{
  var re = /^[a-zA-Z ]+$/;

  return re.test(name);
}

function scaleWindow(e){
    const dx = xPos - e.x;
    const dy = yPos - e.y;
    const scale_xval = scale_base + dx/(chatWindow.offsetWidth);
    const scale_yval = scale_base + dy/(chatWindow.offsetHeight);
    const x = Math.max(Math.abs(scale_xval), Math.abs(scale_yval));
    if(x > 0.25) {
        if (x == Math.abs(scale_xval)) {
            scale_val = scale_xval;
        } else {
            scale_val = scale_yval;
        }
        chatWindow.style.transform = "scale(" + scale_val + ")";
    }
    while(chatWindow.getBoundingClientRect().top <= 10){
        scale_val -= 1/(chatWindow.offsetHeight);
        chatWindow.style.transform = "scale(" + scale_val + ")";
    }
}

function scalerClick(e) {
    xPos = e.x;
    yPos = e.y;
    document.addEventListener("mousemove", scaleWindow);
    document.body.style.cursor = "nw-resize";
}

async function startIdleTimer(duration) {
    /*
    @function Triggers the `wikiAdapter` logic adapter every
    time `duration` seconds have passed.

    @param duration A length of time in seconds
    */

    var timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        if (--timer < 0 && !loading) {
            timer = duration;
            chatInput.value = "...";
            const submitBtn = document.getElementById("submit");
            submitBtn.click();
            chatInput.value = "";
        }
        if (resetIdleTimer) {
            timer = duration, minutes, seconds;
            resetIdleTimer = false;
        }
    }, 1000);
}

function makeid(l)
{
    var text = "";
    var char_list = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for(var i=0; i < l; i++ )
    {
        text += char_list.charAt(Math.floor(Math.random() * char_list.length));
    }
    return text;
}

function getUserSatisfaction() {
    if (responseButtons.style.display !== "block") {
        console.log("Displaying response buttons");
        const bot_message = document.createElement("li");
        bot_message.id = "chattext";
        bot_message.textContent = "Did that answer your question?";
        chatLog.appendChild(bot_message);
        chatLog.appendChild(document.createElement("lb"));
        // Move chat boxes up
        var nodes = chatLog.childNodes;
        num_children = nodes.length;
        nodes[num_children-1].style.marginBottom = "40px";
        chatLog.scrollTop = chatLog.scrollHeight - chatLog.clientHeight;
        responseButtons.style.display = "block";
    } else {
        console.log("Removing response buttons");
        // Move chat boxes back down
        responseButtonsDown();
        responseButtons.style.display = "none";
    }
}
                            
function displayMenu() {
    document.getElementById("dropdownMenu").classList.toggle("show");
}

successBtn.addEventListener('click', function() {
    responseButtonsDown();
    feedback = "yes";
    console.log(feedback);
    eel.userFeedback(prev_question, feedback);
    responseButtonsDown();
    responseButtons.style.display = "none";
});

failBtn.addEventListener('click', function() {
    responseButtonsDown();
    feedback = "no";
    console.log(feedback);
    eel.userFeedback(prev_question, feedback);
    responseButtonsDown();
    responseButtons.style.display = "none";
});

function responseButtonsDown() {
    var nodes = chatLog.childNodes;
    num_children = nodes.length;
    nodes[num_children-1].style.marginBottom = "15px";
}

function clearConversation() {
    chatLog.innerHTML = "";
}

function muteSounds() {
    if(muted){
        muted = false;
        muteBtn.textContent = "Mute Sounds";
    } else {
        muted = true;
        muteBtn.textContent = "Unmute Sounds";
    }
}

function decreaseFontSize(){
    const fs = Number(window.getComputedStyle(chatLog).getPropertyValue("font-size").slice(0, -2));
    if (fs > 8){
        chatLog.style.fontSize = fs - 1;
    }
}

function increaseFontSize(){
    const fs = Number(window.getComputedStyle(chatLog).getPropertyValue("font-size").slice(0, -2));
    if (fs < 18){
        chatLog.style.fontSize = fs + 1;
    }
}
