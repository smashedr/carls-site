/*<![CDATA[*/
var emailriddlerarray=[115,104,97,110,101,64,99,97,114,108,115,46,115,105,116,101];
var encryptedemail_id26='' //variable to contain encrypted email
for (var i=0; i<emailriddlerarray.length; i++)
 encryptedemail_id26+=String.fromCharCode(emailriddlerarray[i])
document.write('<a href="mailto:'+encryptedemail_id26+'">'+
    '<i class="fa fa-envelope-o" aria-hidden="true"></i> '+encryptedemail_id26+'</a>');
/*]]>*/