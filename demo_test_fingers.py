from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.core.window import Window
from kivy.clock import Clock

from kivy.uix.label import Label

import math
import random
import csv
from datetime import datetime

import getfingers


class ForceIndicator(Widget):
    mvc = NumericProperty(0)

    def move(self, force, digit, left_mode):
        window_width, window_height = Window.size
        self.center_y = window_height * (force / 1024)
        if left_mode == True and digit == 0:
            self.x = 350 - (50 * digit)
        else:
            self.x = 100 + (50 * digit)


class MaxIndicator(ForceIndicator):
    pass


class TargetIndicator(Widget):

    def move(self, force, digit, left_mode):
        window_width, window_height = Window.size
        self.center_y = window_height * (force / 1024)
        if left_mode == True and digit == 0:
            self.x = 350 - (50 * digit)
        else:
            self.x = 100 + (50 * digit)


class ForceGame(Widget):
    left_mode = False
    time = NumericProperty(0)
    phase_time = NumericProperty(0)

    digit0 = ObjectProperty(None)
    digit1 = ObjectProperty(None)
    digit2 = ObjectProperty(None)
    digit3 = ObjectProperty(None)
    digit4 = ObjectProperty(None)

    max0 = ObjectProperty(None)
    max1 = ObjectProperty(None)
    max2 = ObjectProperty(None)
    max3 = ObjectProperty(None)
    max4 = ObjectProperty(None)

    target_ind = ObjectProperty(None)

    instruction = ObjectProperty('Relax your hand')

    digit = -1
    pause_flag = False
    mvc = [1] * 5
    mins = [0] * 5
    timelog = []
    forcelog = []
    digitlog = []
    targetlog = []
    mvctarget=0

    getfingers.init()

    def update(self, dt):
        self.time += dt
        self.timelog.append(self.time)
        self.digitlog.append(self.digit)
        self.targetlog.append(self.mvctarget)

        # forces = [int((math.sin(self.time) + 1) * 512)] * 5  # Replace this bit to get force
        forces = getfingers.getforces()

        self.forcelog.append(forces)
        # Get the minimum forces recorded (baseline relaxed hand state)
        if self.time < 10:
            forces = [0] * 5  # Remove this
            self.mins = list(map(min, forces, self.mins))
            self.digit0.move(forces[0], 0, self.left_mode)
            self.digit1.move(forces[1], 1, self.left_mode)
            self.digit2.move(forces[2], 2, self.left_mode)
            self.digit3.move(forces[3], 3, self.left_mode)
            self.digit4.move(forces[4], 4, self.left_mode)

        # Get MVCs
        if 10 < self.time < 70:
            self.instruction = 'PUSH PUSH PUSH'
            self.mvc = list(map(max, forces, self.mvc))
            self.max0.move(self.mvc[0], 0, self.left_mode)
            self.max1.move(self.mvc[1], 1, self.left_mode)
            self.max2.move(self.mvc[2], 2, self.left_mode)
            self.max3.move(self.mvc[3], 3, self.left_mode)
            self.max4.move(self.mvc[4], 4, self.left_mode)

        # Perform task
        if 70 < self.time < 900:  # Edit this to increase experiment duration to match needs
            self.instruction = 'Push your finger to \n match the target'
            self.phase_time += dt
            # Hide the indicator for n seconds, show for m seconds
            if self.pause_flag:
                if self.phase_time > 2:
                    self.phase_time = 0
                    self.target_ind.height = 25
                    digit = random.randint(0, 4)
                    self.mvc_target = random.randrange(self.mins[digit], self.mvc[digit])
                    self.target_ind.move(self.mvc_target, digit, self.left_mode)
                    self.pause_flag = False
            else:
                if self.phase_time > 10:
                    self.digit = -1
                    self.phase_time = 0
                    self.target_ind.height = 0
                    self.pause_flag = True
            # Move the graphics
            self.digit0.move(forces[0], 0, self.left_mode)
            self.digit1.move(forces[1], 1, self.left_mode)
            self.digit2.move(forces[2], 2, self.left_mode)
            self.digit3.move(forces[3], 3, self.left_mode)
            self.digit4.move(forces[4], 4, self.left_mode)

        if self.time > 900:
            with open('{}.txt'.format(datetime.now()), mode='w') as f:
                writer = csv.writer(f)
                writer.writerow(self.mins)
                writer.writerow(self.mvc)
                for k, v in enumerate(self.timelog):
                    writer.writerow(self.digitlog[k] + self.targetlog[k] + self.timelog[k] + self.forcelog[k])
            Clock.unschedule(print)
            quit()


class ForceApp(App):
    def build(self):
        game = ForceGame()

        Clock.schedule_interval(game.update, 1.0 / 100.0)
        return game


if __name__ == '__main__':
    ForceApp().run()
