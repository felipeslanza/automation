$(document).ready(function(){

  $("#signup-button").click(function(){
    $("#signup-box").removeClass("hidden");
    $("#initial-box").addClass("hidden");
  });

  $("#login-button").click(function(){
    $("#login-box").removeClass("hidden");
    $("#initial-box").addClass("hidden");
  });

  $("#back-button").click(function(){
    $("#login-box").addClass("hidden");
    $("#signup-box").addClass("hidden");
    $("#initial-box").removeClass("hidden");
  });

});
