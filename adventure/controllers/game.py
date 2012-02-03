# -*- coding: utf-8 -*-
"""Game Controller"""
import tw.forms as twf

from tg import expose, flash, require, url, request, redirect, tmpl_context, validate
from adventure.lib.base import BaseController
from adventure.model.cards import DBSession, metadata, Card, Link
from adventure.widgets.link_form import create_link_form, edit_link_form
from adventure.widgets.card_form import create_card_form, edit_card_form
from adventure.widgets.card_grid import CardGrid

import shutil
import os
from pkg_resources import resource_filename

__all__ = ['GameController']


class GameController(BaseController):
    """
    The game controller.  Takes care of all game-interaction elements.

    """

    @expose('adventure.templates.game')
    def index(self, card_id=None):
        """It's a game!"""
        if not card_id:
            card = DBSession.query(Card).filter_by(special='root').first()
            card.id = card_id
        else:
            card = DBSession.query(Card).filter_by(id=card_id).first()

        links=dict(left=None, right=None, top=None, back=None, center=None, others=[])
        for link in DBSession.query(Link).filter_by(card_id=card_id).all():
            if link.direction in links.keys():
                links[link.direction] = link.new_card_id
            else:
                links['other'].append((link.direction, link.new_card_id))
        return dict(card=card, links=links)

    @expose('adventure.templates.widget')
    def grid(self):
        return dict(widget=CardGrid)

    @expose('adventure.templates.stats')
    def stats(self):
        cards = DBSession.query(Card.id).all()
        no_links = []
        no_backlinks = []
        for card_id in cards:
            links = DBSession.query(Link).filter_by(card_id=card_id).all()
            if len(links) == 0:
                no_links.append(card_id)
            backlinks = DBSession.query(Link).filter_by(card_id=new_card_id).all()
            if len(backlinks) == 0:
                no_lbackinks.append(card_id)
        return dict(linkless=no_links, backlinkless=no_back_links)

    @expose('adventure.templates.edit')
    def edit_card(self, **kw):
        """Creates new cards."""
        return dict(form=create_card_form())

    @expose('adventure.templates.edit')
    def edit_link(self, **kw):
        """Edit links between cards."""
        data = kw

        link = DBSession.query(Link).filter_by(card_id=kw['card_id']) \
                                   .filter_by(direction=kw['direction']).first()
        if link:
            form = edit_link_form
        else:
            form = create_link_form

        other_cards = DBSession.query(Card.id, Card.description).filter(Card.id != kw['card_id']).all()
        other_cards = map(lambda x: (x[0], '%d: %s' % (x[0], x[1])), other_cards)

        form = form(data, child_args=dict(new_card_id=dict(options=other_cards)))
        return dict(form=form)

    @expose()
    @validate(create_card_form, error_handler=edit_card)
    def save_new_card(self, **kw):
        card = Card()
        card.description = kw['description']
        card.special = kw['special']
        DBSession.add(card)
        DBSession.flush()

        base_dir = os.path.abspath(resource_filename('adventure', 'public'))
        path = os.path.join(base_dir, 'cards')
        try:
            os.makedirs(path)
        except OSError:
            #ignore if the folder already exists
            pass

        image_path = os.path.join(path, str(card.id))
        with open(image_path, "w") as f:
            f.write(kw['image'].value)

        flash("Card %d was successfully created." % card.id)
        redirect(url('/'))

    @expose()
    @validate(edit_link_form, error_handler=edit_link)
    def save_edited_link(self, **kw):
        #return str(kw)
        link = DBSession.query(Link).filter_by(card_id=kw['card_id']).filter_by(direction=kw['direction']).first()
        link.new_card_id = kw['new_card_id']
        DBSession.flush()
        self.reverse_link(kw)

        redirect(url('/'))

    @expose()
    @validate(create_link_form, error_handler=edit_link)
    def save_new_link(self, **kw):
        link = Link()
        link.card_id = kw['card_id']
        link.direction = kw['direction']
        link.new_card_id = kw['new_card_id']
        DBSession.add(link)
        self.reverse_link(kw)

        redirect(url('/game/?card_id=%s' % kw['new_card_id']))

    @expose('json')
    def jit_data(self, *args, **kw):
        return CardGrid.request(request).body

    def reverse_link(self, **kw):
        reversing = dict(right='left', left='right', back='center', center='back')
        if kw['reverse'] and kw['direction'] in reversing:
            back_direction = reversing[kw['direction']]

            olde_link = DBSession.query(Link).filter_by(new_card_id=kw['card_id']).filter_by(direction=back_direction).first()
            if olde_link:
                DBSession.delete(olde_link)

            back_link = DBSession.query(Link).filter_by(card_id=kw['new_card_id']).filter_by(direction=back_direction).first()
            if not back_link:
                back_link = Link()
                back_link.card_id = kw['new_card_id']
                back_link.direction = back_direction
                back_link.new_card_id = kw['card_id']
                DBSession.add(back_link)
            else:
                back_link.new_card_id = kw['card_id']
                DBSession.flush()
