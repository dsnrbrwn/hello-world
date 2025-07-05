"""
Mobile version of Death Game Simulator using Kivy
This version shares the same game logic as the desktop version
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
import math

# Import shared game logic
from game.core_game import GameState

class GameWidget(Widget):
    """Widget that handles the game rendering and touch controls"""
    
    def __init__(self, game_state, **kwargs):
        super().__init__(**kwargs)
        self.game_state = game_state
        self.bind(size=self.update_graphics)
        self.bind(pos=self.update_graphics)
        
        # Touch controls
        self.touch_start = None
        self.is_touching = False
        
    def update_graphics(self, *args):
        """Update graphics when widget size changes"""
        self.canvas.clear()
        with self.canvas:
            # Background
            Color(0.1, 0.1, 0.1, 1)  # Dark gray background
            Rectangle(pos=self.pos, size=self.size)
            
            # Player
            if self.game_state.player_alive:
                # Player color based on health
                if self.game_state.player_health > 70:
                    Color(0, 1, 0, 1)  # Green
                elif self.game_state.player_health > 40:
                    Color(1, 1, 0, 1)  # Yellow
                elif self.game_state.player_health > 20:
                    Color(1, 0.65, 0, 1)  # Orange
                else:
                    Color(1, 0, 0, 1)  # Red
                
                # Scale player position to widget size
                player_x = (self.game_state.player_x / 1024) * self.width + self.x
                player_y = (self.game_state.player_y / 768) * self.height + self.y
                
                Ellipse(pos=(player_x - 15, player_y - 15), size=(30, 30))
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.touch_start = touch.pos
            self.is_touching = True
            return True
        return False
    
    def on_touch_move(self, touch):
        if self.is_touching and self.touch_start:
            # Calculate movement direction
            dx = touch.pos[0] - self.touch_start[0]
            dy = touch.pos[1] - self.touch_start[1]
            
            # Normalize movement (limit speed)
            distance = math.sqrt(dx**2 + dy**2)
            if distance > 0:
                # Scale movement
                move_speed = 3
                dx = (dx / distance) * move_speed
                dy = (dy / distance) * move_speed
                
                # Convert screen coordinates to game coordinates
                game_dx = (dx / self.width) * 1024
                game_dy = -(dy / self.height) * 768  # Flip Y axis
                
                self.game_state.move_player(game_dx, game_dy)
                self.update_graphics()
            
            return True
        return False
    
    def on_touch_up(self, touch):
        if self.is_touching:
            self.is_touching = False
            self.touch_start = None
            return True
        return False

class GameScreen(Screen):
    """Main game screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_state = GameState()
        self.build_ui()
        
        # Start game loop
        Clock.schedule_interval(self.update_game, 1.0/60.0)
    
    def build_ui(self):
        """Build the game UI"""
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Top status bar
        status_layout = BoxLayout(orientation='horizontal', size_hint_y=0.15)
        
        # Health bar
        health_layout = BoxLayout(orientation='vertical', size_hint_x=0.25)
        health_layout.add_widget(Label(text='Health', size_hint_y=0.3))
        self.health_bar = ProgressBar(max=100, value=100, size_hint_y=0.7)
        health_layout.add_widget(self.health_bar)
        
        # Day counter
        day_layout = BoxLayout(orientation='vertical', size_hint_x=0.25)
        day_layout.add_widget(Label(text='Day', size_hint_y=0.3))
        self.day_label = Label(text='1', size_hint_y=0.7)
        day_layout.add_widget(self.day_label)
        
        # Progress bar
        progress_layout = BoxLayout(orientation='vertical', size_hint_x=0.5)
        progress_layout.add_widget(Label(text='Journey Progress', size_hint_y=0.3))
        self.progress_bar = ProgressBar(max=100, value=0, size_hint_y=0.7)
        progress_layout.add_widget(self.progress_bar)
        
        status_layout.add_widget(health_layout)
        status_layout.add_widget(day_layout)
        status_layout.add_widget(progress_layout)
        
        # Game area
        self.game_widget = GameWidget(self.game_state, size_hint_y=0.6)
        
        # Resources display
        resources_layout = BoxLayout(orientation='horizontal', size_hint_y=0.15)
        self.food_label = Label(text='Food: 50')
        self.water_label = Label(text='Water: 30')
        self.medicine_label = Label(text='Medicine: 10')
        self.fuel_label = Label(text='Fuel: 20')
        
        resources_layout.add_widget(self.food_label)
        resources_layout.add_widget(self.water_label)
        resources_layout.add_widget(self.medicine_label)
        resources_layout.add_widget(self.fuel_label)
        
        # Control buttons
        controls_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        
        menu_btn = Button(text='Menu', size_hint_x=0.5)
        menu_btn.bind(on_press=self.show_menu)
        
        rest_btn = Button(text='Rest', size_hint_x=0.5)
        rest_btn.bind(on_press=self.rest_player)
        
        controls_layout.add_widget(menu_btn)
        controls_layout.add_widget(rest_btn)
        
        # Add all layouts to main
        main_layout.add_widget(status_layout)
        main_layout.add_widget(self.game_widget)
        main_layout.add_widget(resources_layout)
        main_layout.add_widget(controls_layout)
        
        self.add_widget(main_layout)
    
    def update_game(self, dt):
        """Update game state and UI"""
        self.game_state.update(dt)
        
        # Update UI elements
        status = self.game_state.get_status()
        
        self.health_bar.value = status['health']
        self.day_label.text = str(status['day'])
        self.progress_bar.value = status['progress']
        
        self.food_label.text = f"Food: {status['food']}"
        self.water_label.text = f"Water: {status['water']}"
        self.medicine_label.text = f"Medicine: {status['medicine']}"
        self.fuel_label.text = f"Fuel: {status['fuel']}"
        
        # Update game widget graphics
        self.game_widget.update_graphics()
        
        # Check for events
        if status['current_event']:
            self.show_event_popup(status['current_event'])
        
        # Check for game over
        if status['game_over']:
            if status['victory']:
                self.show_victory_popup()
            else:
                self.show_game_over_popup()
    
    def show_event_popup(self, event):
        """Show event popup with choices"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Event title and description
        title_label = Label(text=event['title'], size_hint_y=0.2)
        desc_label = Label(text=event['description'], size_hint_y=0.3)
        
        content.add_widget(title_label)
        content.add_widget(desc_label)
        
        # Choice buttons
        choices_layout = BoxLayout(orientation='vertical', size_hint_y=0.5)
        
        for choice in event['choices']:
            btn = Button(text=choice['text'], size_hint_y=0.33)
            btn.bind(on_press=lambda x, choice_id=choice['id']: self.handle_event_choice(choice_id))
            choices_layout.add_widget(btn)
        
        content.add_widget(choices_layout)
        
        # Create popup
        popup = Popup(title='Event!', content=content, size_hint=(0.8, 0.6))
        popup.open()
        
        # Store popup reference to close it later
        self.event_popup = popup
    
    def handle_event_choice(self, choice_id):
        """Handle event choice and close popup"""
        self.game_state.handle_event_choice(choice_id)
        if hasattr(self, 'event_popup'):
            self.event_popup.dismiss()
    
    def show_menu(self, instance):
        """Show menu popup"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        restart_btn = Button(text='Restart Game', size_hint_y=0.5)
        restart_btn.bind(on_press=self.restart_game)
        
        close_btn = Button(text='Close', size_hint_y=0.5)
        close_btn.bind(on_press=lambda x: popup.dismiss())
        
        content.add_widget(restart_btn)
        content.add_widget(close_btn)
        
        popup = Popup(title='Menu', content=content, size_hint=(0.6, 0.4))
        popup.open()
    
    def rest_player(self, instance):
        """Rest to restore stamina"""
        self.game_state.player_stamina = min(100, self.game_state.player_stamina + 20)
        self.game_state.advance_day()  # Resting advances time
    
    def restart_game(self, instance):
        """Restart the game"""
        self.game_state.reset_game()
    
    def show_victory_popup(self):
        """Show victory popup"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        msg = Label(text=f'Victory! You survived {self.game_state.day} days and reached safety!', 
                   size_hint_y=0.7)
        restart_btn = Button(text='Play Again', size_hint_y=0.3)
        restart_btn.bind(on_press=self.restart_game)
        
        content.add_widget(msg)
        content.add_widget(restart_btn)
        
        popup = Popup(title='Victory!', content=content, size_hint=(0.8, 0.5))
        popup.open()
    
    def show_game_over_popup(self):
        """Show game over popup"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        msg = Label(text=f'Game Over! You survived {self.game_state.day} days.', 
                   size_hint_y=0.7)
        restart_btn = Button(text='Try Again', size_hint_y=0.3)
        restart_btn.bind(on_press=self.restart_game)
        
        content.add_widget(msg)
        content.add_widget(restart_btn)
        
        popup = Popup(title='Game Over', content=content, size_hint=(0.8, 0.5))
        popup.open()

class MenuScreen(Screen):
    """Main menu screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """Build menu UI"""
        layout = AnchorLayout(anchor_x='center', anchor_y='center')
        
        menu_layout = BoxLayout(orientation='vertical', size_hint=(0.8, 0.6), spacing=20)
        
        # Title
        title = Label(text='DEATH GAME SIMULATOR', font_size=30, size_hint_y=0.3)
        
        # Start button
        start_btn = Button(text='Start Journey', size_hint_y=0.2)
        start_btn.bind(on_press=self.start_game)
        
        # Instructions
        instructions = Label(
            text='Drag to move your character\nSurvive the journey to safety\nManage your resources carefully',
            size_hint_y=0.3,
            text_size=(None, None)
        )
        
        # Exit button
        exit_btn = Button(text='Exit', size_hint_y=0.2)
        exit_btn.bind(on_press=self.exit_game)
        
        menu_layout.add_widget(title)
        menu_layout.add_widget(start_btn)
        menu_layout.add_widget(instructions)
        menu_layout.add_widget(exit_btn)
        
        layout.add_widget(menu_layout)
        self.add_widget(layout)
    
    def start_game(self, instance):
        """Switch to game screen"""
        self.manager.current = 'game'
    
    def exit_game(self, instance):
        """Exit the app"""
        App.get_running_app().stop()

class DeathGameMobileApp(App):
    """Main Kivy app"""
    
    def build(self):
        """Build the app"""
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        
        return sm

if __name__ == '__main__':
    DeathGameMobileApp().run()