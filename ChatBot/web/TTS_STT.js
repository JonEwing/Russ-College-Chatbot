eel.expose(speak);

// Web Speech API
var synth = window.speechSynthesis;
var recognition = new webkitSpeechRecognition();
recognition.continuous = false;
recognition.lang = 'en-US';
recognition.interimResults = false;

var synth_enabled = false;
var listening = false;
const Instructions = $('instructions');
const TTS_Toggle = GetElementInsideContainer("tts-toggle", "myonoffswitch");
const MicButton = document.getElementById('micButton');

function toggleTextToSpeech() {
  menu = document.getElementById("dropdownMenu");
  toggleButton = menu.childNodes[3];
  menuItem = toggleButton.getElementsByTagName('a')[0];
  
  if (!synth_enabled) {
    menuItem.textContent = "Disable Text-to-Speech";
    window.msg = setup_speech("en", "US");
  } else {
    menuItem.textContent = "Enable Text-to-Speech";
  }

  synth_enabled = !synth_enabled;
}

function speak(response_string) {
    if (window.synth_enabled) {
      window.msg.text = response_string;
      synth.speak(window.msg);
    }
}

function setup_speech(lang, country) {
  window.msg = new SpeechSynthesisUtterance();
  msg.volume = 1; // 0 to 1
  msg.rate = 1; // 0.1 to 10
  msg.pitch = 1; // 0 to 2
  var voices = window.synth.getVoices();
  msg.lang = lang + "-" + country;
  //msg.voice = voices[3];
  return msg;
}

function startVoiceCapture() {
  if (!listening) {
    MicButton.style.color = "#A52A2A";
    recognition.start();
    listening = true;
  } else {
    MicButton.style.color = "#000000";
    recognition.stop();
    listening = false;
  }
}

recognition.onresult = function(event) {
  MicButton.style.color = "#000000";
  recognition.stop();
  listening = false;
  var text = event.results[0][0].transcript;
  console.log(text);
  chatInput.value = text;
}

// From user: naveen @ StackOverflow Aug 24 '11 at 6:57
// Source: https://stackoverflow.com/questions/7171483/simple-way-to-get-element-by-id-within-a-div-tag
function GetElementInsideContainer(containerID, childID) {
  var elm = document.getElementById(childID);
  var parent = elm ? elm.parentNode : {};
  return (parent.id && parent.id === containerID) ? elm : {};
}