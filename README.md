Real-Time Multiplayer Quiz Game
A real-time multiplayer quiz game using Python, socket programming, and multithreading. Players connect to a server, buzz in, and compete to answer questions. The first player to reach five correct answers wins.

Features
Real-time gameplay with immediate feedback
Multithreaded server handling multiple clients
Buzz-in system for question answering
Point-based scoring with winner announcement
Rules
Objective: Be the first to answer five questions correctly.
Buzzing In: Players press Enter to buzz for each question.
Answering: The first player to buzz can answer with 'a', 'b', 'c', or 'd'.
Scoring: Correct answers add a point; incorrect answers subtract a point.
Setup
Run server.py with python server.py <IP Address> <Port>.
Run client.py for each player using python client.py <IP Address> <Port>.
Communication Protocols and Techniques
TCP/IP for reliable data transmission.
Socket Programming for server-client communication.
Multithreading to handle multiple client connections.
