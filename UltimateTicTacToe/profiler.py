"""Profiler"""
import cProfile
import new_bot as bot

cProfile.run("bot.main()", 'stats')

