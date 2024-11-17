from gamestate import GameState


# Prepare game states
game_states = {}
match_state = None

def get_game(manager):
    global game_states
    if manager in game_states:
        return game_states[manager]
    else:
        return None
    

def get_managers(game_state):
    global game_states
    managers = []
    for key, value in game_states.items():
        if(value == game_state):
            managers.append(key)
    return managers


def assign_game(manager):
    global game_states
    global match_state
    if get_game(manager) is not None:
        return
    if match_state is None:
        match_state = GameState()
        game_states[manager] = match_state
        match_state.player_a = manager
    else:
        game_states[manager] = match_state
        to_activate = get_managers(match_state)
        match_state.player_b = manager
        match_state.send_opponent_name()
        for manager in to_activate:
            manager.match_made(match_state)
        match_state = None


def requeue_game(manager):
    global game_states
    global match_state
    del game_states[manager]
    assign_game(manager)


def end_game(game_state, reason):
    global game_states
    global match_state
    # Get the managers associated with the game state
    to_end = get_managers(game_state)
    # First, remove the entry for each manager
    for manager in to_end:
        game_states.pop(manager, None)
    # Then, tell the manager about the state change
    for manager in to_end:
        manager.match_ended(reason)
    # If this game is also the pending match, clear it
    if(game_state == match_state):
        match_state = None


def game_disconnect(manager, reason):
    global game_states
    if manager in game_states:
        end_game(game_states[manager], reason)