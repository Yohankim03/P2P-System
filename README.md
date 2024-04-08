# Peer-to-Peer Messaging System

## Description

This project implements a simple Peer-to-Peer (P2P) messaging system using Python. It facilitates user registration with a central discovery server, allows users to find other users, and supports direct P2P messaging between them without the need for message routing through a central server. The system utilizes SQLite for local storage of user profiles and message history, enhancing privacy and scalability.

## Features

- User registration and discovery through a central server.
- Direct P2P messaging between users.
- Local storage of user profiles and message history using SQLite.
- Command-line interface for easy interaction.

## Requirements

- Python 3.6 or higher
- SQLite3 (typically included with Python)

## Installation

To set up the project locally, clone the repository:
git clone https://github.com/Yohankim03/P2P-System

cd P2P-System


## Setup

1. **Initialize the Database**: First, initialize the database to set up the necessary tables in SQLite.

    ```bash
    python database.py
    ```

2. **Start the Discovery Server**: Launch the server script to listen for registration and lookup requests from clients.

    ```bash
    python discovery.py
    ```

3. **Run the Client Application**: Open a new terminal window and start the client application. You will be prompted to specify a listening port and your username.

    ```bash
    python client.py
    ```

## Usage

After launching the client application, the following commands are available:

- **Register**: This is done automatically upon starting the client.
- **Lookup User**: To find another user's IP address and port, use:

    ```
    lookup <username>
    ```

- **Send Message**: To send a message to another user, execute:

    ```
    send <username> <message>
    ```

- **Exit**: To terminate the client application, type:

    ```
    exit
    ```

