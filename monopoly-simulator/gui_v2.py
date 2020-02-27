from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.bubble import BubbleButton, Bubble
from kivy.graphics.context_instructions import Color, PushMatrix, PopMatrix
from kivy.graphics import Rectangle, Rotate, Ellipse, InstructionGroup
from functools import partial
from kivy.core.window import Window, WindowBase
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from random import seed
from random import randint
import threading
import pandas as pd
import time
import os
import sys
import initialize_game_elements
from action_choices import roll_die
import numpy as np
from card_utility_actions import move_player_after_die_roll
from simple_decision_agent_1 import \
    decision_agent_methods  # this is where you should import your own decision agent methods dict
import json
import diagnostics
import subprocess
import initialize_game_elements
from action_choices import roll_die
import background_agent_v1
import simple_decision_agent_1
import sys
#sys.stdout = open('check_die_roll_0.txt','wt')
#from kivy.core.window import Window
#Window.clearcolor = [1,1,1,1]

np_seed=4

class CreateBoardWindow(Screen):
    board_id = ObjectProperty(None)
    prop_id = ObjectProperty(None)
    players = []

    def __init__(self, game_elem, **kwargs):
        super(CreateBoardWindow, self).__init__(**kwargs)
        self.game_elem = game_elem
        self.color_dict = {"Brown": [0.5859, 0.3, 0, 1], "SkyBlue": [0.68, 0.85, 0.90, 1],
                           "Orchid": [0.5, 0, 0.5, 1],
                           "Red": [1, 0, 0, 1], "Orange": [0.99, 0.64, 0, 1], "Yellow": [1, 1, 0, 1],
                           "Green": [0, 1, 0, 1],
                           "Blue": [0, 0, 1, 1], None: [0.96, 0.96, 0.86, 1]}
        self.obj_instr_directory = []
        self.dice_list = []
        self.start_stop_flag = False
        self.create_board()
        print("init")

    def board_layout_caculator(self, num_properties):
        each_side_num_props = (num_properties/4)
        each_block_width = (1 - 2*(0.11)-0.01)/(each_side_num_props+1)
        return (each_side_num_props, each_block_width)

    def create_board(self):
        each_side_number_of_props, each_block_size = self.board_layout_caculator(len(self.game_elem['location_sequence']))
        Monopoly_center_button = MonopolyButton(text="Play", background_color=self.color_dict[None])
        self.board_id.add_widget(Monopoly_center_button)
        Monopoly_center_button.bind(on_release=self.playing_the_game)
        pos_x = 0.9
        pos_y = 0.1
        i = 0
        for _ in range(each_side_number_of_props+1):
            i += 1
            pos_x -= each_block_size
            label = (self.game_elem['location_sequence'][i - 1].name).replace(' ', '\n')
            try:
                color_t = self.color_dict[str(self.game_elem['location_sequence'][i - 1].color)]
            except:
                color_t = self.color_dict[self.game_elem['location_sequence'][i - 1].color]
            property_button = PropertyButton(text=label,
                                             background_color=color_t,
                                             pos_hint={"x": pos_x, "y": pos_y}, size_hint=(each_block_size, each_block_size))
            self.board_id.add_widget(property_button)

        for _ in range(each_side_number_of_props+1, each_side_number_of_props+11):
            i += 1
            pos_y += each_block_size
            if self.game_elem['location_sequence'][i - 1].name == 'St. James Place':
                label = 'St.James\nPlace'
            elif self.game_elem['location_sequence'][i - 1].name == 'St. Charles Place':
                label = 'St.Charles\nPlace'
            elif self.game_elem['location_sequence'][i - 1].name == 'New York Avenue':
                label = 'NewYork\nAvenue'
            else:
                label = (self.game_elem['location_sequence'][i - 1].name).replace(' ', '\n')
            try:
                color_t = self.color_dict[str(self.game_elem['location_sequence'][i - 1].color)]
            except:
                color_t = self.color_dict[self.game_elem['location_sequence'][i - 1].color]
            property_button = PropertyButton(text=label,
                                             background_color=color_t,
                                             pos_hint={"x": pos_x, "y": pos_y}, size_hint=(each_block_size, each_block_size))
            self.board_id.add_widget(property_button)

        for _ in range(each_side_number_of_props+11, each_side_number_of_props+21):
            i += 1
            pos_x += each_block_size
            if self.game_elem['location_sequence'][i - 1].name == 'Go to Jail':
                label = 'Goto\nJail'
            else:
                label = (self.game_elem['location_sequence'][i - 1].name).replace(' ', '\n')
            try:
                color_t = self.color_dict[str(self.game_elem['location_sequence'][i - 1].color)]
            except:
                color_t = self.color_dict[self.game_elem['location_sequence'][i - 1].color]
            property_button = PropertyButton(text=label,
                                             background_color=color_t,
                                             pos_hint={"x": pos_x, "y": pos_y}, size_hint=(each_block_size, each_block_size))
            self.board_id.add_widget(property_button)

        for _ in range(each_side_number_of_props+21, each_side_number_of_props+30):
            i += 1
            pos_y -= each_block_size
            label = (self.game_elem['location_sequence'][i - 1].name).replace(' ', '\n')
            try:
                color_t = self.color_dict[str(self.game_elem['location_sequence'][i - 1].color)]
            except:
                color_t = self.color_dict[self.game_elem['location_sequence'][i - 1].color]
            property_button = PropertyButton(text=label,
                                             background_color=color_t,
                                             pos_hint={"x": pos_x, "y": pos_y}, size_hint=(each_block_size, each_block_size))
            self.board_id.add_widget(property_button)

        monopoly_display_button = Button(text="MONOPOLY\n PLAY-PAUSE",
                                            background_color=[0.96, 0.96, 0.86, 1],
                                            pos_hint= {"x": 0.48, "y": 0.48}, size_hint= (0.07, 0.07))
        self.board_id.add_widget(monopoly_display_button)
        monopoly_display_button.bind(on_release= self.toggle_button_func)

        self.goo_jail_chance_with_player = " "
        self.goo_jail_cc_with_player = " "

        get_out_of_jail_chestcard_button = Button(text="Community Chest Card" + \
                                                       self.goo_jail_cc_with_player,
                                                  background_color=[0.96, 0.96, 0.86, 1],
                                                  pos_hint={"x": 0.3, "top": 0.7},
                                                  size_hint=(0.12, 0.10))
        self.board_id.add_widget(get_out_of_jail_chestcard_button)

        get_out_of_jail_chancecard_button = Button(text="Chance Card" + \
                                                        self.goo_jail_chance_with_player,
                                                   background_color=[0.96, 0.96, 0.86, 1],
                                                   pos_hint={"x": 0.6, "top": 0.35},
                                                   size_hint=(0.12, 0.10))
        self.board_id.add_widget(get_out_of_jail_chancecard_button)

        self.goo_jail_list = []
        self.goo_jail_list.append(get_out_of_jail_chestcard_button)
        self.goo_jail_list.append(get_out_of_jail_chancecard_button)

        self.color_players_list = [[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1], [0.95, 0.95, 0, 1]]
        player_details_button_pos_y = 0.8
        self.player_detail_list = []
        for i in range(4):
            player_detail_button = Button(text=" ",
                                               background_color=self.color_players_list[i],
                                               pos_hint={"x": 0, "top": player_details_button_pos_y - i * 0.18},
                                               size_hint=(0.11, 0.16))
            self.board_id.add_widget(player_detail_button)
            self.player_detail_list.append(player_detail_button)

        player_details_heading_button = Button(text="Player details",
                                               background_color=[0.96, 0.96, 0.86, 1],
                                               pos_hint={"x": 0, "top": 0.87},
                                               size_hint=(0.11, 0.05))
        self.board_id.add_widget(player_details_heading_button)

        die_roll_heading_button = Button(text="Dice Roll",
                                         background_color=[0.96, 0.96, 0.86, 1],
                                         pos_hint={"x": 0.92, "top": 0.87},
                                         size_hint=(0.07, 0.05))
        self.board_id.add_widget(die_roll_heading_button)

        self.dice_holder_list = []
        for i in range(2):
            die_roll_num = Button(text=" ",
                                             background_color=[0.96, 0.96, 0.86, 1],
                                             pos_hint={"x": 0.93, "top": 0.87-(i+1)*0.10},
                                             size_hint=(0.05, 0.06))
            self.board_id.add_widget(die_roll_num)
            self.dice_holder_list.append(die_roll_num)

    def playing_the_game(self, *args):
        print("playing")
        self.start_stop_flag = True
        threading.Thread(target=self.simulate_game_instance).start()

    def toggle_button_func(self, *args):
        if self.start_stop_flag==False:
            self.start_stop_flag = True
        elif self.start_stop_flag==True:
            self.start_stop_flag = False
            print ('PAUSING THE GAME.... CLICK MONOPOLY BUTTON TO RESUME GAME')


    def simulate_game_instance(self):
        """
        Simulate a game instance.
        :param game_elements: The dict output by set_up_board
        :param np_seed: The numpy seed to use to control randomness.
        :return: None
        """
        np.random.seed(np_seed)
        np.random.shuffle(self.game_elem['players'])
        self.game_elem['seed'] = np_seed
        self.game_elem['card_seed'] = np_seed
        self.game_elem['choice_function'] = np.random.choice
        randstate1 = np.random.RandomState(seed=np_seed)
        randstate2 = np.random.RandomState(seed=np_seed)
        self.game_elem['chance_choice_function'] = randstate1.choice
        self.game_elem['cc_choice_function'] = randstate2.choice
        num_die_rolls = 0
        # game_elements['go_increment'] = 100 # we should not be modifying this here. It is only for testing purposes.
        # One reason to modify go_increment is if your decision agent is not aggressively trying to monopolize. Since go_increment
        # by default is 200 it can lead to runaway cash increases for simple agents like ours.

        print 'players will play in the following order: ','->'.join([p.player_name for p in self.game_elem['players']])
        print 'Beginning play. Rolling first die...'
        current_player_index = 0
        num_active_players = 4
        winner = None
        list_1 = []
        list_2 = []
        while num_active_players > 1:
            if self.start_stop_flag==True:
                current_player = self.game_elem['players'][current_player_index]
                while current_player.status == 'lost':
                    current_player_index += 1
                    current_player_index = current_player_index % len(self.game_elem['players'])
                    current_player = self.game_elem['players'][current_player_index]
                current_player.status = 'current_move'

                # pre-roll for current player + out-of-turn moves for everybody else,
                # till we get num_active_players skip turns in a row.

                skip_turn = 0
                if current_player.make_pre_roll_moves(self.game_elem) == 2: # 2 is the special skip-turn code
                    skip_turn += 1
                out_of_turn_player_index = current_player_index + 1
                out_of_turn_count = 0
                while skip_turn != num_active_players and out_of_turn_count<=200:
                    out_of_turn_count += 1
                    # print 'checkpoint 1'
                    out_of_turn_player = self.game_elem['players'][out_of_turn_player_index%len(self.game_elem['players'])]
                    if out_of_turn_player.status == 'lost':
                        out_of_turn_player_index += 1
                        continue
                    oot_code = out_of_turn_player.make_out_of_turn_moves(self.game_elem)
                    # add to game history
                    self.game_elem['history']['function'].append(out_of_turn_player.make_out_of_turn_moves)
                    params = dict()
                    params['self']=out_of_turn_player
                    params['current_gameboard']=self.game_elem
                    self.game_elem['history']['param'].append(params)
                    self.game_elem['history']['return'].append(oot_code)

                    if  oot_code == 2:
                        skip_turn += 1
                    else:
                        skip_turn = 0
                    out_of_turn_player_index += 1

                # now we roll the dice and get into the post_roll phase,
                # but only if we're not in jail.


                r = roll_die(self.game_elem['dies'], np.random.choice)
                list_1.append(r[0])
                list_2.append(r[1])
                self.dice_list = r
                # add to game history
                self.game_elem['history']['function'].append(roll_die)
                params = dict()
                params['die_objects'] = self.game_elem['dies']
                params['choice'] = np.random.choice
                self.game_elem['history']['param'].append(params)
                self.game_elem['history']['return'].append(r)

                num_die_rolls += 1
                self.game_elem['current_die_total'] = sum(r)
                print 'dies have come up ',str(r)
                if not current_player.currently_in_jail:
                    check_for_go = True
                    move_player_after_die_roll(current_player, sum(r), self.game_elem, check_for_go)
                    # add to game history
                    self.game_elem['history']['function'].append(move_player_after_die_roll)
                    params = dict()
                    params['player'] = current_player
                    params['rel_move'] = sum(r)
                    params['current_gameboard'] = self.game_elem
                    params['check_for_go'] = check_for_go
                    self.game_elem['history']['param'].append(params)
                    self.game_elem['history']['return'].append(None)

                    current_player.process_move_consequences(self.game_elem)
                    # add to game history
                    self.game_elem['history']['function'].append(current_player.process_move_consequences)
                    params = dict()
                    params['self'] = current_player
                    params['current_gameboard'] = self.game_elem
                    self.game_elem['history']['param'].append(params)
                    self.game_elem['history']['return'].append(None)

                    # post-roll for current player. No out-of-turn moves allowed at this point.
                    current_player.make_post_roll_moves(self.game_elem)
                    # add to game history
                    self.game_elem['history']['function'].append(current_player.make_post_roll_moves)
                    params = dict()
                    params['self'] = current_player
                    params['current_gameboard'] = self.game_elem
                    self.game_elem['history']['param'].append(params)
                    self.game_elem['history']['return'].append(None)

                else:
                    current_player.currently_in_jail = False # the player is only allowed to skip one turn (i.e. this one)

                if current_player.current_cash < 0:
                    code = current_player.handle_negative_cash_balance(current_player, self.game_elem)
                    # add to game history
                    self.game_elem['history']['function'].append(current_player.handle_negative_cash_balance)
                    params = dict()
                    params['player'] = current_player
                    params['current_gameboard'] = self.game_elem
                    self.game_elem['history']['param'].append(params)
                    self.game_elem['history']['return'].append(code)
                    if code == -1 or current_player.current_cash < 0:
                        current_player.begin_bankruptcy_proceedings(self.game_elem)
                        # add to game history
                        self.game_elem['history']['function'].append(current_player.begin_bankruptcy_proceedings)
                        params = dict()
                        params['self'] = current_player
                        params['current_gameboard'] = self.game_elem
                        self.game_elem['history']['param'].append(params)
                        self.game_elem['history']['return'].append(None)

                        num_active_players -= 1
                        diagnostics.print_asset_owners(self.game_elem)
                        diagnostics.print_player_cash_balances(self.game_elem)

                        if num_active_players == 1:
                            for p in self.game_elem['players']:
                                if p.status != 'lost':
                                    winner = p
                                    p.status = 'won'
                else:
                    current_player.status = 'waiting_for_move'

                current_player_index = (current_player_index+1)%len(self.game_elem['players'])

                time.sleep(0.1)
                self.update_board()

                if diagnostics.max_cash_balance(self.game_elem) > 300000: # this is our limit for runaway cash for testing purposes only.
                                                                         # We print some diagnostics and return if any player exceeds this.
                    diagnostics.print_asset_owners(self.game_elem)
                    diagnostics.print_player_cash_balances(self.game_elem)
                    return
        '''
        df = pd.DataFrame(list(zip(list_1, list_2)), columns=['die1', 'die2'])
        csv_name = "check_die_roll_0.csv"
        df.to_csv(csv_name)
        '''
        # let's print some numbers
        print 'printing final asset owners: '
        diagnostics.print_asset_owners(self.game_elem)
        print 'number of dice rolls: ',str(num_die_rolls)
        print 'printing final cash balances: '
        diagnostics.print_player_cash_balances(self.game_elem)

        if winner:
            print 'We have a winner: ', winner.player_name
            #winner_list.append(winner.player_name)
        return



    def update_board(self):
        self.canvas.after.clear()
        self.players = []
        pos_x = 0.85
        pos_y = 0.11
        self.color_players_list = [[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1], [1, 1, 0, 1]]
        self.pos_x_list = []
        self.pos_y_list = []

        for i in range(len(self.dice_holder_list)):
            self.dice_holder_list[i].text = str(self.dice_list[i])
        '''
        for i in range(4):
            if self.game_elem['players'][i].has_get_out_of_jail_chance_card == True:
                self.goo_jail_chance_with_player = "is with " + str(self.game_elem['players'][i].player_name)
                break
            else:
                self.goo_jail_chance_with_player = "Inside the deck"
        
        for i in range(4):
            if self.game_elem['players'][i].has_get_out_of_jail_community_chest_card == True:
                self.goo_jail_cc_with_player = "is with " + str(self.game_elem['players'][i].player_name)
                break
            else:
                self.goo_jail_cc_with_player = "Inside the deck"

        self.goo_jail_list[0].text = "Community Chest Card \nGet out of jail card \n" + self.goo_jail_cc_with_player
        self.goo_jail_list[1].text = "Chance Card \nGet out of jail card \n" + self.goo_jail_chance_with_player
        '''

        for i in range(4):
            text_on_button = " "  + self.game_elem['players'][i].player_name + \
                            "\n Current Cash = " + str(self.game_elem['players'][i].current_cash) + \
                            "\n # of houses = " + str(self.game_elem['players'][i].num_total_houses) + \
                             "\n # of hotels = " + str(self.game_elem['players'][i].num_total_hotels)
            if self.game_elem['players'][i].has_get_out_of_jail_community_chest_card == True:
                text_on_button = text_on_button + "\nGOO_Jail community card"
            if self.game_elem['players'][i].has_get_out_of_jail_chance_card == True:
                text_on_button = text_on_button + "\nGOO_Jail chance card"

            self.player_detail_list[i].text = text_on_button
            self.obj_instr_player = InstructionGroup()
            self.obj_instr_player.add(
                Color(self.color_players_list[i][0], self.color_players_list[i][1], self.color_players_list[i][2],
                      self.color_players_list[i][3]))
            try:
                pos_x_n = self.game_elem['players'][i].current_position / 10
                pos_y_n = self.game_elem['players'][i].current_position % 10
            except:
                pos_x_n = 0
                pos_y_n = 0

            if (pos_x_n == 0):
                pos_x = 0.85 - (pos_y_n * 0.07)
                pos_y = 0.11
            elif (pos_x_n == 2):
                pos_x = 0.85 - (10 * (0.07)) + (pos_y_n * 0.07)
                pos_y = 0.11 + (10 * 0.07)
            elif (pos_x_n == 1):
                pos_x = 0.85 - (10 * (0.07))
                pos_y = 0.11 + (pos_y_n * 0.07)
            elif (pos_x_n == 3):
                pos_x = 0.85
                pos_y = 0.11 + (10 * 0.07) - (pos_y_n * 0.07)

            self.obj_instr_player.add(
                Ellipse(pos=((pos_x + i * 0.01) * Window.width, pos_y * Window.height), size=(10, 10)))
            self.players.append(self.obj_instr_player)
            self.pos_x_list.append(pos_x)
            self.pos_y_list.append(pos_y)
            self.canvas.after.add(self.obj_instr_player)

            count_house = 0
            count_hotel = 0
            if (self.game_elem['players'][i].assets) != None:
                self.player_props = []
                self.player_props_x = []
                self.player_props_y = []

                for k in range(len(list(self.game_elem['players'][i].assets))):
                    prop_name = list(self.game_elem['players'][i].assets)[k].name
                    pos_prop = self.game_elem['location_objects'][prop_name].start_position

                    self.obj_instr = InstructionGroup()
                    self.obj_instr.add(Color(self.color_players_list[i][0], self.color_players_list[i][1],
                                             self.color_players_list[i][2],
                                             self.color_players_list[i][3]))
                    prop_x = pos_prop / 10
                    prop_y = pos_prop % 10
                    pos_x_prop = 0
                    pos_y_prop = 0
                    if (prop_x == 0):
                        pos_x_prop = 0.835 - (prop_y * 0.07)
                        pos_y_prop = 0.14
                    elif (prop_x == 2):
                        pos_x_prop = 0.835 - (10 * (0.07)) + (prop_y * 0.07)
                        pos_y_prop = 0.14 + (10 * 0.07)
                    elif (prop_x == 1):
                        pos_x_prop = 0.835 - (10 * (0.07))
                        pos_y_prop = 0.14 + (prop_y * 0.07)
                    elif (prop_x == 3):
                        pos_x_prop = 0.835
                        pos_y_prop = 0.14 + (10 * 0.07) - (prop_y * 0.07)
                    self.obj_instr.add(Rectangle(pos=(pos_x_prop * Window.width, pos_y_prop * Window.height),
                                                 size=(12, 12)))

                    if list(self.game_elem['players'][i].assets)[k].loc_class=='real_estate':
                        if list(self.game_elem['players'][i].assets)[k].num_houses>0:
                            for m in range(list(self.game_elem['players'][i].assets)[k].num_houses):
                                self.obj_instr.add(Color(1,1,1,1))
                                self.obj_instr.add(Ellipse(pos=((pos_x_prop + (m+1)*0.01) * Window.width, pos_y_prop * Window.height),
                                                             size=(12, 12)))
                                count_house+=list(self.game_elem['players'][i].assets)[k].num_houses

                        if list(self.game_elem['players'][i].assets)[k].num_hotels>0:
                            for m in range(list(self.game_elem['players'][i].assets)[k].num_hotels):
                                self.obj_instr.add(Color(1,0.1,0.5,1))
                                self.obj_instr.add(Ellipse(pos=((pos_x_prop + (m+1)*0.01) * Window.width, pos_y_prop * Window.height),
                                                             size=(12, 12)))
                                count_hotel += list(self.game_elem['players'][i].assets)[k].num_hotels

                    self.player_props.append(self.obj_instr)
                    self.player_props_x.append(pos_x_prop)
                    self.player_props_y.append(pos_y_prop)
                    self.canvas.after.add(self.obj_instr)
                    self.obj_instr_directory.append(self.obj_instr)
            self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.players[0].pos = (self.pos_x_list[0] * Window.width, self.pos_y_list[0] * Window.height)
        self.players[1].pos = ((self.pos_x_list[1] + 0.01) * Window.width, self.pos_y_list[0] * Window.height)
        self.players[2].pos = ((self.pos_x_list[2] + 0.02) * Window.width, self.pos_y_list[1] * Window.height)
        self.players[3].pos = ((self.pos_x_list[3] + 0.03) * Window.width, self.pos_y_list[3] * Window.height)
        for i in range(len(self.player_props)):
            self.player_props[i].children[2].pos = (
                self.player_props_x[i] * Window.width, self.player_props_y[i] * Window.height)

    def popup_window(self, property_name):
        show = P()
        property_name_mod = property_name.replace("\n", " ")
        str_prop = "Name of the property: " + property_name_mod
        '''
        if self.game_elem['location_objects'][str(property_name_mod)].color == None:
            pass
        elif self.game_elem['location_objects'][str(property_name_mod)].color != None:
            pass
        '''
        if self.game_elem['location_objects'][str(property_name_mod)].loc_class == 'real_estate':
            str_prop = str_prop + "\nCost: $" + str(self.game_elem['location_objects'][str(property_name_mod)].price) + \
                       "\nRent: $" + str(self.game_elem['location_objects'][str(property_name_mod)].rent) + \
                       "\nRent with 1 house: $" + str(
                self.game_elem['location_objects'][str(property_name_mod)].rent_1_house) + \
                       "\nRent with 2 house: $" + str(
                self.game_elem['location_objects'][str(property_name_mod)].rent_2_houses) + \
                       "\nRent with 3 house: $" + str(
                self.game_elem['location_objects'][str(property_name_mod)].rent_3_houses) + \
                       "\nRent with 4 house: $" + str(
                self.game_elem['location_objects'][str(property_name_mod)].rent_4_houses) + \
                       "\nRent with a hotel: $" + str(
                self.game_elem['location_objects'][str(property_name_mod)].rent_hotel) + \
                       "\nMortgage: $" + str(self.game_elem['location_objects'][str(property_name_mod)].mortgage) + \
                       "\nHouse cost: $" + str(
                self.game_elem['location_objects'][str(property_name_mod)].price_per_house)

        elif self.game_elem['location_objects'][str(property_name_mod)].loc_class == 'tax':
            str_prop = str_prop + "Pay as TAX $" + str(
                self.game_elem['location_objects'][str(property_name_mod)].amount_due)

        elif self.game_elem['location_objects'][str(property_name_mod)].loc_class == 'railroad':
            str_prop = str_prop + "\nCost: $" + str(self.game_elem['location_objects'][str(property_name_mod)].price) + \
                       "\nMortgage: $" + str(self.game_elem['location_objects'][str(property_name_mod)].mortgage)

        elif self.game_elem['location_objects'][str(property_name_mod)].loc_class == 'utility':
            str_prop = str_prop + "\nCost: $" + str(self.game_elem['location_objects'][str(property_name_mod)].price) + \
                       "\nMortgage: $" + str(self.game_elem['location_objects'][str(property_name_mod)].mortgage) + \
                       "\n\nIf one UTILITY is owned, rent is 4 times\n amount shown on dice." + \
                       "\nIf both utilities are owned, rent is 10 times\n amount shown on dice."

        elif self.game_elem['location_objects'][str(property_name_mod)].loc_class == 'action':
            str_prop = "Pick a " + property_name_mod + " Card"

        elif self.game_elem['location_objects'][str(property_name_mod)].loc_class == 'do_nothing':
            pass

        show.ids.popup_id.text = str_prop
        popup_window = Popup(title=property_name_mod, content=show, size_hint=(None, None), size=(400, 400))
        popup_window.open()


class P(FloatLayout):
    pass


class MonopolyButton(Button):
    pass


class PropertyLabel(Label):
    pass


class WindowManager(ScreenManager):
    pass


class PropertyButton(Button):
    pass


class PlayerWidget(Ellipse):
    pass


class MyMainApp(App):

    def __init__(self, game_elem):
        super(MyMainApp, self).__init__()
        self.game_elem = game_elem

    def build(self):
        print('Game Visualization being rendered')
        sm = self.run_func()

        return sm

    def run_func(self):
        Builder.load_file("my.kv")
        sm = WindowManager()
        screens = [CreateBoardWindow(self.game_elem)]
        for screen in screens:
            sm.add_widget(screen)
        self.screen = screens[0]
        sm.current = "GameBoard"
        return sm


def set_up_board(game_schema_file_path, player_decision_agents):
    game_schema = json.load(open(game_schema_file_path, 'r'))
    return initialize_game_elements.initialize_board(game_schema, player_decision_agents)


# this is where everything begins. Assign decision agents to your players, set up the board and start simulating! You can
# control any number of players you like, and assign the rest to the simple agent. We plan to release a more sophisticated
# but still relatively simple agent soon.
player_decision_agents = dict()
# for p in ['player_1','player_3']:
#     player_decision_agents[p] = simple_decision_agent_1.decision_agent_methods
player_decision_agents['player_1'] = background_agent_v1.decision_agent_methods
player_decision_agents['player_2'] = background_agent_v1.decision_agent_methods
player_decision_agents['player_3'] = background_agent_v1.decision_agent_methods
player_decision_agents['player_4'] = background_agent_v1.decision_agent_methods
game_elements = set_up_board('../monopoly_game_schema_v1-2.json',
                             player_decision_agents)
MyMainApp(game_elements).run()

#just testing history.
# print len(game_elements['history']['function'])
# print len(game_elements['history']['param'])
# print len(game_elements['history']['return'])


