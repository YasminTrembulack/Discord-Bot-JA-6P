# Overview

A Discord bot for managing reservations through a calendar interface. The bot allows users to view available dates and book time slots through interactive Discord buttons and embeds. Currently in early development with basic calendar display functionality implemented.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Bot Framework
- Built using discord.py library with commands extension
- Uses Discord's slash commands and button interactions for user interface
- Modular architecture with cogs system for organizing functionality

## Command Structure
- Prefix-based commands (!) for triggering bot actions
- Calendar cog handles all reservation-related functionality
- Interactive UI using Discord's View and Button components

## Data Storage
- Currently uses in-memory storage for reservations
- Data structure: nested dictionaries mapping dates to time slots and user IDs
- Format: `{ "DD/MM/YYYY": { "08:00": user_id, ... } }`
- Designed for future database integration

## User Interface Design
- 7-day rolling calendar view using Discord embeds
- Interactive buttons for date and time selection
- Two-step booking process: date selection followed by time selection
- Visual feedback through Discord's button styling and embed colors

## Event Handling
- Asynchronous event-driven architecture
- Bot ready event for startup confirmation
- Button callback functions for user interactions

# External Dependencies

## Discord API
- discord.py library for bot functionality
- Requires Discord bot token for authentication
- Uses Discord's Intents system for message content access

## Python Libraries
- datetime module for date and time calculations
- timedelta for date arithmetic and calendar generation

## Future Integrations
- Database system planned for persistent reservation storage
- Potential webhook integrations for external calendar systems



https://chatgpt.com/share/68ba2b11-dd74-8001-a2c7-cf585af66e82
https://chatgpt.com/share/68ba2b33-86a0-8001-bbbb-f2ed7c33946f