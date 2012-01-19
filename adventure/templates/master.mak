<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    ${self.meta()}
    <title>${self.title()}</title>
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/style.css')}" />
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/admin.css')}" />
</head>

<body class="${self.body_class()}">
  ${self.header()}
  ${self.main_menu()}
  ${self.content_wrapper()}
  ${self.footer()}
</body>

<%def name="meta()">
  <meta content="text/html; charset=UTF-8" http-equiv="content-type"/>
</%def>

<%def name="title()">
</%def>

<%def name="body_class()">
</%def>

<%def name="header()">
</%def>

<%def name="main_menu()">
  <ul id="mainmenu">
    <li class="first"><a href="${tg.url('/')}" class="${('', 'active')[page=='index']}">Welcome</a></li>
    <li><a href="${tg.url('/game')}" class="${('', 'active')[page=='game']}">Game</a></li>
    % if not request.identity:
      <li id="login" class="loginlogout"><a href="${tg.url('/login')}">Login</a></li>
    % else:
      <li id="login" class="loginlogout"><a href="${tg.url('/logout_handler')}">Logout</a></li>
      <li id="admin" class="loginlogout"><a href="${tg.url('/admin')}">Admin</a></li>
      %if 'new_card' in request.identity['permissions']:
        <li id="new_card" class="loginlogout"><a href="${tg.url('/game/edit_card')}">New Card</a></li>
      %endif
    % endif
  </ul>
</%def>

<%def name="content_wrapper()">
    <div id="content">
    <div>
      <%
      flash=tg.flash_obj.render('flash', use_js=False)
      %>
      % if flash:
        ${flash | n}
      % endif
      ${self.body()}
    </div>
</%def>

<%def name="footer()">
</%def>
</html>
