"""Profiler"""
import cProfile
import bot

prof = cProfile.run("bot.main()", 'stats')

prof.print_stats()
