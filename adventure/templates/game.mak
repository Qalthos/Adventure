<%inherit file="local:templates.master"/>

<%def name="title()">
Unnamed Game
</%def>

<link rel="stylesheet" href="css/game.css"/>
<div id="game" style="background-image:url('images/cards/${card.id}.png')">
  %for direction in ['top', 'left', 'right', 'center', 'back']:
    <div id="move_${direction}"
      %if links.get(direction):
         style="cursor:url('images/cursors/${direction}.cur'), n-resize;
         %if request.identity and 'edit_link' in request.identity['permissions']:
           border: 2px solid green;
         %endif
         "
         onclick="window.location.replace('/game?card_id=${links[direction]}')"
      %elif request.identity and 'edit_link' in request.identity['permissions']:
        style="border: 2px solid red;"
      %endif
    >
      %if request.identity and 'edit_link' in request.identity['permissions']:
        <a href="${tg.url('edit_link', params=dict(card_id=card.id, direction=direction))}" class='edit'>Edit Link</a>
      %endif
    </div>
  %endfor
</div>
