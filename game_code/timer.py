# Copyright (c) 2025 Your Name
# Licensed under the AGPLv3 License. See LICENSE file for details.
#
# This project is based on a tutorial (link: https://www.youtube.com/watch?v=T4IX36sP_0c).
# You can redistribute and/or modify it under the terms of the AGPLv3.
#
# This software comes with no warranty. See the LICENSE file for more information.

import pygame

class Timer:
	def __init__(self, duration, func=None):
		self.duration = duration
		self.func = func
		self.start_time = 0
		self.active = False
		self.complete = False

	def activate(self):
		self.active = True
		self.start_time = pygame.time.get_ticks()

	def deactivate(self):
		self.active = False
		self.start_time = 0
		self.complete = True

	def update(self):
		current_time = pygame.time.get_ticks()
		if current_time - self.start_time >= self.duration:
			if self.func and self.start_time != 0:
				self.func()
			self.deactivate()
