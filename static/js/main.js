var ws;
// var Audio_BG = document.getElementById("Audio_BG");
// function togglePlayBG() {
//   return Audio_BG.paused ? Audio_BG.play() : Audio_BG.pause();
// };


function init() {

  // Connect to Web Socket
  ws = new WebSocket("ws://localhost:9001");

  // Set event handlers.
  ws.onopen = function() {

    var username = document.body.dataset.character

    var user_info = {
      "username": username,
    }

    console.log(user_info);
    ws.send(JSON.stringify(user_info));

    // ws.send(JSON.stringify(document.body.dataset.character))
    // ws.send(JSON.stringify(document.body.dataset.token))
  };
  
  ws.onmessage = function(e) {
    // e.data contains received string.
    // output(e.data);
    // console.log(e.data);
    console.log("non-parsed:", e.data);
    var jobj = JSON.parse(e.data);
    
    output(jobj)
    

  };
  
  ws.onclose = function() {
    output("onclose");
  };

  ws.onerror = function(e) {
    output("onerror");
    console.log(e)
  };

}

function onSubmit() {
  var input = document.getElementById("input");
  // You can send message to the Web Socket using ws.send.
  ws.send(input.value);
  input.value = "";
  input.focus();
}

function onCloseClick() {
  ws.close();
}

function output(jobj) {
  var log = document.getElementById("log");

  var left_pay = toString(jtype)
  var jtype = jobj.jtype.type;
  var jpayload = jobj.jpayload;
  console.log("parsed:", jobj);
  console.log("type:", jtype);
  console.log("payload:", jpayload);

  var health = document.getElementById("health");
  
  var print_str = document.getElementById("attr_str");
  var print_dex = document.getElementById("attr_dex");
  var print_con = document.getElementById("attr_con");

  if (jobj.jtype.type == "attr") {
      
      var left_pay = jpayload;
      
      var print_str = document.getElementById("attr_str");
      var attr_str = left_pay.str.base + left_pay.str.mod;
      console.log(attr_str);

      var print_dex = document.getElementById("attr_dex");
      var attr_dex = left_pay.dex.base + left_pay.dex.mod;
      console.log(attr_dex);

      var print_con = document.getElementById("attr_con");
      var attr_con = left_pay.con.base + left_pay.con.mod;
      console.log(attr_con);

      var print_ins = document.getElementById("attr_ins");
      var attr_ins = left_pay.ins.base + left_pay.ins.mod;
      console.log(attr_ins);

      var print_edu = document.getElementById("attr_edu");
      var attr_edu = left_pay.edu.base + left_pay.edu.mod;
      console.log(attr_edu);

      var print_soc = document.getElementById("attr_soc");
      var attr_soc = left_pay.soc.base + left_pay.soc.mod;
      console.log(attr_soc);

      print_str.innerHTML = attr_str;
      print_dex.innerHTML = attr_dex;
      print_con.innerHTML = attr_con;
      print_ins.innerHTML = attr_ins;
      print_edu.innerHTML = attr_edu;
      print_soc.innerHTML = attr_soc;

      // left column
      var left_col = document.getElementById("left_col");

      // right column
      
  } else if (jobj.jtype.type == "char_info") {
    var left_pay = jpayload;

    var print_name = document.getElementById("char_name");
    var char_name = jpayload.char_name;
    console.log(char_name);

    var print_gender = document.getElementById("char_gender");
    var char_gender = jpayload.char_gender;
    console.log(char_gender);

    var print_xp = document.getElementById("char_xp");
    var char_xp = jpayload.char_xp;
    console.log(char_xp);

    print_name.innerHTML = '<span class="char_name">Name:</span> ' + char_name;
    print_gender.innerHTML = '<span class="char_name">Gender:</span> ' + char_gender;
    print_xp.innerHTML = '<span class="char_name">Exp:</span> ' + char_xp;


  } else if (jobj.jtype.type == "inventory") {

    let left = 'Left Hand: Empty';
    let right = 'Right Hand: Empty';
    inv_list = [];
    Object.entries(jpayload).forEach(([key, value]) => {
      switch (key) {
      case 'left hand':
        left = "Left Hand: " + value;
        $('#left_hand').css({color:'white'},1000).fadeTo(100, 0.3, function() { $(this).fadeTo(500, 1.0).css({color:'#a8a8ed'},1000); });
      case 'right hand':
        right = "Right Hand: " + value;
        $('#right_hand').css({color:'white'},1000).fadeTo(100, 0.3, function() { $(this).fadeTo(500, 1.0).css({color:'#a8a8ed'},1000); })  
      default:
        // inv_list.push(`${value} (${value})<br />`);
        inv_list += value + " (" + key + ")" + "<br>"
      }
    });
      
    inventory.innerHTML = inv_list;
    left_hand.innerHTML = left;
    right_hand.innerHTML = right;
    

  } else if (jobj.jtype.type == "user_settings") {

  } else if (jobj.jtype.type == "map_render") {

    var print_map = document.getElementById("map_render");

    map_render.innerHTML = jpayload.replace(/&/, "&amp;").replace(/</, "&lt;").
        replace(/>/, "&gt;").replace(/"/, "&quot;").
        replace(/\|br\|/g, '<br>').
        replace(/\|self_text\|/g, '<span style="color: #7f7cff;">')       .replace(/\|self_textx\|/g, '</span>').
        replace(/\|self_speech\|/g, '<span style="color: #7f7cff;">')     .replace(/\|self_speechx\|/g, '</span>').
        replace(/\|self_suit\|/g, '<span style="color: #42d4f4;">')       .replace(/\|self_suitx\|/g, '</span>').
        replace(/\|player_speech\|/g, '<span style="color: #a742f4;">')   .replace(/\|player_speechx\|/g, '</span>').
        replace(/\|comp\|/g, '<span style="color: #42d4f4;">')            .replace(/\|compx\|/g, '</span>').
        replace(/\|black\|/g, '<span style="color: black;">')             .replace(/\|blackx\|/g, '</span>').
        replace(/\|y\|/g, '<span style="color: #ffe100;">')               .replace(/\|yx\|/g, '</span>').
        replace(/\|lp\|/g, '<span style="color: #9ea6e2;">')              .replace(/\|lpx\|/g, '</span>').
        replace(/\|room\|/g, '<span style="color: #ffe100;">')            .replace(/\|roomx\|/g, '</span>').
        replace(/\|repeat\|/g, '<span style="color: #a8a8a8;">')          .replace(/\|repeatx\|/g, '</span>').
        replace("|exits|", '<span style="color: #ffe100;">')              .replace("|/exits|", '</span>').
        replace(/\|player\|/g, '<span style="color: white;">')            .replace(/\|playerx\|/g, '</span>').
        replace(/\|npc\|/g, '<span style="color: #ea724d;">')             .replace(/\|npcx\|/g, '</span>').
        replace(/\|alert\|/g, '<span style="color: #ff3b00;">')           .replace(/\|alertx\|/g, '</span>').
        replace("|p|", '<span style="color: #a8a8ed;">')                  .replace("|/p|", '</span>').
        replace("|w|", '<span style="color: white;">')                    .replace("|/w|", '</span>'); // "


  } else if (jobj.jtype.type == "player_list") {

      // right column
      var rc_players = document.getElementById("rc_players_sub");
      var player_list = "";

      for (i in jpayload) {
        console.log(jpayload[i]);

        if (jpayload[i].player_state == 'online') {
          online_status = "<span class='online_status'>" + 'online' + "</span>"
        } else {
          online_status = "<span class='offline_status'>" + 'offline' + "</span>"
        }

        player_rank = jpayload[i].player_title

        // if (jpayload[i].entity_type == 'registered') {
        //   player_registered = 'Citizen'
        // } else if (jpayload[i].entity_type == 'admin') {
        //   player_registered = 'Admin'
        // } else {
        //   player_registered = 'Tourist'
        // }

        player_list += "<p>" + jpayload[i].player_name + " (" + online_status + ") " + "</p>" +
                       "<small>Rank: " + player_rank + "</small><br>"
      }

      rc_players.innerHTML = player_list

  
  } else if (jobj.jtype.type == "vitals") {

      let health = document.getElementById("health")
      health.value = jpayload.hp_current;
      health.max = jpayload.hp_max;

      let health_num = document.getElementById("health_num")
      health_num.innerHTML = 'HP: ' + jpayload.hp_current + " / " + jpayload.hp_max;


  } else if (jobj.jtype.type == "init_round_time") {

      let round_time = document.getElementById("round_time")
      round_time.max = jpayload;


  } else if (jobj.jtype.type == "round_time") {

      let round_time = document.getElementById("round_time")
      round_time.value = jpayload;

      let round_time_num = document.getElementById("round_time_num")
      round_time_num.innerHTML = 'Roundtime: ' + jpayload + ' sec';


  } else if (jobj.jtype.type == "suit_shield") {

      let suit_shield = document.getElementById("suit_shield")
      suit_shield.value = jpayload.shield_current;
      suit_shield.max = jpayload.shield_max;

      let suit_shield_num = document.getElementById("suit_shield_num")
      suit_shield_num.innerHTML = 'Suit: ' + jpayload.shield_current + " / " + jpayload.shield_max;


  } else if (jobj.jtype.type == "wiki") {
      
      var wiki = document.getElementById("rc_central_data");
      var content = "";

      for (i in jpayload) {
        content += '<li><span class="caret"><a href="#">' + jpayload[i].cmd_title + "</a></span>" +
        '<ul class="nested">' +
        "<li>Usage: " + jpayload[i].hotkey + "</li>" +
        "<li>Description: " + jpayload[i].desc + "</li>" +
        "</ul>" +
        "</li>"
      }
      // console.log(attr_str);

      wiki.innerHTML = '<li><span class="caret"><a href="#">Commands</a></span>' + 
      '<hr>' +
      '<ul class="nested">' + content +
      '</ul>' +
      '</li>';

      var toggler = document.getElementsByClassName("caret");
      var i;

      for (i = 0; i < toggler.length; i++) {
        toggler[i].addEventListener("click", function() {
          this.parentElement.querySelector(".nested").classList.toggle("active");
          this.classList.toggle("caret-down");
        });
      }

  } else {

      var escaped = jpayload.replace(/&/, "&amp;").replace(/</, "&lt;").
        replace(/>/, "&gt;").replace(/"/, "&quot;").
        replace("|br|", '<br>').
        replace(/\|self_text\|/g, '<span style="color: #7f7cff;">')       .replace(/\|self_textx\|/g, '</span>').
        replace(/\|self_speech\|/g, '<span style="color: #7f7cff;">')     .replace(/\|self_speechx\|/g, '</span>').
        replace(/\|self_suit\|/g, '<span style="color: #42d4f4;">')       .replace(/\|self_suitx\|/g, '</span>').
        replace(/\|player_speech\|/g, '<span style="color: #a742f4;">')   .replace(/\|player_speechx\|/g, '</span>').
        replace(/\|comp\|/g, '<span style="color: #42d4f4;">')            .replace(/\|compx\|/g, '</span>').
        replace(/\|success\|/g, '<span style="color: #91ff38;">')         .replace(/\|successx\|/g, '</span>').
        replace(/\|y\|/g, '<span style="color: #ffe100;">')               .replace(/\|yx\|/g, '</span>').
        replace(/\|lp\|/g, '<span style="color: #9ea6e2;">')              .replace(/\|lpx\|/g, '</span>').
        replace(/\|room\|/g, '<span style="color: #ffe100;">')            .replace(/\|roomx\|/g, '</span>').
        replace(/\|repeat\|/g, '<span style="color: #a8a8a8;">')          .replace(/\|repeatx\|/g, '</span>').
        replace("|exits|", '<span style="color: #ffe100;">')              .replace("|/exits|", '</span>').
        replace(/\|player\|/g, '<span style="color: white;">')            .replace(/\|playerx\|/g, '</span>').
        replace(/\|npc\|/g, '<span style="color: #ea724d;">')             .replace(/\|npcx\|/g, '</span>').
        replace(/\|alert\|/g, '<span style="color: #ff3b00;">')           .replace(/\|alertx\|/g, '</span>').
        replace("|p|", '<span style="color: #a8a8ed;">')                  .replace("|/p|", '</span>').
        replace("|w|", '<span style="color: white;">')                    .replace("|/w|", '</span>'); // "

      log.innerHTML = log.innerHTML + "<br>" + escaped;
      var log = $('#chatlog');
      log.animate({ scrollTop: log.prop('scrollHeight')}, 10);

  }
}

function openCity(evt, cityName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";


}
